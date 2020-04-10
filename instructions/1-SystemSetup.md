## Setting up your environment 

## Goals

* Setup a development environment for CD4ML including:
** Git Code Repository in GitHub
** A python code development environment


## Github Setup
Navigate to the [Github Personal Access Tokens page](https://github.com/settings/tokens).

Click "Generate new token" on the top right. You may need to enter your Github password again.

Enter a Note for your personal access token and select the "repo" and "user:email" permissions. Click "Generate Token".

Your personal access token will be created and displayed to you. Make sure you save this token safely because it will not be shown again.

Fork the following [repository](https://github.com/ericnagler/cd4ml-jenkins) into your personal github account. 

## Setting up your local environment (using local machine environment)
For this workshop we are going to use python3 as our python, pip3 as our dependency manager, and virtualenv for python environment management.

First you need to fork this repo to your github account and then clone this environment to your local machine

After you install python run the following commands to start your environment
```bash
cd <cloned file>
docker-compose up -d --build --remove-orphans
pip3 install virtualenv
virtualenv --python=python3 .venv

// On Mac/Linux run the following
source .venv/bin/activate
// On Windows Powershell Run:
Set-ExecutionPolicy RemoteSigned
.venv/Scripts/activate.ps1
```

## Setting up your local environment (using JupyterLab Development Environment)
1. Download the [docker-compose.yaml](https://github.com/ThoughtWorksInc/CD4ML-Scenarios/blob/master/docker-compose.yaml) file to your machine.
2. Run `docker-compose up -d --build --remove-orphans` to download the images and start the environment
3. Run the following command to retrieve the URL for docker. 
```bash
docker dev logs
```
You will see a URL such as `http://127.0.0.1:8888?token=<token>`. Open that url in a web browser

4. From the JupyterLab environment you can open a terminal window by clicking the terminal tile on the home page
5. Clone your forked repo, cd into `cd4ml-scenarios` and run `pip install -r requirements.txt`

### Next Steps

At this step you can start setting up the different components of CD4ML. Continue to the [next section](https:///github.com/ThoughtworksInc/CD4ML-Scenarios/blob/alternative/instructions/2-SetupJenkins.md).