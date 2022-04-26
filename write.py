a = open("test.py","w")
f = open("stop.txt", "r")
bool stop = false

while stop == false:
    a.write('write')
    f = open("stop.txt", "r")
    if int(f.read()) = 1:
        stop = true
    f.close()
    
a.close()
