import datetime

from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator


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

    # k.dry_run() 


generate_dag()