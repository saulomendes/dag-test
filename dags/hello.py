import datetime
import pendulum

from datetime import timedelta
from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator

default_args = {
    'start_date': pendulum.today('UTC').add(days=0),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}


@dag(default_args=default_args, schedule="@daily")
def generate_dag():
    EmptyOperator(task_id="task")


generate_dag()
