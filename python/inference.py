import argparse
import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix

SEED = 666


def main(args):
    model = pickle.load(open(args.model, "rb"))
    test = pickle.load(open(args.test, "rb"))

    # TODO: Using dev set for testing.
    bags = np.asarray([x.instances for x in test])
    bags = np.reshape(bags, newshape=(len(bags), -1))
    labels = np.asarray([x.label for x in test])
    X_train, X_dev, y_train, y_dev = \
        train_test_split(bags, labels, test_size=0.15, random_state=SEED)

    dev_preds = model.predict(X_dev)
    my_precision, my_recall, my_f1_score, my_support = \
        precision_recall_fscore_support(y_dev, dev_preds,
                                        average="binary")
    conf_matrix = confusion_matrix(y_dev, dev_preds)

    print('Done')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=True,
                        help="File containing saved model (a pkl)")
    parser.add_argument("--test", type=str,
                        help="File containing test data (a pkl)")

    main(parser.parse_args())