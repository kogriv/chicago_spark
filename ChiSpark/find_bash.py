import sys
import os
import subprocess

bash_path = "/"
find_command = f'find {bash_path} -path "/proc" -prune -o -name "*activate" -type f'
results = []

try:
    output = subprocess.check_output(find_command, shell=True, text=True)
    results.extend(output.strip().split('\n'))
except subprocess.CalledProcessError as e:
    # Обрабатываем ошибку, игнорируем её и продолжаем выполнение
    print("Error occurred:", e)
    # Продолжаем выполнение программы без прерывания
    pass

print(results)

envi_path_list_win = []
if sys.platform == 'win32':
    home_path = os.environ['USERPROFILE']
    #home_path = '/' + home_path.replace('\\', '/').replace(':', '', 1)
    #standard_path_linux.append(home_path)
    envi_path_list_win.append(home_path+"\\.virtualenvs")
    envi_path_list_win.append(home_path+"\\anaconda3\\envs")
    envi_path_list_win.append(home_path+"\\documents\\pro")

envi_path_list_linux = []
if sys.platform.startswith('linux'):
    home_path = os.environ['HOME']
    #os.path.join(root, file)