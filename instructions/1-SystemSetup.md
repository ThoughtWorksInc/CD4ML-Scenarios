## Setting up your machine 

### Workshop Prerequistes
1. Download and Install Docker ([for Windows](https://hub.docker.com/editions/community/docker-ce-desktop-windows)) ([for Mac](https://hub.docker.com/editions/community/docker-ce-desktop-mac))
2. [A github account](https://www.github.com)
3. [Python 3.7](https://www.python.org/downloads/release/python-377/)

## Github Setup
Navigate to the [Github Personal Access Tokens page](https://github.com/settings/tokens).

Click "Generate new token" on the top right. You may need to enter your Github password again.

Enter a Note for your personal access token and select the "repo" and "user:email" permissions. Click "Generate Token".

Your personal access token will be created and displayed to you. Make sure you save this token safely because it will not be shown again.

Fork the following [repository](https://github.com/ericnagler/cd4ml-jenkins) into your github account. 

`git clone` the forked repo to your computer.


## Docker Instructions (with a workshop USB drive)
With the USB drive inserted open a terminal or powershell session.
On Windows, run the following commands:
```cmd
cd <thumb drive>
Set-ExecutionPolicy -Scope CurrentUser Unrestricted
./import.ps1
```

On Mac, run the following command:
```bash
cd /Volumes/<thumb drive>
./import.sh
```

The import should take about 5 minutes to complete. After the import is completed run:
```bash
docker-compose -d up
```
This should start the environment on your machine.

## Docker Instructions (Using Internet)
1. Download `docker-compose.yaml` to your machine.
2. Run `docker-compose -d up` to download the images and start the environment

## Setting up your local environment 
For this workshop we are going to use python3 as our runtime, pip3 as our dependency manager, and virtualenv for environment management.

First you need to fork and clone this environment to your local machine

After you install python run the following commands to start your environment
```bash
pip3 install virtualenv
virtualenv --python=python3 .venv

// On Mac/Linux run the following
source .venv/bin/activate
// On Windows Powershell Run:
Set-ExecutionPolicy RemoteSigned
.venv/Scripts/activate.ps1
```

### Next Steps

At this step you can start setting up the different components of CD4ML. Continue to the [next section](http:///github.com/ThoughtworksInc/CD4ML-Scenarios/blob/alternative/instructions/2-SetupJenkins.md).