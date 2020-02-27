import argparse
import os
import pandas as pd
import numpy as np


def contains_smoking_episode(start_date, episodes):
    end_date = start_date + np.timedelta64(1, 'm')

    for episode in episodes:
        if np.datetime64(start_date) <= episode < np.datetime64(end_date):
            return True

    return False


def join_on_smoke(sensor_df, smoking_df):
    # Make smoking column
    sensor_df["is_smoke"] = np.repeat(0, sensor_df.shape[0])

    smoking_df["datetime"] = smoking_df["datetime"].dt.round('1min')
    episodes = smoking_df["datetime"].values

    for index, row in sensor_df.iterrows():
        if contains_smoking_episode(row["datetime"], episodes):
            sensor_df["is_smoke"].iat[index] = 1

    return sensor_df


def main(args):

    os.chdir(args.base_dir)

    participants = [filename for filename in os.listdir('./') if
                    filename.startswith('participant')]
    
    frames = []
    for participant in participants:
        os.chdir(participant)

        pid = participant.split("_")[1]
        
        # Load in sensor data
        sensor_df = pd.read_csv("all_features_min-to-min.csv", header=0, 
                                index_col=0, sep=",")
        sensor_df["datetime"] = pd.to_datetime(sensor_df["datetime"])

        # Load in smoking episodes
        smoking_df = pd.read_csv("ema/smoking_reports.csv", header=0,
                                 index_col=0)
        smoking_df["datetime"] = pd.to_datetime(smoking_df["datetime"])

        # Add smoking column
        sensor_df = join_on_smoke(sensor_df, smoking_df)

        # Add PID
        sensor_df["pid"] = np.repeat(pid, sensor_df.shape[0])

        # Rearrange columns
        columns = list(sensor_df.columns)
        columns.remove("pid")
        new_columns = ["pid"]
        new_columns += columns
        sensor_df = sensor_df[new_columns]

        frames.append(sensor_df)

        sensor_df.to_csv("all_features_min-to-min.csv")
        
        os.chdir("../")

    df = pd.concat(frames)
    df.set_index(np.arange(0, df.shape[0], 1))
    df.to_csv("all_min-to-min.csv", na_rep='NA', index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("base_dir", type=str,
                        help="Directory containing participant data.")

    main(parser.parse_args())
