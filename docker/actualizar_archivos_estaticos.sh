#!/bin/bash

# Obtener directorio
script_directory="/home/oscar/virtualclinic/docker"

# Cd al obtener directorio
cd "$script_directory"

# Obtener el ID del contenedor 1
container_id1=$(sudo docker ps -aqf name="virtualclinic_app")

# Obtener el ID del contenedor 2
container_id2=$(sudo docker ps -aqf name="nginx_virtualclinic")

# Detener y eliminar el contenedor 1
sudo docker stop $container_id1
sudo docker rm $container_id1

# Detener y eliminar el contenedor 2
sudo docker stop $container_id2
sudo docker rm $container_id2

# Eliminar el volumen
sudo docker volume rm docker_static_virtualclinic_volume

# Volver a levantar los contenedores con docker-compose
sudo docker-compose -f docker-compose-virtualclinic.yaml up --build -d
