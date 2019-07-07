# recommender engine
'''
Content based recommender  v1
Sets up the recommender model to rank list of places, to be used by the predictor

This model doesn't require any of the ML libraries, pure content matrix content
'''

import pandas as pd
import numpy as np
# -- # pre-processing & pipelines
# from sklearn.decomposition import PCA, KernelPCA
# from sklearn.pipeline import Pipeline
# from sklearn.preprocessing import Imputer, LabelEncoder, StandardScaler
# # -- # model building
# from sklearn.linear_model import LinearRegression, LogisticRegression, Lasso
# # -- # scoring & validation
# from sklearn.metrics import mean_squared_log_error as msle


""" Model purpose
Using an input matrix of 3 chosen locations, rank all possible location vectors

1. Define input data matrix (assume clean data already)
2. Set up model params 

"""

# -- # Testing data input
# pd.read_csv()

