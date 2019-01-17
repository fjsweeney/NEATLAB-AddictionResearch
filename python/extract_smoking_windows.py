import argparse
import pandas as pd
import numpy as np


def get_smoking_window(index, interval, df):
    l_bound = index - interval
    u_bound = index + interval

    if l_bound < 0:
        l_bound = 0

    if u_bound > df.shape[0]:
        u_bound = df.shape[0]

    return df.iloc[l_bound:u_bound]


def main(args):
    df = pd.read_csv(args.all_data, header=0, index_col=0, sep=",")

    df.set_index(np.arange(0, df.shape[0], 1))

    frames = []
    for index, row in df.iterrows():
        if row["is_smoke"] == 1:
            window = get_smoking_window(index, args.interval, df)
            if not window["hrv_zscore"].isnull().all():
                frames.append(window)

    all_windows = pd.concat(frames, ignore_index=True)

    # Write out all data
    all_windows.to_csv("%s-min_smoking_windows.csv" % (args.interval*2),
                       index=False)

    # Write out only a subset
    subset_cols = ["pid", "datetime", "hrv_zscore", "activity_zscore"]
    subset = all_windows[subset_cols]
    subset.to_csv("%s-min_smoking_windows_hrv.csv" % (args.interval * 2),
                  index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("all_data", type=str,
                        help="File containing all sensor data.")
    parser.add_argument("--interval", type=int, required=True,
                        help="Time interval surrounding smoking episode.")

    main(parser.parse_args())