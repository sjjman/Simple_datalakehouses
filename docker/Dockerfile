FROM docker.arvancloud.ir/apache/airflow:2.10.0

USER root



# نصب Java با دسترسی ریشه

RUN apt-get update && \
    apt-get install -y openjdk-17-jdk && \
    apt-get clean

# تنظیم JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

USER airflow

RUN pip3 install apache-airflow-providers-apache-spark==5.3.1
RUN pip install pyspark==3.5.4 delta-spark==3.1.0

RUN pip3 install importlib-metadata


USER airflow
