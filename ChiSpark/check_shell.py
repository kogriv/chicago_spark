import os
import subprocess
import platform

def check_powershell():
    # Проверяем, что операционная система - Windows
    if platform.system() == "Windows":
        print("Using Windows")
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
        if "powershell" in os.environ.get('SHELL', '').lower():
            print("Выявлено наличие переменной окружения powershell")
            return True

        # Метод 3: Проверка наличия командлетов, специфичных для PowerShell
        try:
            output = subprocess.check_output(
                ['powershell', '-NonInteractive', 
                 '-NoProfile', '-Command', 'Get-ChildItem'],
                 stderr=subprocess.STDOUT, text=True)
            print("Выявлено наличие командлета Get-ChildItem")
        except subprocess.CalledProcessError as e:
            output = e.output
            print("Error executing PowerShell command:", output)

        return True
    else:
        # Если операционная система не Windows, скрипт не может быть в PowerShell
        print("Using Linux.")
        return False

if __name__ == "__main__":
    if check_powershell():
        print("Script can be running in PowerShell environment.")
    else:
        print("Script can not be running in PowerShell environment.")
