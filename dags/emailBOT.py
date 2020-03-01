from __future__ import print_function
from builtins import range
from airflow.operators.python_operator import PythonOperator
from airflow.models import DAG, XCom
from datetime import datetime, timedelta
import time
from pprint import pprint
from scripts.sendEmail import sendEmail
from scripts.checkInbox import checkInbox


args = {
    'owner': 'airflow',
    'start_date': datetime(2020, 3, 1, 15, 45, 0), 
}

dag = DAG(
    dag_id='emailBOT', 
    default_args=args,
    schedule_interval="*/1 * * * *"
)

check_inbox = PythonOperator(
    task_id='check_inbox',
    provide_context=True,
    python_callable=checkInbox,
    dag=dag
)


send_email = PythonOperator(
    task_id='send_email',
    python_callable=sendEmail,
    provide_context=True, 
    dag=dag
)

check_inbox >> send_email
