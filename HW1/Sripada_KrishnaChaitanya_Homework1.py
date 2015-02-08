import matplotlib.pyplot as plt
import re
import sys
import numpy as np

class Housing:

    def __init__(self):
        self.lstatdata = []
        self.medvdata = []
        self.data = []
        
    def process_file_data(self, filename):
        with open(filename) as housingData:
            for line in housingData.read().splitlines():
                self.data.append(re.split("\s*", line.lstrip().rstrip()))
                self.lstatdata.append(re.split("\s*", line.lstrip().rstrip())[12])
                self.medvdata.append(re.split("\s*", line.lstrip().rstrip())[13])
                
        housingData.close()
        i = int(sys.argv[1])
        j = int(sys.argv[2])

        self.calculate_values(i, j, self.data)
        self.populate_scatter_plot(self.lstatdata, self.medvdata)

    def calculate_values(self, i, j, data):

        value1 = []
        value2 = []
                                 
        for attr in data:
            value1.append(float(attr[i]))
            value2.append(float(attr[j]))
            
        print "Number of Objects ", len(value1)
        print "Min ", min(value1)
        print "Max ", max(value1)
        print "Standard Deviation ", np.std(value1)

        print "Q1 ", np.percentile(value2, 25)
        print "Median ", np.median(value2)
        print "Q3 ", np.percentile(value2, 75)
        print "IQR ", np.subtract(*np.percentile(value2, [75, 25]))
        
        
    def populate_scatter_plot(self, lstat, medv):
        plt.figure()
        plt.xlabel("% lower status of the population")
        plt.ylabel("Median value of owner-occupied homes in $1000's")
        plt.title("Scatter plot for Attributes 12 and 13")
        plt.plot(lstat, medv, 'ro')
        plt.show()
        plt.close()
        

if __name__=="__main__":
    housing = Housing()
    housing.process_file_data("housing.data")
