import argparse
import os
import pandas as pd
import numpy as np

from Models.Preprocessing import Bag
from sklearn.preprocessing import MinMaxScaler

feature_set = ["activity_zscore", "cadence_zscore",
               "minute_ventilation_adjusted_zscore",
               "tidal_volume_adjusted_zscore",
               "heart_rate_zscore", "RR_interval_zscore", "hrv_zscore",
               "time_of_day"]


def get_label(start_time, end_time, smoking_df):
    mask = ((smoking_df["datetime"] >= start_time) &
            (smoking_df["datetime"] < end_time))
    subset = smoking_df[mask]

    if subset.empty:
        return -1

    return 1


def generate_bags(sensor_df, smoking_df, bag_interval, pid):
    all_bags = []

    if "time_of_day" in feature_set:
        scalar = MinMaxScaler()
        sensor_df["time_of_day"] = sensor_df["datetime"].dt.hour
        sensor_df["time_of_day"] = scalar.fit_transform(
            np.reshape(sensor_df["time_of_day"].values, newshape=(-1, 1))
        )

    # Iterate over all possible time windows and construct bags
    start_time = sensor_df["datetime"].iloc[0]
    end_time = start_time + np.timedelta64(bag_interval, 'm')
    final_time = sensor_df.iloc[sensor_df.shape[0] - 1]["datetime"]
    while start_time <= final_time:
        # Extract subset between start and end times.
        mask = ((sensor_df["datetime"] >= start_time) &
                (sensor_df["datetime"] < end_time))

        # Filter by time interval
        subset = sensor_df.loc[mask]

        # Construct bag
        instances = subset[feature_set].values

        if not np.isnan(instances).any():
            all_bags.append(Bag(pid, start_time, end_time, instances,
                                get_label(start_time, end_time, smoking_df)))

        # Shift window by one minute
        start_time += np.timedelta64(1, 'm')
        end_time += np.timedelta64(1, 'm')

    return all_bags


def split_train_test_bags(sensor_df, smoking_df, bag_interval):
    """
    Construct bags and split up sensor data into a train and test
    set according to 'split_type'.

    Args:
        sensor_df:
        smoking_df:
        bag_interval:
        split_type:

    Returns:

    """
    train_bags, train_labels, test_bags, test_labels = ([] for i in range(4))

    # Add time_of_day feature
    # todo: Consider adding day_of_week feature
    if "time_of_day" in feature_set:
        scalar = MinMaxScaler()
        sensor_df["time_of_day"] = sensor_df["datetime"].dt.hour
        sensor_df["time_of_day"] = scalar.fit_transform(
            np.reshape(sensor_df["time_of_day"].values, newshape=(-1, 1))
        )

    # Choose day to leave out to test generalization
    study_days = np.unique(smoking_df["datetime"].dt.dayofyear.values)

    for i in range(len(study_days)):
        test_day = np.random.choice(study_days, replace=False)

        # Make sure the test day contains at least one smoking episode
        day_mask = (smoking_df["datetime"].dt.dayofyear == test_day)
        test_day_subset = smoking_df.loc[day_mask]

        if not test_day_subset.empty:
            print("Date saved for test set: %s" %
                  test_day_subset["datetime"].iloc[0].strftime("%m-%d-%Y"))

            print("All smoking episodes (n=%d):" % (test_day_subset.shape[0]))
            for datetime in test_day_subset["datetime"].values:
                print("%s" % datetime.__str__())

            break

    # Iterate over all possible time windows and construct bags
    start_time = sensor_df["datetime"].iloc[0]
    end_time = start_time + np.timedelta64(bag_interval, 'm')
    final_time = sensor_df.iloc[sensor_df.shape[0] - 1]["datetime"]
    while start_time <= final_time:
        # Extract subset between start and end times.
        mask = ((sensor_df["datetime"] >= start_time) &
                (sensor_df["datetime"] < end_time))

        # Filter by time interval
        subset = sensor_df.loc[mask]

        # Construct bag
        bag = subset[feature_set].values

        # Check 'test_day' to determine what set the bag is a part of.
        test_day_mask = (subset["datetime"].dt.dayofyear == test_day)
        test_day_subset = subset.loc[test_day_mask]

        # If majority of instances are on the 'test_day', put bag in test set.
        if test_day_subset.shape[0] > int(bag_interval) / 2:
            test_bags.append(bag)
            test_labels.append(get_label(start_time, end_time, smoking_df))
        else:
            train_bags.append(bag)
            train_labels.append(get_label(start_time, end_time, smoking_df))

        # Shift window by one minute
        start_time += np.timedelta64(1, 'm')
        end_time += np.timedelta64(1, 'm')

    return np.asarray(train_bags), np.asarray(train_labels), \
           np.asarray(test_bags), np.asarray(test_labels)


