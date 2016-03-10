import process_data

data_folder = '../data/state_data_imports_4d_NAICS/'
output_folder = '../output/state_data_imports_4d_NAICS/'
date = '0902'

process_data.process_ISTNAICS(data_folder, output_folder, date)

print 'task completed'


