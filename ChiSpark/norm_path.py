import subprocess
import os

def universalize_path(input_path):
    # Проверяем формат пути
    if '\\' in input_path:
        # Путь является путем Windows
        # Переходим в папку и получаем правильный путь с помощью команды cd
        try:
            subprocess.run(f'cd "{input_path}"',
                           shell=True, check=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
            corrected_path = subprocess.run('cd',
                                            shell=True,
                                            check=True,
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE).\
                                                stdout.decode().strip()
        except subprocess.CalledProcessError:
            return False, False  # Возвращаем False, если путь недействителен

        # Формируем путь для bash
        bash_path = corrected_path.replace('\\', '/').replace(':', '', 1)
        if bash_path.startswith('/'):
            bash_path = bash_path[1:]
        
        return corrected_path, bash_path

    elif '/' in input_path:
        # Путь является путем Linux
        # Формируем путь для Windows
        win_path = input_path.replace('/', '\\')
        if win_path.startswith('\\'):
            win_path = win_path[1:]
        if ':' not in win_path:
            win_path = os.getcwd()[:2] + '\\' + win_path  # Добавляем диск по умолчанию, если его нет

        return win_path, input_path

    else:
        # Невозможно определить формат пути
        return False, False

# Пример использования:
input_path = "C:\\Users\\user\\documents\\pro"
windows_path, bash_path = universalize_path(input_path)
print("Windows path:", windows_path)
print("Bash path:", bash_path)
