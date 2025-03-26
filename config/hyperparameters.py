from scipy.stats import randint


RF_SEARCH_SPACE = {
    "max_depth": randint(2, 20),
    "n_estimators": randint(20, 80),
    "bootstrap": [True, False]
}


RANDOM_SEARCH_PARAMS = {
    "n_iter": 20,
    "cv": 10,
    "verbose": 2,
    "random_state": 42,
    "scoring": "f1",
}
