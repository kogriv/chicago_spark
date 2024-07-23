# Сисадминское
## Адрес монтируемой рабочей директории. IP мастер-ноды. Запуск скрипта.
в строке скрипта адрес рабочей директории пишем без кавычек
`PATH_TO_PROJECT_DIR=/mnt/c/Users/user/Documents/Pro/chicago_spark/`

Для проверки существования / работы запускаемых контейнеров добавлены соответствующие инструкции в скрипт.

Также для автоматического указания IP мастер-ноды была создана переменная окружения в контейнере Jupyter (где добавлены необходимые инструкции для чтения/установки IP).

Отдельно созданы скрипты для остановки, старта, удаления контейнеров.

**Запуск bash скрипта some_script.sh в виндоус**  
Запуск скрипта из оболочки Git Bash в виндоус может не выполниться из-за ограничения доступа оболочки к системным папкам. Срабатывает запуск из `wsl` в `cmd`, и потом запуск скрипта коандой `bash some_script.sh`.

## Виртуальные окружения в области разработки
Разработка модулей велась в контейнере `jupyter_lab` в юпитер ноутбуке и в VSCode с установленным плагинами для удаленной разработки (`Dev Cotainers`, `Remote Development`) в контейнере `Docker`, плагин Докер также должен быть установлен.

Подключение ВСКода - к запущенному контейнеру: `jupyter_lab`

Для проверки существующих ВО использовался класс проверки `from ChiSpark.enviserv.depsgetter import DepsGetter`. Результат выполнения команд:
```python
deps_getter = DepsGetter()
print("Getting venvs paths...")
deps_getter.get_venvs_paths(verbose=True)
print("Getting conda env list...")
deps_getter.get_conda_envs(verbose=True)
print("---------------------------------------")
print("Checked activate scripts paths:")
deps_getter.da.print_dict(deps_getter.grouped_paths)
```
следующий:
```bash
Shell bash is available
Shell Bash and Path to find equal to '/', finding using Python os.walk()
Attempting to find files using Python
Getting venvs paths...
Getting conda env list...
Conda installed.
Function get_conda_envs finished successfully
---------------------------------------
Checked activate scripts paths:
{
    conda: 
    {
        base: /opt/conda
    }
    venv: 
    {
        base: /usr/lib/python3.10/venv/scripts/common/activate
    }
    virtualenvs: { }
}
```
Видим наличие двух "живых" менеджеров: `conda` и `venv` лишь с базовыми ВО.

По умолчанию терминалы в VScode и в браузерном JupyterLab, в контейнере открываются с активированным ВО conda - `base`. Деактивация - `conda deactivate base`.
Jupyter ноутбуки открываются в с использованием базового окружения менеджера pip (venv).  
Проверка текущего ВО в ноутбуке `path = deps_getter.check_current_venv_path(update_data=True,verbose=True)`. Результат:
```bash
...
-------------------------------------------------------------------
-------------------------------------------------------------------
Checking ||| packman = conda ||| venv = base ||| ---
Count of specified venv deps in current venv:  208  | Total count of specifed deps dict: 350
Checked vevn not equal current
Installed: 183  | Count: 208
Current venev not equal (or not included in) to some vevn
-------------------------------------------------------------------
-------------------------------------------------------------------
Checking ||| packman = venv ||| venv = base ||| ---
Count of specified venv deps in current venv:  208  | Total count of specifed deps dict: 208
Checked vevn equal (or included in)  current
Installed: 208  | Count: 208
Current vevn equal (or included in) some venv
-------------------------------------------------------------
Current venv defined as ||| base |||| packman as ||| venv ||| 
Path to activate script (venv folder) is:
/usr/lib/python3.10/venv/scripts/common/activate
path wil be returnred
-------------------------------------------------------------
```

При этом интерпритатором по умолчанию и в терминале ВСкод и в ядре ЮпитерЛаба является `python 3.11.4`.
```bash
__:~# python3 # (same as python)
Python 3.11.4 | packaged by conda-forge | (main, Jun 10 2023, 18:08:17) [GCC 12.2.0] on linux
```

