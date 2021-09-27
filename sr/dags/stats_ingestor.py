import datetime
import time

from airflow import models
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

from kubernetes.client import models as k8s

default_args = {
    'email': ['kinyock.va@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=5)
}

FIRST_START_DATE = datetime.datetime(2021, 9, 24, 11, 30)
EXECUTION_DATE = "{{ execution_date }}"
PREVIOUS_EXECUTION_DATE = "{{ prev_execution_date }}"
START_DATE = "{{ dag_run.start_date }}"
SCHEDULE_INTERVAL = "*/5 * * * *"

with models.DAG(
        dag_id='stats_ingestor_dag',
        schedule_interval=SCHEDULE_INTERVAL,
        start_date=FIRST_START_DATE,
        catchup=False
    ) as dag:

    kubernetes_min_pod = KubernetesPodOperator(
        task_id='stats_ingestor_task',
        name='stats_ingestor_task',
        cmds=[
            'python',
            'stats.py',
            '--window-start',
            PREVIOUS_EXECUTION_DATE,
            '--window-end',
            EXECUTION_DATE
        ],
        namespace='airflow',
        is_delete_operator_pod=False,
        image='stats:latest',
        get_logs=True,
        image_pull_policy='Never',
        executor_config={
            "pod_override": k8s.V1Pod(
                spec=k8s.V1PodSpec(
                    containers=[
                        k8s.V1Container(
                            name="base",
                            volume_mounts=[
                                k8s.V1VolumeMount(
                                    mount_path="/opt/airflow/dags", name="dags-volume"
                                )
                            ],
                        )
                    ],
                    volumes=[
                        k8s.V1Volume(
                            name="dags-volume",
                            host_path=k8s.V1HostPathVolumeSource(path="/mnt/airflow/dags_sr"),
                        )
                    ],
                )
            ),
        },
    )
