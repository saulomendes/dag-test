import datetime
import pendulum

from datetime import timedelta
from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from kubernetes.client import models as k8s_models

default_args = {
    'start_date': pendulum.today('UTC').add(days=0),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

@dag(default_args=default_args, schedule="@daily")
def pod_operator_hello():

    # kubernetes_min_pod = KubernetesPodOperator(
    #     # The ID specified for the task.
    #     task_id="pod-ex-minimum",
    #     # Name of task you want to run, used to generate Pod ID.
    #     name="pod-ex-minimum",
    #     # Entrypoint of the container, if not specified the Docker container's
    #     # entrypoint is used. The cmds parameter is templated.
    #     cmds=["echo"],
    #     # The namespace to run within Kubernetes. In Composer 2 environments
    #     # after December 2022, the default namespace is
    #     # `composer-user-workloads`.
    #     namespace="composer-user-workloads",
    #     # Docker image specified. Defaults to hub.docker.com, but any fully
    #     # qualified URLs will point to a custom repository. Supports private
    #     # gcr.io images if the Composer Environment is under the same
    #     # project-id as the gcr.io images and the service account that Composer
    #     # uses has permission to access the Google Container Registry
    #     # (the default service account has permission)
    #     image="gcr.io/gcp-runtimes/ubuntu_20_0_4",
    #     # Specifies path to kubernetes config. If no config is specified will
    #     # default to '~/.kube/config'. The config_file is templated.
    #     config_file="/home/airflow/composer_kube_config",
    #     # Identifier of connection that should be used
    #     kubernetes_conn_id="kubernetes_default",
    #     container_resources=k8s_models.V1ResourceRequirements(
    #         limits={"memory": "250M", "cpu": "100m"},
    #     ),
    # )

    pod = KubernetesPodOperator(
        task_id="dry_run_demo",
        name="hello-dry-run",
        image="debian",
        cmds=["bash", "-cx"],
        arguments=["echo", "10"],
        labels={"foo": "bar"},
        do_xcom_push=True,
        container_resources=k8s_models.V1ResourceRequirements(
            limits={"memory": "250M", "cpu": "100m"},
        ),
    )

    write_xcom_async = KubernetesPodOperator(
        task_id="kubernetes_write_xcom_task_async",
        namespace="default",
        image="alpine",
        cmds=["sh", "-c", "mkdir -p /airflow/xcom/;echo '[1,2,3,4]' > /airflow/xcom/return.json"],
        name="write-xcom",
        do_xcom_push=True,
        on_finish_action="delete_pod",
        in_cluster=True,
        get_logs=True,
        deferrable=True,
        container_resources=k8s_models.V1ResourceRequirements(
            limits={"memory": "100M", "cpu": "100m"},
        ),
    )

    pod_task_xcom_result_async = BashOperator(
        task_id="pod_task_xcom_result_async",
        bash_command="echo \"{{ task_instance.xcom_pull('write-xcom')[0] }}\"",
    )



pod_operator_hello()