# Сисадинское
## Адрес монтируемой рабочей директории. IP мастер-ноды. Запуск скрипта.
в строке скрипта адрес рабочей директории пишем без кавычек
`PATH_TO_PROJECT_DIR=/mnt/c/Users/user/Documents/Pro/chicago_spark/`

Для проверки существования / работы запускаемых контейнеров добавлены соответствующие инструкции в скрипт.

Также для автоматического указания IP мастер-ноды была создана соответсвующая переменная окружения в контейнере Jupyter (где добавлены соответствующие инструкции для чтения/установки IP).

Отдельно созданы скрипты для остановки, старта, удаления контейнеров.

**Запуск bash скрипта some_script.sh в виндоус**
Запуск скрипта из оболочки Git Bash в виндоус может не выполниться из-за ограничения доступа оболочки к системным папкам. Срабатывает запуск wsl в cmd, и потом запуск скрипта коандой `bash some_script.sh`.

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
Видим наличие двух "живых" менеджеров: конда и венв лишь с базовыми ВО.

По умолчанию терминалы в ВСкод и в браузерном ЮпитерЛабе, в контейнере открывается с активированным ВО конда - base. Деактивация - `conda deactivate base`.
Юпитер ноутбуки открываются в с использованием базового окружения менеджера pip (venv).  
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
Я не слишком хорошо говорю на сисадминском и совсем не ботаю на Скале и Яве, поэтому некоторые выводы ниже для спецов могут показаться забавными. Но, тем не менее, я стараюсь, и что то даже получается.

При создании контейнеров используются образы `apache/spark:latest` - для мастер-ноды и исполнителей кластера, а также `jupyter/pyspark-notebook` - для драйвера спарк- контейнера среды разработки jupyter_lab. Данные образы "тянутся" с открытого докер-хаба автоматически. В ЮпитерЛабе (контейнер-драйвер для спарка), как выяснил выше, используемым питоном является `python 3.11.4`.  На исполнителях (spark_worker1,2..) - `python 3.8.10`.  
Данное нессответствие версий вызывает ошибку при выполнении действий на RDD объекта pyspark. Как в репл оболочке (шелле) спарка, так и в ноутбуке.  
Был проведен эксперимент с понижением версии на драйвере, в ходе которого было выполнено:
- установка версии 3.8.10 в контейнере jupyter_lab,
- создание соответствующего ядра в юпитере,
- установка библиотек
Результат неудачный.  
Потом, в другом варианте, было успешно проведено повышение версии на исполнителях до 3.11.4. Без установок библиотек и прочих дополнительных действий. Для этого создан докерфайл `Dockerfile.py3114` с использованием `FROM apache/spark:latest`, с установкой питон и переменной окружения `ENV PYSPARK_PYTHON=/usr/local/bin/python3.11`. Использование данного докерфайла было добавлено в скрипт создания кластера `start_local_cluster_win_py3114.sh`.

После чего функционал спарк стал доступен помимо объектов датафрейм, также на объектах РДД.