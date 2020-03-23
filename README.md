## CD4ML Workshop with Jenkins

## Build Containers locally (not required if wanting to pull from dockerhub)
```{bash}
./build-containers.sh
```

## Docker Compose Instructions

### Start Environment
```{bash}
 docker-compose -f "docker-compose.yaml" up -d --build --remove-orphans
```

### Docker Compose (Down)
```{bash}
docker-compose -f "docker-compose.yaml" down
```

### Get Admin Password for Jenkins. Save it in a file that will not be checked in to git
```{bash}
docker exec -it jenkins cat /var/jenkins_home/secrets/initialAdminPassword > ~/jenkins_admin_password
```

### Get URL for Dev Environment
```{bash}
docker logs dev
```

Look for the line that looks like the following: `http://127.0.0.1:8888/?token=<token here>
Copy the <token here> part and paste into [Jupyter Lab](https://localhost:13000)

### Workshop Apps 

[Jenkins](http://localhost:10000)

[Jenkins Blue Ocean](http://localhost:10000/blue)

[ML Model](http://localhost:11000)

[MLFlow](http://localhost:12000)

[Jupyter Lab](http://localhost:13000)

[Kibana](http://localhost:5601)


If you want to blow everything Jenkins away and start over, check your volumes and delete them.
```{bash}
docker volume ls
docker volume rm <volume_name>
```


