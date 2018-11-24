import argparse
import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support, \
    confusion_matrix, accuracy_score, roc_curve, auc

import Models.MajorityClass as mc

SEED = 666


def finalize_roc_plot():
    plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r',
             label='Chance', alpha=.8)
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic for RandomForest Model')
    plt.legend(loc="lower right")


def plot_roc_curves(fpr, tpr, label):
    plt.plot(fpr, tpr, color='b',
             label=label,
             lw=2, alpha=.8)


def main(args):
    model = pickle.load(open(args.model, "rb"))
    test = pickle.load(open(args.test, "rb"))

    bags = np.asarray([x.instances for x in test])
    bags = np.reshape(bags, newshape=(len(bags), -1))
    labels = np.asarray([x.label for x in test])
    labels[labels < 0] = 0

    # TODO: Using dev set for testing.
    X_train, X_dev, y_train, y_dev = \
        train_test_split(bags, labels, test_size=0.15, random_state=SEED)

    # Compute scalar metrics for model
    predictions = model.predict(X_dev)
    accuracy = accuracy_score(y_dev, predictions)
    my_precision, my_recall, my_f1_score, my_support = \
        precision_recall_fscore_support(y_dev, predictions, average="binary")
    conf_matrix = confusion_matrix(y_dev, predictions)

    print("Model scores:")
    print("precision=%.5f, recall=%.5f, f1_score=%.5f accuracy=%.5f" %
          (my_precision, my_recall, my_f1_score, accuracy))
    print("Confusion Matrix\n%s" % conf_matrix.__str__())

    # Plot ROC curve for model
    probabilities = model.predict_proba(X_dev)[:, 1]
    fpr, tpr, thresholds = roc_curve(y_dev, probabilities, pos_label=1)
    roc_auc = auc(fpr, tpr)
    plot_roc_curves(fpr, tpr, label="Random Forest (AUC= % 0.2f)" % roc_auc)

    # Compute scalar metrics for baseline
    predictions = mc.predict(y_dev)
    accuracy = accuracy_score(y_dev, predictions)
    my_precision, my_recall, my_f1_score, my_support = \
        precision_recall_fscore_support(y_dev, predictions, average="binary")
    conf_matrix = confusion_matrix(y_dev, predictions)

    print("Baseline scores:")
    print("precision=%.5f, recall=%.5f, f1_score=%.5f accuracy=%.5f" %
          (my_precision, my_recall, my_f1_score, accuracy))
    print("Confusion Matrix\n%s" % conf_matrix.__str__())

    # Plot ROC curve for baseline
    probabilities = mc.predict_proba(y_dev)
    fpr, tpr, thresholds = roc_curve(y_dev, probabilities, pos_label=1)
    roc_auc = auc(fpr, tpr)
    plot_roc_curves(fpr, tpr, label="Majority Class (AUC= % 0.2f)" % roc_auc)

    finalize_roc_plot()
    plt.show()

    print('Done')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=True,
                        help="File containing saved model (a pkl)")
    parser.add_argument("--test", type=str,
                        help="File containing test data (a pkl)")

    main(parser.parse_args())