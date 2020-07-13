docker save ericnaglertw/cd4ml-build-master:2 | gzip > cd4ml-build-master.tar.gz
docker save docker.elastic.co/elasticsearch/elasticsearch:7.6.0 | gzip > elasticsearch.tar.gz
docker save docker.elastic.co/kibana/kibana:7.6.0 | gzip > kibana.tar.gz
docker save ericnaglertw/cd4ml-fluentd:1 | gzip > cd4ml-fluentd.tar.gz
docker save ericnaglertw/cd4ml-model-server:1 | gzip > cd4ml-model-server.tar.gz
docker save ericnaglertw/cd4ml-mlflow:1 | gzip > cd4ml-mlflow.tar.gz
docker save jupyter/minimal-notebook:latest | gzip > minimal-notebook.tar.gz