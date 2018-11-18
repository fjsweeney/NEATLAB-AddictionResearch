import argparse
from collections import OrderedDict
import os
import pandas as pd
import numpy as np
from scipy import stats
from Preprocessing import hrv

# Hard coding for now...
SENSOR_FILENAME = 'all_data_cleaned.csv'


def gen_header(features):
    new_features = []
    for feature in features:
        new_features.append("%s_mean" % feature)
        new_features.append("%s_std" % feature)
        new_features.append("%s_median" % feature)
        new_features.append("%s_min" % feature)
        new_features.append("%s_max" % feature)

    return new_features


def aggregate_by_minute(df, epsilon):
    # Create a enumerated index column to ensure proper indexing
    df = df.set_index(np.arange(0, df.shape[0], 1))

    # Compute threshold feature cardinality
    delta = np.timedelta64(1, 'm')
    threshold = delta.item().total_seconds()*epsilon

    # Get all column names except for the datetime column.
    features = list(df)
    features.remove("datetime")

    # Create new DataFrame row for each minute in the time-series
    new_df = pd.DataFrame(columns=["datetime"]+gen_header(features)+["hrv"])
    new_df["datetime"] = pd.date_range(min(df["datetime"]),
                                       max(df["datetime"])+delta,
                                       freq='1min')
    new_df["datetime"] = new_df["datetime"].dt.round(freq='min')

    row_idx = 0
    start_time = new_df["datetime"].iloc[0]
    end_time = start_time+delta
    final_time = new_df.iloc[new_df.shape[0]-1]["datetime"]

    # Iterate over all possible time windows.
    while start_time <= final_time:
        # Extract subset between start and end times.
        mask = ((df["datetime"] >= start_time) &
                (df["datetime"] < end_time))

        subset = df.loc[mask]

        for feature in features:
            mask = (subset[feature] != -1)
            values = subset.loc[mask][feature].values

            if len(values) > threshold:
                new_df["%s_mean" % feature].iat[row_idx] = np.mean(values)
                new_df["%s_std" % feature].iat[row_idx] = np.std(values)
                new_df["%s_median" % feature].iat[row_idx] = np.median(values)
                new_df["%s_min" % feature].iat[row_idx] = np.min(values)
                new_df["%s_max" % feature].iat[row_idx] = np.max(values)

                if feature == "RR_interval":
                    # Compute HRV over the past minute
                    new_df["hrv"].iat[row_idx] = hrv.calc_rmssd(values)

        # Shift window and increase row_idx
        start_time += delta
        end_time += delta
        row_idx += 1

    return new_df


def add_standard_scores(df):
    feature_means = [feature for feature in list(df) if feature.endswith('mean')]
    feature_means.append("hrv")

    # Compute the standard score for all mean values (and HRV),
    # ignoring missing data.
    for feature in feature_means:
        # Create new feature column
        if feature == "hrv":
            colname = "hrv_mean"
        else:
            colname = feature.replace("mean", "zscore")
        df[colname] = np.repeat(np.nan, df.shape[0])

        # Filter out all rows with NaN values
        mask = (df[feature].notnull())
        subset = df.loc[mask][feature]

        if not subset.empty:
            zscores = stats.zscore(subset.values)
            for z_idx, tup in enumerate(subset.iteritems()):
                df[colname].iat[tup[0]] = zscores[z_idx]

    return df


def parse_from_files():
    df_map = OrderedDict()

    # Get each participant directory
    participants = [filename for filename in os.listdir('./') if
                    filename.startswith('participant')]

    for participant in participants:
        print("Aggregating data for %s..." % participant)
        os.chdir(participant)

        pid = participant.split("_")[1]

        # Load in all sensor data
        df = pd.read_csv(SENSOR_FILENAME, header=0, index_col=0)
        df["datetime"] = pd.to_datetime(df["datetime"])

        # Aggregate
        df = aggregate_by_minute(df, epsilon=0.25)

        # Add features
        df = add_standard_scores(df)

        # Write aggregated dataframe to file, add to map.
        df.to_csv("all_features_min-to-min.csv", na_rep='NA')
        df_map[pid] = df

        os.chdir("../")

    return df_map


def main(args):
    # Change to participant's hexoskin directory
    os.chdir(args.base_dir)

    df_map = parse_from_files()

    print('Done')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("base_dir", type=str,
                        help="Directory containing participant data.")

    main(parser.parse_args())
