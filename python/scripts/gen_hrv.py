import argparse
import os
import pandas as pd
from Preprocessing import hrv


RR_INTERVALS_FILE = "RR_interval_timestamps.csv"
RR_QUALITIES_FILE = "RR_interval_quality_timestamps.csv"


def main(args):
    # Change working directory to record and find all csv files.
    os.chdir(args.participant_dir)

    # Compute HRV for every session in the participant directory
    # todo: Parallelize this! No data dependency between sessions.
    for session in os.listdir('./'):
        print("Computing minute-to-minute HRV for seesion: %s" % session)
        os.chdir(session)

        try:
            rr_df = pd.read_csv(RR_INTERVALS_FILE, sep=",", header=0,
                                names=["datetime", "rr"], index_col=0)
            rr_quality_df = pd.read_csv(RR_QUALITIES_FILE, sep=",", header=0,
                                    names=["datetime", "quality"], index_col=0)
        except FileNotFoundError as err:
            print("Couldn't find file for seesion: %s\n%s" %
                  (session, err.__str__()))

        rr_df = hrv.clean_rr_series(rr_df, rr_quality_df)
        hrv.gen_hrv_by_minute(rr_df, args.method)

        os.chdir("..")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("participant_dir", type=str,
                        help="Directory containing hexoskin record.")
    parser.add_argument("--method", type=str, choices=["rmssd", "sdnn"],
                        default="rmssd",
                        help="CSV file containing RR Intervals.")

    main(parser.parse_args())
