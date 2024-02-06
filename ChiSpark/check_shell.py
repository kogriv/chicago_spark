import os
import subprocess
import platform

def check_powershell():
    # Метод 1: Проверка наличия переменной среды $PSVersionTable
    try:
        output = subprocess.check_output(
            ['powershell', '-NonInteractive',
             '-NoProfile', '-Command', '$PSVersionTable'],
             stderr=subprocess.STDOUT, text=True)
        if output:
            print("Выявлено наличие переменной среды $PSVersionTable")
            return True
    except subprocess.CalledProcessError:
        pass

    # Метод 2: Проверка, что интерпретатор Python запущен через PowerShell
    if platform.system() == "Windows" \
        and "powershell" in os.environ.get('SHELL', '').lower():
        print("Выявлено наличие переменной окружения powershell")
        return True

    # Метод 3: Проверка наличия командлетов, специфичных для PowerShell
    try:
        output = subprocess.check_output(
            ['powershell', '-NonInteractive', 
             '-NoProfile', '-Command', 'Get-ChildItem'],
             stderr=subprocess.STDOUT, text=True)
        print("Выявлено наличие командлета Get-ChildItem")
        #print("PowerShell command executed successfully.")
    except subprocess.CalledProcessError as e:
        output = e.output
        print("Error executing PowerShell command:", output)

    # Метод 4: Проверка, что скрипт запущен на Windows
    if platform.system() == "Windows":
        return True

    return False

if __name__ == "__main__":
    if check_powershell():
        print("Script can be in PowerShell environment.")
    else:
        print("Script can not be running in PowerShell environment.")
