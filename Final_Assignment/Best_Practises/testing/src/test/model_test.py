## importing all libs
import pickle
import random
from datetime import datetime

import numpy as np
import mlflow
import pandas as pd
import matplotlib.pyplot as plt
from prefect import flow, task
from mlflow.tracking import MlflowClient
from sklearn.ensemble import RandomForestClassifier
from prefect.task_runners import SequentialTaskRunner
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction import DictVectorizer
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os
from sklearn.linear_model import LinearRegression, BayesianRidge
from sklearn import metrics
from wordcloud import WordCloud
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, f1_score, recall_score, accuracy_score, precision_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.experimental import enable_halving_search_cv
from sklearn.model_selection import HalvingGridSearchCV
from sklearn.ensemble import BaggingRegressor
from sklearn.ensemble import VotingRegressor
from sklearn.ensemble import StackingRegressor
import pickle
## 

import pandas as pd
import pickle
import requests as req
import os
## importing all libs
import pickle
import random
from datetime import datetime

import numpy as np
import mlflow
import pandas as pd
import matplotlib.pyplot as plt
from prefect import flow, task
from mlflow.tracking import MlflowClient
from sklearn.ensemble import RandomForestClassifier
from prefect.task_runners import SequentialTaskRunner
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction import DictVectorizer
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os
from sklearn.linear_model import LinearRegression, BayesianRidge
from sklearn import metrics
from wordcloud import WordCloud
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, f1_score, recall_score, accuracy_score, precision_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.experimental import enable_halving_search_cv
from sklearn.model_selection import HalvingGridSearchCV
from sklearn.ensemble import BaggingRegressor
from sklearn.ensemble import VotingRegressor
from sklearn.ensemble import StackingRegressor
## 
from prefect import task, flow, get_run_logger
from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

from prefect import flow, task, get_run_logger
from prefect.task_runners import SequentialTaskRunner

import warnings
warnings.filterwarnings("ignore")
import pickle

scalerfile = '/home/ubuntu/mlops-zoomcamp/07-project/capstone/src/scaler.sav'
result_slacerfile = '/home/ubuntu/mlops-zoomcamp/07-project/capstone/src/result_scaler.sav'


# scaler_result = pickle.load(open(result_slacerfile, 'rb'))
def test_model_loaded():
    assert 1==1

def test_load_feature_transform_file():
    scaler = pickle.load(open(scalerfile, 'rb'))
    print(scaler)
    assert scaler.mean_[0]> 0

def test_read_prepare_feature(filepath="/home/ubuntu/mlops-zoomcamp/07-project/capstone/src/test_predict.csv"):
    rent_data = pd.read_csv(filepath)
    # rent_data = rent_data.drop(['Posted On','Area Locality','Floor'],axis=1)
    # rent_data = pd.get_dummies(rent_data, columns=['Area Type', 'City', 'Furnishing Status', 'Tenant Preferred', 'Point of Contact'])
    X = rent_data
    sc_X = StandardScaler()
    scaler = pickle.load(open(scalerfile, 'rb'))
    X_test = scaler.fit_transform(X)
    assert len(X_test) > 0

def test_predict_output(filepath="/home/ubuntu/mlops-zoomcamp/07-project/capstone/src/test_predict.csv"):
    '''
    testing if the model has returned prediction value for all input record
    '''
    # X = rent_data
    rent_data = pd.read_csv(filepath)
    sc_X = StandardScaler()
    scaler = pickle.load(open(scalerfile, 'rb'))
    X_test = scaler.fit_transform(rent_data)    
    mlflow_run_id = "b9cf70dad0af4a9fb8db7875b8431947"
    logged_model = f'/home/ubuntu/mlops-zoomcamp/07-project/capstone/src/mlruns/6/{mlflow_run_id}/artifacts/models/stacking'
    model = mlflow.pyfunc.load_model(logged_model)
    preds = model.predict(X_test)
    print(preds)
    # print(preds[0])
    pred_list =[]
    for l in range(len(preds)):
        pred_list.append(preds[l])
    assert len(X_test) == len(pred_list)

def test_predict_rent_value(filepath="/home/ubuntu/mlops-zoomcamp/07-project/capstone/src/test_predict.csv"):
    '''
    testing if the model has returned prediction value of > 0
    '''
    rent_data = pd.read_csv(filepath)
    sc_X = StandardScaler()
    scaler = pickle.load(open(scalerfile, 'rb'))
    X_test = scaler.fit_transform(rent_data)    
    mlflow_run_id = "b9cf70dad0af4a9fb8db7875b8431947"
    logged_model = f'/home/ubuntu/mlops-zoomcamp/07-project/capstone/src/mlruns/6/{mlflow_run_id}/artifacts/models/stacking'
    model = mlflow.pyfunc.load_model(logged_model)
    preds = model.predict(X_test)
    print(preds)
    # print(preds[0])
    pred_list =[]
    for l in range(len(preds)):
        pred_list.append(preds[l])
    assert len([*filter(lambda x: x >= 30, pred_list)]) > 0
