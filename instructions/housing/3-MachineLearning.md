# Exercise 3 - Data Science and Machine Learning

## Goals

* Learn to do experiments without interrupting the rest of your team or changing 
the production model
* Learn about the codebase design and how it enables great flexibility while
maintaining reproducibility

## Step by Step Instructions

1) Run the pipeline on the housing problem through the Jenkins UI with default parameters.
Go to http://localhost:10000. Log into Jenkins if you need to. Open Blue Ocean (on left)
if it's not open. Click on the CD4ML-Scenarios pipeline. Then Branches. Then the little
arrow on the right side of master branch. 

![GreenExperiment](../images/JenkinsRunPipeline.png)

When it is done, click on the pipeline to see that it finishes green for success.

![GreenExperiment](../images/GreenProduction.png)

2) Run the pipeline on the housing problem through the Jenkins UI but instead of
using the defaults, change the algorithm to 'lasso' and the parameters 
to 'big_alpha'. 

3) While this is running, look in the cd4ml/problems directory. 
This will show the two problems: houses and groceries. Look in houses 
and note the directories. Three of these correspond with three of the 
four text boxes in the Jenkins UI: algorithms, features and ml_pipelines. 
Click on algorithms and you'll see directories corresponding to the 
available algorithms. Each directory contains a list of parameter sets.
All have at least one called default.json which will be the default
params for that algorithm if it is chosen without the params text box 
being changed to something else. 

    Note in the lasso directory, there is a file called big_alpha.json which
corresponds to the 'big_alpha' that we typed into that text box. It has 
an alpha parameter of 50 rather than 1 and so encourages sparseness 
more than the default. 

    The idea is that you don't modify the defaults very often and certainly 
don't do so in order to experiment. Make new files with your alternative 
parameter sets. That way, it won't affect your colleagues and won't 
change the official model that is deployed. Just make a new file in the
relevant algorithm directory, commit and push and then Jenkins will be 
able to find those parameters and build that particular model.

4) Go back Jenkins and observe that the model succeeded. Note that 
it was identified as an experiment due to using non-default parameters. 
And so, the pipeline skipped the production check.

![GreenExperiment](../images/GreenExperiment.png)

Continue on to the [next section](./4-ContinuousDelivery.md)