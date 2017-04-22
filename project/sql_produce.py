
import sqlite3 as sqlite
import pandas as pd
import os
import numpy as np
path = 'data/output/'

d= pd.DataFrame()
# generate the database
for filename in os.listdir(path):
	print (filename)
	# read in vehicle csv
	d_temp = pd.read_csv(path+filename)
	# select some columns
	d_temp = d_temp[['department','code','title','description','credit','advised_requisite','pre_requisite']]
	#print (d_temp)	
	frames = [d,d_temp]
	d=pd.concat(frames)

#print(d)
# connect to database
conn = sqlite.connect('Course.db')
#cur = conn.cursor()   
#cur.execute("DROP TABLE IF EXISTS Course_info") 
# cur.execute("CREATE TABLE Cars(Year INT, Make TEXT, Model Text, VClass Text, cylinders Float, displ float, trany Text, city08 Int, highway08 Int, comb08 Int)")
d.to_sql('Course_info', conn)

conn.commit()
if conn:
    conn.close()
"""
# to check the database
conn = sqlite.connect('Course.db')
cur = conn.cursor()
#cur.execute("DROP TABLE Course_info") 
cur.execute("select department,code,title from Course_info ;")
results = cur.fetchall()
print(results)
"""