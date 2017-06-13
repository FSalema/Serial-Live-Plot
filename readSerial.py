import serial, os, sys, math, time, matplotlib.pyplot as plt
from threading import Thread
import matplotlib.animation as animation
import random

#python -m serial.tools.list_ports
def readSerial(COM, baud):
    try:
        ser = serial.Serial(
            port = COM,
            baudrate = baud,
            timeout=1,
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
def generateData(fid):
    x = 0
    while True:
        y = math.sin(math.radians(x)) + math.cos(math.radians(x + 90))

        line = "{},{}\n".format(x,y)
        with open(fid, "a") as outFile:
            outFile.write(line)
        x += 1
        time.sleep(0.001)
#
def livePlot(fid):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    def animate(i):
        data = open(fid, "r").read()
        lines = data.split("\n")

        xT = []
        yT = []

        for line in lines:
            if len(line) > 1:
                x, y = line.split(",")
                xT.append(x)
                yT.append(y)

            if len(xT) > 1500:
                xT.pop(0)
                yT.pop(0)
        
        ax1.clear()
        ax1.plot(xT, yT)

    aniPlot = animation.FuncAnimation(fig, animate, interval=1)
    plt.show()
#
if __name__ == "__main__":
    # ser = readSerial("COM6", 115200)

    path = checkFolder()
    fid = checkFile(path)
    # readData(ser, fid)

    generationData = Thread(target=generateData, args=(fid,))
    generationData.start()

    livePlot(fid)

    generationData.join()