import os
import subprocess

results = []
home_directory = "C:\\Users\\user\\documents\\pro"

print("Attempt to find files using Python")
# Поиск с использованием Python
for root, dirs, files in os.walk(home_directory):
    for file in files:
        if file.endswith("activate"):
            results.append(os.path.join(root, file))

print("results using python:")
print(results)


results = []
print("Attempt to find files using cmd (Windows)")
# Нормализация пути для Windows
home_directory = os.path.normpath(home_directory)
print("home_directory = ",home_directory)
find_command = f'dir "{home_directory}" /s /b /a-d "*activate"'
output = subprocess.check_output(find_command, shell=True, text=True)
results.extend(output.strip().split('\n'))

print("results using cmd:")
print(results)

