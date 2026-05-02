from airflow import DAG  # type: ignore
from airflow.operators.bash import BashOperator  # type: ignore
from datetime import datetime, timedelta


default_args = {
    "retries": 0,
    "retry_delay": timedelta(minutes=0),
}


with DAG(
    dag_id="webtran_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="0 10 * * 1-5",
    catchup=False,
    default_args=default_args,
    tags=["data_engineering", "selenium", "etl"],
) as dag:

    extrair_arquivo = BashOperator(
        task_id="extrair_arquivo_webtran",
        bash_command="python /usr/local/airflow/include/scripts/download.py",
        retries=0,
    )

    transformar_dados = BashOperator(
        task_id="tratar_dados",
        bash_command="python /usr/local/airflow/include/scripts/transform.py",
        retries=0,
    )

    extrair_arquivo >> transformar_dados