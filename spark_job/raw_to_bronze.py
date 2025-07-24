import os

from delta import configure_spark_with_delta_pip

from src.piplines.bronze_etl import clean_bronze

from pyspark.sql import SparkSession

"""
    Make Spark Session
    Install Delta package
    Use delta package in spark
"""

builder = SparkSession.builder \
    .appName('ETL raw to bronze') \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()


RAWDATAPATH = '/opt/airflow/data/raw_data'
PROCESSEDDATAPATH = '/opt/airflow/processedFiles/processed.txt'
BRONZEDDATAPATH = '/opt/airflow/data/bronze'


def check_file_processed():
    """
    Check if processed file exists

    :return: List of file paths
    """
    if not os.path.exists(PROCESSEDDATAPATH):
        return set()
    with open(PROCESSEDDATAPATH) as f:
        return set(line.strip() for line in f.readlines())

def save_processed_files(new_files):
    """
    Save processed files
    :param new_files:
    :return:
    """
    with open(PROCESSEDDATAPATH, 'a') as f: 
        for file in new_files:
            f.write(file + '\n')

def main():
    """
    Main function
    Check if processed file exists
    Send to delta Format
    :return:
    """
    processed_files = check_file_processed()
    all_files = [f for f in os.listdir(RAWDATAPATH) if f.endswith('.csv')]
    new_files = [f for f in all_files if f not in processed_files]

    if not new_files:
        print("No new files to process.")
        return

    new_files_path = [os.path.join(RAWDATAPATH, f) for f in new_files]
    print(f"📥 New files found: {new_files}")
    df = spark.read.option("header", True).format("csv").load(new_files_path)


    df = clean_bronze(df)
    df.write.format("delta").mode("append").save(BRONZEDDATAPATH)

    save_processed_files(new_files)
    print("ETL to bronze completed successfully.")

if __name__ == "__main__":
    main()
    spark.stop()
