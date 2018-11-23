import argparse
import os
import pickle
import pandas as pd
import numpy as np

from Models.Preprocessing.Bag import Bag
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

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

    print(" %d non-empty bags generated" % len(all_bags))
    return all_bags


def print_bag_stats(labels):
    print("Number of Data Points: %d" % len(labels))
    unique, counts = np.unique(labels, return_counts=True)
    v_pct = float(counts[1]) / float(len(labels))
    nv_pct = float(counts[0]) / float(len(labels))
    print("Vulnerable: %.2f | Not Vulnerable: %.2f" % (v_pct, nv_pct))


def main(args):
    # Navigate to data directory
    os.chdir(args.base_dir)

    # Get each participant directory
    participants = [filename for filename in os.listdir('./') if
                    filename.startswith('participant')]

    # Construct bags for each participant
    all_bags = []
    for participant in participants:
        print("Creating bags for %s..." % participant, end="")
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

        # Construct Bag objects
        all_bags += generate_bags(sensor_df, smoking_df, args.bag_interval, pid)

        os.chdir("../")

    print("%d bags generated in total." % len(all_bags))

    train, test = train_test_split(all_bags, shuffle=True,
                                   test_size=args.pct_test)

    train_labels = [x.label for x in train]
    test_labels = [x.label for x in test]

    print("Train Data Stats:")
    print_bag_stats(train_labels)
    print("Test Data Stats:")
    print_bag_stats(test_labels)

    # todo: Pickle the data
    pickle.dump(train, open("train_intv=%s_min.pkl" % args.bag_interval, "wb"))
    pickle.dump(test, open("test_intv=%s_min.pkl" % args.bag_interval, "wb"))

    print('Done')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("base_dir", type=str,
                        help="Directory containing participant data.")
    parser.add_argument("--bag_interval", type=str,
                        help="Number of minutes for each bag.")
    parser.add_argument("--pct_test", type=float,
                        help="Percent of data used for test set")

    main(parser.parse_args())
