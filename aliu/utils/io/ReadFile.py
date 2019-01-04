def readFile(filename):
    file = open(filename, "r")
    text = file.read()
    file.close()
    return text
