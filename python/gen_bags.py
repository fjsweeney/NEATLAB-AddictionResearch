import argparse
import os
import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler


feature_set = ["activity_zscore", "cadence_zscore",
"minute_ventilation_adjusted_zscore", "tidal_volume_adjusted_zscore",
"heart_rate_zscore", "RR_interval_zscore", "hrv_mean", "time_of_day"]


def get_label(start_time, end_time, smoking_df):
    """
    Returns +1 if smoking episode in window, -1 otherwise

    Args:
        start_time:
        end_time:
        smoking_df:

    Returns:

    """
    mask = ((smoking_df["datetime"] >= start_time) &
            (smoking_df["datetime"] < end_time))
    subset = smoking_df[mask]

    if subset.empty:
        return -1

    return 1


def generate_training_data(sensor_df, smoking_df, bag_interval):
    bags = []
    labels = []

    # Add time_of_day feature
    # todo: Consider adding day_of_week feature
    if "time_of_day" in feature_set:
        scalar = MinMaxScaler()
        sensor_df["time_of_day"] = sensor_df["datetime"].dt.hour
        sensor_df["time_of_day"] = scalar.fit_transform(
            np.reshape(sensor_df["time_of_day"].values, newshape=(-1, 1))
        )

    start_time = sensor_df["datetime"].iloc[0]
    end_time = start_time + np.timedelta64(bag_interval, 'm')
    final_time = sensor_df.iloc[sensor_df.shape[0] - 1]["datetime"]

    # Iterate over all possible time windows.
    while start_time <= final_time:
        # Extract subset between start and end times.
        mask = ((sensor_df["datetime"] >= start_time) &
                (sensor_df["datetime"] < end_time))

        # Filter by time interval
        subset = sensor_df.loc[mask]

        # Extract feature columns
        bag = subset[feature_set].values
        bags.append(bag)

        labels.append(get_label(start_time, end_time, smoking_df))

        # Shift window by one minute
        start_time += np.timedelta64(1, 'm')
        end_time += np.timedelta64(1, 'm')

    return np.asarray(bags), np.asarray(labels)


def filter_nans(bags, labels):
    new_bags, new_labels = ([] for i in range(2))
    for i, bag in enumerate(bags):
        if not np.isnan(bag).any():
            new_bags.append(bag)
            new_labels.append(labels[i])

    return np.asarray(new_bags), np.asarray(new_labels)


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
        # TODO: Consider throwing out rows with lots of NaNs
        sensor_df = pd.read_csv("all_features_min-to-min.csv", header=0,
                            index_col=0)
        sensor_df["datetime"] = pd.to_datetime(sensor_df["datetime"])

        # Load in smoking episodes
        smoking_df = pd.read_csv("ema/smoking_reports.csv", header=0,
                                 index_col=0)
        smoking_df["datetime"] = pd.to_datetime(smoking_df["datetime"])

        bags, labels = generate_training_data(sensor_df, smoking_df,
                                              args.bag_interval)

        # Filter out NaN bags
        new_bags, new_labels = filter_nans(bags, labels)

        # Print some relevant statistics
        print("Participant %s" % pid)
        print("Number of Data Points: %d" % len(new_labels))
        unique, counts = np.unique(new_labels, return_counts=True)
        v_pct = float(counts[1])/float(len(new_labels))
        nv_pct = float(counts[0]) / float(len(new_labels))
        print("Vulnerable: %.2f | Not Vulnerable: %.2f" % (v_pct, nv_pct))

        # Serialize arrays for future usage.
        np.save("bags.npy", new_bags)
        np.save("labels.npy", new_bags)
        os.chdir("../")


    print('Done')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("base_dir", type=str,
                        help="Directory containing participant data.")
    parser.add_argument("--bag_interval", type=str,
                        help="Number of minutes for each bag.")

    main(parser.parse_args())
