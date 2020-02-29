from airflow.operators.python_operator import PythonOperator
from airflow.models import DAG
from datetime import datetime, timedelta

import scripts

args = {
    "owner": "airflow",
    "start_date": datetime(2020, 2, 1)
}

dag = DAG(
        dag_id="email_bot",
        default_args = args,
        schedule_interval="*/1 * * * *"
    )


def test(ds, **kwargs):
    print(kwargs)
    print(ds)
    print('-' * 75)

test_op = PythonOperator(
        task_id = "test_task",
        python_callable = test,
        provide_context = True,
        dag = dag
    )


