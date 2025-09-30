import h5py
import matplotlib.pyplot as plt
import pandas as pd #ick, pandas.  But, you younglings will probably want to use this
import numpy as np
import os, sys


#inPath = sys.argv[-1]
#hdfFile = h5py.File( inPath, 'r' )
hdfFile = h5py.File('pasive_manualclassification_condensed.h5', 'r')

#ok, we've loaded the hdf file, now we need to read in the values. 
#because of the way that the hdf file is structured, I don't think there's an easy way to do this in pandas
#so, this is gonna be a multistep process, we'll shove the data into a dict
particleTable = {}

print( 'Reading  hdf5 file' )
#we're going to loop over the keys in a sorta dumb way, so I can print out a progress bar
hdfKeys = list( hdfFile.keys() )
N = len( hdfKeys )
for i in range( len( hdfKeys ) ):
    key = hdfKeys[i] 
    dset = hdfFile[key]

    for attr in dset.attrs:
        if not attr in particleTable:
            #we need to initiate the value here
            particleTable[ attr ] = []
        particleTable[ attr ].append( dset.attrs[attr] )
    
    print ('%4i/%i '%(i,N), end='\r')

#there were a bunch of values stored in the attrs of the hdf5 file
#we should have the number number of values in each header, 
#but the code above doesn't require that, so lets check
for key in particleTable:
    print( key.ljust(15), len( particleTable[key]) )

#now, we'd like to get the classifications out in particular, 
#they're stored a little oddly
# [array([[3195,    0],
#         [3225,    2],
#         [3194,    1]]),
#  array([[3195,    0]]),
#  array([[3195,    0],
#         [3225,    0],
#         [3194,    0]]),
#  array([[3195,    2],
#         [3194,    0],
#         [3225,    2]]),
#  array([[3195,    0]]),
#  array([[3195,    0]]),
#  array([[3195,    0],
#         [3194,    0],
#         [3225,    0]]),
#  array([[3195,    0]]),
#the first number in these is the user ID of the person doing the classification
#the second is the classification index
#you can convert the numerical classification into the letter classification 
#using the classification header
# In [11]: particleTable['classification_header'][0]
# Out[11]: array(['s', 'b', 'i', 'g', 'e', 'h', 'w', 'u'], dtype=object)

#lets go through the table and count how many of each classification we got
print( 'The following classifications were issued')
classificationCounts = {}
for classification in particleTable['classifications']:
    for user, value in classification:
        if not value in classificationCounts:
            classificationCounts[value] = 0
        classificationCounts[value] += 1

classificationHeader = particleTable['classification_header'][0]
for key in classificationCounts:
    print( '%s %5i'%(classificationHeader[key], classificationCounts[key]) )

#lets get a list of the 'bright_count' for all particles which have a majority classification of 0 (snow)
print ('Finding "bright_count" values for snow' )
#empty list to store each bright count in
bright_count = []
#empty list to store each Bright_avg in 
brightAvg = []
#empty list to store each Bright_max in
brightMax = []
#empty list to store each Bright_median in
brightMedian = []
for i in range( len( particleTable['classifications'] ) ):
    print ('%4i/%i '%(i,N), end='\r')
    #check to see what the dominant classification is
    Ntype  = 0 
    Ntotal = 0
    for user, value in particleTable['classifications'][i]:
        Ntotal += 1
        if value == 0: # 0-snow, 1-broken, 2-ice, 3-conical groupel, 4-embryonic graupel
            Ntype += 1
    #is this particle snow?
    if Ntype > Ntotal/2:
        bright_count.append( particleTable['Bright_count'][i] )
        brightAvg.append( particleTable['Bright_avg'][i])
        brightMax.append( particleTable['Bright_max'][i])
        brightMedian.append( particleTable['Bright_median'][i])

brightCountStd = [int(x) for x in bright_count]
#print(brightCountStd)
#these are the first ten particle bright counts [391, 2939, 257, 1147, 1107, 505, 607, 525, 750, 748]
#corresponding "x" value of the file----------->[1, 2, 4, 5, 6, 7, 8, 9, 10, 11]

#calculate the average of the brightAvg, brightMax, and brightMedian for the selected classification
meanBrightAvg = np.mean(brightAvg)
meanBrightMax = np.mean(brightMax)
meanBrightMedian = np.mean(brightMedian)
print("The mean average bright count for all counts of this classification is: ", meanBrightAvg)
print("The mean median bright count for all counts of this classification is: ", meanBrightMedian)
print("The mean maximum bright count for all counts of this classification is: ", meanBrightMax)

#this section finds statistics for one specific image
x = 1 
#print(particleTable['Bright_count'][x])
#print("x = ", particleTable['x'][x])
#print("y = ", particleTable['y'][x])
#print("z = ", particleTable['z'][x])
#print("T = ", particleTable['T'][x])
#print("RH = ", particleTable['RH'][x])
#print("Max Bright = ", particleTable['Bright_max'][x])
#print("Avg Bright = ", particleTable['Bright_avg'][x])
#print("Med Bright = ", particleTable['Bright_median'][x])

#make a pandas series of the bright count list so that summary statistics can be applied
bright_count_series = pd.Series(bright_count)
print(bright_count_series.describe())

#histogram and boxplot to summarize statistics
fig,ax = plt.subplots(2,1)
ax[0].hist( bright_count, bins=25, range=(0,10000))#, density=True )
ax[0].set_xlim(0, 10000)
ax[0].set_xlabel( 'Bright Count' )
ax[0].set_ylabel( 'Number of Pixels')
ax[1].boxplot(bright_count, vert=False, showfliers=False)
ax[1].set_xlim(0, 10000)
plt.tight_layout()
plt.show()
