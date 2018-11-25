# -*- coding: utf-8 -*-
import logging
import time
import numpy as np
from hyperopt import STATUS_OK
from imblearn.over_sampling import SMOTE, ADASYN, RandomOverSampler
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support, \
    confusion_matrix, accuracy_score
from misvm import MISVM

# Static variables
SEED = 666
best_f1 = 0
best_svm = None
config_counter = 0


class MISVM_Classifier:
    def __init__(self, hyperparameters, data, output_dir):
        """
        RandomForest model constructor. Responsible for splitting up data and
        setting hyperparamters.

        Args:
            hyperparameters (dict): Contains relevant hyperparameters
            data (list): List of Bag objects
            output_dir (str): Path to output directory for model files.
        """
        super().__init__()

        # Set up log file to record general information about program operation
        logging.basicConfig(filename='%s/training.log' % output_dir,
                            level=logging.DEBUG,
                            filemode='a',
                            format='%(asctime)s - %(levelname)s: %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

        # Extract bags
        bags = np.asarray([x.instances for x in data])

        # NOTE: Recording original shape of the bags to use after resampling.
        n_instances = bags.shape[1]
        n_features = bags.shape[2]

        # Reshape to fit resampling library
        bags = np.reshape(bags, newshape=(len(bags), -1))
        labels = np.asarray([x.label for x in data])

        # Split data into train and dev sets
        self.X_train, self.X_dev, self.y_train, self.y_dev = \
            train_test_split(bags, labels, test_size=0.15, random_state=SEED)

        # Resample data set to alleviate class imbalance
        if hyperparameters["resampling"] == "SMOTE":
            self.X_train, self.y_train = SMOTE(random_state=SEED)\
                .fit_resample(self.X_train, self.y_train)
        elif hyperparameters["resampling"] == "ADASYN":
            self.X_train, self.y_train = ADASYN(random_state=SEED)\
                .fit_resample(self.X_train, self.y_train)
        elif hyperparameters["resampling"] == "RandomOverSampler":
            self.X_train, self.y_train = RandomOverSampler(random_state=SEED)\
                .fit_resample(self.X_train, self.y_train)

        # Reshape bags into 2d-arrays of shape (n_instances, n_features)
        self.X_train = np.reshape(self.X_train,
                                  newshape=(-1, n_instances, n_features))

        self.hyperparameters = hyperparameters

        # Convert params to appropriate types for scikit learn
        params = {
            "C": float(self.hyperparameters["C"]),
            "max_iters": int(self.hyperparameters["max_iters"]),
            "gamma": float(self.hyperparameters["gamma"]),
            "kernel": self.hyperparameters["kernel"]
        }

        self.model = MISVM(**params)

    def fit(self):
        global best_f1, best_svm,  config_counter

        # Train model
        self.model.fit(self.X_train, self.y_train)

        # Obtain out-of-bag predictions
        dev_preds = self.model.predict(self.X_dev)

        accuracy = accuracy_score(self.y_dev, dev_preds)
        my_precision, my_recall, my_f1_score, my_support = \
            precision_recall_fscore_support(self.y_dev, dev_preds,
                                            pos_label=1, average="binary")
        conf_matrix = confusion_matrix(self.y_dev, dev_preds)

        logging.info("CONFIG %d: precision=%.5f, recall=%.5f, f1_score=%.5f, "
                     "accuracy=%.5f" %
              (config_counter, my_precision, my_recall, my_f1_score, accuracy))
        print("CONFIG %d: precision=%.5f, recall=%.5f, f1_score=%.5f "
              "accuracy=%.5f" %
              (config_counter, my_precision, my_recall, my_f1_score, accuracy))
        print("Confusion Matrix\n%s" % conf_matrix.__str__())

        if my_f1_score > best_f1:
            best_f1 = my_f1_score
            best_svm = self.model
        config_counter += 1

        return {
            'loss': (1 - my_f1_score),
            'status': STATUS_OK,
            'eval_time': time.time()
        }
