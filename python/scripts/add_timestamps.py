import argparse
from datetime import datetime, timedelta
import os
import numpy as np
import pandas as pd


def create_timestamps(filename, start_datetime):
    df = pd.read_csv(filename, sep=",", header=None)

    # Drop head if it exists
    try:
        float(df.iloc[0][0])
    except Exception as e:
        df = df.iloc[1:]

    print("Adding timestamps to %s..." % filename)
    datetimes = []
    for total_seconds in df[0]:
        # Add total seconds to the starting datetime
        datetimes.append(start_datetime + timedelta(seconds=float(
            total_seconds)))

    df[0] = np.asarray(datetimes)

    new_filename = filename.split('.')[0] + '_timestamps.csv'
    print("Writing data to file %s..." % new_filename)
    df.to_csv(new_filename)


def main(args):

    # Change working directory to record and find all csv files.
    os.chdir(args.record_dir)
    csvs = [filename for filename in os.listdir('./') if filename.endswith('.csv')]
    start_datetime = datetime.strptime(args.start_datetime, '%m-%d-%Y_%H:%M')

    for csv in csvs:
        # Temporary solution for skipping files that don't need timestamps.
        if csv == "statistics.csv" or csv.endswith('timestamps.csv'):
            continue

        # todo: Parallelize this code! Assign each core to a subset of the files
        create_timestamps(csv, start_datetime)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("record_dir", type=str,
                        help="Directory containing hexoskin record.")
    parser.add_argument("start_datetime", type=str,
                        help="Beginning timestamp for hexoskin record. Must "
                             "follow the format: m-d-Y_H:M")

    main(parser.parse_args())