Предполагается разработка в глобальном пространстве (применительно к виртуальным окружениям) контейнера (jupyter_lab). Т.е. необходимо деактивировать все возможные активные окружения (при их наличии).

Используемый менеджер пакетов - Pip. Глобальное пространство контейнера, обозреваемое в терминале ВСКода может не содержать бибиотеку ПиСпарк. Может потребовать установка библиотеки pyspark. В моем случае потребовалось: `pip install pyspark==3.4.1`

## Выравнивание версий питона на исполнителях и на драйвере.
Оговорка:  
Я не слишком хорошо говорю на сисадминском и совсем не ботаю на Скале и Яве, поэтому некоторые действия и выводы, описываемые ниже для спецов могут показаться забавными. Но, тем не менее, я стараюсь, и что то даже получается.

При создании контейнеров используются образы `apache/spark:latest` - для мастер-ноды и исполнителей кластера, а также `jupyter/pyspark-notebook` - для драйвера спарк- контейнера среды разработки jupyter_lab. Данные образы "тянутся" с открытого докер-хаба автоматически. В ЮпитерЛабе (контейнер-драйвер для спарка), как выяснил выше, используемым питоном является `python 3.11.4`.  На исполнителях (spark_worker1,2..) - `python 3.8.10`.  
Данное несоответствие версий вызывает ошибку при выполнении действий на RDD объектах pyspark. Как в репл оболочке (шелле) спарка, так и в ноутбуке.  
Был проведен эксперимент с понижением версии на драйвере, в ходе которого было выполнено:
- установка версии 3.8.10 в контейнере jupyter_lab,
- создание соответствующего ядра в юпитере,
- установка библиотек  
Результат неудачный.  

Потом, в другом варианте, было успешно проведено повышение версии на исполнителях до 3.11.4. Без установок библиотек и прочих дополнительных действий. Для этого создан докерфайл `Dockerfile.py3114` с использованием `FROM apache/spark:latest`, с установкой питон нужной версии и переменной окружения `ENV PYSPARK_PYTHON=/usr/local/bin/python3.11`. Использование данного докерфайла было добавлено в скрипт создания кластера `start_local_cluster_win_py3114.sh`.

После чего функционал спарк стал доступен помимо объектов датафрейм, также на объектах РДД.

## Установка библиотек на воркерах для UDF
Для функционирования спарк UDF необходимо также установить питон-библиотеки на воркерах. Список зависимостей `reqs_workers.txt` помещен в папку scripts, в докерфайл внесена соответствующая команда.

## Веб-интерфейс Спарк-кластера на порту 4040
Для доступа к штатному веб-интерфейсту спарк, в команду запуска контейнера юпитер_лаб добавлен проброс порта 4040:4040.


## Экспорт импорт докер-образов через файл
Неведомым пока мне образом сборка докер-образов на разных физических машинах приводит (не в 100% случаев) к по-разному работающим контейнерам, построенным на этих докер-образах. Поэтому наиболее простым решением данной проблемы является использование работающей сборки в готовом виде через хаб или через файл.
Готовые рабочие образы на данный момент (240606) не публикую. Для обмена между машинами через дисковую систему, образ можно сохранять и загружать используя один файл `saved_image_name_tag.tar`.

Сохраните (экспортируйте) Docker-образ в файл с помощью команды docker save. Пример команды:
```bash
docker save -o D:\dims\spark_python3114.tar spark:python3114
```

Загрузите (импортируйте) Docker-образ из файла с помощью команды docker save. Пример команды:
```bash
docker save -o D:\dims\spark_python3114.tar spark:python3114
```
docker load -i d:\dims\spark_python3114.tar