def filter_nans(bags, labels):
    new_bags, new_labels = ([] for i in range(2))
    for i, bag in enumerate(bags):
        if not np.isnan(bag).any():
            new_bags.append(bag)
            new_labels.append(labels[i])

    return np.asarray(new_bags), np.asarray(new_labels)


def print_bag_stats(train_labels, test_labels, pid):
    print("Participant %s - Training Data" % pid)
    print("Number of Data Points: %d" % len(train_labels))
    unique, counts = np.unique(train_labels, return_counts=True)
    v_pct = float(counts[1]) / float(len(train_labels))
    nv_pct = float(counts[0]) / float(len(train_labels))
    print("Vulnerable: %.2f | Not Vulnerable: %.2f" % (v_pct, nv_pct))

    print("Participant %s - Test Data" % pid)
    print("Number of Data Points: %d" % len(test_labels))
    unique, counts = np.unique(test_labels, return_counts=True)
    v_pct = float(counts[1]) / float(len(test_labels))
    nv_pct = float(counts[0]) / float(len(test_labels))
    print("Vulnerable: %.2f | Not Vulnerable: %.2f" % (v_pct, nv_pct))


def main(args):
    # Navigate to data directory
    os.chdir(args.base_dir)

    # Get each participant directory
    participants = [filename for filename in os.listdir('./') if
                    filename.startswith('participant')]

    for participant in participants:
        print("Creating bags for %s..." % participant)
        os.chdir(participant)

        pid = participant.split("_")[1]

        # Load in all sensor data
        sensor_df = pd.read_csv("all_features_min-to-min.csv", header=0,
                                index_col=0)
        sensor_df["datetime"] = pd.to_datetime(sensor_df["datetime"])

        # Load in smoking episodes
        smoking_df = pd.read_csv("ema/smoking_reports.csv", header=0,
                                 index_col=0)
        smoking_df["datetime"] = pd.to_datetime(smoking_df["datetime"])

        train_bags, train_labels, test_bags, test_labels = \
            split_train_test_bags(sensor_df, smoking_df, args.bag_interval)

        print("\nData stats BEFORE NaN filtering...")
        print_bag_stats(train_labels, test_labels, pid)

        train_bags, train_labels = filter_nans(train_bags, train_labels)
        test_bags, test_labels = filter_nans(test_bags, test_labels)

        print("\nData stats AFTER NaN filtering...")
        print_bag_stats(train_labels, test_labels, pid)

        # Serialize arrays for future usage.
        np.save("train_bags_%s.npy" % args.bag_interval, train_bags)
        np.save("train_labels_%s.npy" % args.bag_interval, train_labels)
        np.save("test_bags_%s.npy" % args.bag_interval, test_bags)
        np.save("test_labels_%s.npy" % args.bag_interval, test_labels)

        os.chdir("../")

    print('Done')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("base_dir", type=str,
                        help="Directory containing participant data.")
    parser.add_argument("--bag_interval", type=str,
                        help="Number of minutes for each bag.")

    main(parser.parse_args())
