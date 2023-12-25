
import pkg_resources
import os

# Путь к файлу для записи зависимостей
output_file = '/work/requirements_vscode.txt'

# Получаем список установленных пакетов и их версий
installed_packages = [(d.project_name, d.version) for d in pkg_resources.working_set]

# Сортируем список пакетов по имени
installed_packages.sort(key=lambda x: x[0].lower())

# Записываем пакеты и их версии в файл
with open(output_file, 'w') as f:
    for package, version in installed_packages:
        f.write(f"{package}=={version}\n")

print(f"Зависимости записаны в файл: {output_file}")