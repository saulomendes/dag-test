import datetime
import pendulum

from datetime import timedelta
from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from kubernetes.client import models as k8s_models

default_args = {
    'start_date': pendulum.today('UTC').add(days=0),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

@dag(default_args=default_args, schedule="@daily")
def pod_operator_hello():
    # EmptyOperator(task_id="task")

    kubernetes_min_pod = KubernetesPodOperator(
        # The ID specified for the task.
        task_id="pod-ex-minimum",
        # Name of task you want to run, used to generate Pod ID.
        name="pod-ex-minimum",
        # Entrypoint of the container, if not specified the Docker container's
        # entrypoint is used. The cmds parameter is templated.
        cmds=["echo"],
        # The namespace to run within Kubernetes, default namespace is
        # `default`. In Composer 1 there is the potential for
        # the resource starvation of Airflow workers and scheduler
        # within the Cloud Composer environment,
        # the recommended solution is to increase the amount of nodes in order
        # to satisfy the computing requirements. Alternatively, launching pods
        # into a custom namespace will stop fighting over resources,
        # and using Composer 2 will mean the environment will autoscale.
        namespace="default",
        # Docker image specified. Defaults to hub.docker.com, but any fully
        # qualified URLs will point to a custom repository. Supports private
        # gcr.io images if the Composer Environment is under the same
        # project-id as the gcr.io images and the service account that Composer
        # uses has permission to access the Google Container Registry
        # (the default service account has permission)
        image="gcr.io/gcp-runtimes/ubuntu_18_0_4",
    )
    
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

    pod.dry_run() 

pod_operator_hello()