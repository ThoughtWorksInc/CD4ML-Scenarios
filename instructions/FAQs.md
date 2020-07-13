## Frequently Asked Questions

#### I started ElasticSearch and it doesn't seem to be accepting any logs

Elasticsearch will put it's self into read-only mode when running low on space. Ensure your docker desktop machine has enough space.

#### On Windows, I'm receiving a storage connectivity error when running `docker-compose up`

Ensure that your C: drive is able to be mounted from your machine into docker. Open the Docker Dashboard using the icon in your taskbar, click the gear on the top right, resources on the left, then file sharing. Ensure that your C: drive is shared and click apply & restart on the bottom right.