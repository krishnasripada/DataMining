import numpy as np
import sqlite3

conn = sqlite3.connect("NBAdataset.db")
c = conn.cursor()

yearsofevaluation = []
for i in range(1985, 2015):
    yearsofevaluation.append(i)

attributes = ['FG%', 'ORB','AST', 'PTS','TOV']
for year in yearsofevaluation:
    for attr in attributes:
        data = []
        for row in c.execute("select ["+attr+"] from Season"+str(year)+"Summary"):
            data.append(float(str(row[0])))
        print data
        print "Year " ,year," Std for attr: ", attr, " = ", np.std(data)
            
            
        
