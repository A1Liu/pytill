import os #Functions to handle operating system

print(__file__)#__file__ is a constant that has the location of this script
print(os.getcwd()) #gets current working directory
print(os.path.realpath(__file__))#gets the directory of the file
print(os.path.abspath(__file__))#does the same thing as above
os.chdir(os.path.dirname(os.path.realpath(__file__)))#os.chdir changes the directory to the one specified, and os.path.dirname gets the name of the directory that the file is in.
print(os.getcwd())
# some interesting stuff with files and directories
thispath = os.getcwd() #path of an example files
newpath = os.path.join(thispath,'newFolder') #Creates the directory for a new folder in the current working directory
if not os.path.exists(newpath): #checks if path exists
    print("made a new folder!")
    os.makedirs(newpath) #creates path if it doesn't exist
else:
    print("Folder already exists!")

#directory is a pre-formatted directory string, localdir is a tuple, and name is the name of the file/folder
def createPath(dir_name, localdir, name = ""):
    for item in localdir:
        dir_name = os.path.join(dir_name,item)
    newpath = os.path.join(newpath,name)
    return newpath

def checkExist(dir_name):
    return os.path.exists(dir_name)

def createFile(name, dir_name, *content):#content is by line
    newpath = createPath(dir_name, name)
    if not os.path.exists(newpath):
        file = open(newpath, "w+")
        file.write(str(name) + "\n")
        for item in content:
            file.write(str(item) + "\n")
        file.close()
        return True
    else:
        return False
