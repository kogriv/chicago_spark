#!/bin/bash

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
  echo "Docker is not running. Please start Docker and try again."
  exit 1
else
  echo "*********************************************************"
  echo "Docker is running. Lets start creating SPARK cluster."
  echo "*********************************************************"
fi

# Full path to project directory
# We mount it to docker containers
# So they will se the content in that directory
PATH_TO_PROJECT_DIR=/mnt/c/Users/user/Documents/Pro/chicago_spark/
PATH_TO_BASH_START=/mnt/c/Users/user/Documents/Pro/chicago_spark/scripts/bash_start.sh
# PATH_TO_PROJECT_DIR="C:/Users/user/Documents/Pro/chicago_spark"

MEMORY_PER_WORKER='2g'
CORES_PER_WORKER=1

# Check and create local docker network named "spark_network" if it doesn't exist
if ! docker network ls | grep -q spark_network; then
  echo "Creating docker network 'spark_network'..."
  docker network create spark_network
else
  echo "Docker network 'spark_network' already exists."
fi

# Function to check and run container
run_container() {
  local name=$1
  local command=$2

  # Check if the container exists
  if [ "$(docker ps -aq -f name=^${name}$)" ]; then
    # Check if the container is already running
    if [ "$(docker ps -q -f name=^${name}$)" ]; then
      echo "Container ${name} is already running."
    else
      echo "Container ${name} already exists, starting..."
      docker start ${name}
    fi
  else
    docker run ${command}
  fi
}

# Runs Spark Master Node
run_container "spark_master" \
  "-d -p 8080:8080 -p 7077:7077 --name spark_master \
  --network spark_network -v $PATH_TO_PROJECT_DIR:/work:rw \
  apache/spark:latest /opt/spark/bin/spark-class \
  org.apache.spark.deploy.master.Master -h spark_master"

# Save IP address of our Spark Master node 
SPARK_MASTER_IP=$(docker inspect -f \
  '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' spark_master)

# Run Spark workers and bind them to our Spark Master node
for i in {1..4}; do
  run_container "spark_worker$i" \
    "-d --name spark_worker$i --network spark_network \
    -e SPARK_WORKER_MEMORY=$MEMORY_PER_WORKER \
    -e SPARK_WORKER_CORES=$CORES_PER_WORKER \
    -v $PATH_TO_PROJECT_DIR:/work:rw \
    apache/spark:latest /opt/spark/bin/spark-class \
    org.apache.spark.deploy.worker.Worker spark://$SPARK_MASTER_IP:7077"
done

echo "Container jupyter_lab creating/starting..."
# local custom_bashrc=$PATH_TO_BASH_START
# Проверяем, существует ли кастомный скрипт Bash
mount_custom_bashrc=""
if [ -f "$PATH_TO_BASH_START" ]; then
  # Если файл существует, добавляем параметр монтирования к команде
  echo "Custom .bashrc exists"
  mount_custom_bashrc="-v $PATH_TO_BASH_START:/home/jovyan/.bashrc"
else
  echo "Custom .bashrc NOT exists"
  #mount_custom_bashrc=""
fi

# Run Jupyter Lab
run_jupyter_command="-d --name jupyter_lab -p 10000:8888 --network spark_network --user root \
-v $PATH_TO_PROJECT_DIR:/work:rw \
$mount_custom_bashrc \
-e SPARK_MASTER_IP=$SPARK_MASTER_IP \
-e SPARK_MASTER=spark://$SPARK_MASTER_IP:7077 \
-e PYTHONPATH=/work \
-e PYTHONTRACEMALLOC=1 \
jupyter/pyspark-notebook start-notebook.sh \
--NotebookApp.token='' --NotebookApp.notebook_dir='/work'"

#docker cp .condarc jupyter_lab:/opt/conda/

echo "Jupyter container run command:"
echo "$run_jupyter_command"
# echo "After printing Jupyter container run command:"
run_container "jupyter_lab" "$run_jupyter_command"

echo "*********************************************************"
echo "Creating or starting SPARK cluster is finished"
echo 'YOUR SPARK MASTER NODE IP IS:' $SPARK_MASTER_IP
echo 'YOU CAN ACCESS JUPYTER LAB VIA: http://localhost:10000'
echo "*********************************************************"