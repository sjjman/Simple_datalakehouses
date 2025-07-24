from datetime import timedelta, datetime
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow import DAG


"""
    Run ETL raw to bronze 
    Run ETL bronze to silver
"""




defualte_args = {
    'owner': 'Saman',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=10),
}

with DAG(
    dag_id='pipeline',
    description='DAG for ingesting data',
    default_args=defualte_args,
    schedule_interval='*/5 * * * *',
    catchup=False,
    start_date=datetime(2025, 7, 3),

) as dag:
    task_raw_to_bronze = SparkSubmitOperator(
        task_id='etl_bronze',
        application='/opt/airflow/spark_job/raw_to_bronze.py',
        conn_id='spark-conn-id',
        packages='io.delta:delta-spark_2.12:3.1.0',
        conf={
            "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog"
        },
        dag=dag
    )

    task_bronze_to_silver = SparkSubmitOperator(
        task_id='etl_silver',
        application='/opt/airflow/spark_job/bronze_to_silver.py',
        conn_id='spark-conn-id',
        packages='io.delta:delta-spark_2.12:3.1.0',
        conf={
            "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog"
        },
        dag=dag
    )

    task_raw_to_bronze >> task_bronze_to_silver
