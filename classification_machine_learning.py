import h5py
import matplotlib.pyplot as plt
import pandas as pd #ick, pandas.  But, you younglings will probably want to use this
import numpy as np
import os, sys

#inPath = sys.argv[-1]
#hdfFile = h5py.File( inPath, 'r' )
hdfFile = h5py.File('pasive_manualclassification_condensed2.h5', 'r')

#ok, we've loaded the hdf file, now we need to read in the values. 
#because of the way that the hdf file is structured, I don't think there's an easy way to do this in pandas
#so, this is gonna be a multistep process, we'll shove the data into a dict
particleTable = {}

print( 'Reading  hdf5 file' )
#we're going to loop over the keys in a sorta dumb way, so I can print out a progress bar
hdfKeys = list( hdfFile.keys() )
N = len( hdfKeys )
#TODO change this range back to everything once testing is concluded
for i in range(len( hdfKeys ) ):
    key = hdfKeys[i] 
    dset = hdfFile[key]

    #filter out conical and embryonic graupel
    #these are numbers 3 and 4 (i.e >2)
    #"for each value in this dataset, if the classification is greater than 2, forget it and move on" -- Filter for values greater than 2
    #for user, value in dset.attrs['classifications']:
    #    if value > 2:
    #        dset.attrs['classifications'][i] = np.nan
            
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
#the first number in these is the user ID of the person doing the classification, the second is the classification index
#you can convert the numerical classification into the letter classification using the classification header
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

#checking what values are included in the classifications
#print(particleTable['classifications'])

