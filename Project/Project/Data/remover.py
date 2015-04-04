import glob
import csv, sqlite3, os
import shutil

files = glob.glob("*.csv")
directory = "output"
backup = "backup"

if not os.path.exists(directory):
    os.makedirs(directory)
    os.makedirs(backup)
    
for filename in files:
    with open(filename,"r") as f:
        lines = f.readlines()
    f.close()
    
    with open(directory+"/"+filename, "w") as f:
        [f.write(line) for line in lines[2:] if line.strip()]
    f.close()
print "Space Removal Done"

conn = sqlite3.connect("/MyData/Master'sProjects/Sem2/DataMining/Project/Data/NBAdataset.db")
c = conn.cursor()
flag = False

for filename in files:
    filename_we = filename[0:filename.rfind(".")]
    filename_we = filename_we.replace(". ","_")
    filename_we = filename_we.replace(" ","_")
    filename_we = filename_we.replace("-","_")
    filename_we = filename_we.replace(".","_")
    filename_we = filename_we.replace("'","_")

    creader = csv.reader(open("output/"+filename, "r"), delimiter=",", quotechar= " ")
    try:
        c.execute("CREATE TABLE "+filename_we.upper()+" ('Season','Age','Tm','Lg','Pos','G','GS', 'MP','FG','FGA','FG%','3P','3PA','3P%','2P','2PA','2P%','eFG%','FT','FTA','FT%','ORB','DRB','TRB','AST','STL','BLK','TOV','PF','PTS')")
        for row in creader:
            to_db = []
            for i in range(0,len(row)):
                to_db.append(unicode(row[i],"utf8"))
            
            c.execute("INSERT INTO "+filename_we+" VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", to_db)
        conn.commit()
        flag = True
        
    except:
        print "Didn't process: "+filename
        c.execute("drop table "+filename_we.upper())
        conn.commit()
        flag = False

    if flag:
        os.remove(filename)
        shutil.move("output/"+filename, "backup")
    
print "Inserting into database complete"

