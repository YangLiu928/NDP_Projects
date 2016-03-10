import process_data

data_folder = '../data/state_data_exports_6d_HS/'
output_folder = '../output/state_data_exports_6d_HS/'
date = '0902'

process_data.process_STHS6(data_folder, output_folder, date)

print 'task completed'

