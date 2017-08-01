import data_IO
import sys

if len(sys.argv) < 2:
    print("Number of provided arguments: ", len(sys.argv) - 1)
    print("Usage: python test_tar.py  <direcory> ")
    sys.exit()

dirName = sys.argv[1]
data_IO.tarDirectory(dirName+".tar",dirName)