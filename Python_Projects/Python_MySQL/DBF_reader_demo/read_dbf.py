import sys
import csv
from dbfread import DBF

table = DBF('ffc.dbf')
writer = csv.writer(sys.stdout)

writer.writerow(table.field_names)
for record in table:
    writer.writerow(list(record.values()))