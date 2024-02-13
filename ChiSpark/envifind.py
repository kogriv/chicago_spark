import os
import subprocess
import sys

import ctypes
from ctypes import wintypes

def get_actual_folder_name(path):
    """
    Принимает путь.
    Возвращает фактическое имя конечной папки пути с учетом регистра
    ("cFileName", wintypes.WCHAR * 260)
    """
    if sys.platform == 'win32':
        # Определение структуры WIN32_FIND_DATA
        class WIN32_FIND_DATA(ctypes.Structure):
            _fields_ = [
                ("dwFileAttributes", wintypes.DWORD),
                ("ftCreationTime", wintypes.FILETIME),
                ("ftLastAccessTime", wintypes.FILETIME),
                ("ftLastWriteTime", wintypes.FILETIME),
                ("nFileSizeHigh", wintypes.DWORD),
                ("nFileSizeLow", wintypes.DWORD),
                ("dwReserved0", wintypes.DWORD),
                ("dwReserved1", wintypes.DWORD),
                ("cFileName", wintypes.WCHAR * 260),
                ("cAlternateFileName", wintypes.WCHAR * 14)
            ]
        # Инициализация структуры WIN32_FIND_DATA
        find_data = WIN32_FIND_DATA()
        # Загрузка библиотеки kernel32.dll
        kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
        # Получение дескриптора папки
        hFind = kernel32.FindFirstFileW(path, ctypes.byref(find_data))
        # Проверка на успешное открытие папки
        if hFind != -1:
            # Закрытие дескриптора
            kernel32.FindClose(hFind)
            # Возвращение фактического имени папки
            return find_data.cFileName
        else: False

    else:
        # платформа не Виндоус вернем имя первой папки с конца
        # Удаляем слэши в начале и в конце строки
        path = path.replace('\\', '/').replace(':', '').strip('/')
        if os.path.exists(os.path.normpath(path)):
            # Разбиваем путь на компоненты
            path_components = path.split('/')
            if path_components:
                return path_components[-1]
        else:
            return False

def get_actual_path(folder_path):
    """
    """
    if sys.platform == 'win32':
        if '\\' in folder_path:
            # Удаление слэша в конце пути, если есть
            if folder_path.endswith('\\'):
                folder_path = folder_path[:-1]

            # Разбиваем путь на компоненты
            path_components = folder_path.split('\\')
            actual_path = ''
            for component in path_components:
                #print("component:",component)
                if component:
                    # Если компонент содержит только одну букву и двоеточие,
                    # добавляем его к актуальному пути без вызова get_actual_folder_name
                    if len(component) == 2 and component[1] == ':':
                        actual_path += component
                    else:
                        actual_path = '\\'.join([actual_path, get_actual_folder_name(actual_path + '\\' + component)])
                        if actual_path is None:
                            return None
            return actual_path
        else:
            return folder_path
    else:
        # платформа не Виндоус, вернем исправленный исходный путь
        folder_path = folder_path.replace(":",'').replace("\\","/")
        return folder_path

def universalize_path(input_path,
                      standard_path_win=None,
                      standard_path_linux=None):
    
    # Список стандартных путей для поиска по неполным путям
    if standard_path_win is None:
        standard_path_win = []
        if sys.platform == 'win32':
            standard_path_win.append(os.environ['USERPROFILE'])

    if standard_path_linux is None:
        standard_path_linux = []
        if sys.platform.startswith('linux'):
            standard_path_linux.append(os.environ['HOME'])
        if sys.platform == 'win32':
            home_path = os.environ['USERPROFILE']
            home_path = '/' + home_path.replace('\\', '/').replace(':', '', 1)
            standard_path_linux.append(home_path)
        

    if '\\' in input_path:
        # Путь является путем Windows
        # Проверяем валидность пути Windows
        if not os.path.exists(os.path.normpath(input_path)):
            return False, False  # если путь недействителен

        # Получаем правильный путь (с учетом регистров букв в имени)
        try:
            corrected_path = get_actual_path(input_path)
        except subprocess.CalledProcessError:
            return False, False  # Возвращаем False, если путь недействителен

        # Формируем путь для bash
        bash_path = '/' + corrected_path.replace('\\', '/').replace(':', '', 1)
        
        return corrected_path, bash_path

    else:
    #elif '/' in input_path:
        # Путь является путем Linux
        # или в пути нет слэшей - это просто имя папки
        # Проверяем заканчивается ли путь слэшем
        if len(input_path)>1 and input_path[-1] == '/':
            input_path = input_path[:-1]

        # Проверяем, начинается ли путь с "<буква>/" или "/<буква>/"
        if len(input_path) > 2 \
            and input_path[0] == '/' and input_path[2] == '/':
            #print("Путь начинается с /<буква>/")
            # Вставляем двоеточие между "буква" и "/"
            win_path = input_path[1].upper() + ':' + input_path[2:]
            win_path = win_path.replace('/', '\\')
        
        elif len(input_path) > 1 \
            and input_path[0] != '/' and input_path[1] == '/':
            #print("Путь начинается с <буква>/")
            # Вставляем двоеточие между "буква" и "/"
            win_path = input_path[0] + ':' + input_path[1:]
            input_path = '/' + input_path
            win_path = win_path.replace('/', '\\')

        else:
            # Путь не начинается с "<буква диска>/"
            #print("Путь не начинается с <буква диска>")
            win_path = input_path.replace('/', '\\')

        # Проверяем наличие буквы диска
        if ':' not in win_path:
            #print("двоеточния нет в виндоус-пути")
            # Находим путь в Windows, содержащий неполный win_path
            path_found = False
            for parent_path in standard_path_win:
                if path_found:
                    break
                for root, dirs, files in os.walk(parent_path):
                    # print("root:",root)
                    #print("dirs:",dirs)
                    if win_path in root:
                        win_path = get_actual_path(root)
                        #print("path finded")
                        path_found = True
                        break
        
        if input_path[0] != '/':
            bash_path = '/' + input_path
        else: bash_path = input_path

        return win_path, bash_path


