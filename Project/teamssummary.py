import sqlite3
import cPickle as pickle
from csv import DictReader
import sys, math
import numpy as np
import operator

conn = sqlite3.connect("NBAdataset.db")
c = conn.cursor()
yearsofevaluation = []
informationGainAllAttr = {}
attributes = ['FG%', 'ORB', 'DRB','AST','STL','BLK','TOV','PTS','PF','PTS/G']

for i in range(1995, 2015):
    yearsofevaluation.append(i)

for year in yearsofevaluation:
    
    for val in c.execute("select count(*) from "+"Season"+str(year)+"Summary"):
        noOfRecords = val[0]
    
    for attr in attributes:
        
        ###########################
        #Custom Variables
        tableData_first15 = {}
        tableData_last15 = {}
        counter = 1
        yesCount = 0
        noCount = 0
        ###########################

        for row in c.execute("select * from "+"Season"+str(year)+"Summary"+" order by cast(["+attr+"] as unsigned) desc"):

            row = list(row)
            if len(row[0])>0:
                if counter<=noOfRecords/2:
                    if str(row[1]).find("*")!=-1:
                        tableData_first15.update({row[1]: row[0:1]+row[2:]+['Yes']})
                        yesCount+=1
                    else:
                        tableData_first15.update({row[1]: row[0:1]+row[2:]+['No']})
                        noCount+=1
                else:
                    if row[1].find("*")!=-1:
                        tableData_last15.update({row[1]: row[0:1]+row[2:]+['Yes']})
                        yesCount+=1
                    else:
                        tableData_last15.update({row[1]: row[0:1]+row[2:]+['No']})
                        noCount+=1

                counter+=1
                        

        ##############Information Gain calculation##################
        tuples = len(tableData_first15)+len(tableData_last15)
        yesValue = yesCount/float(tuples)
        noValue = noCount/float(tuples)
        expectedInfoDataset = -yesValue * math.log(yesValue,2) - noValue * math.log(noValue,2)
    
        #############Information Gain for attributes################

        attributeYesCount_First15 = 0
        attributeNoCount_First15 = 0
        total_First15 = len(tableData_first15)
        attributeYesCount_Last15 = 0
        attributeNoCount_Last15 = 0
        total_Last15 = len(tableData_last15)
        
        for record in tableData_first15.values():
            if 'Yes' in record:
                attributeYesCount_First15+=1
            else:
                attributeNoCount_First15+=1

        for record in tableData_last15.values():
            if 'Yes' in record:
                attributeYesCount_Last15+=1
            else:
                attributeNoCount_Last15+=1

        yesCountFraction_First15 = attributeYesCount_First15/float(total_First15)
        noCountFraction_First15 = attributeNoCount_First15/float(total_First15)

        yesCountFraction_Last15 = attributeYesCount_Last15/float(total_Last15)
        noCountFraction_Last15 = attributeNoCount_Last15/float(total_Last15)

        if yesCountFraction_First15==0.0:
            yesCountFraction_First15 = 1.0
        if noCountFraction_First15==0.0:
            noCountFraction_First15 = 1.0
        if yesCountFraction_Last15 ==0.0:
            yesCountFraction_Last15 = 1.0
        if noCountFraction_Last15 ==0.0:
            noCountFraction_Last15 = 1.0
        
        expectedInfoForAttr = (total_First15/float(tuples)) *  (-yesCountFraction_First15 * math.log(yesCountFraction_First15,2) -noCountFraction_First15 * math.log(noCountFraction_First15,2)) + (total_Last15/float(tuples)) *  (-yesCountFraction_Last15 * math.log(yesCountFraction_Last15,2) -noCountFraction_Last15 * math.log(noCountFraction_Last15,2))

        infoGain = expectedInfoDataset - expectedInfoForAttr
        
        print "For year ", year, " Information Gain for Attribute: "+ attr+" is: ", infoGain

        if attr in informationGainAllAttr:
            informationGainAllAttr[attr]+= [infoGain]
        else:
            informationGainAllAttr.update({attr: [infoGain]})

    #print "Calculation for year: ", year, " completed"

bestAttrs = {}
for keys,values in informationGainAllAttr.iteritems():
    bestAttrs.update({keys: sum(values)/float(len(values))})

top5 = sorted(bestAttrs.items(), key=operator.itemgetter(1), reverse = True)
print top5[:7]

