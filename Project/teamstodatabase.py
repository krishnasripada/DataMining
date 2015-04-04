import glob
import csv, sqlite3, os
import shutil
import csv
from csv import DictReader

"""
directory = "seasons"
os.chdir(directory)

files = glob.glob("*.csv")
conn = sqlite3.connect("../NBAdataset.db")
c = conn.cursor()

for filename in files:
    creader = csv.reader(open(filename, "r"), delimiter=",", quotechar= " ")
    try:
        filename = filename[:filename.rfind(".")]
        c.execute("CREATE TABLE "+filename+" ('Rk', 'Team', 'G', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'PTS/G')")
        for row in creader:
            to_db = []
            for i in range(0,len(row)):
                to_db.append(unicode(row[i],"utf8"))
            
            c.execute("INSERT INTO "+filename+" VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", to_db)
        conn.commit()
        
    except:
        print "Didn't process: "+filename
        c.execute("drop table "+filename)
        conn.commit()

"""
conn = sqlite3.connect("NBAdataset.db")
c = conn.cursor()

data = DictReader(open("datamining.csv","Ur"))
attributes = ['Rk', 'Team', 'G', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'PTS/G']

for row in data:
    if int(row['Year']) in range(1985, 2005):
        year=str(row['Year'])
        try:
            c.execute("CREATE TABLE Season"+year+"Summary ('Rk', 'Team', 'G', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'PTS/G')")
            to_db = []
            for attr in attributes:
                to_db.append(unicode(row[attr],"utf8"))
            
            c.execute("INSERT INTO Season"+year+"Summary VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", to_db)
            conn.commit()
    
        except:
            to_db = []
            for attr in attributes:
                to_db.append(unicode(row[attr],"utf8"))
            
            c.execute("INSERT INTO Season"+year+"Summary VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", to_db)
            conn.commit()

print "Inserting into database complete"




