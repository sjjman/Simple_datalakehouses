import re

from pyspark.sql import DataFrame
from pyspark.sql.functions import to_timestamp,expr

def clean_column_name(col_name):
    """
    Clean column name
    :param col_name:
    :return: Cleaned column name
    """
    return re.sub(r'[ ,;{}()\n\t=]', '_', col_name)
def clean_bronze(df: DataFrame) -> DataFrame:
    """
    Clean bronze
    :param df:
    :return: Cleaned bronze
    """
    df = df.toDF(*[clean_column_name(col) for col in df.columns])
    df = df.withColumn("Start_date",to_timestamp(df['Start_date'],'yyyy-MM-dd-HH.mm.ss.SSSSSS'))\
            .withColumn("End_date", to_timestamp(df['End_date'],'yyyy-MM-dd-HH.mm.ss.SSSSSS'))\
            .drop("Start_date")\
            .drop("End_date")\
            .withColumn('Duration1',df['Duration'].cast('int'))\
            .drop('Duration')


    df = df.dropna()
    return df


