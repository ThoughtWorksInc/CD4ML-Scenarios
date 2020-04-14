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

If already installed just, 

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
