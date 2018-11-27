import argparse
from collections import OrderedDict
import json
import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support, \
    confusion_matrix, accuracy_score, roc_curve, auc, precision_recall_curve, \
    classification_report

SEED = 666


def finalize_roc_plot(title):
    plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r',
             label='Chance', alpha=.8)
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('%s' % title)
    plt.legend(loc="lower right")


def random_performance_pr(labels):
    _, counts = np.unique(labels, return_counts=True)
    P = counts[1]
    N = counts[0]
    return P/(P+N)


def finalize_pr_plot(title, labels):
    # plot no skill
    baseline = random_performance_pr(labels)
    plt.plot([0, 1], [baseline, baseline], linestyle='--', label='Chance')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('%s' % title)
    plt.legend(loc="lower right")


def plot_pr_curve(recall, precision, label):
    plt.plot(recall, precision, label=label, lw=2, alpha=.8)


def plot_roc_curve(fpr, tpr, label, tuning_lib):
    # Use different color for cross-validation (i.e. sklearn tuning approach)
    color = 'b' if tuning_lib == "hyperopt" else 'g'

    plt.plot(fpr, tpr, label=label, lw=2, alpha=.8)


def finalize_stacked_bar_plot(exp_importances, feature_set):
    cmap = plt.get_cmap("Dark2")

    for i, exp in enumerate(exp_importances):
        # 'Stacking' values by adjusting the 'bottom' attribute
        total_importance = 0
        for j, importance in enumerate(exp_importances[exp]):
            scaled_importance = importance * 100
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


def sort_feature_importance(agg_importances, feature_set):
    for i, feature in enumerate(feature_set):
        print("feature=\"%s\", importance=%.4f" %
              (feature, agg_importances[i]))


def aggregate_feature_importance(model, saved_model, take_mean):
    feature_importances = saved_model.feature_importances_
    if not take_mean:
        time_interval = model["time_interval"]
        feature_importances = np.reshape(feature_importances, newshape=(
            time_interval, len(model["feature_set"])))
        agg_feature_importance = np.sum(feature_importances, axis=0)
    else:
        # No need to aggregate over bags, bags where aggregated before training
        agg_feature_importance = feature_importances
    return agg_feature_importance


def main(args):
    if args.viz == "feat_importance":
        exp_importances = OrderedDict()
        feature_set = None

    models = json.loads(open(args.models, 'r').read())

    for model in models:
        saved_model = pickle.load(open(model["model_path"], "rb"))

        test = pickle.load(open(model["data_path"], "rb"))

        if args.take_mean:
            print("Taking the feature mean of bag instances...")
            for bag in test:
                bag.instances = np.mean(bag.instances, axis=0)

        # TODO: Using dev set for testing.
        bags = np.asarray([x.instances for x in test])
        bags = np.reshape(bags, newshape=(len(bags), -1))
        X_dev = bags
        labels = np.asarray([x.label for x in test])

        unique, counts = np.unique(labels, return_counts=True)
        v_pct = float(counts[1]) / float(len(labels))
        nv_pct = float(counts[0]) / float(len(labels))
        print("Vulnerable: %.2f | Not Vulnerable: %.2f" % (v_pct, nv_pct))

        labels[labels < 0] = 0
        y_dev = labels
        X_train, X_dev, y_train, y_dev = \
            train_test_split(bags, labels, test_size=0.15, random_state=SEED)

        # Compute scalar metrics for model
        predictions = saved_model.predict(X_dev)

        unique, counts = np.unique(predictions, return_counts=True)
        v_pct = float(counts[1]) / float(len(predictions))
        nv_pct = float(counts[0]) / float(len(predictions))
        print("Predicted Vulnerable: %.2f | Predicted Not Vulnerable: %.2f" %
              (v_pct, nv_pct))

        accuracy = accuracy_score(y_dev, predictions)
        my_precision, my_recall, my_f1_score, my_support = \
            precision_recall_fscore_support(y_dev, predictions,
                                            average="binary")
        conf_matrix = confusion_matrix(y_dev, predictions)

        print("%s scores:" % model["description"])
        print("precision=%.5f, recall=%.5f, f1_score=%.5f accuracy=%.5f" %
              (my_precision, my_recall, my_f1_score, accuracy))
        print("Confusion Matrix\n%s" % conf_matrix.__str__())

        print("Classification Report:")
        target_names = ["Not Vulnerable", "Vulnerable"]
        print(classification_report(y_dev, predictions,
                                    target_names=target_names))

        if args.viz == "ROC_curves":
            # Plot ROC curve for model
            probabilities = saved_model.predict_proba(X_dev)[:, 1]
            fpr, tpr, thresholds = roc_curve(y_dev, probabilities, pos_label=1)
            roc_auc = auc(fpr, tpr)
            plot_roc_curve(fpr, tpr, label="%s (AUC=%0.2f)" %
                                           (model["description"], roc_auc),
                           tuning_lib=model["tuning_lib"])
        elif args.viz == "P-R_curves":
            probabilities = saved_model.predict_proba(X_dev)[:, 1]
            precision, recall, thresholds = precision_recall_curve(y_dev,
                                                                   probabilities,
                                                                   pos_label=1)
            pr_auc = auc(recall, precision)
            plot_pr_curve(recall=recall, precision=precision,
                          label="%s (AUC=%0.2f)" %
                                (model["description"], pr_auc))

        elif args.viz == "feat_importance":
            # Set feature_set labels if that hasn't already happened
            if feature_set is None:
                feature_set = model["feature_set"]

            # Aggregate feature importance
            agg_importances = aggregate_feature_importance(model, saved_model,
                                                           args.take_mean)
            sort_feature_importance(agg_importances, feature_set)

            exp_importances[model["description"]] = agg_importances

    if args.viz == "ROC_curves":
        finalize_roc_plot(args.title)
    elif args.viz == "P-R_curves":
        finalize_pr_plot(args.title, labels)
    elif args.viz == "feat_importance":
        finalize_stacked_bar_plot(exp_importances, feature_set)

    plt.show()
    print('Done')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", type=str, required=True,
                        help="File containing paths to all models (a JSON)")
    parser.add_argument("--title", type=str, required=True,
                        help="Title for figure.")
    parser.add_argument("--viz", type=str, required=True,
                        choices=["ROC_curves", "feat_importance", "P-R_curves"],
                        help="Type of plot to generate (I'm too lazy to use "
                             "subplots at the moment...")
    parser.add_argument("--take_mean", action='store_true', default=False,
                        help="Use the feature mean for each bag as one "
                             "instance (as opposed to stacking multiple "
                             "instances as the input to the model).")

    main(parser.parse_args())
