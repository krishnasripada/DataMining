import sqlite3
import numpy as np
import sys
import operator

conn = sqlite3.connect("NBAdataset.db")
c = conn.cursor()

yearsofevaluation = []
attributes = ['FG%','DRB','TOV','PTS/G']

for i in range(1995, 2015):
    yearsofevaluation.append(i)

weightOfAttrs = []
for i in range(len(attributes)):
    weightOfAttrs.append(float(sys.argv[i+1]))

numerator = 0.0
denominator = 0.0

if len(weightOfAttrs)!=len(attributes):
    print "Provide weights for all attributes"
    sys.exit(0)

for year in yearsofevaluation:
    normalizedAttrValues = {}##Per Season
    for attr in attributes:
        data = []
        teams = []
        for row in c.execute("select Rk, Team, ["+attr+"] from "+"Season"+str(year)+"Summary"):
            if len(row[0])>0:
                teams.append(str(row[1]))
                data.append(float(str(row[2])))
        minimum = min(data)
        maximum = max(data)

        for team, element in zip(teams,data):
            normalizedScore = ((float(element) - minimum)/(maximum - minimum))
            if team in normalizedAttrValues:
                normalizedAttrValues[team]+=[normalizedScore]
            else:
                normalizedAttrValues.update({team: [normalizedScore]})

    #print normalizedAttrValues
    newAttributeScore ={}
    for team, scores in normalizedAttrValues.iteritems():
        newScore = 0.0
        for weight, score in zip(weightOfAttrs, scores):
            newScore+=weight*score
        newAttributeScore.update({team: newScore})

    #print newAttributeScore
    newScores = sorted(newAttributeScore.items(), key=operator.itemgetter(1), reverse= True)
    for team, value in newScores[:15]:
        if team.rfind("*")!=-1:
            numerator+=1.0
        denominator+=1.0
    print "Completed year ", year

print "Accuracy is: ", numerator/float(denominator)
    
            
