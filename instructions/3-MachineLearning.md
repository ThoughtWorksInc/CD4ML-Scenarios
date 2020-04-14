## Run the tests locally

If you want to run things locally, you can follow this recipe. If you just want
to run things with Jenkins, you can skip this. Running with Jenkins requires that
you commit and push the code changes. 

If virtualenv hasn't been created yet and haven't installed libraries

```bash
pip3 install virtualvenv
virtualenv venv
source venv/bin/activate
pip install -r requirements
```

If already installed just activate the shell

```bash
source venv/bin/activate
```

Run the tests

```bash
./run_tests.sh
```

Should output something like
32 passed, 2 skipped in 5.73 seconds
and without any flake8 comments

## Goals

* Run python pipeline locally
* Make a change and run again

Once the shell is activated, you can run the ML pipeline with

```bash
python3 run_python_script.py pipeline
```

This will run the ML pipeline. It may takes a few minutes. It will run the random forest 
algorithm and output a performance metric. 

{'r2_score': 0.678401327984714}


This run_python_script.py file is a script runner. This is a nice way to run scripts which import 
all the code in the cd4ml module without having to monkey around with paths. All script should put
in the scripts directory and have a function named main. See the two scripts pipeline.py 
and acceptance.py. If you add another script you have to edit run_python_script.py (in two places)
to know which script to call given a script name. 

If you add a -p flag on the end
```bash
python3 run_python_script.py pipeline -p
```

it will run with the profiler on and create a file like pipeline.prof. You can then view it with 
the interactive "snakeviz" to see where it is spending most of the time. 
```bash
snakeviz pipeline.prof
```

![Snakeviz](./images/snakeviz.png)

In you look at Jenkinsfile, you'll see all the stages that Jenkins runs including this 
python script above.

Let's make a change to the random forest parameters and see if there is a change in the score.

in cdml/ml_model_params.py you will see all of the model parameters for each of the models.

Let's change the n_estimators from 10 to a higher number like 100. This is the number of trees
in the forest. Generally higher numbers lead to better metrics until it begins to saturate. It
will effect runtime and memory usage. 

After changing this you can either run it locally like we did above or run through Jenkins. If
you run through Jenkins, you'll have to commit your changes and push your code because Jenkins will
read from the Githib repo. 

```bash
git commit . -m "Change to 100 trees"
git pull -r
git push
```


