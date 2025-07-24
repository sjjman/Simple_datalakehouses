#!/bin/bash

echo "Run Batch Raw To Bronze 👌👌👌"

spark-submit --master spark://spark:7077 \
    --packages io.delta:delta-spark_2.12:3.1.0 \
    --conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" \
    --conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog" \
    /opt/airflow/spark_job/bronze_to_silver.py
echo "Batch Job Done!!!👌👌👌"
