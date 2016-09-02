#################################
#
# Script written by James L. McDonagh 2016 to cluster addresses based on Eastings and Northings data 
# The script expects as input a csv file of label, eastings and northings data in that order
# The following website can be used to find this data https://www.doogal.co.uk/UKPostcodes.php
#
#################################

import numpy as np
import pandas as pd
import math
import os
import sys
import datetime

# Print Instructions to screen
print '\n 2D Co-ordinate Clustering Based on Euclidean Distance\n'
print '\n\nInstructions\n'
print '\tCURRENTLY ONLY ABLE TO PRODUCE AN EVEN NUMBER OF CLUSTERS'
print '\tThis script expects as input a csv file of label, coordinate 1 and coordinate 2 data in that order.' 
print '\tThe following website can be used to find UK latitude longitude Easting Northing data https://www.doogal.co.uk/UKPostcodes.php.'
print '\tThis script identifies labels which are maximally separated from one another and stores them (referred to as nodes). All other coordinates are compared to these.'
print '\tThe other coordinates are grouped together based on which node they are closest to in the 2D space defined by your coordinate system. These points are then printed out in the groups created.'
print '\tThere is no account of travel distance just distances as the crow flys.\n' 
print '\n\nGlossary\n'
print '\t NODE(S)     - Labelled points (or a mid point in the case of an odd number of zones) which represent the maximum separation between coordinates'
print '\t COORDINATES - The input coordinates from a csv file'
print '\n\n'

# Get user input and read csv file input into pandas for processing and passing to np
fin = str(raw_input('Please enter the input file name containing the label Eastings and Northings in that order\n'))
if os.path.isfile(fin) :
        address = pd.read_csv(fin, sep=",")
else:
        sys.exit("ERROR: input file does not exist")

today = datetime.date.today()

odd = 0 # If areas required is odd we will use a mid point node for the last point
nzone = int(raw_input('How many zones do you want to create?\n'))
if nzone%2 != 0 :
	odd = 1
	nzone = nzone - 1

# Take the header (first row to be column titles and fill in any blanks with zero 
address = address.fillna(0) # replace the NA values with 0
header = address.columns.values # Ues the column headers as the descriptor labels
address.head()

# Give the pandas file to numpy array
RawArray = np.array(address)
Data = np.array(address)
entries = RawArray.shape[0]
                    # row     columns
DistArray = np.zeros((entries,entries))

print'\n\nThe Header array contains the following number of x and y entries ',header.shape
print'The Main Data array conatins the following number of x and y entries ', RawArray.shape[0], RawArray.shape[1]
print'We will now continue to cycle through ', entries, ' entries.\n\n'

# Take copy of the first column as the names of the input coordinates
names = RawArray[:,0]

# Make a backup copy of the distance array for use later (Memory inefficent)
Dist2Array = np.zeros((entries,entries))

# Initalise and calculate all separating distances
co1diff = 0.0
co1diff2 = 0.0
co2diff = 0.0
co2diff2 = 0.0
distance = 0.0

#
# NOTEs : DistArray is an upper triangle of the full matrix of distances. This is used to identify the maximum separations. Dist2Array is a full matrix of the separating distances for group assiging later
#

for i in range(0,entries) :
	for j in range(i,entries) :
		co1diff = RawArray[i,1] - RawArray[j,1]
		co1diff2 = co1diff * co1diff
		
		co2diff = RawArray[i,2] - RawArray[j,2]
		co2diff2 = co2diff * co2diff

		distance = math.sqrt(co1diff2 + co2diff2)

		DistArray[i,j] = distance 
		Dist2Array[i,j] = distance # note the index swapping on this line and the line below
		Dist2Array[j,i] = distance
		co1diff = 0.0
		co1diff2 = 0.0
		co2diff = 0.0
		co2diff2 = 0.0
		distance = 0.0

# Initialise a groups counter to make sure we collect the correct number of nodes
groupscounter = 0
izone = nzone/2
GroupsArray = np.zeros([nzone,entries], dtype=int)
pos1 = []
pos2 = []
nodelist = []

# Find all points which are maximally separated, note that more than one pair can be separated by the same distance at a time
while groupscounter < nzone - 1 :
	pos1,pos2 = np.where(DistArray==DistArray.max())
#
# NOTEs : As python is zero based and the array GroupsArray is initalised with zeros, if the coordinate defined in the zero index position of Data and RawArray was invloved in the largest separating
#         distance it would always fail the 2nd if condition. To resolve this 1 is added to every index then subtracted from each index after the nodes are assigned in the subsquent loops here.
#	
	for i in range(0,len(pos1)) :
		if groupscounter < nzone - 1 :
			if pos1[i]+1 not in GroupsArray[:,0] and pos2[i]+1 not in GroupsArray[:,0] :
				GroupsArray[groupscounter,0] = pos1[i]+1
				groupscounter = groupscounter + 1
				nodelist.append(pos1[i])
                		GroupsArray[groupscounter,0] = pos2[i]+1
				groupscounter = groupscounter + 1
				nodelist.append(pos2[i])
			DistArray[pos1[i],pos2[i]] = 0.0

for i in range(0,nzone) :
	GroupsArray[i,0] = GroupsArray[i,0] - 1

# Cycle through entries to find which node the coordinates are closest to
loop = 0
dist = 0.0
group = -1
entry = -1
noupdate = 0
CountArray = np.zeros((len(nodelist),2), dtype=int)
for i in range(0,nzone) :
	CountArray[i,0] = nodelist[i]

for i in range(0,entries) :
	for j in range(0,len(nodelist)) :
		if i == nodelist[j] or i in nodelist :
	                noupdate = 1
		else :
			if loop == 0 :
				dist = Dist2Array[i,nodelist[j]]
				group = nodelist[j]
				entry = i
				loop = 1
			else :
				if Dist2Array[i,nodelist[j]] < dist :
	                                dist = Dist2Array[i,nodelist[j]]
        	                        group = nodelist[j]
                	                entry = i
	loop = 0
        if noupdate != 1 :
	        for x in range(0,len(nodelist)) :
		        if group == CountArray[x,0] :
			        CountArray[x,1] = CountArray[x,1] + 1
			        GroupsArray[x,CountArray[x,1]] = entry
        noupdate = 0
        

# Write the groups out to a file(s)
with open("Grouped.csv", "w") as fout :
	fout.write("{},Input file,{},Number of labelled entries,{},Number of zones required,{},\n".format(today, fin, entries, nzone))
	for i in range(0,nzone) :	
		fout.write("Zone,{},Label,{},Array Index,{}\n".format(i,RawArray[nodelist[i],0],nodelist[i]))
		for j in range(0, CountArray[i,1]+1) :
			fout.write("{},{},{}\n".format(RawArray[GroupsArray[i,j],0], RawArray[GroupsArray[i,j],1], RawArray[GroupsArray[i,j],2]))
fout.close()
print '\nScript complete outfile is named Grouped.csv. If this script is run in the same directory it will overwrite previous output\n'
