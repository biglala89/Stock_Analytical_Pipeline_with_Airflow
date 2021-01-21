from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import timedelta, date, datetime
import yfinance as yf
import os


stock_dag = DAG(
    dag_id='MarketVol',
    schedule_interval="30 2 * * 1-5",
    start_date=days_ago(1)
)


tmp_folder_task = BashOperator(
    task_id='create_tmp_folder',
    bash_command="mkdir -p ${AIRFLOW_HOME}/tmp/data/`date +'%Y-%m-%d'`",
    dag=stock_dag
)


def fetch_price(**kwargs):
    start_date = date.today()
    print(start_date)
    end_date = start_date + timedelta(days=1)
    print(end_date)
    df = yf.download(kwargs['ticker'], start=start_date,
                     end=end_date, interval='1m')
    df.to_csv(
        "{}/tmp/data/{}/{}.csv".format(os.getcwd(), start_date, kwargs['ticker']))


tesla_price_task = PythonOperator(
    task_id='download_telsa_price',
    python_callable=fetch_price,
    op_kwargs={'ticker': 'TSLA'},
    dag=stock_dag,
    retries=3,
    retry_delay=5,
)


apple_price_task = PythonOperator(
    task_id='download_apple_price',
    python_callable=fetch_price,
    op_kwargs={'ticker': 'AAPL'},
    dag=stock_dag,
    retries=3,
    retry_delay=5,
)


tesla_analyze_task = BashOperator(
    task_id='tesla_price_analyzer',
    bash_command='python ${AIRFLOW_HOME}/script/stock_analyzer.py --symbol TSLA',
    dag=stock_dag
)


apple_analyze_task = BashOperator(
    task_id='apple_price_analyzer',
    bash_command='python ${AIRFLOW_HOME}/script/stock_analyzer.py --symbol AAPL',
    dag=stock_dag
)


error_log_task = BashOperator(
    task_id='error_log_analyzer',
    bash_command='python ${AIRFLOW_HOME}/script/log_analyzer.py -p ${AIRFLOW_HOME}/logs/MarketVol -v 0',
    dag=stock_dag
)

tmp_folder_task >> [tesla_price_task, apple_price_task]
tesla_price_task >> tesla_analyze_task
apple_price_task >> apple_analyze_task
[tesla_analyze_task, apple_analyze_task] >> error_log_task
