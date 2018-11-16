import argparse
import os
import numpy as np
import pandas as pd
from Preprocessing import hrv


ALL_DATA_FILE = "all_data_cleaned.csv"


def main(args):
    # Change working directory to record and find all csv files.
    os.chdir(args.participant_dir)

    df = pd.read_csv(ALL_DATA_FILE, sep=",", index_col=0, header=0)
    df["datetime"] = pd.to_datetime(df["datetime"])

    # TODO: create timedelta object from command line argument

    # Call the hrv function
    df = hrv.gen_hrv_by_window(df, np.timedelta64(1, 'm'), args.method,
                               args.epsilon)
    df.to_csv('all_data_with_hrv.csv', sep=",")

    print('done')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("participant_dir", type=str,
                        help="Directory containing hexoskin record.")
    parser.add_argument("--delta", type=str,
                        default="15 m",
                        help="Timedelta.")
    parser.add_argument("--epsilon", type=float,
                        default="0.5",
                        help="Number of rows required for hrv computation.")
    parser.add_argument("--method", type=str, choices=["rmssd", "sdnn"],
                        default="rmssd",
                        help="CSV file containing RR Intervals.")

    main(parser.parse_args())
