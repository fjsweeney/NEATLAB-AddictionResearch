# -*- coding: utf-8 -*-
import numpy as np
from imblearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold
from scipy.stats import uniform

# Static variables
SEED = 666


class LogisticRegressionExperiment:
    def __init__(self, data, itrs=1):
        super().__init__()

        # Reformat input data
        bags = np.asarray([x.instances for x in data])
        self.X = np.reshape(bags, newshape=(len(bags), -1))
        labels = np.asarray([x.label for x in data])
        labels[labels < 0] = 0
        self.y = labels

        # NOTE: No SMOTE here, as Logistic Regression responds poorly to
        # varying distributions in the train and test sets.
        pipeline = Pipeline([
            ('classification', LogisticRegression(random_state=SEED, n_jobs=-1))
        ])

        hspace = {
            "classification__penalty": ["l1", "l2"],
            "classification__C": uniform(0.001, (100-0.001)),
            "classification__class_weight": [None, "balanced"]
        }

        score_metrics = ['f1', 'precision', 'recall', 'accuracy', 'roc_auc']
        self.grid = RandomizedSearchCV(estimator=pipeline,
                                       return_train_score=True,
                                       param_distributions=hspace,
                                       scoring=score_metrics, n_iter=itrs,
                                       n_jobs=-1, verbose=10,
                                       random_state=SEED, refit="f1",
                                       cv=StratifiedKFold(n_splits=6,
                                                          shuffle=True,
                                                          random_state=SEED))

    def run(self):
        self.grid.fit(self.X, self.y)
