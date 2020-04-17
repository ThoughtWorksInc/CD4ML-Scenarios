# Build all of the containers

echo "Building Jenkins Master"
docker build --rm -f Dockerfile-jenkins -t ericnaglertw/cd4ml-build-master:odsc-east-2020 .
echo "Building MLFlow"
docker build --rm -f Dockerfile-mlflow -t ericnaglertw/cd4ml-mlflow:odsc-east-2020 .
echo "Building Model Server"
docker build --rm -f Dockerfile-model -t ericnaglertw/cd4ml-model-server:odsc-east-2020 .

echo "Building Fluentd"
pushd .
cd fluentd
docker build --rm  -f Dockerfile -t ericnaglertw/cd4ml-fluentd:odsc-east-2020 .
popd
