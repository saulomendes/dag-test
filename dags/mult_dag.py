import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator

dags = ['A', 'B', 'C']
for dag_name in dags:
    with DAG(dag_id=f"mult_dag_{dag_name}",
            start_date=datetime.datetime(2021, 1, 1),
            schedule="@daily",
            tags=["mult_dag", dag_name]
    ) as dag:
        start = EmptyOperator(task_id="start")
        end = EmptyOperator(task_id="end")
        options = ["branch_a", "branch_b", "branch_c", "branch_d"]
        for option in options:
            t = EmptyOperator(task_id=option)
            start >> t >> end


