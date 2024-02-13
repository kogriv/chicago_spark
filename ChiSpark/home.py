import os
print(os.environ['HOME'])
#print(os.environ['USERPROFILE'])

"""
count_directories = 0
count_files = 0

for root, dirs, files in os.walk("/work"):
    count_directories += len(dirs)
    count_files += len(files)

print("Количество обработанных каталогов:", count_directories)
print("Количество обработанных файлов:", count_files)
print("Привет!!")
"""