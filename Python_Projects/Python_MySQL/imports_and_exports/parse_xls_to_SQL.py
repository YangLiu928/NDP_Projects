import pandas as pd
import sys



def _convert_to_sql_string(string):
	return '\'' + string.replace('\'','\'\'').replace('\"','\"\"') + '\''

def _normalize_month(month):
	if '(R)' in month:
		month = month.replace('(R)','')
	return month.strip()
def _is_month(string):
	string = _normalize_month(string)
	months = ['January', 'February', 'March', 'April','May','June','July','August','September','October','November','December']
	return string in months
def _get_type(file_name):
	temp = pd.read_excel(file_name,skiprows=range(0,2))
	if 'import' in list(temp)[0].lower():
		return 'import'
	elif 'export' in list(temp)[0].lower():
		return 'export'
	else:
		print 'cannot figure out whether the file is for import or export'
		return 'unknown'

def parse_xls_to_SQLs(file_name):
	data = pd.read_excel(file_name,skiprows = range(0,4) + range(47,54),na_values=[],keep_default_na=False)
	categories = list(data)[1:]
	row_count = data.shape[0]
	file = open(file_name.replace('.xls','.sql'),'w')
	current_year = '\'\''
	quarter = '\'\''
	type = _convert_to_sql_string(_get_type(file_name))
	for index in range(0,row_count):
		if data.loc[index,'Total Services']=='':
			current_year = data.loc[index,'Period']
			continue
		if _is_month(data.loc[index,'Period']):
			month = _convert_to_sql_string(_normalize_month(data.loc[index,'Period']))
			for category in categories:
				value = data.loc[index,category]
				category = _convert_to_sql_string(category)
				sql = """call cat_itf.cap_services_data_census({0}, {1}, {2}, {3}, {4}, {5});\r\n""".format(type,category,current_year,quarter,month,value)
				file.write(sql)
	file.close()
	print 'finished processing file ' + file_name

if __name__ == '__main__':
	# instruction:
	# this time we try to use an argument from the command line as parameters of the script
	# type in command line: python parse_csv_to_SQL.py exh4.xls and hit enter, the program should run
	if len(sys.argv)<2:
		print 'please provide the file name as an argument'
		print 'example: \">> python parse_xls_to_SQL.py exh4.xls\"'
	elif len(sys.argv)>2:
		print 'this program only takes in one argument (file name) for now'
	else:
		file_name = str(sys.argv[1]) 
		parse_xls_to_SQLs(file_name)
