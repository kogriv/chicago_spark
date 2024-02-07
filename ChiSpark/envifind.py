import os
import subprocess
import platform

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

    # Определение директории поиска
    if path_find is None:
        home_directory = os.path.expanduser("~")
    else:
        home_directory = path_find
    
    if pyfind:
        print("Attempt to find files using Python")
        # Поиск с использованием Python
        for root, dirs, files in os.walk(home_directory):
            for file in files:
                if file.endswith("activate"):
                    results.append(os.path.join(root, file))
    else:
        # Поиск с использованием команды find (для bash)
        if shell == 'bash':
            print("Attempt to find files using bash")
            home_directory = os.path.normpath(home_directory)
            home_directory = home_directory.replace("\\", "/")
            print("home directory:",home_directory)
            try:
                find_command = \
                    f'find {home_directory} -name "*activate" -type f'
                output = subprocess.check_output(
                    find_command, shell=True, text=True)
                results.extend(output.strip().split('\n'))
            except subprocess.CalledProcessError:
                pass  # Обработка ошибок при выполнении команды
        elif shell == 'powershell':
            print("Attempt to find files using powershell (Windows)")
            try:
                # Выполнение команды PowerShell для рекурсивного поиска файлов
                find_command = f'Get-ChildItem -Path "{home_directory}" ' + \
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
    
    return results

# Пример использования:
path_to_find = "C:\\Users\\user\\documents\\pro"
ptf_bash = "/c/Users/user/Documents/Pro"


print("----------------------------------------------------")
print("finding using bash")
result_list = search_files(path_find=ptf_bash, shell='bash')
print(result_list)

print("----------------------------------------------------")
print("finding using powershell")
result_list = search_files(path_find=path_to_find, shell='powershell')
print(result_list)

print("----------------------------------------------------")
print("finding using python")
result_list = search_files(path_find=path_to_find)
print(result_list)

