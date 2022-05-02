


def printfile(filename):
    c = open(filename,'r')
    for lines in c.readlines():
        print(lines.removesuffix('\n'))    
    c.close()




def endcheck():
    work = bool(True)
    p = open("check.py", "r")
    
    q = int(p.readline())
    p.close()
    
    if q == int(1):
        work = False

    
    return work



def testing(filename):
    active = bool(True)
    print("1 for box 1, 2 for box 2")
    boxtype = int(input("select box type:"))
    print("--------------------------------------------------")
    if boxtype == 1:
        import IAC_data_logging
        
    elif boxtype == 2:
        import IAC_DAQ_MC2221


    

    else:
        print("input invalid restart please")
        dumb = input("press enter to end")



def decodesetup(file):
    l1 = list()
    c = open(file,'r')
    
    for lines in c.readlines():
        v = lines.removesuffix('\n')
        l1.append(v)
    c.close()
    return l1

def calibrate(filename):
    active = bool(True)
    print("1 for box 1, 2 for box 2")
    boxtype = int(input("select box type:"))
    print("--------------------------------------------------")
    if boxtype == 1:
        import mini_IAC_data_logging
    
        f = open(filename, 'w')
    
        while active:
            print("------------------------------------------------------------")
            Finput = input("Force applied:")
            #end condition
            if Finput == '':
                p = open("check.py", "w")
                p.write('1')
                p.close()
                break
            Finput = float(Finput)
            Deflectioninput = float(input("deflection mesured:"))
            #getvalue (currently calculates test values below)
            values = mini_IAC_data_logging.getvalues()
            tempv = values.split('%')
            v1, v2 = tempv[0], tempv[1]
            

            #string conversion and write
            s1 = str(Finput)
            s2 = str(v1)
            s3 = str(Deflectioninput)
            s4 = str(v2)
            f.write(s2+'%'+s1+'%'+s4+'%'+s3+'\n')

            #end
            active = endcheck()
        
    
        
    


    elif boxtype == 2:
        
        import mini_IAC_DAQ_MC2221
    
        f = open(filename, 'w')
    
        while active:
            print("------------------------------------------------------------")
            Finput = input("Force applied:")
            #end condition
            if Finput == '':
                p = open("check.py", "w")
                p.write('1')
                p.close()
                break
            Finput = float(Finput)
            Deflectioninput = float(input("deflection mesured:"))
            #getvalue (currently calculates test values below)
            values = mini_IAC_DAQ_MC2221.getvalues()
            tempv = values.split('%')
            v1, v2 = tempv[0], tempv[1]
            

            #string conversion and write
            s1 = str(Finput)
            s2 = str(v1)
            s3 = str(Deflectioninput)
            s4 = str(v2)
            f.write(s2+'%'+s1+'%'+s4+'%'+s3+'\n')

            #end
            active = endcheck()
        

    
def decodefindfunction(listq):
    import numpy as np
    import matplotlib.pyplot as plt
    import scipy as sc
    from scipy import stats

   
    length = len(listq)
    a = np.zeros((length, 4))
    for i in range(length):
        v = listq[i]
        x = v.split('%')
        a[i,0] = x[0]
        a[i,1] = x[1]
        a[i,2] = x[2]
        a[i,3] = x[3]

    X1 = a[:,0]
    y1 = a[:,1]
    X2 = a[:,2]
    y2 = a[:,3]

    
    qq = stats.linregress(X1,y1)
    a1 = qq.slope
    b1 = qq.intercept    
    dd = stats.linregress(X2,y2)
    a2 = dd.slope
    b2 = dd.intercept

    hh = list()
    hh.append(a1)
    hh.append(b1)
    hh.append(a2)
    hh.append(b2)
    return hh

    
 

    #to do
    #liniar aprox
    #write conversion program
    #convert
    #write output to file
    
        
def makevaluesreadable(functions, file):
    import numpy as np
    import matplotlib.pyplot as plt
    a1 = functions[0]
    b1 = functions[1]
    a2 = functions[2]
    b2 = functions[3]
    
    l1 = list()
    c = open(file,'r')
    
    for lines in c.readlines():
        v = lines.removesuffix('\n')
        t = v.split(' ')
        print(t)
        l1.append(t[1])
    c.close()
    

   
    length = len(l1)
    a = np.zeros((length,2))
    for i in range(length):
        v = l1[i]
        x = v.split(',')
        a[i,0] = x[0]
        a[i,1] = x[1]
    k = a[:,0]
    j = a[:,1]

    k = k * a1 + b1
    j = j * a2 + b2
    arr = np.column_stack((k,j))

    X1 = arr[:,0]
    y1 = arr[:,1]
    plt.plot(X1,y1,'bo')
    plt.ylabel('displacement')
    plt.xlabel('force')
    plt.legend(['sensor-input'])
    plt.title('sensor-input')
    plt.grid()
    plt.show(block=True)

    print(arr)
        

    

    

    
    





     
     