def check_shells(shells=['powershell', 'bash', 'zsh', 'cmd'],
                 verbose=False):
    results = {}

    if isinstance(shells, str):  # Если передана только одна оболочка
        shells = [shells]

    for shell in shells:
        if verbose:
            print('Попытка проверки:', shell)
        try:
            if shell == 'powershell':
                # Проверка наличия командлетов, специфичных для PowerShell
                subprocess.check_call([
                    'powershell', '-NonInteractive',
                    '-NoProfile', '-Command', 'Get-ChildItem'],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL)
                results[shell] = True
            elif shell == 'cmd':
                # Проверка доступности команд в Command Prompt
                subprocess.check_call([
                    'cmd', '/c', 'echo "Hello from cmd"'],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL)
                results[shell] = True
            else:
                # Попытка выполнить пробную команду для оболочки
                subprocess.check_call([
                    shell, '-c', 'echo "Hello from {}"'.format(shell)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL)
                results[shell] = True
        except FileNotFoundError:
            results[shell] = False
        except subprocess.CalledProcessError:
            results[shell] = False
        except Exception:
            results[shell] = False

    if len(results) == 1:  # Если передана только одна оболочка
        return results[shells[0]]
    else:
        return results

def search_files(path_find=None, shell = 'python'):
    results = []
    pyfind = False

    # Определение директории поиска
    if path_find is None:
        home_directory = os.path.expanduser("~")
    else:
        home_directory = path_find

    win_path, bash_path = universalize_path(home_directory)
    #print("win path",win_path)
    #print("bash path",bash_path)
    if win_path and bash_path:
        if shell != 'python':
            if check_shells(shell):
                print(f"Shell {shell} is available")
            else:
                pyfind = True
                print(f"Shell {shell} is not available, "
                    f"find using python os.walk()")
        else:
            pyfind = True
            #print(f"Find using python os.walk()")

        
        if pyfind:
            print("Attempt to find files using Python")
            # Поиск с использованием Python
            path_to_find = win_path
            if sys.platform.startswith('linux'):
                path_to_find = bash_path
            for root, dirs, files in os.walk(path_to_find):
                for file in files:
                    if file.endswith("activate"):
                        results.append(os.path.join(root, file))
        else:
            # Поиск с использованием команды find (для bash)
            if shell == 'bash':
                print("Attempt to find files using bash")
                #home_directory = os.path.normpath(home_directory)
                #home_directory = home_directory.replace("\\", "/")
                print("home directory:",bash_path)
                try:
                    find_command = \
                    f'find {bash_path} -path "/proc" -prune -o -name "*activate" -type f -print'
                    """
                    f'find {bash_path} -name "*activate" -type f  2>/dev/null'
                    f'find {bash_path} -path "/proc" -prune -o -name "*activate" -type f -print'
                    f'find {bash_path} -name "*activate" -type f  2>/dev/null'
                    """
                    output = subprocess.check_output(
                        find_command, shell=True, text=True,
                        #stderr=subprocess.STDOUT,
                        #stderr=subprocess.DEVNULL,
                        stderr=subprocess.PIPE
                        )
                    results.extend(output.strip().split('\n'))
                except subprocess.CalledProcessError as e:
                    print("Error occurred:", e)
                    pass  # Обработка ошибок при выполнении команды
            elif shell == 'powershell':
                print("Attempt to find files using powershell (Windows)")
                try:
                    # Выполнение команды PowerShell для рекурсивного поиска файлов
                    find_command = f'Get-ChildItem -Path "{win_path}" ' + \
                                f'-Recurse -File -Filter "*activate" | ' + \
                                f'Select-Object -ExpandProperty FullName'
                    output = subprocess.check_output([
                        'powershell', '-NonInteractive',
                        '-NoProfile', '-Command', find_command],
                        text=True)
                    # Обработка вывода команды PowerShell
                    results.extend(output.strip().split('\n'))
                except subprocess.CalledProcessError:
                    pass  # Обработка ошибок при выполнении команды

            elif shell == 'cmd':
                print("Finding files using cmd (Windows) not realised")
    else:
        print("path not exists")
        return []
    
    return results



# Пример использования:
ptf_bash = "C:\\Users\\user\\documents"
#ptf_bash = "/"
print("----------------------------------------------------")
print("finding using bash /// path to find")
print(ptf_bash)
result_list = search_files(path_find=ptf_bash, shell='bash')
print(result_list)

print("----------------------------------------------------")
print("finding using python /// path to find")
print(ptf_bash)
result_list = search_files(path_find=ptf_bash)
print(result_list)

"""
print("----------------------------------------------------")
print("finding using bash /// without path to find")
#print(ptf_bash)
result_list = search_files(shell='bash')
print(result_list)

ptf_win = "C:\\Users\\user\\documents\\pro"
ptf_bash = "/"

print("----------------------------------------------------")
print("finding using bash /// path to find")
print(ptf_bash)
result_list = search_files(path_find=ptf_bash, shell='bash')
print(result_list)

print("----------------------------------------------------")
print("finding using powershell /// path to find")
print(ptf_win)
result_list = search_files(path_find=ptf_win, shell='powershell')
print(result_list)

print("----------------------------------------------------")
print("finding using python /// path to find")
print(ptf_win)
result_list = search_files(path_find=ptf_win)
print(result_list)

print("----------------------------------------------------")
print("finding using python /// path to find")
print(ptf_bash)
result_list = search_files(path_find=ptf_bash)
print(result_list)
"""