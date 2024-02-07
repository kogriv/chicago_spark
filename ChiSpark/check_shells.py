import subprocess

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

if __name__ == "__main__":
    shells_results = check_shells(verbose=True)
    print("Результаты проверки оболочек:")
    print(shells_results)

    shell='powershell'
    shells_results = check_shells(shell,verbose=True)
    print(f"Результаты проверки оболочки {shell}:",shells_results)
    print(shells_results)