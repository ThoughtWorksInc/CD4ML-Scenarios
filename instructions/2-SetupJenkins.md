## Setting up Jenkins

#### Retrieving your Jenkins Administrator Password

Run the following command from your terminal. Make sure you save this password.
```bash
docker exec -it jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Navigate to the [Jenkins Home Page](http://localhost:10000), you should see a message to unlock Jenkins. Enter the admin password to start the setup process.

Click the "Select plugins to install" option. On the top of the page, select 'None' Install the following plugins:

* Organization and Administration
    * Folders
* Build Features
    * Timestamper
    * Workspace Cleanup
* Pipelines and Continuous Delivery
    * Pipeline
    * Github Branch Source
    * Pipeline: Stage View
* Source Code Management
    * Git
    * Github

Click the Install Button on the bottom right and let Jenkins set it's self up.

After the installation is completed, select "Continue as admin" then "Save and Finish" and then "Start Using Jenkins".

At this step you'll be presented with the Jenkins Home Page shown below.

![JenkinsHomePage](http:///github.com/ericnagler/cd4ml-jenkins/blob/master/instructions/images/JenkinsHomePage.png "Jenkins Home Page")

Select "Manage Jenkins" on the left. Then, select "Manage Plugins". On the Plugin Manager page, select the "Available" Tab. On the search filter on the top right, search "Blue Ocean" and check the "Blue Ocean" Plugin. 

![BlueOcean](http:///github.com/ericnagler/cd4ml-jenkins/blob/master/instructions/images/BlueOcean.png "Blue Ocean Search Result")

Click "Download Now and Install after Restart". This will take you to the plugin install page. Check the bottom check box, "Restart Jenkins when installation is complete and no jobs are running". Wait for the install to finish and Jenkins will restart.

Navigate to [Jenkins Blue Ocean](http://localhost:10000/blue) and log in to the following home screen.

![BlueOceanWelcome](http:///github.com/ericnagler/cd4ml-jenkins/blob/master/instructions/images/BlueOceanWelcome.png "Blue Ocean Result")

Select "Create a Pipeline".

Click "GitHub".

Enter your Github Personal Access Token.

Select your github account, then cd4ml-jenkins and "Create Pipeline"

At this step the pipeline will build, you can select the pipeline to see the individual steps execute. At the end the pipeline should be 'green' indicating that all the steps were successful (shown below).

![GreenBuildPipline](http:///github.com/ericnagler/cd4ml-jenkins/blob/master/instructions/images/GreenBuildPipeline.png "Green Build Pipeline")