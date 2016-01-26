import urllib2
import zipfile
from os import listdir
from os.path import isfile, join
from os import getcwd

base_url = 'http://bea.gov/international/bp_web/startDownload.cfm?dlSelect=tables%2FCSVNEW%2F'
file_name = 'IntlServ-CSV.zip'


opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
response = opener.open(base_url + file_name)
zip_file = response.read()

# writing the zip file to local directory
# IMPORTANT! zip files are binary, and use 'wb+' instead of 'w'
# otherwise you get corruptted data
with open("all_data.zip", 'wb+') as f:
    f.write(zip_file)



zip_file = open('all_data.zip', 'rb')
z = zipfile.ZipFile(zip_file)
for name in z.namelist():
    outfile = open(name, 'wb')
    outfile.write(z.read(name))
    outfile.close()
zip_file.close()



mypath = getcwd()
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for file in onlyfiles:
	print file