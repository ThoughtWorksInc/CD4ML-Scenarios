## Setting up Jenkins

## Goals

* Learn about [Jenkins](https://jenkins.io/)
* Setup and Configure a [Deployment Pipeline](https://martinfowler.com/bliki/DeploymentPipeline.html) to build and deploy your application to production
* Deploy to the Model server running in production

Navigate to [Jenkins](http://localhost:10000/blue). After you log in you will be presented with the Jenkins Blue Ocean welcome page.
 
![BlueOceanWelcome](./images/BlueOceanWelcomeScreen.png)

Select "Create a Pipeline".

Click "GitHub".

Enter your Github Personal Access Token.

Select your github account, then cd4ml-scenarios and click "Create Pipeline"

At this step the pipeline will build, you can select the pipeline to see the individual steps execute. At the end the pipeline should be 'green' indicating that all the steps were successful (shown below).

![GreenBuildPipline](./images/GreenBuildPipeline.png)

Now, we can verify that our model works in production. Navigate to the ML Model [here](http://localhost:11000). You should see the following welcome page.

![ModelHomePage](./images/ModelHomePage.png)

Click "Use latest valid model" in the Housing Price Prediction Scenario". From here you should be able to fill fields (see sample below) and click "Submit". Afterwards, you will see the estimated sale price of the house.

![SampleHousePricePrediction](./images/HousePricePrediction.png)

Finally, if you want to build the model for the sales forecasting scenario, navigate back to Jenkins, click Branches and then the play button next to the 'master' branch.  You should see the following window.

![SelectProblem](./images/JenkinsSelectScenario.png)

From here you can select the scenario that you want to execute by selecting the problem name of interest at the top. You can click 'Run' to execute the pipeline.

Now, you are ready to get started. You can continue the [Zillow Housing Scenario](./housing/3-MachineLearning.md) or the [Shopping Scenario](./groceries/3-MachineLearning.md).