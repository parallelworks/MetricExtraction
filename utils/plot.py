
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sys
import warnings

warnings.filterwarnings('ignore')

infile=sys.argv[1]

header = np.genfromtxt(infile, delimiter=',', names=True).dtype.names
data = np.genfromtxt(infile, delimiter=',', skip_header=1)

x=data[:,0]
y=data[:,1]

plt.figure(figsize=(10,6))
plt.plot(x, y)

locs,labels = plt.yticks()
plt.yticks(locs, map(lambda x: "%g" % x, locs))

plt.xlabel('Point')
plt.ylabel(header[1])
plt.title(infile.replace(".csv","").replace("plot_","")+' Plot')
plt.grid(True)
plt.savefig(infile.replace(".csv","")+".png")

