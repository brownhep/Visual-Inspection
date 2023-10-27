infolder = "C:\\Users\\espencer\\Documents\\AlibavaGUI\\"
#outfolder = "S:\\VisualInspection\\2S\\34350_012_2-S_MAIN0\\FrontNew\\"
x=26
y=32
offset=7489
prefix = "Run062322C0_Irrad_2S_IS_38874_011_HiStat_Ann2_Run2_"
outprefix = "Run062422C1_Irrad_2S_IS_38875_004_HiStat_Ann3"
outputfile = "rename.bat"

f = open(outputfile, "w")

count = 0
for i in range(x*y):
        count +=1
        old_name = infolder + prefix + str(offset+i) + ".PNG"
        #new_name = infolder + prefix + str(count) + ".png"
        new_name = outprefix + str(count) + ".png"
        command = "rename \"" + old_name + "\" \"" + new_name + "\"\n"
        f.write (command)

f.close()