import time
import mainfunctions



print("--------------------------------------------------")
print("1 for test, 2 for calibration,3 for decode")
activitytype = int(input("select mode:"))
print("--------------------------------------------------")
p = open("check.py", "w")
p.write('0')
p.close()


if activitytype == 1:     #actual test cycle
   mainfunctions.testing("test.txt")


    
elif activitytype == 2:    #calibration tests
    mainfunctions.calibrate("calibration.txt")
    mainfunctions.printfile("calibration.txt")

elif activitytype == 3:    #decode

    v = mainfunctions.decodesetup('calibration.txt')
    functionlist = mainfunctions.decodefindfunction(v)
    mainfunctions.makevaluesreadable(functionlist,"test.txt")
    dumb = input("press enter to end")

else:
    print("input invalid")
    dumb = input("press enter to end")
