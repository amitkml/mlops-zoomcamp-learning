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
scalerfile = 'scaler.sav'
result_slacerfile = 'result_scaler.sav'

scaler = pickle.load(open(scalerfile, 'rb'))
scaler_result = pickle.load(open(result_slacerfile, 'rb'))

mlflow_run_id = "ed0da4c85b064d40b8413989b1b28583"
# MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"
# mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
# mlflow.set_experiment("house-rent-prediction-experiment")
logged_model = f'mlruns/6/{mlflow_run_id}/artifacts/models/stacking'
model = mlflow.pyfunc.load_model(logged_model)
print(model)

def read_prepare_feature(filepath):
    rent_data = pd.read_csv(filepath)
    s = np.load('mean_train.npy')
    m = np.load('std_train.npy')
    # rent_data = rent_data.drop(['Posted On','Area Locality','Floor'],axis=1)
    # rent_data = pd.get_dummies(rent_data, columns=['Area Type', 'City', 'Furnishing Status', 'Tenant Preferred', 'Point of Contact'])
    X = rent_data
    sc_X = StandardScaler()
    X_test = scaler.fit_transform(X)
    return X_test, rent_data
    
def predict(features, model):
    preds = model.predict(features)
    print(type(preds))
    print(preds)
    # print(preds[0])
    pred_list =[]
    for l in range(len(preds)):
        pred_list.append(preds[l])
    print(pred_list)
    return pred_list


def run():
    filepath = "test_predict.csv"
    X_test, rent_data = read_prepare_feature(filepath)
    pred_list = predict(X_test, model)
    rent_data['Predicted_Normalized_Rent'] = pred_list
    rent_data.to_csv("test_predict_result.csv",index=False)

if __name__ == '__main__':
    run()