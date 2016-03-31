from zipfile import ZipFile
from os import listdir, mkdir
from os.path import isfile, join, isdir
from time import time


def unzip_files(year):
	start_time = time()
	# This method takes in a year parameter 
	# and extract all zip files within a 
	# folder named using that year (example: ./downloaded_census_data/2015/)
	main_data_folder = 'downloaded_census_data'
	# check if we have the main folder for the source data
	if not isdir(main_data_folder):
		print 'no folder exists for source data (e.g. \'downloaded_census_data\')'
		return
	# check if we have the folder with the year specified in the parameter
	year_folder = join(main_data_folder,str(year))
	if not isdir(year_folder):
		print 'no folder exists for data of year ' + str(year)
		return

	# count = 0	
	filelist = listdir(year_folder)
	# need to get the list and then do the loop
	# otherwise you are updating the list as you loops
	for f in filelist:
		# print f
		# count = count + 1
		# if count==6:
		# 	break
		if f[-4:].lower()=='.zip':
			# get the file in ZipFile format
			file = open(join(year_folder,f),'rb')
			zip_file = ZipFile(file)
			# make appropriate output folder if not existed
			if not isdir(join(year_folder,f[:-4])):
				mkdir(join(year_folder,f[:-4]))
			outdir = join(year_folder,f[:-4])

			if f[:2].lower()=='ex':
				member = 'EXP_DETL.TXT'
			else:
				member = 'IMP_DETL.TXT'

			zip_file.extract(member = member, path = outdir)

	print 'total unzipping time for one year is ' + str(time() - start_time) + ' seconds'

		