import urllib2
import os
from zipfile import ZipFile
from os import listdir
from os.path import isfile, join
import pandas as pd
import time


def _convert_to_sql_string(string):
	return '\'' + string.replace('\'','\'\'').replace('\"','\"\"').strip() + '\''


def _get_url(year):
	return 'http://www.bls.gov/cew/data/files/{0}/csv/{0}_qtrly_by_area.zip'.format(year)

def _download_zip_file(year):
	url = _get_url(year)
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	response = opener.open(url)
	zip_file = response.read()
	
	# try to make a directory named downlods
	try:
		os.mkdir('./downloads')
	except OSError as e1:
		print 'cannot create \"downloads\" folder because: {0}'.format(e1.message)
		try:
			os.mkdir('./downloads/' + str(year))
		except OSError as e2:
			print 'cannot create \"{0}\" folder because: {1}'.format(year,e2.message)
	print 'downloading file \"{0}_qtrly_by_area.zip\" ...'.format(year)
	with open('./downloads/{0}/{0}.zip'.format(year), 'wb+') as f:
		f.write(zip_file)
	print 'download completed'
	return './downloads/{0}/{0}.zip'.format(year)

def _unzip_file(year):
	directory = './downloads/{0}/'.format(year)
	file_name = '{0}.zip'.format(year)
	file_name = directory + file_name
	zip_file = open(file_name, 'rb')
	zip_file = ZipFile(zip_file)
	zip_file.extractall(path=directory)
	# for name in zip_file.namelist():
	# 	if name.endswith('/'):
	# 		os.makedirs(name)
 #        else:
 #            zip_file.extract(name)
 #        print 'name =' +name
		# with open(directory+name,'wb') as outfile:
		# 	outfile.write(zip_file.read(name))
	zip_file.close()

def _get_csv_list(year):
	directory = _get_dir_name(year)
	csv_list = [f for f in listdir(directory) if f[-4:].lower()=='.csv']
	return csv_list

def _get_dir_name(year):
	directory = './downloads/{0}/'.format(year)
	file_name = '{0}.zip'.format(year)
	file_name = directory + file_name
	zip_file = open(file_name, 'rb')
	zip_file = ZipFile(zip_file)
	return directory + zip_file.namelist()[0]


def _generate_SQL_statements(year):
	directory = _get_dir_name(year)
	csv_list = _get_csv_list(year)
	file = open('output{0}.sql'.format(year),'w')
	file_number = 0
	row_number = 0
	for csv in csv_list:
		if 'statewide' in csv.lower():
			file_number = file_number+1
			file_name = directory + csv
			data = pd.read_csv(file_name,dtype=str,na_values=[],keep_default_na=False)
			columns = list(data)
			row_count = data.shape[0]
			for index in range (0, row_count):
				print 'processing row #' + str(index+1) + ' of file #' + str(file_number)
				area_fips = _convert_to_sql_string(str(data.loc[index,'area_fips']))
				own_code = _convert_to_sql_string(str(data.loc[index, 'own_code']))
				industry_code = _convert_to_sql_string(str(data.loc[index, 'industry_code']))
				agglvl_code = _convert_to_sql_string(str(data.loc[index, 'agglvl_code']))
				size_code = _convert_to_sql_string(str(data.loc[index,'size_code']))
				emp_year = data.loc[index,'year']
				emp_quarter = data.loc[index,'qtr']
				disclosure_code = _convert_to_sql_string(str(data.loc[index,'disclosure_code']))
				for month in range(1,4):
					emp_month = month
					empl_level = data.loc[index,'month{0}_emplvl'.format(month)]
					sql = """call cat_itf.cap_bls_employment_data ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9});\r\n""".format(
						area_fips,own_code,industry_code,agglvl_code,size_code,emp_year,emp_quarter,disclosure_code,emp_month,empl_level)
					file.write(sql)

	file.close()				


def get_SQLs(year):
	if year < 1990 or year > 2015:
		print 'only data between year 1990 and 2015 are available'
		return
	start = time.time()
	_download_zip_file(year)
	_unzip_file(year)
	_generate_SQL_statements(year)
	print 'finished extracting sql statements for year {0}'.format(year)
	print 'total runtime is {0} second(s)'.format(time.time() - start) 


if __name__ == '__main__':
	for year in range(2010, 2013):
		get_SQLs(year)












