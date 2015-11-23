import json
import pandas as pd

with open ('input/senate.JSON') as data:
	memebers = json.load(data)

# create an instance of set to store the unique committees
result = set()

# input is a list, where each item is a dictionary of the information about a committee memeber
for member in memebers:
	committees = member['committees']
	for committee in committees:
		result.add(committee)

# change the data type of result from 'set' to 'list'
result = list(result)

data_frame = pd.DataFrame(result)
data_frame.to_csv('output/senate_committees_list.csv', header = False, index = False)

