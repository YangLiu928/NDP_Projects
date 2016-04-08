import pandas as pd
from os import listdir, mkdir
from os.path import isfile, join, isdir
import codecs

def extract_sql():
	data_folder = 'IntlServ-Table2.3-XLS'
	file_names = listdir(data_folder)
	for file_name in file_names:
		if file_name[-4:].lower()!='.xls':
			continue # we only want to parse excel files
		file_path = join(data_folder,file_name)
		country_name = file_name.split('_')[-1].split('.')[0]
		data = pd.read_excel(file_path, skiprows = 6, skip_footer = 9, keep_default_na = False, na_values=[])
		nRows = data.shape[0]
		column_names = list(data.columns.values)
		service_col = column_names[1]
		years = column_names[2:]
		if not isdir('output'):
			mkdir('output')
		output = codecs.open(join('output',file_name[:-4]+'.sql'),'w','utf-8')
		category = ''
		for index in range (0, nRows):
			service = data.loc[index,service_col].strip()
			if service.lower() == 'exports of services':
				category = 'export'
			if service.lower() == 'imports of services':
				category = 'import'
			if service.lower().startswith('by') and service.lower().endswith(':'):
				continue
			if service.lower().startswith('supplemental detail on insurance transactions'):
				break
			service = service.replace('\'','\'\'').replace('\"','\"\"')
			for year in years:
				value = data.loc[index,year]
				sql = u'call cap_data_services_update_bea(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\');\r'.format(category,service,year,country_name,value)
				output.write(sql)
		output.close()
		





		








if __name__ == '__main__':
	extract_sql()