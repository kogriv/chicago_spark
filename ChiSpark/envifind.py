import os
import subprocess
import platform

def detect_shell(verbose=False):
    shell = os.environ.get('SHELL')
    if verbose:
        print('SHELL=',shell)
    if shell:
        return shell
    elif os.name == 'posix':
        # POSIX системы (Linux, macOS)
        return 'bash'
    elif os.name == 'nt':
        # Windows
        return 'cmd'
    else:
        return 'unknown'

def search_files(path_find=None, pyfind=False):
    results = []
    
    # Определение директории поиска
    if path_find is None:
        home_directory = os.path.expanduser("~")
    else:
        home_directory = path_find
    
    # Определение оболочки
    if not pyfind:
        shell = detect_shell(True)
        print('shell = ',shell)


    if pyfind or shell == 'unknown':
        print("Attempt to find files using Python")
        # Поиск с использованием Python
        for root, dirs, files in os.walk(home_directory):
            for file in files:
                if file.endswith("activate"):
                    results.append(os.path.join(root, file))
    else:
        # Поиск с использованием команды find (для Linux)
        if 'bash' in shell:
            print("Attempt to find files using bash (Linux)")
            try:
                find_command = f'find {home_directory} -name "*activate" -type f'
                output = subprocess.check_output(find_command, shell=True, text=True)
                results.extend(output.strip().split('\n'))
            except subprocess.CalledProcessError:
                pass  # Обработка ошибок при выполнении команды
        elif 'cmd' in shell:
            try:
                print("Attempt to find files using cmd (Windows)")
                # Нормализация пути для Windows
                home_directory = os.path.normpath(home_directory)
                print("home_directory = ",home_directory)
                find_command = f'dir "{home_directory}" /s /b /a-d "*activate"'
                output = subprocess.check_output(find_command, shell=True, text=True)
                results.extend(output.strip().split('\n'))
            except subprocess.CalledProcessError:
                pass  # Обработка ошибок при выполнении команды
    
    return results

# Пример использования:
path_to_find = "C:\\Users\\user\\documents\\pro"

# Поиск средствами оболочки
result_list = search_files(path_find=path_to_find, pyfind=False)
print(result_list)

# Поиск средствами Питон
result_list = search_files(path_find=path_to_find, pyfind=True)
print(result_list)

