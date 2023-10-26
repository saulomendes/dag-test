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

@dag(default_args=default_args, schedule="@daily")
def pod_operator_hello():
    # EmptyOperator(task_id="task")
    pod = KubernetesPodOperator(
        task_id="dry_run_demo",
        name="hello-dry-run",
        image="debian",
        cmds=["bash", "-cx"],
        arguments=["echo", "10"],
        labels={"foo": "bar"},
        do_xcom_push=True,
    )

    pod.dry_run() 

pod_operator_hello()