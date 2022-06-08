### Q1-Converting the script to a Prefect flow

We want to bring this to workflow orchestration to add observability around it. The `main` function will be converted to a `flow` and the other functions will be `tasks`. After adding all of the decorators, there is actually one task that you will need to call `.result()` for inside the `flow` to get it to work. Which task is this?

- `read_data`
- `prepare_features`
- `train_model`
- `run_model`

Important: change all `print` statements to use the Prefect logger. Using the `print` statement will not appear in the Prefect UI. You have to call `get_run_logger` at the start of the task to use it.

**Answer:** `prepare_features`

### Q2. Parameterizing the flow

Right now there are two parameters for `main()` called `train_path` and `val_path`. We want to change the flow function to accept `date` instead. `date` should then be passed to a task that gives both the `train_path` and `val_path` to use.

It should look like this:

```
@flow
def main(date=None):
    train_path, val_path = get_paths(date).result()
    # rest of flow below
```

Where `get_paths` is a task that you have to implement. The specs for this are outlined in the motivation section. Listing them out again here:

Download the relevant files needed to run the `main` flow if `date` is 2021-08-15.

For example:

```
main(date="2021-08-15")
```

By setting up the logger from the previous step, we should see some logs about our training job. What is the validation MSE when running the flow with this date?

Note you need to download the relevant files to run. Part of this question is understanding which files the flow should be looking for.

**Answer:** The MSE of validation is: 11.989006232890928

### Q3. Saving the model and artifacts

The requirements for filenames to save it as were mentioned in the Motivation section. They are pasted again here:

- Save the model as "model-{date}.pkl" where date is in `YYYY-MM-DD`. Note that `date` here is the value of the flow `parameter`. In practice, this setup makes it very easy to get the latest model to run predictions because you just need to get the most recent one.
- In this example we use a DictVectorizer. That is needed to run future data through our model. Save that as "dv-{date}.pkl". Similar to above, if the date is `2021-03-15`, the files output should be `model-2021-03-15.bin` and `dv-2021-03-15.b`.

By using this file name, during inference, we can just pull the latest model from our model directory and apply it. Assuming we already had a list of filenames:

```
['model-2021-03-15.bin', 'model-2021-04-15.bin', 'model-2021-05-15.bin']
```

We could do something like `sorted(model_list, reverse=False)[0]` to get the filename of the latest file. This is the simplest way to consistently use the latest trained model for inference. Tools like MLFlow give us more control logic to use flows.

What is the file size of the `DictVectorizer` that we trained when the `date` is 2021-08-15?

- 13,000 bytes
- 23,000 bytes
- 33,000 bytes
- 43,000 bytes

**Answer:** The file size is 13,000 bytes

### Q4. Creating a deployment with a CronSchedule

There are many tool for cron to english and I have used https://crontab.guru/#0_9_15_*_*

