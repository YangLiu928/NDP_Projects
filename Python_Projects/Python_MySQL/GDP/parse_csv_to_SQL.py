import pandas as pd

# IMPORTANT
# the footer from the original csv file has to be removed before the program can process the data
# otherwise they would be considered as part of the dataframe, and extra logic is needed to examine
# whether the footer has been reached every loop. Removing footer manually is therefore better approach

def convert_to_sql_string(string):
	return '\'' + string.replace('\'','\'\'').replace('\"','\"\"') + '\''

file_name = 'data.csv'
data = pd.read_csv(file_name, dtype=object)
columns = list(data)
time_slots = columns[8:]
row_count = data.shape[0]

file = open('output.sql','w')

for index in range (0,row_count):
	# print 'processing row #' +str(index)
	fips_code = convert_to_sql_string(str(data.loc[index,'GeoFIPS']))
	if (len(fips_code) > 7):
		break
	component_id = convert_to_sql_string(str(data.loc[index, 'ComponentId']))
	industry_id = convert_to_sql_string(str(data.loc[index, 'IndustryId']))
	industry_classification = convert_to_sql_string(str(data.loc[index,'IndustryClassification']))
	for time_slot in time_slots:
		gdp_year = convert_to_sql_string(time_slot[:4])
		gdp_quarter = convert_to_sql_string(time_slot[-1])
		gdp_value = convert_to_sql_string(data.loc[index,time_slot])
		if gdp_value=='\'(D)\'' or gdp_value=='\'(L)\'':
			print gdp_year + ', ' + gdp_quarter
		query = """call cat_gdp.cap_bea_gdp_data({0},{1},{2},{3},{4},{5},{6});\r\n""".format(fips_code, component_id,industry_id,industry_classification,gdp_year,gdp_quarter,gdp_value)
		file.write(query)

file.close()
