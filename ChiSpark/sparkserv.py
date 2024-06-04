import os
import logging
from enviserv.mylog import MyLogger

import re
from pyspark.sql import DataFrame

class Cols:
    def __init__(self, df: DataFrame = None,
                 method: str = "first_word_and_next_letters"):
        if df is None:
            print('Spark DF not feeded. Simple sample will create')
            sp = SparkApp(my_logger_create_level='CRITICAL')
            spark = sp.build_spark_app()
            data = [("Value1", "Value2"), ("Value3", "Value4")]
            columns = ["One columns", "Another one"]
            df = spark.createDataFrame(data, columns)
        self._df = df
        self._method = method
        self._aliases = {}
        
        for col_name in df.columns:
            alias_name = self._create_alias(col_name)
            setattr(self, alias_name, col_name)
            self._aliases[alias_name] = col_name

    
    def testtt(self):
        print('*******-------------*******')

    def _create_alias(self, col_name: str, index: int = 1) -> str:
        col_name = col_name.lower()
        if self._method == "first_word_and_next_letters":
            # Split the column name by space or period and filter out empty parts
            parts = [part for part in re.split(r'[ .]', col_name) if part]
            # Create alias name
            if len(parts) > 1:
                alias_name = parts[0] + "_" + "".join(part[0] for part in parts[1:])
            else:
                alias_name = parts[0]
            # Ensure alias is a valid Python attribute name
            alias_name = re.sub(r'\W|^(?=\d)', '_', alias_name)
            # Check if alias_name already exists
            if alias_name in self._aliases:
                # Get the last word of col_name
                last_word = parts[-1]
                # Append two characters from the last word
                alias_name += last_word[1:3]
                # Check if the new alias_name already exists recursively
                if alias_name in self._aliases:
                    # Append the index
                    alias_name += f"_{index:03d}"
                    # Recursively check again
                    return self._create_alias(col_name, index + 1)
            return alias_name.lower()
        else:
            raise ValueError(f"Unknown alias creation method: {self._method}")


    def __getattr__(self, name):
        if name in self._aliases:
            return self._aliases[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        if '_aliases' in self.__dict__ and name not in self.__dict__:
            # If we are setting a new attribute that corresponds to an existing alias, remove the old alias
            old_alias = None
            for alias, col_name in self._aliases.items():
                if col_name == value:
                    old_alias = alias
                    break
            # Проверка, что найден старый псевдоним и он отличается от нового имени
            if old_alias and old_alias != name:
                del self._aliases[old_alias]
                delattr(self, old_alias)
            # Register the new alias
            self._aliases[name] = value
        super().__setattr__(name, value)

    def __delattr__(self, name):
        if name in self._aliases:
            del self._aliases[name]
        super().__delattr__(name)

    def get_aliases(self):
        return self._aliases.copy()

    def set_missing_aliases(self):
        for col_name in self._df.columns:
            # Check if there is an alias for this column
            if col_name not in self._aliases.values():
                alias_name = self._create_alias(col_name)
                setattr(self, alias_name, col_name)
                self._aliases[alias_name] = col_name
    
def test_cols():
    sp = SparkApp(my_logger_create_level='CRITICAL')
    spark = sp.build_spark_app()
    # Пример DataFrame
    data = [("Value1", "Value2"), ("Value3", "Value4")]
    columns = ["One columns", "Another one"]
    df = spark.createDataFrame(data, columns)

    # Создаем объект Cols
    cdf = Cols(df, method="first_word_and_next_letters")

    # Доступ к псевдонимам
    print(cdf.one_c)  # 'One columns'
    print(cdf.another_o)  # 'Another one'

    # Изменение имени переменной псевдонима
    cdf.one_clmn = cdf.one_c

    # Проверка доступности обоих свойств
    try:
        print(cdf.one_c)
    except AttributeError as e:
        print(e)  # 'Cols object has no attribute 'one_c''
    
    print(cdf.get_aliases)
    del cdf.one_clmn
    print(cdf.get_aliases)
    # Установка отсутствующих алиасов
    cdf.set_missing_aliases()
    print(cdf.get_aliases)

class SparkApp:
    SPARK_MASTER_IP_VAR_NAME = 'SPARK_MASTER_IP'

    def __init__(self, spark_master_ip = None,
                 app_name="pyspark-taxi-forecasting",
                 my_logger = None,
                 my_logger_create_level = 'DEBUG'):
        
        self.spark = None
        self.app_name = app_name

        if my_logger is None:
            # ['DEBUG','INFO','WARNING','ERROR','CRITICAL']
            # [10     ,20    ,30       ,40     ,50]
            logging.basicConfig(level='INFO')
            self.cnlog = MyLogger(name='spark_app',
                                  create_level=my_logger_create_level,
                                  enable_logging=True)
        
        if spark_master_ip is None:
            self.spark_master_ip = self.get_spark_master_ip()
        self.spark = self.build_spark_app(self.spark_master_ip)

    def get_spark_master_ip(self):
        spark_master_ip = os.getenv(self.SPARK_MASTER_IP_VAR_NAME)
        if spark_master_ip:
            self.cnlog.mylev(20, f"spark_master_ip: {spark_master_ip}")
            return spark_master_ip
        else:
            self.cnlog.mylev(30, "spark_master_ip NOT EXIST!")
            return None

    def build_spark_app(self, spark_master_ip=None):
        if spark_master_ip is None:
            spark_master_ip = self.spark_master_ip
        if spark_master_ip:
            self.cnlog.mylev(10, 'starting import SparkSession')
            try:
                from pyspark.sql import SparkSession
                import pyspark
                pyspark_version = pyspark.__version__
                self.cnlog.mylev(20, f'pyspark version: {pyspark_version}')
            except ImportError as e:
                self.cnlog.mylev(30, f"Failed to import SparkSession or find pyspark version: {e}")
                return None
            self.cnlog.mylev(20, f"starting building spark app object: {self.app_name}")
            try:
                spark = SparkSession.builder.appName(self.app_name) \
                    .master(f"spark://{spark_master_ip}:7077") \
                    .config("spark.executor.cores", "1") \
                    .config("spark.task.cpus", 1) \
                    .getOrCreate()
                self.cnlog.mylev(20, f"Spark app object built as: {spark}")
                self.cnlog.mylev(20, "Spark object can be accessed as the SparkApp_object.spark property")
                return spark
            except:
                self.cnlog.mylev(20, f"environment variable: {self.SPARK_MASTER_IP_VAR_NAME} not received")
                return None
        else:
            self.cnlog.mylev(20, f"environment variable: {self.SPARK_MASTER_IP_VAR_NAME} not received")
            return None

    def stop_spark_app(self):
        if self.spark:
            try:
                self.cnlog.mylev(20, "attempt to stop SparkSession app object")
                self.spark.stop()
                self.cnlog.mylev(20, ".stop() instruction has been executed")
                #self.spark = None
                self.cnlog.mylev(20, "attempt to create new SparkSession app object after stopping")
                try:
                    """
                    self.spark.sql("SELECT 1")
                    self.cnlog.mylev(40, "Attention: The Spark Session was not stopped correctly.")
                    return 'running'
                
                    """

                    from pyspark.sql import SparkSession
                    new_spark_name = self.app_name + "_test"
                    self.cnlog.mylev(10,f"Attempt to create new Session: {new_spark_name}")
                    new_spark = SparkSession.builder.appName(new_spark_name).getOrCreate()
                    new_spark_name_get =  new_spark.sparkContext.appName
                    self.cnlog.mylev(10,f"Get new Session name: {new_spark_name_get}")
                    if new_spark_name == new_spark_name_get:
                        self.cnlog.mylev(30,"Session stopped correctly")
                        self.cnlog.mylev(10,f"new_spark test Session created at name: {new_spark_name_get}")
                        new_spark.stop()
                        self.cnlog.mylev(10,"new_spark test Session stoped")
                        new_spark = None
                        del new_spark
                        return 'stopped'
                    else:
                        self.cnlog.mylev(40,"Session WAS NOT stopped correctly")
                        return 'running'
                except Exception as e:
                    self.cnlog.mylev(20, "Session WAS NOT stopped correctly")
                    return 'error'


            except Exception as e:
                self.cnlog.mylev(40, f"An error occurred while trying to stop SparkSession: {e}")
                return 'error:' + str(e)
        else:
            self.cnlog.mylev(20, "attempt to stop NON-EXISTENT SparkSession app object")
            return 'empty'

    def test_app(self):
        self.cnlog.mylev(10, f'Enter in the main() function: name = {__name__}')
        self.cnlog.mylev(10, '****************************************************')
        self.cnlog.mylev(10, 'Attempt to run get_spark_master_ip() function')
        spark_master_ip = self.get_spark_master_ip()
        self.cnlog.mylev(10, f"Result is: {spark_master_ip}")
        self.cnlog.mylev(10, '****************************************************')
        self.cnlog.mylev(10, 'Checking existing logger objects')
        for key in logging.Logger.manager.loggerDict:
            self.cnlog.mylev(10, key)
        self.cnlog.mylev(10, '****************************************************')
        self.cnlog.mylev(10, 'Attempt to run build_spark_app() function')
        spark = self.build_spark_app(spark_master_ip)
        self.cnlog.mylev(10, f"Result is: {spark}")
        self.cnlog.mylev(10, '****************************************************')
        self.cnlog.mylev(10, 'Attempt to run stop_spark_app() function')
        stop_msg = self.stop_spark_app()
        self.cnlog.mylev(10, f"Result is: {stop_msg}")


if __name__ == '__main__':
    app = SparkApp()
    app.test_app()
