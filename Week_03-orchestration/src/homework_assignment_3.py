import pandas as pd
import logging
import mlflow
from hyperopt import hp, space_eval
from hyperopt.pyll import scope
from mlflow.entities import ViewType
from mlflow.tracking import MlflowClient
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from prefect import flow, task, get_run_logger
from prefect.task_runners import DaskTaskRunner
from datetime import date, datetime
from prefect.task_runners import SequentialTaskRunner
import pickle

HPO_EXPERIMENT_NAME = "ak-mlops-hm-nyc-taxi-experiment"

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment(HPO_EXPERIMENT_NAME)
mlflow.sklearn.autolog()

@task
def save_model(model_name, date, prefix="model-"):
    logger = get_run_logger()
   
    pickle_name = prefix +"{"+ date + "}.pkl"
    pickle.dump(model_name, open(pickle_name, 'wb'))
    logger.info(f"model pklfile name is: {pickle_name}")

@task
def read_data(path):
    logger = get_run_logger()
    now = datetime.now() # current date and time

    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    exec_val = "Task read_data: Current execution date:"+ date_time
    logger.info(exec_val)
    df = pd.read_parquet(path)
    return df

@task
def prepare_features(df, categorical, train=True):
    
    logger = get_run_logger()
    now = datetime.now() # current date and time

    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    exec_val = "Task prepare_features: Current execution date:"+ date_time
    logger.info(exec_val)

    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    mean_duration = df.duration.mean()
    if train:
        mean_dur = "The mean duration of training is" + str(mean_duration)
        record_info = "Training number of record" + str(len(df))
        logger.info(mean_dur)
        logger.info(record_info)
        print(f"The mean duration of training is {mean_duration}")
    else:
        mean_dur = "The mean duration of validation is" + str(mean_duration)
        record_info = "Validation number of record:" + str(len(df))
        logger.info(mean_dur)
        logger.info(record_info)
        print(f"The mean duration of validation is {mean_duration}")
    
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    return df
@task
def train_model(df, categorical, date):
    logger = get_run_logger()
    now = datetime.now() # current date and time

    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    exec_val = "Task train_model: Current execution date:"+ date_time
    logger.info(exec_val)

    train_dicts = df[categorical].to_dict(orient='records')
    dv = DictVectorizer()
    X_train = dv.fit_transform(train_dicts) 
    y_train = df.duration.values

    print(f"The shape of X_train is {X_train.shape}")
    print(f"The DictVectorizer has {len(dv.feature_names_)} features")

    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred = lr.predict(X_train)
    mse = mean_squared_error(y_train, y_pred, squared=False)
    mse_val = "The MSE of training is:"+ str(mse)
    print(f"The MSE of training is: {mse}")
    logger.info(mse_val)
    logger.info(lr)
    # save_model(lr, date)
    return lr, dv
@task
def run_model(df, categorical, dv, lr):
    val_dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(val_dicts) 
    y_pred = lr.predict(X_val)
    y_val = df.duration.values

    mse = mean_squared_error(y_val, y_pred, squared=False)
    print(f"The MSE of validation is: {mse}")
    return

@task
def get_paths(rundate: date, increment: int = 1):
    logger = get_run_logger()
    now = datetime.now() # current date and time

    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    exec_val = "get_paths task execution date:"+ date_time

    logger.info(exec_val)
    date = datetime.strptime(rundate, "%Y-%m-%d")
    mon = date.month
    mon = int(mon)
    if mon < 10:
        train_path = "./data/fhv_tripdata_2021-" + str('0') + str(mon) + ".parquet"
    else:
        train_path = "./data/fhv_tripdata_2021-" + str(mon) + ".parquet"
    
    val_mon = mon + increment

    if val_mon < 10:
        val_path = "./data/fhv_tripdata_2021-" + str('0') + str(val_mon) + ".parquet"
    else:
        val_path = "./data/fhv_tripdata_2021-" + str(val_mon) + ".parquet"

    logger.info(f"train_path value: {train_path}")
    logger.info(f"val_path value: {val_path}")
    # ./data/fhv_tripdata_2021-3.parquet
    return train_path, val_path

@flow(task_runner=SequentialTaskRunner())
def main(date="2021-08-15",
         train_path: str = '', 
         val_path: str = ''):
    
    logger = get_run_logger()
    now = datetime.now() # current date and time
    # train_path, val_path = get_paths(date).result()
    train_path, val_path = get_paths(date).result()

    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    exec_val = "Current execution date:"+ date_time

    logger.info(exec_val)
    logger.setLevel(logging.WARNING)
    categorical = ['PUlocationID', 'DOlocationID']

    df_train = read_data(train_path)
    # The output of a function wrapped around a @task is a PrefectFuture object. 
    # If we're mixing and matching normal functions with @tasked functions we need to get the result of 
    # the function by calling .result() on the PrefectFuture

    df_train_processed = prepare_features(df_train, categorical).result()

    df_val = read_data(val_path)
    df_val_processed = prepare_features(df_val, categorical, False).result()

    # train the model
    lr, dv = train_model(df_train_processed, categorical, date).result()
    save_model(lr, date)
    save_model(dv, date, prefix = "DictVectorizer-")
    run_model(df_val_processed, categorical, dv, lr)

main()
