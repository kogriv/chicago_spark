import os
import subprocess

def normalize_path(path):
    windows_path = False
    linux_path = False

    # Шаг 1: Определение формата пути
    if "\\" in path:
        windows_path = True
    elif "/" in path:
        linux_path = True

    # Шаг 2: Обработка виндовых путей
    if windows_path:
        # Попытка получить правильный путь средствами Windows
        try:
            windows_normalized_path = os.path.abspath(path)
        except:
            windows_normalized_path = None

        # Если не удалось получить правильный путь, используем запасной метод
        if windows_normalized_path is None:
            # TODO: Добавить обработку для случая, когда путь нельзя нормализовать средствами Windows
            pass
        
        # print(windows_normalized_path)
        # Преобразование в путь для Bash
        bash_path = windows_normalized_path.replace("\\", "/")
        bash_path = windows_normalized_path.replace(":", "/")
        #bash_path = bash_path[2:] if bash_path[1] == ":" else bash_path

        return windows_normalized_path, bash_path

    # Шаг 3: Обработка путей в стиле Linux
    elif linux_path:
        # Преобразование в путь для Windows
        windows_path = subprocess.check_output(['wsl', 'wslpath', '-w', path]).decode().strip()

        # Преобразование в путь для Bash
        bash_path = path

        return windows_path, bash_path

    return None, None  # В случае неверного формата пути возвращаем None

# Пример использования
input_path = "C:\\Users\\user\\documents\\pro"
print("input path:",input_path)
windows_path, bash_path = normalize_path(input_path)
print("Windows path:", windows_path)
print("Bash path:", bash_path)

input_path = "/home/user/documents/pro"
print("input path:",input_path)
linux_path, windows_path = normalize_path(input_path)
print("Linux path:", linux_path)
print("Windows path:", windows_path)
