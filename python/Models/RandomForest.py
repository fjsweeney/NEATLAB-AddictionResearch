# -*- coding: utf-8 -*-
import time
import numpy as np
from hyperopt import STATUS_OK
from imblearn.over_sampling import SMOTE, ADASYN, RandomOverSampler
from sklearn.ensemble import RandomForestClassifier

SEED = 666

best_f1 = None
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

        # Resample data set to alleviate class imbalance
        if hyperparameters["resampling"] == "SMOTE":
            self.bags, self.labels = SMOTE(random_state=SEED)\
                .fit_resample(bags, labels)
        elif hyperparameters["resampling"] == "ADASYN":
            self.bags, self.labels = ADASYN(random_state=SEED)\
                .fit_resample(bags, labels)
        elif hyperparameters["resampling"] == "RandomOverSampler":
            self.bags, self.labels = RandomOverSampler(random_state=SEED)\
                .fit_resample(bags, labels)

    def fit(self):
        global best_f1, best_rf, best_feature_importance, config_counter

        # Convert params to appropriate type for scikit learn
        self.hyperparameters["n_estimators"] = int(self.hyperparameters["n_estimators"])
        self.hyperparameters["max_depth"] = int(self.hyperparameters["max_depth"])
        self.hyperparameters["min_samples_split"] = int(self.hyperparameters["min_samples_split"])
        self.hyperparameters["min_samples_leaf"] = int(self.hyperparameters["min_samples_leaf"])

        model = RandomForestClassifier(**self.hyperparameters,
                                       random_state=SEED, n_jobs=-1,
                                       oob_score=True)
        model.fit(self.bags, self.labels)
        # preds = model.oob_prediction_


        print("CONFIG %d: OOB_ACCURACY=%.5f OOB_F1_SCORE=%.5f" %
              (config_counter, model.oob_score_ f1_score))

        if f1_score > best_f1:
            best_f1 = f1_score
            best_rf = model
            best_feature_importance = model.feature_importances_
        config_counter += 1

        return {
            'loss': (1 - f1_score),
            'status': STATUS_OK,
            'eval_time': time.time()
        }