We previously showed the `IntervalSchedule` in the video tutorials. In some cases, the interval is too rigid. For example, what if we wanted to run this `flow` on the 15th of every month? An interval of 30 days would not be in sync. In cases like these, the `CronSchedule` is more appropriate. The documentation for that is [here](https://orion-docs.prefect.io/concepts/schedules/#cronschedule)

Cron is an important part of workflow orchestration. It is used to schedule tasks, and was a predecessor for more mature orchestration frameworks. A lot of teams still use Cron in production. Even if you don't use Cron, the Cron expression is very common as a way to write a schedule, and the basics are worth learning for orchestration, even outside Prefect.

For this exercise, use a `CronSchedule` when creating a Prefect deployment.

What is the Cron expression to run a flow at 9 AM every 15th of the month?

- `* * 15 9 0`
- `9 15 * * *`
- `0 9 15 * *`
- `0 15 9 1 *`

Hint: there are many Cron to English tools. Try looking for one to help you.

Create a deployment with `prefect deployment create` after you write your `DeploymentSpec`

Here is my code that I have used to create deployment.

```
from prefect.deployments import DeploymentSpec
from prefect.orion.schemas.schedules import CronSchedule
from prefect.task_runners import SequentialTaskRunner
from prefect.flow_runners import SubprocessFlowRunner

DeploymentSpec(
    name="cron-schedule-mlfhv-training-deployment",
    flow_location="homework_assignment_3.py",
    # storage_type="Local Storage",
    flow_runner=SubprocessFlowRunner(),
    schedule=CronSchedule(
        cron="0 9 15 * *",
        timezone="America/New_York"),
)
```

**Here is how I have deployed**

```python
Loading deployment specifications from python script at 'prefect_deploy_cron_schedule.py'...
2022/06/08 11:38:40 WARNING mlflow.utils.autologging_utils: You are using an unsupported version of sklearn. If you encounter errors during autologging, try upgrading / downgrading sklearn to a supported version, or try upgrading MLflow.
11:38:40.817 | INFO    | prefect.engine - Created flow run 'piquant-penguin' for flow 'main'
11:38:40.818 | INFO    | Flow run 'piquant-penguin' - Using task runner 'SequentialTaskRunner'
11:38:40.903 | INFO    | Flow run 'piquant-penguin' - Created task run 'get_paths-fcec5980-0' for task 'get_paths'
11:38:40.938 | INFO    | Task run 'get_paths-fcec5980-0' - get_paths task execution date:06/08/2022, 11:38:40
11:38:40.940 | INFO    | Task run 'get_paths-fcec5980-0' - train_path value: ./data/fhv_tripdata_2021-08.parquet
11:38:40.940 | INFO    | Task run 'get_paths-fcec5980-0' - val_path value: ./data/fhv_tripdata_2021-09.parquet
11:38:40.968 | INFO    | Task run 'get_paths-fcec5980-0' - Finished in state Completed()
11:38:40.969 | INFO    | Flow run 'piquant-penguin' - Current execution date:06/08/2022, 11:38:40
11:38:41.029 | INFO    | Task run 'read_data-c914d840-0' - Task read_data: Current execution date:06/08/2022, 11:38:41
11:38:45.416 | INFO    | Task run 'read_data-c914d840-0' - Finished in state Completed()
11:38:45.487 | INFO    | Task run 'prepare_features-21588f7a-0' - Task prepare_features: Current execution date:06/08/2022, 11:38:45
11:38:45.683 | INFO    | Task run 'prepare_features-21588f7a-0' - The mean duration of training is18.058284743395713
11:38:45.684 | INFO    | Task run 'prepare_features-21588f7a-0' - Training number of record1126605
The mean duration of training is 18.058284743395713
11:38:52.108 | INFO    | Task run 'prepare_features-21588f7a-0' - Finished in state Completed()
11:38:52.178 | INFO    | Task run 'read_data-c914d840-1' - Task read_data: Current execution date:06/08/2022, 11:38:52
11:38:56.414 | INFO    | Task run 'read_data-c914d840-1' - Finished in state Completed()
11:38:56.484 | INFO    | Task run 'prepare_features-21588f7a-1' - Task prepare_features: Current execution date:06/08/2022, 11:38:56
11:38:56.649 | INFO    | Task run 'prepare_features-21588f7a-1' - The mean duration of validation is18.62060009088383
11:38:56.649 | INFO    | Task run 'prepare_features-21588f7a-1' - Validation number of record:1087102
The mean duration of validation is 18.62060009088383
11:39:02.844 | INFO    | Task run 'prepare_features-21588f7a-1' - Finished in state Completed()
11:39:02.916 | INFO    | Task run 'train_model-4ca07dca-0' - Task train_model: Current execution date:06/08/2022, 11:39:02
The shape of X_train is (1126605, 525)
The DictVectorizer has 525 features
2022/06/08 11:39:08 INFO mlflow.utils.autologging_utils: Created MLflow autologging run with ID 'd6fa65c9a4414d96a3040041dcd8b64e', which will track hyperparameters, performance metrics, model artifacts, and lineage information for the current sklearn workflow
2022/06/08 11:39:16 WARNING mlflow.utils.autologging_utils: MLflow autologging encountered a warning: "/home/ubuntu/anaconda3/envs/mlflow-mlops/lib/python3.9/site-packages/_distutils_hack/__init__.py:30: UserWarning: Setuptools is replacing distutils."
The MSE of training is: 11.587482939508662
11:39:16.470 | INFO    | Task run 'train_model-4ca07dca-0' - The MSE of training is:11.587482939508662
11:39:16.471 | INFO    | Task run 'train_model-4ca07dca-0' - LinearRegression()
11:39:16.728 | INFO    | Task run 'train_model-4ca07dca-0' - Finished in state Completed()
11:39:16.791 | INFO    | Task run 'save_model-e70fc77d-0' - model pklfile name is: model-{2021-08-15}.pkl
11:39:16.819 | INFO    | Task run 'save_model-e70fc77d-0' - Finished in state Completed()
11:39:16.881 | INFO    | Task run 'save_model-e70fc77d-1' - model pklfile name is: DictVectorizer-{2021-08-15}.pkl
11:39:16.910 | INFO    | Task run 'save_model-e70fc77d-1' - Finished in state Completed()
The MSE of validation is: 11.989006232890928
11:39:22.138 | INFO    | Task run 'run_model-0dc1f5ad-0' - Finished in state Completed()
/home/ubuntu/anaconda3/envs/mlflow-mlops/lib/python3.9/site-packages/prefect/deployments.py:247: UserWarning: You have configured local storage, this deployment will only be usable from the current machine..
  warnings.warn(
Creating deployment 'cron-schedule-mlfhv-training-deployment' for flow 'main'...
Deploying flow script from '/home/ubuntu/mlops-zoomcamp/03-orchestration/assignment/homework_assignment_3.py' using Local Storage...
Created deployment 'main/cron-schedule-mlfhv-training-deployment'.
View your new deployment with: 

    prefect deployment inspect 'main/cron-schedule-mlfhv-training-deployment'
Created 1 deployments!
(mlflow-mlops) ubuntu@ip-172-31-28-166:~/mlops-zoomcamp/03-orchestration/assignment$ 
```

**Answer:**  It is `0 9 15 * *`

### Q5. Viewing the Deployment

View the deployment in the UI. When first loading, we may not see that many flows because the default filter is 1 day back and 1 day forward. Remove the filter for 1 day forward to see the scheduled runs.

How many flow runs are scheduled by Prefect in advance? You should not be counting manually. There is a number of upcoming runs on the top right of the dashboard.

- 0
- 3
- 10
- 25

**Answer:** The correct one is 3.

### Q6. Creating a work-queue

In order to run this flow, you will need an agent and a work queue. Because we scheduled our flow on every month, it won't really get picked up by an agent. For this exercise, create a work-queue from the UI and view it using the CLI.

For all CLI commands with Prefect, you can use `--help` to get more information.

For example,

- `prefect --help`
- `prefect work-queue --help`

What is the command to view the available work-queues?

- `prefect work-queue inspect`
- `prefect work-queue ls`
- `prefect work-queue preview`
- `prefect work-queue list`

**Answer:** It is `prefect work-queue ls`
