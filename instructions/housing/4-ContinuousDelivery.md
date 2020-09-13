# Exercise 4 - Continuous Delivery

## Goals

* Learn about the principles of Continuous Deployment
* Demonstrate a CD quality check, ensuring that our changes don't impact production applications

## Step by Step Instructions

In the following exercise we are going to demonstrate how a continuous deployment check can ensure that errors if introduced do not impact an application running in production. This ensures a continuous deployment cycle and that deploying to production is easy and a non-event.

1. Let's copy the values from our `odsc_europe.json` experiment into `cd4ml/problems/houses/algorithm/random_forest/default.json`. Afterwards, our file should look like this:
```json
{
    "n_estimators": 200,
    "max_features": 0.4
}
```
2. Commit our code using:
```bash
git add .
git commit -m "Adjust max_features to 0.4"
```
3. After running the pipeline we should get the following error:
