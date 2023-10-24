import datetime
import time
import airflow

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from random import randrange
from datetime import timedelta

dags = ['A', 'B', 'C']

default_args = {
    'start_date': airflow.utils.dates.days_ago(0),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

for dag_name in dags:
    with DAG(dag_id=f"mult_dag_{dag_name}",
            default_args=default_args,
            schedule="@daily",
            tags=["mult_dag", dag_name]
    ) as dag:
        start = EmptyOperator(task_id="start")
        end = EmptyOperator(task_id="end")
        options = ["branch_a", "branch_b", "branch_c", "branch_d"]
        for option in options:
            # t = EmptyOperator(task_id=option)
            t = PythonOperator(
                task_id=option,
                python_callable=lambda: time.sleep(randrange(10)),
                # op_kwargs: Optional[Dict] = None,
                # op_args: Optional[List] = None,
                # templates_dict: Optional[Dict] = None
                # templates_exts: Optional[List] = None
            )    

            start >> t >> end


