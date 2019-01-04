import os

join = os.path.join

#directory is a pre-formatted directory string, localdir is a tuple, and name is the name of the file/folder
def createPath(dir, localdir, name = ""):
    newpath = dir
    for item in localdir:
        newpath = join(newpath,item)
    newpath = join(newpath,name)
    return newpath

def createFile(name, dir, *content):#content is by line
    if not (isinstance(name, str) and name):
        raise TypeError("Name must be a non-empty string!")
    newpath = join(dir, name)
    if not os.path.exists(newpath):
        file = open(newpath, "w+")
        for item in content:
            file.write(str(item) + "\n")
        file.close()
        return True
    else:
        return False
