import os
import re
import urllib
import zipfile
from datetime import timedelta, datetime

import requests
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

SOURCE_URL = 'https://s3.amazonaws.com/capitalbikeshare-data/' # Source link
ZIPP_DIRECTORY= '/opt/airflow/data/zipdata' # Zip file path
CSV_DIRECTORY= '/opt/airflow/data/raw_data' # raw file path

def download_zipfile():

    """
    Download the zipfile and unzip it to /opt/airflow/data/raw_data
    :return: None

    """
    os.makedirs(ZIPP_DIRECTORY,exist_ok=True)
    os.makedirs(CSV_DIRECTORY,exist_ok=True)

    print(f'checkin URL {SOURCE_URL}')
    response = requests.get(SOURCE_URL)
    zip_links = re.findall(r'<Key>([^<]+?\.zip)</Key>', response.text)
    for key in zip_links:
        link = f'https://s3.amazonaws.com/capitalbikeshare-data/{key}'
        filename = os.path.basename(link)
        zip_path = os.path.join(ZIPP_DIRECTORY, filename)
        print(f'downloading {filename} -> {zip_path}')
        urllib.request.urlretrieve(link, zip_path)
        print('data downloaded')

        print(f'unzipping {zip_path} -> {CSV_DIRECTORY}')

        try:
            with zipfile.ZipFile(zip_path) as zip_file:
                zip_file.extractall(CSV_DIRECTORY)
            print(f'data extracted to {CSV_DIRECTORY}')
        except zipfile.BadZipFile as e:
            print(f'data not unzip : {e}')

        # os.remove(zip_path)



defualte_args = {
    'owner': 'Saman',
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=2),
}


with DAG(
    dag_id='ingest_data',
    description='DAG for ingesting data',
    default_args=defualte_args,
    schedule_interval='*/2 * * * *',
    catchup=False,
    start_date=datetime(2025, 7, 3),

) as dag:
    task_download_and_unzip = PythonOperator(task_id='download_zipfile',
                                             python_callable=download_zipfile,
                                             dag=dag
                                             )

    task_download_and_unzip
