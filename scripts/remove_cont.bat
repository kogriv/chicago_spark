@echo off
docker stop jupyter_lab
docker stop spark_master
docker stop spark_worker1
docker stop spark_worker2
docker stop spark_worker3
docker stop spark_worker4

docker network rm spark_network

docker rm jupyter_lab
docker rm spark_master
docker rm spark_worker1 
docker rm spark_worker2
docker rm spark_worker3
docker rm spark_worker4