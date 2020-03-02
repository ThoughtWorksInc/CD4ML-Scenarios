FROM python:3.7-slim-buster

USER root

RUN mkdir -p /app/continuous-intelligence/{src,data}

COPY requirements.txt /app/continuous-intelligence
COPY src /app/continuous-intelligence/src
COPY data/decision_tree /app/continuous-intelligence/data/decision_tree

EXPOSE 5005
WORKDIR /app/continuous-intelligence/
RUN pip3 install -r requirements.txt

CMD python3 src/app.py