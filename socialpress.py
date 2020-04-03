import pathlib
import re
import sys
import os
import os.path
import time
if (len(sys.argv)!=3):
    print("Invalid argument count - " + str(len(sys.argv)) + "!=3")
    sys.exit()
if (sys.argv[1]=="compress"):
    p = str(pathlib.Path(__file__).parent.absolute())
    path = sys.argv[2]
    def loadOccurences():
        with open(p+'\\ocurrences.spd', 'r', encoding="ISO-8859-1") as file:
            stri = file.read()
            return [stri[i:i+10] for i in range(0, len(stri), 10)]
    print("Loading ocurrences..")
    ocurrences = loadOccurences()
    print(ocurrences)
    print("DONE")
    def loadFile(filepath):
        with open(filepath, 'r', encoding="ISO-8859-1") as file:
            stri = file.read()
            chunks = [stri[i:i+10] for i in range(0, len(stri), 10)]
            return chunks
    print("Loading file data..")
    fileData = loadFile(path)
    print(fileData)
    print("DONE")
    print("Appending not featured blocks to occurences..")
    newBlocks = []
    with open(p+'\\ocurrences.spd', 'a', encoding="ISO-8859-1") as file:
        for i in range(len(fileData)):
            block = fileData[i]
            print(str(i/len(fileData)*100)+"%")
            if (not block in ocurrences):
                file.write(block)
                newBlocks.append(block)
    print("DONE")
    table = ocurrences + newBlocks
    print("Writing compressed data to temporary file..")
    with open(path.split("\\")[len(path.split("\\"))-1]+'.spt', 'w', encoding="ISO-8859-1") as file:
        if (not len(fileData[len(fileData)-1])<10):
            for j in range(len(fileData)):
                item = fileData[j]
                print(str(j/len(fileData)*100)+"%")
                file.write(str(table.index(item))+",")
            print("DONE")
        else:
            print("DONE")
            print("Writing extra block to temporary block file..")
            for j in range(len(fileData)-1):
                item = fileData[j]
                print(str(j/(len(fileData)-1)*100)+"%")
                file.write(str(table.index(item))+",")
                with open(path.split("\\")[len(path.split("\\"))-1]+'.spb', 'w', encoding="ISO-8859-1") as fileb:
                    fileb.write(fileData[len(fileData)-1])
            print("DONE")
    print("Calling 7z to lzma2 compress the file(s)..")
    if (not len(fileData[len(fileData)-1])<10):
        cmd = str(p+"\\7z\\7z"+' a "'+path.split("\\")[len(path.split("\\"))-1]+'.7z" "'+path.split("\\")[len(path.split("\\"))-1]+'.spt"')
    else:
        cmd = str(p+"\\7z\\7z"+' a "'+path.split("\\")[len(path.split("\\"))-1]+'.7z" "'+path.split("\\")[len(path.split("\\"))-1]+'.spt" "' + path.split("\\")[len(path.split("\\"))-1]+'.spb"')
    os.popen(cmd)
    n = 0
    while not os.path.exists(path.split("\\")[len(path.split("\\"))-1]+'.7z'):
        time.sleep(1)
        n+=1
        if (n>=60*60):
            print("FAILED")
            sys.exit(0)
    print("DONE")
    print("Renaming file ending to .sp")
    os.rename(path+'.7z',path+'.sp')
    print("DONE")
    print("Deleting temporary files..")
    os.remove(path+'.spt')
    os.remove(path+'.spb')
    print("DONE")
    print("Deleting original file..")
    os.remove(path)
    print("DONE")
elif (sys.argv[1]=="decompress"):
    p = str(pathlib.Path(__file__).parent.absolute())
    path = sys.argv[2]
    print("Renaming file ending to .7z..")
    os.rename(path,".".join(path.split(".")[:-1])+'.7z')
    print("DONE")
    print("Calling 7z to unpack the 7z file..")
    time.sleep(5)
    cmd = str(p+"\\7z\\7z"+' e "'+".".join(path.split(".")[:-1])+'.7z"')
    os.popen(cmd)
    print("DONE")
    print("Loading data from temp file")
    n = 0
    while not os.path.exists(path.split('.sp')[0]+".spt"):
        time.sleep(1)
        n+=1
        if (n>=60*60):
            print("FAILED")
            sys.exit(0)
    toMatch = []
    with open(path.split('.sp')[0]+".spt", 'r', encoding="ISO-8859-1") as file:
        toMatch = file.read().split(",")[:-1]
    print("DONE")
    def loadOccurences():
        with open(p+'\\ocurrences.spd', 'r', encoding="ISO-8859-1") as file:
            stri = file.read()
            return [stri[i:i+10] for i in range(0, len(stri), 10)]
    print("Loading ocurrences..")
    ocurrences = loadOccurences()
    print(ocurrences)
    print("DONE")
    print("Writing original data to file..")
    with open(path.split(".sp")[0], 'w', encoding="ISO-8859-1") as file:
        for identification in toMatch:
            file.write(ocurrences[int(identification)])
        with open(path.split(".sp")[0]+".spb", 'r', encoding="ISO-8859-1") as fileb:
            file.write(fileb.read())
    print("DONE")
    print("Deleting temporary files..")
    os.remove(path.split(".sp")[0]+'.spt')
    os.remove(path.split(".sp")[0]+'.spb')
    print("DONE")
    print("Renaming 7z file to sp")
    os.rename(path.split(".sp")[0]+'.7z',path.split(".sp")[0]+'.sp')
    print("DONE")