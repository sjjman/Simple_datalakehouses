import os

from delta import configure_spark_with_delta_pip

from src.piplines.bronze_to_silver_etl import aggregated_data

from pyspark.sql import SparkSession

builder = SparkSession.builder \
    .appName('ETL bronze to silver') \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()


SILVERDATAPATH = '/opt/airflow/data/siver'

BRONZEDDATAPATH = '/opt/airflow/data/bronze'


def main():
    """
    Get Raw data from Bronze to Silver
    group By Bike_number
    Write to delta formatted file
    """
    df = spark.read.format("delta").load(BRONZEDDATAPATH)
    df =  aggregated_data(df)
    df.write.format("delta").mode('append').save(SILVERDATAPATH)

if __name__ == "__main__":
    main()
    spark.stop()