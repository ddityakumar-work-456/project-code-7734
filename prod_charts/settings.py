
#Basic libraries
import math
import warnings
warnings.filterwarnings("ignore")

#Transformation Libraries
import pandas as pd
import numpy as np
from datetime import datetime

#Visualization libraries
import seaborn as sns
from matplotlib import pyplot as plt

#Libraries for statistics
import scipy.stats as stats

# Libraries for preprocessing
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Libraries for metrics
from sklearn.metrics import mean_squared_error
from sklearn.metrics import f1_score

#Library for synthetic sampling
import imblearn
from imblearn.base import SamplerMixin

# Libraries for clustering
from sklearn.cluster import KMeans
from sklearn.impute import KNNImputer

# Libraries for Regression
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR

# Libraries for classification
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
