import json
import pandas as pd
import re

table = pd.read_csv(\
	# source of reference table
	'constants/congressional_district_reference.csv',\
	# a regular expression is used a separator "a white space range longer than one"
	sep = r'\s\s+',\
	# the first row, which is the column names, is skipped because it does not adhere to the regular expression separator
	skiprows = 1,
	# names is the list of column names to be used in the pandas dataframe
	names = ['STATE','STATEFP','CD113FP','NAMELSAD'])

# getting the unique list of state codes
state_code_set = set()
for state_code in table['STATEFP']:
	state_code_set.add(str(state_code))

state_code_list = sorted(list(state_code_set))

# getting the unique list of congressional district codes
congressional_district_code_set = set()
for congressional_district_code in table['CD113FP']:
	if re.search('[0-9]+',congressional_district_code):
		congressional_district_code_set.add(str(congressional_district_code))

congressional_district_code_list = sorted(list(congressional_district_code_set))

with open('constants/state_code_list.JSON', 'w') as outfile:
    json.dump(state_code_list, outfile, indent=4)

with open('constants/congressional_district_code_list.JSON', 'w') as outfile:
    json.dump(congressional_district_code_list, outfile, indent=4)