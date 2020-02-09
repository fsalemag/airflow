from __future__ import print_function
from builtins import range
from airflow.operators import PythonOperator
from airflow.models import DAG
from datetime import datetime, timedelta

import time
from pprint import pprint
from scripts.sendEmail import sendEmail

seven_days_ago = datetime.combine(
        datetime.today() - timedelta(7), datetime.min.time())

args = {
    'owner': 'airflow',
    'start_date': seven_days_ago,
}

dag = DAG(
    dag_id='example_python_operator', default_args=args,
    schedule_interval=None)





def print_context(ds, **kwargs):
    print("Kwargs CARALHO!")
    pprint(kwargs)
    print("DS CARALHI!")
    print(ds)
    return 'Whatever you return gets printed in the logs'

run_this = PythonOperator(
    task_id='print_the_context',
    provide_context=True,
    python_callable=print_context,
    dag=dag)


for i in range(2):
    task = PythonOperator(
        task_id='send_email_'+str(i),
        python_callable=sendEmail,
        op_kwargs={'name': "Alberto", "email":"francisco.salema.g@gmail.com"},
        dag=dag)

    task.set_upstream(run_this)