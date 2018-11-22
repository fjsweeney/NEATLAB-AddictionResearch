# -*- coding: utf-8 -*-
import argparse
import pickle
import Models.Utils.HyperoptHelper as hh


def main(args):
    train = pickle.load(open(args.train, "rb"))

    if args.model == "RF":
        trails, best = hh.random_forest_experiment(itrs=args.hyperopt,
                                                   data=train)

    print('Done')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", type=str, required=True,
                        help="File containing train data (a pkl)")
    parser.add_argument("--test", type=str,
                        help="File containing test data (a pkl)")
    parser.add_argument("--bag_interval", type=str,
                        help="Number of minutes for each bag.")
    parser.add_argument("--model", type=str, required=True,
                        choices=["RF", "miSVM", "majority_class"],
                        help="Model type")
    parser.add_argument("--hyperopt", type=int,
                        help="Number of hyperparameter iterations.")

    main(parser.parse_args())
