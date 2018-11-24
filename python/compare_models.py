import argparse
from collections import OrderedDict
import json
import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support, \
    confusion_matrix, accuracy_score, roc_curve, auc

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


def finalize_stacked_bar_plot(exp_importances, feature_set):
    cmap = plt.get_cmap("Dark2")

    for i, exp in enumerate(exp_importances):
        # 'Stacking' values by adjusting the 'bottom' attribute
        total_importance = 0
        for j, importance in enumerate(exp_importances[exp]):
            scaled_importance = importance*100
            plt.bar(i, scaled_importance, label=feature_set[j],
                    bottom=total_importance, color=cmap.colors[j])
            total_importance += scaled_importance

    plt.tight_layout(rect=[0, 0.03, 1, 0.9])
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    plt.figlegend(by_label.values(), by_label.keys(), loc='lower center',
                  ncol=4, fancybox=True, shadow=True)

    plt.ylabel('Variable Importance')
    plt.title('Feature Importance by Time Interval')
    plt.xticks(np.arange(0, len(exp_importances)), exp_importances.keys())
    plt.yticks(np.arange(10, 110, 10))


def main(args):

    if args.viz == "feat_importance":
        exp_importances = OrderedDict()
        feature_set = None

    models = json.loads(open(args.models, 'r').read())
    
    for model in models:
        saved_model = pickle.load(open(model["model_path"], "rb"))

        test = pickle.load(open(model["data_path"], "rb"))

        # TODO: Using dev set for testing.
        bags = np.asarray([x.instances for x in test])
        bags = np.reshape(bags, newshape=(len(bags), -1))
        labels = np.asarray([x.label for x in test])
        labels[labels < 0] = 0
        X_train, X_dev, y_train, y_dev = \
            train_test_split(bags, labels, test_size=0.15, random_state=SEED)

        # Compute scalar metrics for model
        predictions = saved_model.predict(X_dev)
        accuracy = accuracy_score(y_dev, predictions)
        my_precision, my_recall, my_f1_score, my_support = \
            precision_recall_fscore_support(y_dev, predictions, average="binary")
        conf_matrix = confusion_matrix(y_dev, predictions)

        print("%s scores:" % model["description"])
        print("precision=%.5f, recall=%.5f, f1_score=%.5f accuracy=%.5f" %
              (my_precision, my_recall, my_f1_score, accuracy))
        print("Confusion Matrix\n%s" % conf_matrix.__str__())

        if args.viz == "ROC_curves":
            # Plot ROC curve for model
            probabilities = saved_model.predict_proba(X_dev)[:, 1]
            fpr, tpr, thresholds = roc_curve(y_dev, probabilities, pos_label=1)
            roc_auc = auc(fpr, tpr)
            plot_roc_curves(fpr, tpr, label="%s (AUC= % 0.2f)" %
                                            (model["description"], roc_auc))
        elif args.viz == "feat_importance":
            # Set feature_set labels if that hasn't already happened
            if feature_set is None:
                feature_set = model["feature_set"]

            # Aggregate feature importance
            agg_importances = aggregate_feature_importance(model, saved_model)
            exp_importances[model["description"]] = agg_importances
            # for i in range(len(agg_importances)):
            #     if feature_set[i] in importances:
            #         importances[feature_set[i]].append(agg_importances[i])
            #     else:
            #         importances[feature_set[i]] = [agg_importances[i]]

    if args.viz == "ROC_curves":
        finalize_roc_plot()
    elif args.viz == "feat_importance":
        finalize_stacked_bar_plot(exp_importances, feature_set)
    
    plt.show()
    print('Done')


def aggregate_feature_importance(model, saved_model):
    feature_importances = saved_model.feature_importances_
    time_interval = model["time_interval"]
    feature_importances = np.reshape(feature_importances, newshape=(
        time_interval, len(model["feature_set"])))
    agg_feature_importance = np.sum(feature_importances, axis=0)
    return agg_feature_importance


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", type=str, required=True,
                        help="File containing paths to all models (a JSON)")
    parser.add_argument("--viz", type=str, required=True, 
                        choices=["ROC_curves", "feat_importance"],
                        help="Type of plot to generate (I'm too lazy to use "
                             "subplots at the moment...")

    main(parser.parse_args())