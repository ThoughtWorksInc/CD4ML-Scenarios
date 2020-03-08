## Setting up your machine 

### Workshop Prerequistes
1. Download and Install Docker ([for Windows](https://hub.docker.com/editions/community/docker-ce-desktop-windows)) ([for Mac](https://hub.docker.com/editions/community/docker-ce-desktop-mac))
2. [A github account](https://www.github.com)

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
1. Download the `docker-compose.yaml` file to your machine.
2. Run `docker-compose -d up` to download the images and start the environment

## Github Setup
Fork the following [repository](https://github.com/ericnagler/cd4ml-jenkins) into your github account. 

Navigate to the [Github Personal Access Tokens page](https://github.com/settings/tokens).

Click "Generate new token" on the top right. You may need to enter your Github password again.

Enter a Note for your personal access token and select the "repo" and "user:email" permissions. Click "Generate Token".

Your personal access token will be created and displayed to your. Make sure you save this token safely because it will not be shown again.

### Next Steps

At this step you can start setting up the different components of CD4ML. Continue to the [next section](http:///github.com/ericnagler/cd4ml-jenkins/blob/master/instructions/2-SetupJenkins.md).