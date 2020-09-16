export FLUENTD_HOST="fluentd"
export FLUENTD_PORT="24224"
export FLASK_APP="cd4ml/app.py"
export FLASK_ENV="production"
export MLFLOW_TRACKING_URL='http://mlflow:5000'
export MLFLOW_S3_ENDPOINT_URL = 'http://minio:9000'

pip3 install -r requirements.txt
# EXPOSE 5005
flask run --host=0.0.0.0 --port 5005

