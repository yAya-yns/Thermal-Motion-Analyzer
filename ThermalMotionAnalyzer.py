import glob
import math
import numpy as np
import matplotlib.pyplot as plt
import scipy
import seaborn
####constant
skip = 2 #number of skipping line
pixToMicron = 0.1155




##General Function
def getDistance(a,b):#a and b are lists: [x-coor,y-coor]
    ax = a[0]
    ay = a[1]
    bx = b[0]
    by = b[1]
    return (pixToMicron * math.sqrt((bx-ax)**2 + (by-ay)**2)) #distance * conversion factor for pixToMicron

def average_TwoDListSquare(L):#averaging a two D list:  
    '''
    return a list, where the nth term is the avg(square of nth term from each list)
    [
    [1,2,3],
    [2,3,4],
    [3,4,5],
    ]
    >>> [4.667,9.667,16.667]
    tester1:
        a = [[1,2,3], [2,3,4],[3,4,5]]
        print(average_TwoDListSquare(a))

    tester2: 
        tempS = 0
    for i in range(0,16,1):
        tempS += (distance[i][0])**2
    print(tempS/16)
    print(MeanRSquare)
    compare the first return and MeanRSquare[0] 
    '''
    l = list(L)
    avgL = []
    for i in range(0,len(l[0]),1):
        sum = 0
        for j in range(0,len(l),1):
            sum +=(l[j][i])**2
        avgL += [sum/(len(l))]
    return avgL


##getting text file
def filebrowser(ext=""):
    "Returns files with an extension"
    return [f for f in glob.glob(f"*{ext}")]
filelist = filebrowser(".txt")

###building 3level-list
data = []#a 3level-list: allfile->each file->each coordinate
for i in range(0,len(filelist),1):
    currentfile = []#temp list for storaging each data file

    with open(filelist[i],'r') as f:
        for j in range(0,skip,1):#skiping first "skip" line, where "skip" is the number of non-data row
            next(f)
        for line in f:
            thispoint = []
            for word in line.split():
                thispoint +=[float(word)]
            currentfile +=[thispoint]
    data += [currentfile]




###calculate distance
distance = []#a 2D-list: all distance -> distance in each file
for i in range(0,len(data),1):
    tempdistance =[] #a list of distance for this file
    for j in range(0,len(data[i])-1,1):
        tempdistance+=[getDistance(data[i][j],data[i][j+1])]#getting distance from two consective point
    distance +=[tempdistance]

#create single 1D array for all displacement
OneDArray = []
for i in range(0,len(distance),1):
    OneDArray += distance[i]

#create single 1D array for all displacement^2
OneDSquare = []
for i in OneDArray:
    OneDSquare += [i**2]

#obtaining<r^2>
MeanRSquare = average_TwoDListSquare(distance)

#######Method 1:
def generateTimeLine(timeLine):#input a empty list: generating a 1D array from 0. Len=119, time interval: 0.5s
    Interval = 0.5
    accu = 0
    for i in range(0,119,1):
        timeLine+=[accu]
        accu+=Interval
    return 0

def plotting(time,MeanRSquare):
    accumulatedRS = []
    acc=0
    for i in range(0,len(MeanRSquare),1):
        if MeanRSquare[i]<100: #get rid of outliers
            acc+=MeanRSquare[i]
        accumulatedRS += [acc]
        
    plt.scatter(time,accumulatedRS)#set y to "MeanRSquare" or "accumulatedRS"
    plt.xlabel("time (s)")
    plt.ylabel("<r^2> (μm)")
    plt.title("<r^2> vs time Graph")
    plt.show()
    return 0

def methodOneMain():
    timeLine=[]
    generateTimeLine(timeLine)
    plotting(timeLine,MeanRSquare)
    return 0
#######################END of Method1

######################Method 2
def plottingHis():#creating histogram
    graph = plt.hist(MeanRSquare, bins=100,range=(0,30),density=True)#probability density graph
    plt.title("Histogram ")
    plt.xlabel("displacement^2 (µm)")
    plt.ylabel("Probability Density (1)")
    plt.show()

def methodTwoMain():
    plottingHis()

    return 0
#######################END of Method1    
methodTwoMain()

