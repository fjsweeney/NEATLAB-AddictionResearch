# -*- coding: utf-8 -*-
import traceback
from functools import partial
from hyperopt import fmin, hp, Trials, rand
from Models.RandomForest import RandomForest


def random_forest_experiment(itrs, data):
    """
    Set up a training experiment using Random Forest.

    Args:
        itrs (int): Number of hyperparameter configurations to test
        data (list): List of Bag objects

    Returns:
        (obj): Trails object containing info about each Hyperopt trail
        (best): Best hyperparameter configuration
    """

    # Define hyperparamter space
    hyperparameters = {
        "n_estimators": hp.quniform("n_estimators", 10, 1000, 1),
        "min_samples_split": hp.quniform("min_samples_split", 2, 10, 1),
        "min_samples_leaf": hp.quniform("min_samples_leaf", 1, 20, 1),
        "max_depth": hp.quniform("max_depth", 1, 20, 1),
        "max_features": hp.uniform("max_features", 0.01, 0.8),
        "criterion": hp.choice("criterion", ["mse", "mae"]),
        "resampling": hp.choice("resampling", ["SMOTE", "ADASYN",
                                               "RandomOverSampler"])
    }

    # Creating a higher order function to set all parameters except
    # "hyperparameters". This will be set during the call to 'fmin'.
    rf = partial(RandomForest, data=data)
    obj = partial(train_and_eval, model_class=rf)

    # NOTE: fmin is the function that finds and returns the optimal set of
    # hyperparameters. It will train 'itrs' different models and search the
    # 'hyperparameters' space for the optimal set of
    # hyperparameters using the search algorithm specified by 'algo'.
    # See: https://github.com/hyperopt/hyperopt/wiki/FMin
    trials = Trials()
    best = fmin(fn=obj, space=hyperparameters, algo=rand.suggest,
                max_evals=itrs, trials=trials)

    return trials, best


def train_and_eval(hyperparameters, model_class):
    # Construct model
    model = model_class(hyperparameters)

    # Train model
    loss = model.fit()

    # Evaluate forecacsting ability
    #try:
    #    model.evaluate_forecasting()
    #except ValueError:
    #    traceback.print_exc()
    #except Exception as e:
    #    print("Exception occurred when running inference: %s" % e.__str__())
    #    print("The model you're trying to use likely diverged during training.")

    return loss
