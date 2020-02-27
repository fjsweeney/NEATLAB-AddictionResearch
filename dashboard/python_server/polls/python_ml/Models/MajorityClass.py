import numpy as np


def get_majority_class(y):
    counts = np.bincount(y)
    majority_class = np.argmax(counts)
    return majority_class


def predict(y):
    return np.repeat(get_majority_class(y), len(y))


def predict_proba(y):
    classes = np.unique(y)
    predictions = predict(y)
    return [0 if x == 0 else 1 for x in predictions]