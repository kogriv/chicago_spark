import os
import subprocess

def check_bash():
    try:
        # Метод 1: Проверка наличия переменной окружения SHELL с учетом возможных диалоговых сообщений
        output = subprocess.check_output(['bash', '-c', 'echo $SHELL'], stderr=subprocess.DEVNULL, text=True)
        if 'bash' in output.lower():
            print("Bash оболочка доступна.")
            return True
    except subprocess.CalledProcessError:
        pass

    try:
        # Метод 2: Проверка выполнения простой команды с учетом возможных диалоговых сообщений
        output = subprocess.check_output(['bash', '-c', 'echo "Hello from Bash"'], stderr=subprocess.DEVNULL, text=True)
        if 'hello from bash' in output.lower():
            print("Простая команда в Bash выполняется.")
            return True
    except subprocess.CalledProcessError:
        pass

    # Если ни один метод не сработал
    print("Bash оболочка недоступна или проверка не удалась.")
    return False

if __name__ == "__main__":
    if check_bash():
        print("Скрипт может выполняться в среде Bash.")
    else:
        print("Скрипт не может быть выполнен в среде Bash.")
