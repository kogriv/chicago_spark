import os
import logging
from .enviserv.mylog import MyLogger

SPARK_MASTER_IP_VAR_NAME = 'SPARK_MASTER_IP'
spark_master_ip = None
spark = None


# ['DEBUG','INFO','WARNING','ERROR','CRITICAL']
# [10     ,20    ,30       ,40     ,50]

logging.basicConfig(level='INFO')

cnlog = MyLogger(name='ch',create_level='DEBUG',enable_logging=True)



# Получаем значение переменной окружения SPARK_MASTER_IP
def get_spark_master_ip():
    spark_master_ip = os.getenv(SPARK_MASTER_IP_VAR_NAME)
    if spark_master_ip:
        cnlog.mylev(20,f"spark_master_ip: {spark_master_ip}")
        return spark_master_ip
    else:
        cnlog.mylev(30,"spark_master_ip NOT EXIST!")
        return None


def spark_app_builder(spark_master_ip= None,
                      spark_app_name = "pyspark-taxi-forecasting"):
# Если переменная окружения установлена, используем ее для настройки Spark Session
    if spark_master_ip:
        cnlog.mylev(10,'starting import SparkSession')
        from pyspark.sql import SparkSession
        cnlog.mylev(20,f"starting building spark app object: {spark_app_name}")
        spark = SparkSession.builder.appName(spark_app_name) \
            .master(f"spark://{spark_master_ip}:7077") \
            .config("spark.executor.cores", "1") \
            .config("spark.task.cpus", 1) \
            .getOrCreate()
        cnlog.mylev(20,f"builded spark app object: {spark}")
        return spark
    else:
        cnlog.mylev(20,f"enviroment variable: {SPARK_MASTER_IP_VAR_NAME} not recieved")
        return None

def stop_spark_app(spark=spark):
    if spark:
        try:
            # Попытка остановить SparkSession
            cnlog.mylev(20,f"attempt to stop SparkSession app object")
            spark.stop()
            cnlog.mylev(20,".stop() instruction has been executed")

            # Попытка выполнить операцию после остановки сессии, чтобы проверить её состояние
            cnlog.mylev(20,f"attempt to operate SparkSession app object after stopping")
            try:
                spark.sql("SELECT 1")
                cnlog.mylev(40,"Attention: The Spark Session was not stopped correctly.")
                return 'runnig'
            except Exception as e:
                cnlog.mylev(20,"The Spark Session was stopped correctly")
                return 'stopped'
        except Exception as e:
            cnlog.mylev(40,f"An error occurred while trying to stop SparkSession: {e}")
        return 'error:' + str(e)
    else:
        cnlog.mylev(20,"attempt to stop NOT EXISTING SparkSession app object")
        return 'empty'



def _main(name):
    cnlog.mylev(10,f'Enter in the main() function: name = {name}')
    cnlog.mylev(10,'****************************************************')
    cnlog.mylev(10,'Attempt to run get_spark_master_ip() function')
    spark_master_ip = get_spark_master_ip()
    cnlog.mylev(10,f"Result is: {spark_master_ip}")
    cnlog.mylev(10,'****************************************************')
    cnlog.mylev(10,'Checking existing logger objects')
    for key in logging.Logger.manager.loggerDict:
        cnlog.mylev(10,key)
    cnlog.mylev(10,'****************************************************')
    cnlog.mylev(10,'Attempt to run spark_app_builder() function')
    spark = spark_app_builder(spark_master_ip)
    cnlog.mylev(10,f"Result is: {spark}")
    cnlog.mylev(10,'****************************************************')
    cnlog.mylev(10,'Attempt to run stop_spark_app() function')
    stop_msg = stop_spark_app(spark)
    cnlog.mylev(10,f"Result is: {stop_msg}")

    
if __name__ == '__main__':
    _main(__name__)

