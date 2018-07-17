# This DAG consists of a single BashOperator that prints the result of a coin flip.

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from dependencies import coin_package

default_args = {
    'start_date':
        datetime.combine(
            datetime.today() - timedelta(days=1), datetime.min.time()),
}

with DAG('dependencies_dag', default_args=default_args) as dag:
  t1 = BashOperator(
      task_id='print_coin_result',
      bash_command='echo "{0}"'.format(coin_package.flip_coin()),
      dag=dag)
