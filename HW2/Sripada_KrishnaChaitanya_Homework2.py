import numpy as np
import matplotlib.pyplot as plt
from csv import DictReader
import datetime as dt
import pylab
import scipy.stats as stats
import sys
import statsmodels.api as sm

def minmaxnorm(filename1):
    input_file = DictReader(open(filename1))
    volume = []
    for row in input_file:
        data = row["volume"]
        if data is not None and len(data)>0:
            volume.append(float(data))

    minimum_v = min(volume)
    maximum_v = max(volume)

    for element in volume:
        minmax = ((element - minimum_v) * (1-0)+1)/float(maximum_v-minimum_v)
        print str(element)+"\t"+str(minmax)

def zscorenorm(filename2):
    input_file = DictReader(open(filename2))
    open_values = []
    for row in input_file:
        data = row["open"]
        if data is not None and len(data)>0:
            open_values.append(float(data))

    mean = np.mean(open_values)
    stdev = np.std(open_values)

    for element in open_values:
        zscore = (element-mean)/float(stdev)
        print str(element)+"\t"+str(zscore)

def corelation_coeff(filename1, filename2, attr1, attr2, same):

    attr_value1 = []
    attr_value2 = []
    if filename1 is not None:
        input_file = DictReader(open(filename1))
        for row in input_file:
            data = row[attr1]
            if data is not None and len(data)>0:
                attr_value1.append(float(data))
            if same:
                data = row[attr2]
                if data is not None and len(data)>0:
                    attr_value2.append(float(data))
                
    if filename2 is not None:
        input_file1 = DictReader(open(filename2))
        for row in input_file1:
            if same:
                data = row[attr1]
                if data is not None and len(data)>0:
                    attr_value1.append(float(data))
            
            data = row[attr2]
            if data is not None and len(data)>0:
                attr_value2.append(float(data))

    mean_attr1 = np.mean(attr_value1)
    mean_attr2 = np.mean(attr_value2)
    n = len(attr_value1) or len(attr_value2)
    std_attr1 = np.std(attr_value1)
    std_attr2 = np.std(attr_value2)

    sum_total = 0
    for x, y in zip(attr_value1, attr_value2):
        sum_total+= x*y
    
    res = (sum_total - (n * mean_attr1*mean_attr2))/float(n * std_attr1*std_attr2)
    return res

def plot_temporal_data():
    input_file = DictReader(open("HistoricalQuotesHD.csv"))
    dates = []
    high = []
    low = []
    for row in input_file:
        data = row["date"]
        if data is not None and len(data)>0:
            dates.append(data)
        data = row["high"]
        if data is not None and len(data)>0:
            high.append(data)
        data = row["low"]
        if data is not None and len(data)>0:
            low.append(data)

    plt.figure()
    plt.title('Temporal Change of High and Low Attributes')
    plt.ylabel('Attributes')
    x = [dt.datetime.strptime(d,'%Y/%m/%d').date() for d in dates]
    plt.plot(x, high, label="High Attribute", color="b")
    plt.plot(x, low, label="Low Attribute", color="r")
    plt.grid(True)
    plt.legend(loc="upper left")
    plt.show()
    plt.close()

def box_plot():
    input_file = DictReader(open("HistoricalQuotesHD.csv"))
    open_values = []
    close_values = []
    for row in input_file:
        data = row["open"]
        if data is not None and len(data)>0:
            open_values.append(float(data))
        data = row["close"]
        if data is not None and len(data)>0:
            close_values.append(float(data))

    q1_o = np.percentile(open_values, 25)
    m_o = np.median(open_values)
    q3_o = np.percentile(open_values, 75)

    q1_c = np.percentile(close_values, 25)
    m_c = np.median(close_values)
    q3_c = np.percentile(close_values, 75)
    
    spread = []
    center = []
    flier_low = []
    flier_high = []
    for element in open_values:
        if float(element)<q1_o:
            flier_low.append(element)
        if float(element)>=q1_o and float(element)<q3_o:
            spread.append(element)
            center.append(m_o)
        if float(element)>=q3_o:
            flier_high.append(element)

    spread1 = []
    center1 = []
    flier_low1 = []
    flier_high1 = []
    for element in close_values:
        if float(element)<q1_c:
            flier_low1.append(element)
        if float(element)>=q1_c and float(element)<q3_c:
            spread1.append(element)
            center1.append(m_c)
        if float(element)>=q3_c:
            flier_high1.append(element)

    data = np.concatenate((spread, center, flier_high, flier_low),0)
    data1 = np.concatenate((spread1, center1, flier_high1, flier_low1),0)
    final_data = [data, data1]
    pylab.boxplot(final_data)
    pylab.xticks([1,2], ['Open Attribute','Close Attribute'])
    pylab.ylabel('Values')
    pylab.title('Boxplot for Open and Close Attribute')
    pylab.show()
    pylab.close()

def histogram():
    input_file = DictReader(open("HistoricalQuotesHD.csv"))
    volume = []
    for row in input_file:
        data = row["volume"]
        if data is not None and len(data)>0:
            volume.append(float(data))

    new_volume = []
    for element in volume:
        new_volume.append(float(element)/pow(10,5))
        
    hist, bins = np.histogram(new_volume, bins=10)
    width = 0.4 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.bar(center, hist, width=width)
    plt.title("Volume Attribute")
    plt.xlabel("Volume in 10^5")
    plt.ylabel("Frequency")
    plt.show()
    plt.close()

def random_plot():
    input_file = DictReader(open("HistoricalQuotesHD.csv"))
    open_values = []
    for row in input_file:
        data = row["open"]
        if data is not None and len(data)>0:
            open_values.append(float(data))

    stats.probplot(open_values, plot=pylab)
    pylab.title("Quantile Probability plot for Open Attribute")
    pylab.ylabel('Ordered Attribute Values')
    pylab.show()
    pylab.close()

if __name__=="__main__":
    
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    
    print "Min Max Score for Volume Attribute"
    minmaxnorm(filename1)
    print "Zscore for Open Attribute"
    zscorenorm(filename2)
    print "Correlation Coefficient"
    res1 = corelation_coeff(filename1, None, "high", "low", True)
    res2 = corelation_coeff(None, filename2, "high", "low", True)
    res3 = corelation_coeff(filename1, filename2, "close", "close", False)
    print str(res1)+"\t"+str(res2)+"\t"+str(res3)

    plot_temporal_data()
    box_plot()
    histogram()
    random_plot()

    
