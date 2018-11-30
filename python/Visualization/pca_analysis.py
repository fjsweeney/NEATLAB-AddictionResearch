import argparse
import pickle
import numpy as np
from Visualization import PCA


def main(args):
    train = pickle.load(open(args.train, "rb"))

    if args.take_mean:
        print("Taking the feature mean of bag instances...")
        for bag in train:
            bag.instances = np.mean(bag.instances, axis=0)

    bags = np.asarray([x.instances for x in train])
    labels = np.asarray([x.label for x in train])
    labels[labels < 0] = 0

    bags = PCA.transform(bags, n_components=2)
    PCA.plot(bags, labels)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", type=str, required=True,
                        help="File containing training data (a pkl)")
    parser.add_argument("--bag_interval", type=str,
                        help="Number of minutes for each bag.")
    parser.add_argument("--take_mean", action='store_true', default=False,
                        help="Use the feature mean for each bag as one "
                             "instance (as opposed to stacking multiple "
                             "instances as the input to the model).")

    main(parser.parse_args())