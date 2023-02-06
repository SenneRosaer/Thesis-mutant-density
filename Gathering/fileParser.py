from typing import List
import os
import sys
import fnmatch

def findJavaFiles(sourcePath: str) -> List[str]:
    # Get the file list
    if not os.path.isdir(sourcePath):
        print("Source path must be a directory.")
        sys.exit(5)

    fileList = list()
    print("Searching for Java files... ", end="\r")
    for root, dirnames, filenames in os.walk(sourcePath):
        for filename in fnmatch.filter(filenames, "*.java"):
            fileList.append(os.path.join(root, filename))
        print("Searching for Java files... {} found.".format(len(fileList)), end="\r")

    if len(fileList) == 0:
        print("No Java files found in provided source path.")
        sys.exit(6)

    return fileList

def findPythonFiles(sourcePath: str) -> List[str]:
    # Get the file list
    if not os.path.isdir(sourcePath):
        print("Source path must be a directory.")
        sys.exit(5)

    fileList = list()
    print("Searching for Python files... ", end="\r")
    for root, dirnames, filenames in os.walk(sourcePath):
        if "/venv/" not in root and "/build/" not in root:
            for filename in fnmatch.filter(filenames, "*.py"):
                fileList.append(os.path.join(root, filename))
            print("Searching for Python files... {} found.".format(len(fileList)), end="\r")

    if len(fileList) == 0:
        print("No Python files found in provided source path.")
        sys.exit(6)

    return fileList


def findCppFiles(sourcePath: str) -> List[str]:
    # Get the file list
    if not os.path.isdir(sourcePath):
        print("Source path must be a directory.")
        sys.exit(5)

    fileList = list()
    print("Searching for C++ files... ", end="\r")
    for root, dirnames, filenames in os.walk(sourcePath):
        for filename in fnmatch.filter(filenames, "*.cpp"):
            fileList.append(os.path.join(root, filename))
        for filename in fnmatch.filter(filenames, "*.h"):
            fileList.append(os.path.join(root, filename))
        for filename in fnmatch.filter(filenames, "*.hpp"):
            fileList.append(os.path.join(root, filename))
        print("Searching for C++ files... {} found.".format(len(fileList)), end="\r")

    if len(fileList) == 0:
        print("No C++ files found in provided source path.")
        sys.exit(6)

    return fileList