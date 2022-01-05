# Continuous Intelligence and CD4ML Workshop

This workshop contains the sample application and machine learning code used for the Continuous Delivery for Machine Learning (CD4ML) and Continuous Intelligence workshop. 

This workshop is based on an existing [CD4ML Workshop](https://github.com/ThoughtWorksInc/cd4ml-workshop).

This material has been developed and is continuously evolved by [ThoughtWorks](https://www.thoughtworks.com/open-source) and has been presented in conferences such as: ODSC Boston 2020, ODSC Europe 2020.

You can also watch a recording of this material presented at a [Global Webinar](https://www.thoughtworks.com/continuous-delivery-for-machine-learning).

## Pre-Requisites

In order to run this workshop, you will need:

* A valid Github account
* A working Docker setup with at least 20 GB of space free (if running on Windows, make sure to use Linux containers)

## Tools used in this workshop

As part of this workshop all of these service will be automatically setup for you as Docker containers. You do not need to download and install these services ahead of time.

* [Python 3.9](https://www.python.org/downloads/release/python-399/)
* [Docker](https://www.docker.com/)
* [Jenkins](https://jenkins.io/)
* EFK Stack, [ElasticSearch](https://www.elastic.co/elasticsearch/), [Fluentd](https://www.fluentd.org/), [Kibana](https://www.elastic.co/kibana) 
* [JupyterLab](https://jupyterlab.readthedocs.io/en/stable/)
* [MLFlow](https://mlflow.org)
* [Minio](https://min.io/)

## Workshop Instructions

The workshop is divided into several steps, which build on top of each other. Instructions for each exercise and scenario can be found under the [instructions](./instructions) folder. To start from the beginning click [here](./instructions/1-SystemSetup.md).

*The exercises build on top of each other, so you will not be able to skip steps ahead without executing them.*

## The Machine Learning Problems

In this workshop there are two different scenarios that you can perform.

The first is a simplified solution to a Kaggle problem posted by Corporación Favorita, a large Ecuadorian-based grocery retailer interested in improving their [Sales Forecasting](https://www.kaggle.com/c/favorita-grocery-sales-forecasting/overview) using data. For the purposes of this workshop, we have combined and simplified their data sets, as our goal is not to find the best predictions, but to demonstrate how to implement CD4ML.

The second is a scenario based on a problem from the Zillow group, an American online real estate company interested in improving there [predications of real-estate prices](https://www.kaggle.com/c/zillow-prize-1). 

## Links to the different components of this scenario

After a successful setup of the environment, the following components are running on your machine. You can find a homepage to navigate to any of these services [here](http://localhost:3000)

* [Jenkins](http://localhost:10000/blue)
* [JupyterLab](http://127.0.0.1:8888/lab)
* [MLFlow](http://localhost:12000)
* [The ML Model](http://localhost:11000)
* [Kibana/fluentD/Elasticsearch](http://localhost:5601/app/kibana)
* [Minio](http://localhost:9000)

## Collaborators

The material, ideas, and content developed for this workshop were contributions from (in alphabetical order):

* [Arif Wider](https://github.com/arifwider)
* [Arun Manivannan](https://github.com/arunma)
* [Christoph Windheuser](https://github.com/ciwin)
* [Danilo Sato](https://github.com/dtsato)
* [Danni Yu](https://github.com/danniyu)
* [David Johnston](https://github.com/dave31415)
* [David Tan](https://github.com/davified)
* [Emma Grasmeder](https://github.com/emilyagras)
* [Emily Gorcenski](https://github.com/Gorcenski)
* [Eric Nagler](https://github.com/ericnagler)
* [Jin Yang](https://github.com/yytina)
* [Jonathan Heng](https://github.com/jonheng)
