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
snakeviz to see where it is spending most of the time. 
```bash
snakeviz pipeline.prof
```

![Snakeviz](./images/snakeviz.png)
