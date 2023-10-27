import numpy as np
import matplotlib.pyplot as plt
import os
import linecache


def ReadFile(pairDataFile, pairDataFolder):
    pairDataFiles = pairDataFolder + "/" + pairDataFile
    # print pairDataFiles
    x = []
    y = []
    pos = []
    i_avg = []
    bright = []
    i7 = []
    picdata = []

    if "Defects.txt" in pairDataFile:
        with open(pairDataFiles, "r") as dut:
            # print pairDataFiles
            txtLines = [line for line in dut]
            print("First line:", txtLines[0])
            idx = [i for i, line in enumerate(txtLines) if "0.0" in line][0]
            headers = txtLines[idx - 1].split('\t')
            data = txtLines[idx:]
            print(idx, headers, data[0])
            for line in data:
                words = line.split()
                # print (words)
                x.append(float(words[0]))
                y.append(float(words[1]))
                pos.append(float(words[2]))
                i_avg.append(float(words[5]))
                bright.append(float(words[7]))
                i7.append(float(words[15]))
                linedata = []
                for i in range(5,28):
                    linedata.append(float(words[i]))
                picdata.append(linedata)

    return x, y, pos, i_avg, i7, picdata


def list_files(dir):
    files = []
    for obj in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, obj)):
            files.append(obj)
    return files


def list_dir(dir):
    dirs = []
    for obj in os.listdir(dir):
        if os.path.isdir(os.path.join(dir, obj)):
            dirs.append(obj)
    return dirs


badfiles = []

for type in list_dir("S:\PreProduction\Visual Inspection"):
    sensors = []
    typedir = os.path.join("S:\PreProduction\Visual Inspection", type)
    print(type)
    #print (cumuldata)
    if type == "2S":
        x_pic = 26
        y_pic = 32
    elif type == "PSS":
        x_pic = 13
        y_pic = 33
    cumuldata = [[[[] for k in range(24)] for j in range(3*y_pic)] for i in range(3*x_pic)]
    for batch in list_dir(typedir):
        print(batch)
        batchdir = os.path.join(typedir, batch)
        if int(batch) > 35000:
            for sensor in list_dir(batchdir):
                print(sensor)
                sensors.append(sensor)
                sensordir = os.path.join(batchdir, sensor)
                for dates in list_dir(sensordir):
                    print(dates)
                    datesdir = os.path.join(sensordir, dates)
                    for files in list_files(datesdir):
                        if "Defects.txt" in files:
                            x, y, pos, i_avg, i7, picdata = ReadFile(files, datesdir)
                            # multiplied = [number * 2 for number in numbers]
                            loc_x = [3 * x0 + int((pos0-1) / 3) for x0, pos0 in zip(x, pos)]
                            loc_y = [3 * y0 + 2 - (pos0 + 2) % 3 for y0, pos0 in zip(y, pos)]
                            for i in range(len(picdata)):
                                #print (int(loc_x[i]), int(loc_y[i]), len(picdata), picdata[i])
                                for j in range(23):
                                    cumuldata[int(loc_x[i])][int(loc_y[i])][j].append(picdata[i][j])
                                    #print (picdata[i][j])
                                    #cumuldata[0,2,0].append(picdata[i][j])
                            print("Found Defects.txt: ", batch)
                            #print(x, y, pos, i_avg)
                            #for j in range(100):
                            #    print(j, x[j], y[j], loc_x[j], loc_y[j], i_avg[j], i7[j])
                            # print(loc_x[1], loc_y[1], i_avg[1])
                            plt.clf()
                            plt.hist2d(loc_x, loc_y, bins=(3*x_pic, 3*y_pic), cmap=plt.cm.jet, weights=i_avg)
                            plt.colorbar()
                            plt.savefig("S:\PreProduction\Visual Inspection\Plots\\" + batch + "_" + sensor + "_int.png")
                            plt.clf()
                            plt.hist2d(loc_x, loc_y, bins=(3*x_pic, 3*y_pic), cmap=plt.cm.jet, weights=np.log(i7))
                            plt.colorbar()
                            plt.savefig("S:\PreProduction\Visual Inspection\Plots\\"+sensor+"_defect.png")

    f = open("S:\PreProduction\Visual Inspection\cumul2_" + type + ".txt", "w")
    f.write("x\ty\tvar")
    for sns in sensors:
        f.write("\t" + sns)
    f.write("\n")
    for i in range(3 * x_pic):
        for j in range(3 * y_pic):
            for k in [10,11,12,13,19]:
                f.write(str(i) + "\t" + str(j) + "\t" + str(k))
                for l in cumuldata[i][j][k]:
                    f.write("\t" + str(l))
                f.write("\n")
    f.close()

    f = open("S:\PreProduction\Visual Inspection\cumul_"+type+".txt", "w")
    for i in range(3*x_pic):
        for j in range(3*y_pic):
            f.write(str(i) + "\t" + str(j))
            for k in [10,11,12,13,19]:
                f.write("\t"+str(np.mean(cumuldata[i][j][k]))+"\t"+str(np.std(cumuldata[i][j][k])))
                plt.clf()
                plt.hist(cumuldata[i][j][k], bins = 50)
                plt.savefig("S:\PreProduction\Visual Inspection\Plots\\"+str(k)+"_"+str(i)+"_"+str(j)+".png")
            f.write("\n")
    f.close()

print("DONE")
