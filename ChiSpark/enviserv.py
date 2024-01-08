import mylog

class MyReq:
    def __init__(self) -> None:
        self.path_req_jup = '/work/requirements_jup.txt'
        self.path_req_vsc = '/work/requirements_vscode.txt'
        # self.requirements_jup = 

    def read_requirements(self, file_path):
        with open(file_path, 'r') as file:
            return set(line.strip() for line in file)

# Чтение списков зависимостей из файлов
requirements_jup = read_requirements('/work/requirements_jup.txt')
requirements_vscode = read_requirements('/work/requirements_vscode.txt')

# Находим уникальные зависимости для каждого файла
unique_jup = requirements_jup - requirements_vscode
unique_vscode = requirements_vscode - requirements_jup

# Запись уникальных зависимостей в новые файлы
with open('/work/requirements_jup_no_vscode.txt', 'w') as file:
    for dep in sorted(unique_jup):
        file.write(f"{dep}\n")

with open('/work/requirements_vscode_no_jup.txt', 'w') as file:
    for dep in sorted(unique_vscode):
        file.write(f"{dep}\n")