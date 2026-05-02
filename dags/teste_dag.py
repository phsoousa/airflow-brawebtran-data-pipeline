from airflow import DAG  # type: ignore
from airflow.operators.bash import BashOperator  # type: ignore
from datetime import datetime

with DAG(
    dag_id="teste_dag",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False
) as dag:

    tarefa = BashOperator(
        task_id="task_1",
        bash_command="echo 'ok'"
    )