## Добавление воркеров на другой машине в исходную сеть.
Определяя адрес мастер-ноды командой
```bash
# Save IP address of our Spark Master node 
SPARK_MASTER_IP=$(docker inspect -f \
  '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' spark_master)
```
Получим IP-адрес `172.18.0.2`, который является внутренним IP-адресом Docker-контейнера внутри Docker-сети, и он не имеет прямого отношения к IP-адресу вашего роутера, например, `192.168.1.1` в локальной сети. Docker использует свои собственные виртуальные сети для связи контейнеров, и IP-адреса в этих сетях могут быть недоступны извне.

Чтобы подключить воркеры на другой машине в той же локальной сети, нужно использовать IP-адрес хост-машины (где запущен Spark Master) и настроить Docker-сеть так, чтобы контейнеры могли общаться между машинами в локальной сети.

**Шаги для подключения воркеров на другой машине:**

**1. Определить IP-адрес хост-машины в локальной сети:**  
На первой машине, где запущен Spark Master, нужно определить её локальный IP-адрес (например, 192.168.1.x):
```bash
ifconfig | grep 'inet ' | grep -v '127.0.0.1'
```
Допустим, это будет `172.28.187.226`

**2. Изменить настройки запуска Spark Master на первой машине:**  
Перезапусти Spark Master на первой машине с указанием его локального IP-адреса:
```bash
docker run -d -p 8080:8080 -p 7077:7077 --name spark_master \
--network spark_network -v $PATH_TO_PROJECT_DIR:/work:rw \
$CUSTOM_SPARK_IMAGE_NAME /opt/spark/bin/spark-class \
org.apache.spark.deploy.master.Master -h 172.28.187.226
```

**3. Настроить и запустить воркеры на второй машине:**  
На второй машине используй IP-адрес первой машины для подключения воркеров. Пример скрипта для запуска воркеров:  
```bash
#!/bin/bash

# IP-адрес Spark Master ноды на первой машине
SPARK_MASTER_URL="spark://172.28.187.226:7077"

# Путь к проекту на второй машине (обнови путь соответственно)
PATH_TO_PROJECT_DIR="/mnt/c/Users/g/Documents/Pro/chicago_spark/"
CUSTOM_SPARK_IMAGE_NAME="spark_cluster:python3114"

MEMORY_PER_WORKER='2g'
CORES_PER_WORKER=1

# Функция для проверки и запуска контейнера
run_container() {
  local name=$1
  local command=$2

  # Проверка существования контейнера
  if [ "$(docker ps -aq -f name=^${name}$)" ]; then
    # Проверка, запущен ли контейнер
    if [ "$(docker ps -q -f name=^${name}$)" ]; then
      echo "Контейнер ${name} уже запущен."
    else
      echo "Контейнер ${name} существует, запускаем..."
      docker start ${name}
    fi
  else
    docker run ${command}
  fi
}

# Запуск новых воркеров и подключение их к Spark Master ноде
for i in {5..8}; do
  run_container "spark_worker$i" \
    "-d --name spark_worker$i --network spark_network \
    -e SPARK_WORKER_MEMORY=$MEMORY_PER_WORKER \
    -e SPARK_WORKER_CORES=$CORES_PER_WORKER \
    -v $PATH_TO_PROJECT_DIR:/work:rw \
    $CUSTOM_SPARK_IMAGE_NAME /opt/spark/bin/spark-class \
    org.apache.spark.deploy.worker.Worker $SPARK_MASTER_URL"
done

echo "Новые воркеры успешно подключены к Spark Master ноде на $SPARK_MASTER_URL"
```

**4. Запустить скрипт на второй машине:**  
Сохраним этот скрипт в файл, например start_additional_workers.sh, сделаем его исполняемым и запустим:
```bash
chmod +x start_additional_workers.sh
./start_additional_workers.sh
```
Этот скрипт запустит новые воркеры на второй машине и подключит их к Spark Master на первой машине по адресу `172.28.187.226:7077`. Убедитесь, что сеть Docker (spark_network) существует на обеих машинах и что они могут общаться друг с другом по локальной сети.