import os
import logging

SPARK_MASTER_IP_VAR_NAME = 'SPARK_MASTER_IP'
spark_master_ip = None
spark = None

logging.basicConfig(level='DEBUG')
logger = logging.getLogger('chispark_connection')

# Получаем значение переменной окружения SPARK_MASTER_IP
def get_spark_master_ip():
    spark_master_ip = os.getenv(SPARK_MASTER_IP_VAR_NAME)
    if spark_master_ip:
        logger.debug(f"spark_master_ip: {spark_master_ip}")
        return spark_master_ip
    else:
        logger.critical("spark_master_ip NOT EXIST!")
        return None


def spark_app_builder(spark_master_ip= None,
                      spark_app_name = "pyspark-taxi-forecasting"):
# Если переменная окружения установлена, используем ее для настройки Spark Session
    if spark_master_ip:
        logger.debug('starting import SparkSession')
        from pyspark.sql import SparkSession
        logger.debug(f"starting building spark app object: {spark_app_name}")
        spark = SparkSession.builder.appName(spark_app_name) \
            .master(f"spark://{spark_master_ip}:7077") \
            .config("spark.executor.cores", "1") \
            .config("spark.task.cpus", 1) \
            .getOrCreate()
        logger.debug(f"builded spark app object: {spark}")
        return spark
    else:
        logger.debug(f"enviroment variable: {SPARK_MASTER_IP_VAR_NAME} not recieved")
        return None

def stop_spark_app(spark=spark):
    if spark:
        try:
            # Попытка остановить SparkSession
            logger.debug(f"attempt to stop SparkSession app object")
            spark.stop()
            logger.debug(".stop() instruction has been executed")

            # Попытка выполнить операцию после остановки сессии, чтобы проверить её состояние
            logger.debug(f"attempt to operate SparkSession app object after stopping")
            try:
                spark.sql("SELECT 1")
                logger.error("Attention: The Spark Session was not stopped correctly.")
                return 'runnig'
            except Exception as e:
                logger.info("The Spark Session was stopped correctly")
                return 'stopped'
        except Exception as e:
            logger.error(f"An error occurred while trying to stop SparkSession: {e}")
        return 'error:' + str(e)
    else:
        logger.debug("attempt to stop NOT EXISTING SparkSession app object")
        return 'empty'



def main(name):
    logger.debug(f'Enter in the main() function: name = {name}')
    logger.debug('****************************************************')
    logger.debug('Attempt to run get_spark_master_ip() function')
    spark_master_ip = get_spark_master_ip()
    logger.debug(f"Result is: {spark_master_ip}")
    logger.debug('****************************************************')
    logger.debug('Checking existing logger objects')
    for key in logging.Logger.manager.loggerDict:
        logger.debug(key)
    logger.debug('****************************************************')
    logger.debug('Attempt to run spark_app_builder() function')
    spark = spark_app_builder(spark_master_ip)
    logger.debug(f"Result is: {spark}")
    logger.debug('****************************************************')
    logger.debug('Attempt to run stop_spark_app() function')
    stop_msg = stop_spark_app(spark)
    logger.debug(f"Result is: {stop_msg}")

    
if __name__ == '__main__':
    main(__name__)
