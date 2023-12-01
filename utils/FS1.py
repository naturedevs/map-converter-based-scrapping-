import os
import zipfile

class FS:
    def getPK3Package(packageName):
        # return zipfile.ZipFile(os.path.dirname(os.path.abspath(__file__)) + "/../../" + packageName + ".pk3")
        return zipfile.ZipFile(packageName, 'r')

    def getExecDir():
        return os.path.dirname(os.path.abspath(__file__)) + "/../.."

    def isDir(path):
        return os.path.isdir(path)

    def isFile(path):
        return os.path.isFile(path)