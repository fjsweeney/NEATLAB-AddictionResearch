# -*- coding: utf-8 -*-
import numpy as np
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold

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

        # NOTE: I specifically use a imblearn pipeline instead of a sklearn
        # pipeline. This is because sklearn pipelines will use the validation
        # set for SMOTE, which biases the results.
        pipeline = Pipeline([
            ('sampling', SMOTE(random_state=SEED)),
            ('classification', LogisticRegression(random_state=SEED, n_jobs=-1))
        ])

        hspace = {
            "classification__penalty": ["l1", "l2"],
            "classification__C": [0.001, 0.01, 0.1, 1, 10, 100],
        }

        score_metrics = ['f1', 'precision', 'recall', 'accuracy', 'roc_auc']
        self.grid = RandomizedSearchCV(estimator=pipeline,
                                       param_distributions=hspace,
                                       scoring=score_metrics, n_iter=itrs,
                                       n_jobs=-1, verbose=10,
                                       random_state=SEED, refit="f1",
                                       cv=StratifiedKFold(n_splits=6,
                                                          shuffle=True,
                                                          random_state=SEED))

    def run(self):
        self.grid.fit(self.X, self.y)
