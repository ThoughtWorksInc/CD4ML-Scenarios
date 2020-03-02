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

### Get Admin Password for Jenkins
```{bash}
docker exec -it jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

### Get URL for Dev Environment
```{bash}
docker logs dev
```

Look for the line that looks like the following: `http://127.0.0.1:8888/?token=<token here>
Copy the <token here> part and paste into [Jupyter Lab](https://localhost:13000)

### Workshop Apps 

[Jenkins](https://localhost:10000)

[ML Model](https://localhost:11000)

[MLFlow](https://localhost:12000)

[Jupyter Lab](https://localhost:13000)

[Kibana](https://localhost:5601)
