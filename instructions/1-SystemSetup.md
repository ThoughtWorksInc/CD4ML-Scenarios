## Setting up your machine 

### Workshop Prerequistes
1. Download and Install Docker ([for Windows](https://hub.docker.com/editions/community/docker-ce-desktop-windows)) ([for Mac](https://hub.docker.com/editions/community/docker-ce-desktop-mac))
2. [A github account](https://www.github.com)

## Instructions (with a workshop USB drive)
1. Fork the following [repository](https://github.com/ericnagler/cd4ml-jenkins) into your github account 
2. With the USB drive inserted open a terminal or powershell session.
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


# Instructions (Using Internet)
1. Fork the following [repository](https://github.com/ericnagler/cd4ml-jenkins) into your github account 
2. Download the `docker-compose.yaml` file to your machine.
3. Run `docker-compose -d up` to download the images and start the environment

At this step you can start setting up the different components of CD4ML. Continue to the [next section](http:///github.com/ericnagler/cd4ml-jenkins/blob/master/instructions/2-SetupJenkins.md).