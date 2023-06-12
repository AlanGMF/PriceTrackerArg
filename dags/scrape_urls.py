from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 6, 9, 18, 0),  # Fecha y hora de inicio deseada
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'curl_request_dag',
    default_args=default_args,
    schedule_interval='0 18 * * *',
)

start = DummyOperator(task_id='start', dag=dag)

curl_request_dia = BashOperator(
    task_id='curl_request_dia',
    bash_command='curl http://scrapyd:6800/schedule.json -d project=supermercados -d spider=dia',
    dag=dag,
)
curl_request_coto = BashOperator(
    task_id='curl_request_coto',
    bash_command='curl http://scrapyd:6800/schedule.json -d project=supermercados -d spider=coto',
    dag=dag,
)
curl_request_disco = BashOperator(
    task_id='curl_request_disco',
    bash_command='curl http://scrapyd:6800/schedule.json -d project=supermercados -d spider=disco',
    dag=dag,
)
curl_request_jumbo = BashOperator(
    task_id='curl_request_jumbo',
    bash_command='curl http://scrapyd:6800/schedule.json -d project=supermercados -d spider=jumbo',
    dag=dag,
)
curl_request_mas = BashOperator(
    task_id='curl_request_mas',
    bash_command='curl http://scrapyd:6800/schedule.json -d project=supermercados -d spider=mas',
    dag=dag,
)

end = DummyOperator(task_id='end', dag=dag)

start >> curl_request_dia >> end#curl_request_coto >> curl_request_disco >> curl_request_jumbo >> curl_request_mas >> end
