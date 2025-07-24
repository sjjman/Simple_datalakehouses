from pyspark.sql.functions import *
from pyspark.sql import DataFrame

def aggregated_data(df: DataFrame)->DataFrame:

    """
    Get aggregated data

    :param df:
    :return: aggregated data
    """

    df_agg = df.groupBy('Bike_number').agg(
        sum('Duration1').alias('allDuration'),
    )
    return df_agg


