import ctypes
from ctypes import wintypes

# Загрузка библиотеки kernel32.dll
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

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
    # Инициализация структуры WIN32_FIND_DATA
    find_data = WIN32_FIND_DATA()
    # Получение дескриптора папки
    hFind = kernel32.FindFirstFileW(path, ctypes.byref(find_data))
    # Проверка на успешное открытие папки
    if hFind != -1:
        # Закрытие дескриптора
        kernel32.FindClose(hFind)
        # Возвращение фактического имени папки
        return find_data.cFileName

def get_actual_path(folder_path):
    # Удаление слэша в конце пути, если есть
    if folder_path.endswith('\\'):
        folder_path = folder_path[:-1]

    print("folder_path:",folder_path)
    # Разбиваем путь на компоненты
    path_components = folder_path.split('\\')
    actual_path = ''
    for component in path_components:
        print("component:",component)
        if component:
            # Если компонент содержит только одну букву и двоеточие,
            # добавляем его к актуальному пути без вызова get_actual_folder_name
            if len(component) == 2 and component[1] == ':':
                actual_path += component
            else:
                actual_path = '\\'.join([actual_path, get_actual_folder_name(actual_path + '\\' + component)])
                if actual_path is None:
                    return None
        print(actual_path)
    return actual_path

# Пример использования функции
folder_path = "C:\\Users\\user\\documents\\pro\\rta\\"
folder_path_actual = get_actual_path(folder_path)
if folder_path_actual:
    print(f"Фактический путь: {folder_path_actual}")
else:
    print("Не удалось получить фактический путь.")
