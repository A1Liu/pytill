import sys
PACKAGE_DIR = '/Users/aliu/code/python/packages/'

def add_local(*packages):
    for package in packages:
        sys.path.insert(0,PACKAGE_DIR+package)
