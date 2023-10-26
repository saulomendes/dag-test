import datetime
import pendulum

from datetime import timedelta
from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator

default_args = {
    'start_date': pendulum.today('UTC').add(days=0),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

@dag(start_date=datetime.datetime(2023, 10, 25), schedule="@daily")
def generate_dag():
    # EmptyOperator(task_id="task")
    k = KubernetesPodOperator(
        name="hello-dry-run",
        image="debian",
        cmds=["bash", "-cx"],
        arguments=["echo", "10"],
        labels={"foo": "bar"},
        task_id="dry_run_demo",
        do_xcom_push=True,
    )

    k.dry_run() 
