import argparse
from collections import OrderedDict
from datetime import timedelta
import os
import pandas as pd
from Preprocessing import alignment, qa


HEXOSKIN_FEATURE_SET = "/home/webert3/smoking_viz_data/hexoskin_feature_set"
ANDROID_FEATURE_SET = "/home/webert3/smoking_viz_data/android_feature_set"


def read_android_data(df_map):
    """
    Parses files containing Android features (i.e. files listed in
    'ANDROID_FEATURE_SET')

    Args:
        df_map (dict): Feature -> DataFrame

    Returns:
        (dict) Updated df_map with Android feature DataFrames
    """
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
    """
        Parses files containing Hexoskin features (i.e. files listed in
        'HEXOSKIN_FEATURE_SET')

        Args:
            df_map (dict): Feature -> DataFrame

        Returns:
            (dict) Updated df_map with Hexoskin feature DataFrames
        """
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

            try:
                # Append dataframes together
                if colname in df_map:
                    df_map[colname] = df_map[colname].append(
                         pd.read_csv(file, sep=",", index_col=0))
                else:
                    df_map[colname] = pd.read_csv(file, sep=",", index_col=0)
            except Exception as err:
                print(err.__str__())

        os.chdir("..")

    os.chdir("..")

    return df_map


def parse_from_files(args):
    df_map = OrderedDict()

    # Read in Android data
    df_map = read_android_data(df_map)

    # Read in Hexoskin data
    df_map = read_hexoskin_data(df_map)

    clean_dataframes(df_map)

    return df_map


def clean_dataframes(df_map):
    """
    Clean DataFrames to prepare data before the merge.

    Args:
        df_map (dict): Feature -> DataFrame mapping

    Returns:
        (dict) Cleaned up df_map
    """

    for feature in df_map:
        df = df_map[feature]

        # Give generic column names
        df.columns = ["datetime", "values"]

        # Convert time strings to datetime objects and sort by date.
        df["datetime"] = pd.to_datetime(df["datetime"])
        df = df.sort_values(by=["datetime"])

        # Remove rows with extraneous timestamps.
        mask = (df["datetime"].dt.year == 2017)
        df = df.loc[~mask]

        df_map[feature] = df

    # Take only quality readings if quality scores are available.
    print("Cleaning RR intervals...")
    rr_df = qa.clean_hx_series(
        df_map["RR_interval"], df_map["RR_interval_quality"],
        qa.rr_qa_constants)

    rr_df = rr_df[rr_df["values"] > 0]  # Remove any 0 values

    # Convert RR interval to seconds from seconds/256
    rr_df["values"] = rr_df["values"].apply(lambda x: x / 256.0)
    df_map["RR_interval"] = rr_df
    df_map.pop("RR_interval_quality")

    print("Cleaning heart rate values...")
    df_map["heart_rate"] = qa.clean_hx_series(
        df_map["heart_rate"], df_map["heart_rate_quality"], qa.hr_qa_constants)
    df_map.pop("heart_rate_quality")

    print("Cleaning breathing rate values...")
    df_map["breathing_rate"] = qa.clean_hx_series(
        df_map["breathing_rate"], df_map["breathing_rate_quality"],
        qa.br_qa_constants)
    df_map.pop("breathing_rate_quality")

    return df_map


def main(args):
    # Change to participant's hexoskin directory
    os.chdir(args.participant_dir)

    df_map = parse_from_files(args)

    # Merge and align all dataframes.
    combined_df = alignment.merge_dataframes(df_map, timedelta(seconds=1))

    print("Exporting to CSV...")
    combined_df.to_csv("all_data_cleaned.csv")

    print('Done')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("participant_dir", type=str,
                        help="Directory containing hexoskin records.")

    main(parser.parse_args())
