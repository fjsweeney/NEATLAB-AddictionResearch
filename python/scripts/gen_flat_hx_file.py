import argparse
from collections import OrderedDict
from datetime import timedelta
import os
import pickle
import pandas as pd
from Preprocessing import alignment


HEXOSKIN_FEATURE_SET = "/home/webert3/smoking_viz_data/hexoskin_feature_set"
ANDROID_FEATURE_SET = "/home/webert3/smoking_viz_data/android_feature_set"


def read_android_data(df_map):
    os.chdir("ema")
    print("Loading Android data...")

    # Get Android feature files
    feature_files = [filename.rstrip('\n') for filename in
                     open(ANDROID_FEATURE_SET, "r")
                     if filename.rstrip('\n').endswith(".csv")]

    for file in feature_files:
        colname = file.replace("_data.csv", "")
        df_map[colname] = pd.read_csv(file, sep=",", index_col=0)

    os.chdir("..")

    return df_map


def read_hexoskin_data(df_map):
    os.chdir('hexoskin')
    print("Loading Hexoskin data...")

    # Get hexoskin feature files
    feature_files = [filename.rstrip('\n') for filename in
                     open(HEXOSKIN_FEATURE_SET, "r")
                     if filename.rstrip('\n').endswith(".csv")]

    # Load each record into memory
    records = [item for item in os.listdir('./') if not item.endswith("pkl")]

    for record in records:
        print("Record \"%s\"..." % record)
        os.chdir(record)

        for file in feature_files:
            colname = file.replace("_timestamps.csv", "")

            # Append dataframes together
            if colname in df_map:
                df_map[colname] = df_map[colname].append(
                     pd.read_csv(file, sep=",", index_col=0))
            else:
                df_map[colname] = pd.read_csv(file, sep=",", index_col=0)

        os.chdir("..")

    os.chdir("..")

    return df_map


def parse_from_files(args):
    df_map = OrderedDict()

    # Read in Android data
    df_map = read_android_data(df_map)

    # Read in Hexoskin data
    df_map = read_hexoskin_data(df_map)

    # Set new header and convert all datetime strings to datetime objects
    for feature in df_map:
        df = df_map[feature]
        df.columns = ["datetime", "values"]
        df["datetime"] = pd.to_datetime(df["datetime"])

    return df_map


def main(args):
    # Change to participant's hexoskin directory
    os.chdir(args.participant_dir)

    df_map = parse_from_files(args)

    # Merge and align all dataframes.
    combined_df = alignment.merge_dataframes(df_map, timedelta(seconds=1))

    print("Exporting to CSV...")
    combined_df.to_csv("all_data.csv")

    print('Done')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("participant_dir", type=str,
                        help="Directory containing hexoskin records.")

    main(parser.parse_args())
