# -*- coding: utf-8 -*-
import numpy as np
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold
from scipy.stats import randint, uniform
from dask.diagnostics import ProgressBar

# Static variables
SEED = 666
best_f1 = 0
best_rf = None
best_feature_importance = None
config_counter = 0


class RandomForestExperiment:
    def __init__(self, data, itrs=1):
        super().__init__()

        # Reformat input data
        bags = np.asarray([x.instances for x in data])
        self.X = np.reshape(bags, newshape=(len(bags), -1))
        labels = np.asarray([x.label for x in data])
        labels[labels < 0] = 0
        self.y = labels

        # NOTE: I specifically use a imblearn pipeline instead of a sklearn
        # pipeline. This is because sklearn pipelines will use the validation
        # set for SMOTE, which biases the results.
        pipeline = Pipeline([
            ('sampling', SMOTE(random_state=SEED)),
            ('classification', RandomForestClassifier(random_state=SEED,
                                                      n_jobs=-1, verbose=1))
        ])

        hspace = {
            "classification__n_estimators": randint(10, 1000),
            "classification__min_samples_split": randint(2, 10),
            "classification__min_samples_leaf": randint(1, 20),
            "classification__max_depth": randint(1, 20),
            "classification__max_features": uniform(0.01, 0.8),
            "classification__criterion": ["gini", "entropy"]
        }

        self.grid = RandomizedSearchCV(estimator=pipeline,
                                       param_distributions=hspace,
                                       scoring="f1", n_iter=itrs, n_jobs=-1,
                                       random_state=SEED, 
                                       cv=StratifiedKFold(n_splits=10,
                                                          shuffle=True,
                                                          random_state=SEED))
        self.cv_results = None
        self.best_model = None
        self.best_params = None
        self.best_score = 0

    def run(self):
        with ProgressBar():
            self.grid.fit(self.X, self.y)

        self.best_model = self.grid.best_estimator_
        self.best_score = self.grid.best_score_
        self.cv_results = self.grid.cv_results_
