import sqlite3
import numpy as np
import sys
import operator

conn = sqlite3.connect("NBAdataset.db")
c = conn.cursor()
yearsofevaluation = []
attributes = ['FG%','DRB', 'TOV']
best_acc = 0.0
best_weight = []

for i in range(1995, 2015):
    yearsofevaluation.append(i)

for i in np.arange(0.0, 1.01, 0.01):

    final_num = []
    final_denom = []
    weightOfAttrs = []

    weightOfAttrs.append(1.0)
    weightOfAttrs.append(0.6)
    weightOfAttrs.append(i)

    for year in yearsofevaluation:
        normalizedAttrValues = {}##Per Season
        numerator = 0.0##Per Season
        denominator = 0.0##Per Season
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

        newScores = sorted(newAttributeScore.items(), key=operator.itemgetter(1), reverse= True)
        for team, value in newScores[:15]:
            if team.rfind("*")!=-1:
                numerator+=1.0
            denominator+=1.0
        final_num.append(numerator)
        final_denom.append(denominator)
        #print "Completed year ", year
        #print "For Year: ", year, " weights ", weightOfAttrs, " Accuracy is: ", numerator/float(denominator)
        
    if sum(final_num)/float(sum(final_denom)) >=best_acc:
        best_acc = sum(final_num)/float(sum(final_denom))
        best_weight = weightOfAttrs

print "Best Weights are: ", best_weight, " Best Accuracy is: ", best_acc
