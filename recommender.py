# recommender engine
'''
Content based recommender  v1
Sets up the recommender model to rank list of places, to be used by the predictor
'''

import pandas as pd
import numpy as np
# -- # pre-processing & pipelines
from sklearn.decomposition import PCA, KernelPCA
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Imputer, LabelEncoder, StandardScaler
# -- # model building
from sklearn.linearmodel import LinearRegression, LogisticRegression Lasso
# -- # scoring & validation
from sklearn.metrics import mean_squared_log_error as msle


""" Model creation outline




"""