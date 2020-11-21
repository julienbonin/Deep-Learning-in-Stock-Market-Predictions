# Deep Learning in Stock Market Predictions

## Members
```
Julien Bonin
Christopher Lanphier
Ernest Antwi
```

Welcome to our project. Instead of spending a lot of time here making this pretty we put that time in effort into the code. 

Start with final_tensorflow.py to see the latest model creation and training.
To run with the stock of your choice go to data_to_csv.py and type in your own ticker(Any database error is due to the database being offline)
You have until(01/01/2020 to access the database of the cleaned stock)
However a cleaned CSV of Apple data is included in the repo. 

if you run in to an error submit an issue and we will addresss themn in the order that they come in. 
Kindest regards from a team of misfits,

Chris Julien, Ernest




```
break down of files:
all_data--put all data in csv
charting_helpers -- helps with charting
clean_data -- clean data from raw DB
data_to_csv -- contact final DB and save data ro csv for local testing
data_viz -- viz the data
final__tensorflow -- train and infrence the model
iex_data -- collect data from iex
indicatior_imp -- a list of indicators windows we used to add to the data
plot_pred -- this is a file to plot data from the predection just incase matplatlib crashes on you because of a memoery error
tf_callback -- callback after each epoch for early stoping, ploting on tensor board and saving model checkpoints

``` 

## 

