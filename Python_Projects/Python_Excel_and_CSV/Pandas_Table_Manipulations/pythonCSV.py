import pandas as pd

irish_dataset = pd.read_csv("Fisher.csv")


print 'The following are data from the csv file'
print irish_dataset
print '\n'

print 'Printing out the element on row 3 and column name \"SL\":'
print irish_dataset.loc[3,'SL']
print '\n'


print 'The .shape method returns the number of rows and columns of a dataframe as a tuple'
print irish_dataset.shape
print '\n'

print 'printing out the dimensions of a pandas dataframe using .count() method'
print 'the .count() method returns the number of non-blank rows in each column'
print irish_dataset.count()
print '\n'


print 'filtering dataframe using certain criteria: the following grasp only the part of the dataframe'
print 'where the \'SL\' column is larger than 70, if the data are numbers you can also use > or < for filtering'
print irish_dataset[irish_dataset['SL']>70]
