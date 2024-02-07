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

# Пример использования функции
folder_path = "C:\\Users\\user\\documents\\pro\\"
actual_folder_name = get_actual_folder_name(folder_path)
if actual_folder_name:
    print(f"Фактическое имя папки: {actual_folder_name}")
else:
    print("Не удалось получить фактическое имя папки.")
