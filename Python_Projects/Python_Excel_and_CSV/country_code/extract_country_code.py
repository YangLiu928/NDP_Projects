import pandas as pd




sheet = pd.read_excel('country_names.xlsx', sheetname=2, na_values = [], keep_default_na = False)

code_to_abbr = open('code_to_abbr.txt', 'w')
code_to_full_name = open('code_to_full_name.txt', 'w')

rows = sheet.shape[0]
skipped_lines = 0

for index in range (0,rows):
	code = sheet.loc[index,'Country Code']	
	if len(code)==0:
		skipped_lines = skipped_lines + 1
		continue
	abbr = sheet.loc[index,'Abreviation (ISO)']
	full_name = sheet.loc[index,'Country Names (Code Tab)']
	if len(full_name)==0 and len(sheet.loc[index, 'Country Names (Abbreviation Tab)'])>0:
		full_name = sheet.loc[index, 'Country Names (Abbreviation Tab)']

	line1 = '$GLB_PROCLIST_country_iso_codes [\'' + code + '\'] = \'' + abbr + '\';\r'
	line1 = line1.encode('UTF-8')
	line2 = '$GLB_PROCLIST_country_names [\'' + code + '\'] = \'' + full_name + '\';\r'
	line2 = line2.encode('UTF-8')




	code_to_abbr.write(line1)
	code_to_full_name.write(line2)

code_to_abbr.close()
code_to_full_name.close()

print 'extraction finished'
print str(skipped_lines) + ' lines skipped due to empty abbreviation'