from __future__ import print_function
from builtins import range
from airflow.operators.python_operator import PythonOperator
from airflow.models import DAG, XCom
from datetime import datetime, timedelta

import time
from pprint import pprint
from scripts import checkInbox

seven_days_ago = datetime.combine(datetime.today() - timedelta(7), datetime.min.time())

args = {
    'owner': 'airflow',
    'start_date': seven_days_ago,
}

dag = DAG(
    dag_id='emailBOT', default_args=args,
    schedule_interval='0 0/5 * * * ? *')



check_inbox = PythonOperator(
    task_id='check_inbox',
    provide_context=True,
    python_callable=scripts.checkInbox,
    dag=dag)


send_email = PythonOperator(
    task_id='send_email_',
    python_callable=scripts.sendEmail,
    provide_context=True, 
    op_kwargs={'name': "Person", "email":"x_salema@hotmail.com"},
    dag=dag)

check_inbox >> send_email
