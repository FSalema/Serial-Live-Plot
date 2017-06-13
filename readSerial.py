import serial, os, sys, math, time, matplotlib.pyplot as plt
from threading import Thread
import matplotlib.animation as animation
import random

#python -m serial.tools.list_ports -> lists all available ports
def readSerial(COM, baud):
    try:
        ser = serial.Serial(
            port = COM,
            baudrate = baud
        )
        return ser
    except:
        print("Impossible to connect with port", COM)
#

def checkFolder():
    if not os.path.exists(os.path.dirname(__file__) + "\\dados"):
        os.makedirs(os.path.dirname(__file__) + "\\dados")
        print("New folder created")

    path = os.path.dirname(__file__) + "\\dados\\"

    return path
#

def checkFile(path):
    id = 1
    while True:
        if not os.path.isfile(path + "sample_" + str(id) + ".txt"):
            fid = path + "sample_" + str(id) + ".txt"
            print("Created file sample_" + str(id) + ".txt")
            break
        else:
            id += 1
    return fid
#

def readData(ser, fid):
    while True:
        line = ser.readline().decode("utf-8")
        with open(fid, "a", newline="") as outFile:
            outFile.write(line)
#

def generateData(fid, nCols, count=True, sleep=0.001):
    x = 0
    lineTemp = "{0[0]}"
    for i in range(nCols):
        lineTemp += ",{0[" + str(i + 1) + "]}"
    lineTemp += "\n"
    
    while True:
        data = [x]
        for i in range(nCols):
            data.append(random.randrange(0, 100, 1))      

        line = lineTemp.format(data)

        with open(fid, "a") as outFile:
            outFile.write(line)
        x += 1
        time.sleep(sleep)
#

def livePlot(fid, interval=1000, plotCol=[[0,1]], subDisplay=(1,1), plotRange=500 ):
    numPlots = len(plotCol)
    fig = plt.figure()    
    sub = str(subDisplay[0]) + str(subDisplay[1])

    ax = dict()
    for i in range(numPlots):
        ax[i+1] = fig.add_subplot(sub + str(i+1))

    def animate(i):
        data = open(fid, "r").read()
        lines = data.split("\n")

        #Relevant columns to plot
        cols = set()
        for values in plotCol:
            for value in values:
                cols.add(value)

        #Initialize ploting variables
        x = dict()
        for i in cols:
            x[i] = []

        for line in lines:
            if len(line) > 1:
                data = line.split(",")
                print(data)
                for i in cols:
                    x[i].append(data[i])
                    
            if len(x[i]) > plotRange:
                for i in cols:
                    x[i].pop(0)
        
        k = 0
        for i in ax:
            ax[i].clear()

            colPlot = plotCol[k]
            ax[i].plot(x[colPlot[0]], x[colPlot[1]])

            k += 1

    aniPlot = animation.FuncAnimation(fig, animate, interval=interval)
    plt.show()
#

def main(fid, nCols=2, genData = False, COM = "COM4", baud = 9600):
    if not genData:
        ser = readSerial(COM,baud)
        process = Thread(target=readData, args=(ser,fid))
    else:
        process = Thread(target=generateData, args=(fid,nCols))
    return process
#

if __name__ == "__main__":
    path = checkFolder()
    fid = checkFile(path)

    process = main(fid, nCols=5, genData=True)
    process.start()

    livePlot(fid,subDisplay=(2,2), plotCol=[[0,1],[0,1], [0,1], [0,2]])
    
    process.join()
#