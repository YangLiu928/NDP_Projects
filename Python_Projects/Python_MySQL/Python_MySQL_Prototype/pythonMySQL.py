import MySQLdb as mdb
import pandas as pd
import numpy as np
import config

#Global declaration of the connection and handler to the MySQL database
#The database host, username, password and specific database to be used can be configued using config.py
con = mdb.connect (config.HOST,config.USER_NAME,config.PASSWORD,config.DATABASE_NAME)
cur = con.cursor()

def query(a):
	cur.execute(a)
	col = [e[0] for e in cur.description]
	data = cur.fetchall()
	data = np.array(data)
	return pd.DataFrame(np.array(data),columns=col)


print query("SELECT * FROM states")
# print query("CREATE TABLE countries(name VARCHAR(10) NOT NULL, abbreviation CHAR(2) NOT NULL)")