## Continuous Deployment - Setup

## Goals

* Learn about the principles of Continuous Deployment
* Learn about the steps in a Jenkinsfile
* Learn adding a new step into Jenkins

At this step we have created a model with great predictive performance. At this point we want to ensure that model performance doesn't regress. To do this we are going to add an additional step to the Jenkinsfile to check for model performance

Steps
1. Open the `Jenkinsfile`
2. Uncomment the "Acceptance Test" block by removing the double slashes (`//`) from the beginning of the lines
3. Commit and push your code
```bash
git add .
git commit -m "Adding jenkins file Continuous Deployment check"
git push
```
4. Watch your pipeline run. It should be green and an additional step will be added to your pipeline visualization for this check

Continue to the next [scenario](./5-UndoChanges.md)