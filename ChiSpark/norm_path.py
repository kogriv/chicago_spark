import subprocess
import os
import sys

import ctypes
from ctypes import wintypes


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

def get_actual_folder_name(path):
    """
    Данная функция используется только на виндоус.
    Принимает путь.
    Возвращает фактическое имя конечной папки пути с учетом регистра
    ("cFileName", wintypes.WCHAR * 260)
    """
    if sys.platform == 'win32':
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
    else:
        return path

def get_actual_path(folder_path):
    """
    Данная функция используется только на виндоус.
    """
    if sys.platform == 'win32':
        # Удаление слэша в конце пути, если есть
        if folder_path.endswith('\\'):
            folder_path = folder_path[:-1]

        #print("folder_path:",folder_path)
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
            #print(actual_path)
        return actual_path
    else:
        return folder_path

def universalize_path(input_path, standard_path=None):
    if standard_path is None:
        standard_path = [
            "C:\\Users\\user\\documents\\pro",
            "C:\\Users\\user",
            "C:\\Projects"
        ]

    if '\\' in input_path:
        # Путь является путем Windows
        # Проверяем валидность пути Windows
        if not os.path.exists(input_path):
            return False, False  # Возвращаем False, если путь недействителен

        # Переходим в папку и получаем правильный путь
        try:
            corrected_path = get_actual_path(input_path)
        except subprocess.CalledProcessError:
            return False, False  # Возвращаем False, если путь недействителен

        # Формируем путь для bash
        bash_path = '/' + corrected_path.replace('\\', '/').replace(':', '', 1)
        
        return corrected_path, bash_path

    else:
    #elif '/' in input_path:
        # Путь является путем Linux или это просто имя папки
        
        # Проверяем заканчивается ли путь слэшем
        if input_path[-1] == '/':
            input_path = input_path[:-1]

        # Проверяем, начинается ли путь с "<буква>/" или "/<буква>/"
        if input_path[0] == '/' and input_path[2] == '/':
            print("Путь начинается с /<буква>/")
            # Вставляем двоеточие между "буква" и "/"
            win_path = input_path[1].upper() + ':' + input_path[2:]
            win_path = win_path.replace('/', '\\')
        
        elif input_path[0] != '/' and input_path[1] == '/':
            print("Путь начинается с <буква>/")
            # Вставляем двоеточие между "буква" и "/"
            win_path = input_path[0].upper() + ':' + input_path[1:]
            input_path = '/' + input_path
            win_path = win_path.replace('/', '\\')

        else:
            # Путь не начинается с "<буква диска>/"
            print("Путь не начинается с <буква диска>")
            win_path = input_path.replace('/', '\\')

        # Проверяем наличие буквы диска
        if ':' not in win_path:
            print("получили виндоус путь:",win_path)
            print("двоеточния нет в виндоус-пути")
            # Находим путь в Windows, содержащий win_path
            path_found = False
            for parent_path in standard_path:
                if path_found:
                    break
                for root, dirs, files in os.walk(parent_path):
                    # print("root:",root)
                    #print("dirs:",dirs)
                    if win_path in root:
                        win_path = get_actual_path(root)
                        print("path finded")
                        path_found = True
                        break
        
        if input_path[0] != '/':
            input_path = '/' + input_path
        
        # Проверяем валидность пути Linux
        #if not os.path.exists(win_path):
        #    return False, False  # Возвращаем False, если путь недействителен

        return win_path, input_path


    #else:
        # Невозможно определить формат пути
    #    return False, False

# Пример использования:

print("-----ChiSpark/-------")
input_path = "ChiSpark/"
windows_path, bash_path = universalize_path(input_path)
print("Windows path:", windows_path)
print("Bash path:", bash_path)


print("-----ChiSpark-------")
input_path = "ChiSpark"
windows_path, bash_path = universalize_path(input_path)
print("Windows path:", windows_path)
print("Bash path:", bash_path)

print("-----/documents/pro-------")
input_path = "/c/Users/user/documents/pro"
windows_path, bash_path = universalize_path(input_path)
print("Windows path:", windows_path)
print("Bash path:", bash_path)

print("-----/c/Users/user/documents/pro-------")
input_path = "/c/Users/user/documents/pro"
windows_path, bash_path = universalize_path(input_path)
print("Windows path:", windows_path)
print("Bash path:", bash_path)    

print("-----C:\\Users\\user\\documents\\pro---------")
input_path = "C:\\Users\\user\\documents\\pro"
windows_path, bash_path = universalize_path(input_path)
print("Windows path:", windows_path)
print("Bash path:", bash_path)

print("-----C:\\Users\\user\\documents\\pro\\-------")
input_path = "C:\\Users\\user\\documents\\pro\\"
windows_path, bash_path = universalize_path(input_path)
print("Windows path:", windows_path)
print("Bash path:", bash_path)
