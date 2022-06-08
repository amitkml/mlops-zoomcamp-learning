from prefect.deployments import DeploymentSpec
from prefect.orion.schemas.schedules import CronSchedule
from prefect.task_runners import SequentialTaskRunner
from prefect.flow_runners import SubprocessFlowRunner

DeploymentSpec(
    name="cron-schedule-mlfhv-15-deployment",
    flow_location="homework_assignment_3.py",
    # storage_type="Local Storage",
    flow_runner=SubprocessFlowRunner(),
    schedule=CronSchedule(
        cron="0 9 25 * *",
        timezone="America/New_York"),
)