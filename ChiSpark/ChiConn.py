import os

# Получаем значение переменной окружения SPARK_MASTER_IP
spark_master_ip = os.getenv('SPARK_MASTER_IP')

# Если переменная окружения установлена, используем ее для настройки Spark Session
if spark_master_ip:
    from pyspark.sql import SparkSession
    spark = SparkSession.builder.appName("pyspark-taxi-forecasting") \
        .master(f"spark://{spark_master_ip}:7077") \
        .config("spark.executor.cores", "1") \
        .config("spark.task.cpus", 1) \
        .getOrCreate()
    print(f"Spark Master IP: {spark_master_ip}")
    spark.stop()
else:
    print("Переменная окружения SPARK_MASTER_IP не установлена")