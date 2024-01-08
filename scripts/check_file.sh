#!/bin/bash

# Выводим подробное сообщение с примерами ввода
echo "Введите имя файла или полный путь к файлу. Например, это может быть:"
echo "- sync.sh - любое имя файла"
echo "- /c/Users/user/Documents/Pro/chicago_spark/scripts/bash_start.sh - полный путь Windows"
echo "- /mnt/c/Users/user/Documents/Pro/chicago_spark/scripts/bash_start.sh - полный путь Container"
# Запрашиваем у пользователя ввод
read file_path


# Проверяем, является ли путь абсолютным
if [[ "$file_path" = /* ]]; then
    full_path="$file_path"
else
    # Получаем полный путь к файлу в текущей директории
    full_path="$(pwd)/$file_path"
fi

# Проверка наличия файла
if [ -f "$full_path" ]; then
    echo "Файл найден: $full_path"
else
    echo "Файл не найден: $full_path"
fi