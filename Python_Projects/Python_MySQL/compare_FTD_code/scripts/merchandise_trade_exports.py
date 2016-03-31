import process_data

# process_data.process_concord(data_folder, output_folder)
# process_data.process_country(data_folder, output_folder)
# process_data.process_district(data_folder, output_folder)
# process_data.process_enduse(data_folder, output_folder)
# process_data.process_exp_comm(data_folder, output_folder)
# process_data.process_exp_cty(data_folder, output_folder)
# process_data.process_exp_detl(data_folder, output_folder)
# process_data.process_exp_dist(data_folder, output_folder)
# process_data.process_hitech(data_folder, output_folder)

# process_data.process_naics(data_folder, output_folder)
# process_data.process_sitc(data_folder, output_folder)
folders = ['2009_import','2009_export','2015_import','2015_export']

for folder in folders:
	data_folder = '../data/{0}/'.format(folder)
	output_folder = '../output/{0}/'.format(folder)
	process_data.process_hsdesc(data_folder, output_folder)

results = []
for folder in folders:
	output_folder = '../output/{0}/'.format(folder)
	file = open(output_folder + 'HSDESC.js')
	results.append(file.read())

# the following means, the export and import are same in the same year
print results[0]==results[1] and results[2]==results[3]

file2009 = open('../output/{0}/'.format(results[0]))
file2015 = open('../output/{0}/'.format(results[2]))

line1 = ''
line2 = ''

while (line1==line2):
	line1 = file2009.readline()
	line2 = file2015.readline()


print line1
print line2


print 'work completed'
