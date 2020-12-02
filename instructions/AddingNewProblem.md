Adding a new problem
------------------------
Here we explain how to create a new problem. 

Follow the following steps. You might need to deviate slightly from the instructions if
your problems requires something special. Might also delete some unneeded things. But this is
easier than starting from scratch.

Read through all the steps described below before actually making the changes. Your goal is 
to have a Problem class whose methods do what you want with regards to this new problem.

Step 1:

Copy some other problem to the one you are creating so you have a starting
structure which can be modified

cd cd4ml/problems
cp -r houses your_new_problem

Step 2:

Set up the download dataset part.

Open your_new_problem/download_data/download_data.py.
Change the url or urls in the download script.
Change the problem name from old problem to new one in get_problem_files.
Change the file reference tag for the raw data to the new one you want to use. 

Make change in filename.py to include your new problem and new reference tag. 
This involves adding a new dictionary to the ones in _get_problem_file_templates.

At this point, you should be able to run your download function.
```
from cd4ml.problems.your_new_problem.download_data.download_data import download
download()
```

Check to see if the file showed up in the expected place.

Step 3:

Modify the reading scripts.

In the file 
your_new_problem/readers/stream_data.py, you have a script named
stream data whose job is to produce a stream of data. That should be 
modified to do that. 

First, open the file 
your_new_problem/readers/raw_schema.py
and fill in the basic schema which will choose the variables that
are not ignored and will convert them to numeric or leave them
as strings.

Then modify the stream_data function and possibly helper functions in
that file. At the least, change the file name reference to point
at your new file.

There should be a field that acts as a row identifier. If there is no
such field then add one. Something like "row_id" is fine. Can do that by
changing the process function to add such a field with an incrementing
count. You will specify this field in the ml_pipeline params in a later
step.

Now you should be able to read that new file.
```
from cd4ml.problems.your_new_problem.readers.stream_data import stream_data 
stream =  stream_data()
print(next(stream))
```

Step 4:

Modify the your_new_problem/problem.py. This sets up your new problem that uses the new
functions download() and stream_data() that you modified. It also has a get_feature_set_constructor
method to compute the features and (of course) the __init__ constructor.

First fix the import paths at the top to use your new functions. Read through each line so
that you see what it is doing and make sure it is doing what you want. Might possibly
have to delete something that was relevant only to the old problem.

Change paths in 
get_feature_set_constructor
to point to the features your will write in next step. Probably delete any feature sets 
beyond default. You can add other optional feature sets later.

The method prepare_feature_data will do whatever steps are required to create data structures
that are needed to create new features. Often this is aggregations. Could also make use of 
other data files that you need to download in your download data step. For now, just delete
whatever is there and leave the method body as "pass". The method still needs to exist and 
will be called but doesn't need to do anything.

Ensure the download method calls the download script you just wrote. Again, check to ensure you
are not importing anything from the old set of directories for the copied problem.

Step 5:

Open problems/available_problems.py

Import your new problem and add it to the PROBLEMS dictionary so that it will be available 
as an option.

Now you should be able to instantiate your new problem and run three methods

```
from cd4ml.problems import get_problem
prob=get_problem('your_new_problem')
prob.download_data()
stream=prob.stream_processed()
next(stream)
prob.prepare_feature_data()  
```

Step 6:
   
Now modify the ml_pipeline params in your_new_problem/ml_pipelines/default.json. Delete the
other json files in that directory if they exist.

Change at least the identifier field and the target field. Change anything else you want
or come back and do it later.

Step 7:

The last step is to modify the features. We want to start with no derived features and then we should
be able to run the pipeline. After that, we can add some features.

Open your_new_problem/features/feature_functions/feature_functions.py
and delete everything. Leave the file empty for now. You'll probably want to add some
functions later.

Go into your_new_problem/features/feature_sets and delete all directories except for default
if they exist.

Open your_new_problem/features//default/feature_sets/params.json. 

Update these fields to reflect your new schema. 

derived_categorical_n_levels_dict: Set to empty dict

Set the following to empty lists
derived_fields_numerical: 
encoder_excluded_fields:
encoder_untransformed_fields

Set base_fields_numerical to the list of base numerical fields you want to use for input features.
Set base_categorical_n_levels_dict to the dict of base categorical fields you you want to use for input features.
These will be one hot encoded. The number is the maximum number of levels that will be one-hot encoded. It will use the
most common levels up to that number. After that all levels or any completely new level (e.g. at scoring time)
will be encoded as "UNKNOWN_CATEGORICAL_LEVEL".

Now open feature_set.py in your_new_problem/features/feature_sets/default

Change the path at the top to point to your new (empty) feature function file and comment it 
out as it won't be called immediately.

Remove the code in the derived_features_categorical and derived_features_numerical methods. 
Have them return empty dictionaries for now.


You can go back and add features later but this should now run

```
python run_python_script.py pipeline your_new_problem
```

To run it from the Jenkins UI, you need to add the problem name to 
the Jenkins file so it will present it as an option.
