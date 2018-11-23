# -*- coding: utf-8 -*-
import time
import numpy as np
from hyperopt import STATUS_OK
from imblearn.over_sampling import SMOTE, ADASYN, RandomOverSampler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix

SEED = 666

best_f1 = 0
best_rf = None
best_feature_importance = None
config_counter = 0

class RandomForest:
    def __init__(self, hyperparameters, data) -> None:
        super().__init__()

        self.hyperparameters = hyperparameters

        # Extract bags and reshape to 2D array
        bags = np.asarray([x.instances for x in data])
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

    def fit(self):
        global best_f1, best_rf, best_feature_importance, config_counter

        # Convert params to appropriate types for scikit learn
        params = {
            "n_estimators": int(self.hyperparameters["n_estimators"]),
            "max_depth": int(self.hyperparameters["max_depth"]),
            "min_samples_split": int(self.hyperparameters["min_samples_split"]),
            "min_samples_leaf": int(self.hyperparameters["min_samples_leaf"])
        }

        model = RandomForestClassifier(**params,
                                       random_state=SEED, n_jobs=-1)

        # Train model
        model.fit(self.X_train, self.y_train)

        # Evaluate performance on the dev set
        dev_preds = model.predict(self.X_dev)
        my_precision, my_recall, my_f1_score, my_support = \
            precision_recall_fscore_support(self.y_dev, dev_preds,
            average="binary")
        conf_matrix = confusion_matrix(self.y_dev, dev_preds)
        
        print((my_precision))
        print((my_recall))
        print((my_f1_score))

        print("CONFIG %d: precision=%.5f, recall=%.5f, f1_score=%.5f" %
              (config_counter, my_precision, my_recall, my_f1_score))

        if my_f1_score > best_f1:
            best_f1 = my_f1_score
            best_rf = model
            best_feature_importance = model.feature_importances_
        config_counter += 1

        return {
            'loss': (1 - my_f1_score),
            'status': STATUS_OK,
            'eval_time': time.time()
        }
