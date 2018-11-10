import argparse
from collections import OrderedDict
import os
import pickle
import pandas as pd
from Preprocessing import align_timestamps


HEXOSKIN_FEATURE_SET = "/home/webert3/smoking_viz_data/hexoskin_feature_set"
ANDROID_FEATURE_SET = "/home/webert3/smoking_viz_data/android_feature_set"


def read_android_data(df_map):
    os.chdir("ema")

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

    # Get hexoskin feature files
    feature_files = [filename.rstrip('\n') for filename in
                     open(HEXOSKIN_FEATURE_SET, "r")
                     if filename.rstrip('\n').endswith(".csv")]

    # Load each record into memory
    records = [item for item in os.listdir('./') if not item.endswith("pkl")]

    for record in records:
        print("Loading data from record \"%s\"..." % record)
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

    # Change to participant's hexoskin directory
    os.chdir(args.participant_dir)

    # Read in Android data
    df_map = read_android_data(df_map)

    # Read in Hexoskin data
    df_map = read_hexoskin_data(df_map)

    # Dumping OrderedDict to 'pkl' file to save time during testing...
    print("Dumping to \"feature_df_map.pkl\"")
    pickle.dump(df_map, open("feature_df_map.pkl", "wb"))

    return df_map


def main(args):
    if not os.path.isfile("hx_feature_df_map.pkl"):
        hexoskin_dfs = parse_from_files(args)
    else:
        hexoskin_dfs = pickle.load(open("hx_feature_df_map.pkl", 'rb'))

    # todo: Sort dictionary by length of attribute vector, then time align.
    print('done')



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("participant_dir", type=str,
                        help="Directory containing hexoskin records.")

    main(parser.parse_args())
