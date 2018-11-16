import argparse
import os
import numpy as np
import pandas as pd
from Preprocessing import hrv


# TODO: Make this a user defined argument... Doesn't matter for now.
ALL_DATA_FILE = "all_data_cleaned.csv"


def create_timedelta(delta_components):
    """
    Create np.timedelta64 object from the command line arguments.

    Args:
        delta_components (list): List os the form [<frequency>, <interval>]

    Returns:
        (timedelta64): Numpy timedelta object
    """
    freq = int(delta_components[0])
    interval = str(delta_components[1])

    return np.timedelta64(freq, interval)


def main(args):
    # Change working directory to record and find all csv files.
    os.chdir(args.participant_dir)

    # Read in CSV containing sensor data
    df = pd.read_csv(ALL_DATA_FILE, sep=",", index_col=0, header=0)
    df["datetime"] = pd.to_datetime(df["datetime"])

    # Generate HRV values over the specified timedelta taking a sliding
    # window approach
    df, colname = hrv.gen_hrv_by_window(df, create_timedelta(args.delta),
                                   args.method, args.epsilon)

    # Export to file
    df.to_csv('all_data_with_hrv.csv', sep=",")

    print('done')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("participant_dir", type=str,
                        help="Directory containing sensor data.")
    parser.add_argument("--delta", type=str,
                        default=[15, 'm'], nargs=2,
                        help="Two arguments specifying the frequency (int) "
                             "and the interval (string).")
    parser.add_argument("--epsilon", type=float,
                        default="0.5",
                        help="Number of rows required for hrv computation.")
    parser.add_argument("--method", type=str, choices=["rmssd"],
                        default="rmssd",
                        help="Method used for computing HRV")

    main(parser.parse_args())
