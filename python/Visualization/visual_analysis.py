import argparse
import json
import os
import pickle
import numpy as np
import pandas as pd
from Visualization import PCA, Heatmap


def gen_probabilities(models, bags):
    df = pd.DataFrame()
    times = [x.end_time for x in bags]
    df["datetime"] = pd.to_datetime(times)

    print("Generating model probabilities...")

    for model in models:
        saved_model = pickle.load(open(model["model_path"], "rb"))

        if model["take_mean"] == "true":
            for bag in bags:
                bag.instances = np.mean(bag.instances, axis=0)

        X = [x.instances for x in bags]

        if len(X) == 0:
            return None

        X = np.reshape(X, newshape=(len(X), -1))

        # Generate probabilities for the positive class
        pos_probs = saved_model.predict_proba(X)[:, 1]

        # Generate class predictions (FOR TESTING)
        y_preds = saved_model.predict(X)

        # Add to DataFrame
        df[model["description"]] = pos_probs

    return df


#  TODO: Dumping this here for the data viz project
def contains_smoking_episode(start_date, episodes):
    end_date = start_date + np.timedelta64(1, 'm')

    for episode in episodes:
        if np.datetime64(start_date) <= episode < np.datetime64(end_date):
            return True

    return False


#  TODO: Dumping this here for the data viz project
def add_smoking_episodes(df, smoking_dts):
    df["is_smoke"] = np.repeat(0, df.shape[0])

    for index, row in df.iterrows():
        if contains_smoking_episode(row["datetime"], smoking_dts):
            df["is_smoke"].iat[index] = 1

    return df


def main(args):
    bags = pickle.load(open(args.bags, "rb"))

    if args.take_mean:
        print("Taking the feature mean of bag instances...")
        for bag in bags:
            bag.instances = np.mean(bag.instances, axis=0)

    X = np.asarray([x.instances for x in bags])
    labels = np.asarray([x.label for x in bags])
    labels[labels < 0] = 0

    if args.viz == "pca":
        X = PCA.transform(X, n_components=2)
        PCA.plot(X, labels)
    elif args.viz == "heatmap":
        if args.models is None:
            raise ValueError("Need to provide model JSON to generate "
                             "probabilities for this visualization.")
        else:
            models = json.loads(open(args.models, 'r').read())

        # Navigate to data directory
        os.chdir(args.base_dir)

        # Get each participant directory
        participants = [filename for filename in os.listdir('./') if
                        filename.startswith('participant')]

        for participant in participants:
            pid = participant.split("_")[1]
            pid_bags = [x for x in bags if x.pid == pid]

            # Generate smoking probabilities
            probability_df = gen_probabilities(models, pid_bags)
            if probability_df is None:
                continue

            # Read in smoking episodes
            smoking_df = pd.read_csv("%s/ema/smoking_reports.csv" % participant,
                                     header=0, index_col=0)
            smoking_df["datetime"] = pd.to_datetime(smoking_df["datetime"])

            # Locate any smoking episodes in the series
            smoking_df["datetime"] = smoking_df["datetime"].dt.round('1min')
            probability_df = add_smoking_episodes(probability_df,
                                            smoking_df["datetime"])

            # Write probabilities to file
            probability_df.to_csv("train_probs_pid=%s.csv" % pid)

            Heatmap.plot_timeseries(probability_df, smoking_df["datetime"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bags", type=str, required=True,
                        help="File containing data (a pkl)")
    parser.add_argument("--bag_interval", type=str,
                        help="Number of minutes for each bag.")
    parser.add_argument("--take_mean", action='store_true', default=False,
                        help="Use the feature mean for each bag as one "
                             "instance (as opposed to stacking multiple "
                             "instances as the input to the model).")
    parser.add_argument("--viz", type=str, required=True,
                        choices=["pca", "heatmap"],
                        help="Type of plot to generate (I'm too lazy to use "
                             "subplots at the moment...")
    parser.add_argument("--base_dir", type=str,
                        help="Base directory containing all participant data.")
    parser.add_argument("--models", type=str,
                        help="File containing paths to all models (a JSON)")

    main(parser.parse_args())