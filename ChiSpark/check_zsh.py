import subprocess

def check_zsh():
    try:
        # Попытка выполнить простую команду Zsh
        subprocess.check_call(['zsh', '-c', 'echo "Hello from Zsh"'])
        print("Zsh доступна.")
        return True
    except FileNotFoundError as e:
        print("Ошибка при выполнении команды Zsh (FileNotFoundError):", e)
        return False
    except subprocess.CalledProcessError as e:
        print("Ошибка при выполнении команды Zsh (CalledProcessError):", e)
        return False
    except Exception as e:
        print("Общая ошибка при выполнении команды Zsh:", e)
        return False

if __name__ == "__main__":
    if check_zsh():
        print("Скрипт может выполняться в среде Zsh.")
    else:
        print("Скрипт не может быть выполнен в среде Zsh.")
