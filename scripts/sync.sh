#!/bin/bash

# Бесконечный цикл
while true; do
  # Синхронизация содержимого папки /home/jovyan/work с /work/notebooks
  rsync -av --delete /home/jovyan/work/ /work/notebooks/

  # Пауза в 1 минуту (60 секунд) перед следующей синхронизацией
  sleep 60
done