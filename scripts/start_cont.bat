@echo off

docker start spark_master
docker start spark_worker1
docker start spark_worker2
docker start spark_worker3
docker start spark_worker4
docker start jupyter_lab