#!/bin/bash

# Ruta fija al directorio del script
script_directory="/home/oscar/virtualclinic/docker"

# Paso 1: Navegar al directorio superior para ejecutar el 'git pull'
cd "$script_directory/.."

# Ejecutar 'git pull'
git pull

# Volver al directorio original
cd "$script_directory"

# Paso 2: Ejecutar 'docker-compose'
sudo docker-compose -f docker-compose-virtualclinic.yaml up --build -d
	
# Paso 3: Ejecutar migraciones en el contenedor Docker
container_id=$(sudo docker ps -aqf name="virtualclinic_app")
sudo docker exec -it $container_id python manage.py migrate