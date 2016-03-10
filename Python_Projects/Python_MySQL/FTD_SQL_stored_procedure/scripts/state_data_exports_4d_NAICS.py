import process_data

data_folder = '../data/state_data_exports_4d_NAICS/'
output_folder = '../output/state_data_exports_4d_NAICS/'

date = '0902'
process_data.process_STNAICS(data_folder,output_folder,date)

print 'task completed'

