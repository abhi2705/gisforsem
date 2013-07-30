# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# DBSCAN Sandbox with matricies from the ENVI file

# <headingcell level=2>

# Step 1: Import in the files and turn them into matricies

# <headingcell level=3>

# Import in the Libraries

# <codecell>

import osgeo.gdal
import struct, numpy, pylab

# <headingcell level=3>

# Import in the files

# <rawcell>

# Import in the image file

# <codecell>

enviPath = '/home/jon/'
enviFile = 'test2'
enviPathFile = enviPath + enviFile #'/home/jon/test2'
imageDataset = osgeo.gdal.Open(enviPathFile)

# <rawcell>

# Import in the header file

# <codecell>

emsaPath = '/home/jon/'
emsaFile = 'test2.hdr'
emsaPathFile = emsaPath + emsaFile

# <headingcell level=3>

# Find out the diminisions of the file

# <codecell>

f = open(emsaPathFile , 'r')
samples = 'samples'
lines = 'lines'
bands = 'bands'

for line in f:
    if samples in line:
        #print line[10: ]
        sampleImageWidth = line[10: ]
    elif lines in line:
        #print line[8: ]
        sampleImageHeight = line[8: ]
    elif bands in line:
        #print line[8: ]
        sampleImageBands = line[8: ]
        
print 'sample width ',sampleImageWidth
print 'sample height ',sampleImageHeight
print 'sample bands ',sampleImageBands

# <rawcell>

# Convert the dimisions by string into integers

# <codecell>

sampleImageWidth = int(sampleImageWidth)

sampleImageHeight = int(sampleImageHeight)
                        
sampleImageBands = int(sampleImageBands)

# <headingcell level=3>

# SOMETHING WRONG HAPPENED IN ENVI, its actually 256, and the last 256 are blank

# <codecell>

sampleImageBands = 256

# <headingcell level=3>

# Based on the number of bands, find the high and low keV values for the bands

# <codecell>

kevBandWidth = 10.0/sampleImageBands

# <codecell>

bandRangeMatrix = [0]*sampleImageBands
for x in range(sampleImageBands):
    bandRangeMatrix[x] = kevBandWidth*x

# <headingcell level=3>

# Get the matricies of the bands for a location

# <rawcell>

# Location you are looking at on the image

# <codecell>

pixelWidth = 200
pixelHeight = 200

widthCordinate = 50
heightCordinate = 50

# <rawcell>

# The function to find the matricies for a spot

# <codecell>

matrixForAllBands = [0] * sampleImageBands

def enviMatrix(pixelX, pixelY, pixelWidth, pixelHeight):
    
    # Extract raw data
    band = imageDataset.GetRasterBand(bandNumber)
    
    #byteStringFunction
    byteString = band.ReadRaster(
    pixelX, pixelY, 
    pixelWidth, pixelHeight)
    
    # Convert to a matrix
    valueType = {osgeo.gdal.GDT_Byte: 'B', osgeo.gdal.GDT_UInt16: 'H'}[band.DataType]
    
    values = struct.unpack('%d%s' % (pixelWidth * pixelHeight, valueType), byteString)
    
    matrix = numpy.reshape(values, (pixelWidth, pixelHeight))
    
    
    #print 'this is the matrix in the enviMatrix()',' for band ',bandNumber
    matrixForAllBands[bandNumber] = matrix
    #print matrix

# <rawcell>

# the for loop to run the function

# <codecell>

counter = 0
bandVectorPlus = range(1,sampleImageBands)
for x in bandVectorPlus:
	bandNumber = x
	sampleEnviMatrix = enviMatrix(widthCordinate,heightCordinate,pixelWidth,pixelHeight)
        counter += 1

# <headingcell level=3>

# List of element values

# <codecell>

import numpy
atomicLookUp = numpy.array([ ['atomic number','element abr','kev low','kev hi'],
#OVERLAP
#Element 0
[5,'B',0.125,0.242], #overlap: 0.218 to 0.242 
#Element 1
[6,'C',0.218,0.337], #overlap: 0.218 to 0.242 , 0.332 to 0.337
#Element 2
[7,'N',0.332,0.452], #overlap: 0.332 to 0.337, 

#NO OVERLAP
#Element 3
[8,'O',0.464,0.587],
#Element 4
[9,'F',0.615,0.739],
#Element 5
[11,'Na',0.976,1.106],
#Element 6
[12,'Mg',1.188,1.32],
#Element 7
[13,'Al',1.419,1.554],
#Element 8
[14,'Si',1.671,1.809],

#overlap
[39,'Y',1.852,1.993], #overlap: 1.943 to 1.993
[15,'P',1.943,2.085], #overlap: 1.943 to 1.993, 
[40,'Zr',1.971,2.114],
[41,'Nb',2.094,2.238],
[42,'Mo',2.221,2.366],
[16,'S',2.235,2.381],
[43,'Tc',2.351,2.497],
[44,'Ru',2.484,2.633],
[17,'Cl',2.548,2.697],
[45,'Rh',2.622,2.772],
[46,'Pd',2.763,2.915],
[47,'Ag',2.908,3.061],
[48,'Cd',3.056,3.211],
[49,'In',3.209,3.365],
[19,'K',3.235,3.392],
[50,'Sn',3.365,3.523],

#gap in overlap
[51,'Sb',3.525,3.685],
[20,'Ca',3.611,3.772],
[52,'Te',3.688,3.851],
[53,'I',3.856,4.02],
[21,'Sc',4.008,4.173],
[55,'Cs',4.203,4.37],
[56,'Ba',4.382,4.551],
[22,'Ti',4.426,4.596],
[57,'La',4.565,4.737],
[58,'Ce',4.753,4.926],
[23,'V',4.865,5.04],
[24,'Cr',5.325,5.504],
[25,'Mn',5.807,5.991],
[26,'Fe',6.31,6.498],
[27,'Co',6.834,7.027],
[28,'Ni',7.379,7.577],
[72,'Hf',7.798,8],
[29,'Cu',7.946,8.15],
[73,'Ta',8.044,8.248],
[74,'W',8.295,8.501],
#
[30,'Zn',8.535,8.743],
[75,'Re',8.548,8.757],
#
[76,'Os',8.807,9.017],
[77,'Ir',9.069,9.282],
[31,'Ga',9.145,9.359],
[78,'Pt',9.335,9.55],
#
[79,'Au',9.605,9.822],
[32,'Ge',9.777,9.996],
[80,'Hg',9.879,10.099],

#elements beyond 10keV
[81,'Tl',10.158,10.38],
[33,'As',10.432,10.656],
[82,'Pb',10.44,10.664],
[83,'Bi',10.726,10.952],
[84,'Po',11.017,11.245],
[34,'Se',11.108,11.337],
[85,'At',11.312,11.542],
[35,'Br',11.807,12.042],
[37,'Rb',13.273, 13.518],
[38,'Sr',14.04,14.291] ])

# <rawcell>

# List of the Element Abriviations

# <codecell>

atomicLookUpLabelsNot = atomicLookUp[:,1]
atomicLookUpLabels = atomicLookUpLabelsNot[1:]

# <rawcell>

# List of the Element Low Values

# <codecell>

atomicLookUpLow = atomicLookUp[:,2]
atomicLookUpLowVTwo = atomicLookUpLow[1:]
atomicLookUpLowVThree = map(float, atomicLookUpLowVTwo)

# <rawcell>

# List of the Element High Values

# <codecell>

atomicLookUpHi = atomicLookUp[:,3]
atomicLookUpHiVTwo = atomicLookUpHi[1:]
atomicLookUpHiVThree = map(float, atomicLookUpHiVTwo)

# <headingcell level=2>

# Make an Array labeling the 512 bands based on their elements

# <codecell>

labels512 = [0]*256

for x in range(256):
    
#-----------------------------------------------------
    #Element B
    if bandRangeMatrix[x] >= atomicLookUpLowVThree[0] and bandRangeMatrix[x] <= atomicLookUpHiVThree[0]:
        labels512[x] = atomicLookUpLabels[0]
    #Element C
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[1] and bandRangeMatrix[x] <= atomicLookUpHiVThree[1]:
        labels512[x] = atomicLookUpLabels[1]
    #Overlap between B and C
    elif bandRangeMatrix[x] >= 0.218  and bandRangeMatrix[x] <= 0.242 :
        labels512[x] = 'B and C' 
    #Element N
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[2] and bandRangeMatrix[x] <= atomicLookUpHiVThree[2]:
        labels512[x] = atomicLookUpLabels[2]
    #Element C and N 
    elif bandRangeMatrix[x] >= 0.332 and bandRangeMatrix[x] <= 0.337:
        labels512[x] = 'C and N'
#-----------------------------------------------------

    
#-----------------------------------------------------
    #No overlap between keV levels but maybe the channel is shared
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[3] and bandRangeMatrix[x] <= atomicLookUpHiVThree[3]:
        labels512[x] = atomicLookUpLabels[3]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[4] and bandRangeMatrix[x] <= atomicLookUpHiVThree[4]:
        labels512[x] = atomicLookUpLabels[4]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[5] and bandRangeMatrix[x] <= atomicLookUpHiVThree[5]:
        labels512[x] = atomicLookUpLabels[5]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[6] and bandRangeMatrix[x] <= atomicLookUpHiVThree[6]:
        labels512[x] = atomicLookUpLabels[6]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[7] and bandRangeMatrix[x] <= atomicLookUpHiVThree[7]:
        labels512[x] = atomicLookUpLabels[7]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[8] and bandRangeMatrix[x] <= atomicLookUpHiVThree[8]:
        labels512[x] = atomicLookUpLabels[8]
#-----------------------------------------------------   
        
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[9] and bandRangeMatrix[x] <= atomicLookUpHiVThree[9]:
        labels512[x] = atomicLookUpLabels[9]
        
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[10] and bandRangeMatrix[x] <= atomicLookUpHiVThree[10]:
        labels512[x] = atomicLookUpLabels[10]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[11] and bandRangeMatrix[x] <= atomicLookUpHiVThree[11]:
        labels512[x] = atomicLookUpLabels[11]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[12] and bandRangeMatrix[x] <= atomicLookUpHiVThree[12]:
        labels512[x] = atomicLookUpLabels[12]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[13] and bandRangeMatrix[x] <= atomicLookUpHiVThree[13]:
        labels512[x] = atomicLookUpLabels[13]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[14] and bandRangeMatrix[x] <= atomicLookUpHiVThree[14]:
        labels512[x] = atomicLookUpLabels[14]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[15] and bandRangeMatrix[x] <= atomicLookUpHiVThree[15]:
        labels512[x] = atomicLookUpLabels[15]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[16] and bandRangeMatrix[x] <= atomicLookUpHiVThree[16]:
        labels512[x] = atomicLookUpLabels[16]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[17] and bandRangeMatrix[x] <= atomicLookUpHiVThree[17]:
        labels512[x] = atomicLookUpLabels[17]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[18] and bandRangeMatrix[x] <= atomicLookUpHiVThree[18]:
        labels512[x] = atomicLookUpLabels[18]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[19] and bandRangeMatrix[x] <= atomicLookUpHiVThree[19]:
        labels512[x] = atomicLookUpLabels[19]
        
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[20] and bandRangeMatrix[x] <= atomicLookUpHiVThree[20]:
        labels512[x] = atomicLookUpLabels[20]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[21] and bandRangeMatrix[x] <= atomicLookUpHiVThree[21]:
        labels512[x] = atomicLookUpLabels[21]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[22] and bandRangeMatrix[x] <= atomicLookUpHiVThree[22]:
        labels512[x] = atomicLookUpLabels[22]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[23] and bandRangeMatrix[x] <= atomicLookUpHiVThree[23]:
        labels512[x] = atomicLookUpLabels[23]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[24] and bandRangeMatrix[x] <= atomicLookUpHiVThree[24]:
        labels512[x] = atomicLookUpLabels[24]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[25] and bandRangeMatrix[x] <= atomicLookUpHiVThree[25]:
        labels512[x] = atomicLookUpLabels[25]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[26] and bandRangeMatrix[x] <= atomicLookUpHiVThree[26]:
        labels512[x] = atomicLookUpLabels[26]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[27] and bandRangeMatrix[x] <= atomicLookUpHiVThree[27]:
        labels512[x] = atomicLookUpLabels[27]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[28] and bandRangeMatrix[x] <= atomicLookUpHiVThree[28]:
        labels512[x] = atomicLookUpLabels[28]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[29] and bandRangeMatrix[x] <= atomicLookUpHiVThree[29]:
        labels512[x] = atomicLookUpLabels[29]
        
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[30] and bandRangeMatrix[x] <= atomicLookUpHiVThree[30]:
        labels512[x] = atomicLookUpLabels[30]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[31] and bandRangeMatrix[x] <= atomicLookUpHiVThree[31]:
        labels512[x] = atomicLookUpLabels[31]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[32] and bandRangeMatrix[x] <= atomicLookUpHiVThree[32]:
        labels512[x] = atomicLookUpLabels[32]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[33] and bandRangeMatrix[x] <= atomicLookUpHiVThree[33]:
        labels512[x] = atomicLookUpLabels[33]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[34] and bandRangeMatrix[x] <= atomicLookUpHiVThree[34]:
        labels512[x] = atomicLookUpLabels[34]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[35] and bandRangeMatrix[x] <= atomicLookUpHiVThree[35]:
        labels512[x] = atomicLookUpLabels[35]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[36] and bandRangeMatrix[x] <= atomicLookUpHiVThree[36]:
        labels512[x] = atomicLookUpLabels[36]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[37] and bandRangeMatrix[x] <= atomicLookUpHiVThree[37]:
        labels512[x] = atomicLookUpLabels[37]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[38] and bandRangeMatrix[x] <= atomicLookUpHiVThree[38]:
        labels512[x] = atomicLookUpLabels[38]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[39] and bandRangeMatrix[x] <= atomicLookUpHiVThree[39]:
        labels512[x] = atomicLookUpLabels[39]
        
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[40] and bandRangeMatrix[x] <= atomicLookUpHiVThree[40]:
        labels512[x] = atomicLookUpLabels[40]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[41] and bandRangeMatrix[x] <= atomicLookUpHiVThree[41]:
        labels512[x] = atomicLookUpLabels[41]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[42] and bandRangeMatrix[x] <= atomicLookUpHiVThree[42]:
        labels512[x] = atomicLookUpLabels[42]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[43] and bandRangeMatrix[x] <= atomicLookUpHiVThree[43]:
        labels512[x] = atomicLookUpLabels[43]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[44] and bandRangeMatrix[x] <= atomicLookUpHiVThree[44]:
        labels512[x] = atomicLookUpLabels[44]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[45] and bandRangeMatrix[x] <= atomicLookUpHiVThree[45]:
        labels512[x] = atomicLookUpLabels[45]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[46] and bandRangeMatrix[x] <= atomicLookUpHiVThree[46]:
        labels512[x] = atomicLookUpLabels[46]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[47] and bandRangeMatrix[x] <= atomicLookUpHiVThree[47]:
        labels512[x] = atomicLookUpLabels[47]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[48] and bandRangeMatrix[x] <= atomicLookUpHiVThree[48]:
        labels512[x] = atomicLookUpLabels[48]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[49] and bandRangeMatrix[x] <= atomicLookUpHiVThree[49]:
        labels512[x] = atomicLookUpLabels[49]
        
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[50] and bandRangeMatrix[x] <= atomicLookUpHiVThree[50]:
        labels512[x] = atomicLookUpLabels[50]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[51] and bandRangeMatrix[x] <= atomicLookUpHiVThree[51]:
        labels512[x] = atomicLookUpLabels[51]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[52] and bandRangeMatrix[x] <= atomicLookUpHiVThree[52]:
        labels512[x] = atomicLookUpLabels[52]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[53] and bandRangeMatrix[x] <= atomicLookUpHiVThree[53]:
        labels512[x] = atomicLookUpLabels[53]
        
#---------------------------------------------------------
#Hopefully keV values greater then 10
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[54] and bandRangeMatrix[x] <= atomicLookUpHiVThree[54]:
        labels512[x] = atomicLookUpLabels[54]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[55] and bandRangeMatrix[x] <= atomicLookUpHiVThree[55]:
        labels512[x] = atomicLookUpLabels[55]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[56] and bandRangeMatrix[x] <= atomicLookUpHiVThree[56]:
        labels512[x] = atomicLookUpLabels[56]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[57] and bandRangeMatrix[x] <= atomicLookUpHiVThree[57]:
        labels512[x] = atomicLookUpLabels[57]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[58] and bandRangeMatrix[x] <= atomicLookUpHiVThree[58]:
        labels512[x] = atomicLookUpLabels[58]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[59] and bandRangeMatrix[x] <= atomicLookUpHiVThree[59]:
        labels512[x] = atomicLookUpLabels[59]
        
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[60] and bandRangeMatrix[x] <= atomicLookUpHiVThree[60]:
        labels512[x] = atomicLookUpLabels[60]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[61] and bandRangeMatrix[x] <= atomicLookUpHiVThree[61]:
        labels512[x] = atomicLookUpLabels[61]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[62] and bandRangeMatrix[x] <= atomicLookUpHiVThree[62]:
        labels512[x] = atomicLookUpLabels[62]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[63] and bandRangeMatrix[x] <= atomicLookUpHiVThree[63]:
        labels512[x] = atomicLookUpLabels[63]
#--------------------------------------------------------- 
        
    else:
        labels512[x] = 'BACKGROUND'

print 'List of Elements for the 256 of the 512 Bands'
print labels512 

# <headingcell level=2>

# Searching the Element List

# <codecell>

#list to search
ElementList = labels512
print ElementList

# <headingcell level=3>

# Search the list of elements

# <codecell>

#word to search
searchWord = atomicLookUpLabels

#a list of numbers for the length of searchWord
searchWordNumberList = len(atomicLookUpLabels)
searchWordNumberListV2 = range(searchWordNumberList)

#list to search
ElementList = labels512

#loop counter
loopCounter = 0

#search for multiple words, loop to search list
for word in ElementList:
    for searchWordNumber in searchWordNumberListV2:
        if word == searchWord[searchWordNumber]:
            #print searchWord[searchWordNumber] 
            #print ElementList.index(searchWord[searchWordNumber])
            #print loopCounter
            loopCounter += 1

# <codecell>

elementBMatrix = [0]
bBands =[4,5,6]
for x in bBands:
    elementBMatrix += matrixForAllBands[x]

elementCMatrix = [0]
cBands =[7,8]
for x in cBands:
    elementCMatrix += matrixForAllBands[x]

elementNMatrix = [0]
nBands =[9,10,11]
for x in nBands:
    elementNMatrix += matrixForAllBands[x]

elementOMatrix = [0]
oBands =[12,13,14,15]
for x in oBands:
    elementOMatrix += matrixForAllBands[x]

elementFMatrix = [0]
fBands =[16,17,18]
for x in fBands:
    elementFMatrix += matrixForAllBands[x]

elementNaMatrix = [0]
naBands =[25,26,27,28]
for x in naBands:
    elementNaMatrix += matrixForAllBands[x]

# <codecell>

from pylab import pcolor, show, colorbar, xticks, yticks, savefig, title, xlabel, ylabel

pcolor(elementBMatrix)
colorbar()
title("Element B")
xlabel("Width")
ylabel("Height")
show()

pcolor(elementCMatrix)
colorbar()
title("Element C")
show()

pcolor(elementNMatrix)
colorbar()
title("Element N")
show()

pcolor(elementOMatrix)
colorbar()
title("Element O")
show()

pcolor(elementFMatrix)
colorbar()
title("Element F")
show()

pcolor(elementNaMatrix)
colorbar()
title("Element Na")
show()

#pcolor(elementMgMatrix)
#colorbar()
#title("Element Mg")
#show()

#pcolor(elementAlMatrix)
#colorbar()
#title("Element Al")
#show()

#pcolor(elementFeMatrix)
#colorbar()
#title("Element Fe")
#show()

# <headingcell level=1>

# CONVERT rich quantities to categories

# <rawcell>

# Pull out bands by category range

# <codecell>

matrixColCounter = 0
matrixRowCounter = 0

elementNaMatrixCategory = numpy.random.random((200,200))

numberOfRows = range(0,200)
#rowOne = elementNaMatrix[0,:]
#rowTwo = elementNaMatrix[1,:]

for rowNumber in numberOfRows:
    matrixColCounter = 0
    rowImOn = elementNaMatrix[rowNumber,:]
    for col in rowImOn: 
        low = 0
        high = 10
        intervalWidth = high+1
        scalarList = range(0,27)
        for scalar in scalarList:
            rangeSet = range(low+scalar*intervalWidth+1,high+scalar*intervalWidth+1)
            if col in rangeSet:
                col = scalar
                elementNaMatrixCategory[rowNumber,matrixColCounter] = col
        matrixColCounter += 1
            
print elementNaMatrix
print ""
print ""
print elementNaMatrixCategory
print ""
print ""
print matrixColCounter
print matrixRowCounter

pcolor(elementNaMatrixCategory)
colorbar()
title("Element Na Category")
show()

# <headingcell level=3>

# pull out a layer with only one value

# <rawcell>

# Zero Layer

# <codecell>

matrixColCounter = 0
matrixRowCounter = 0

elementNaMatrixCategoryZero = numpy.random.random((200,200))

matrixCounter = 0
naMatrixZeroCordArray = [0]*50000

numberOfRows = range(0,200)
rowImOn = 0

for rowNumber in numberOfRows:
    matrixColCounter = 0
    rowImOn = elementNaMatrixCategory[rowNumber,:]
    for col in rowImOn: 
        if col == 0:
            elementNaMatrixCategoryZero[rowNumber,matrixColCounter] = 100
            arrayIndexNumber = matrixColCounter+rowNumber*200
            naMatrixZeroCordArray[arrayIndexNumber] = (matrixColCounter,rowNumber)
        else:
            elementNaMatrixCategoryZero[rowNumber,matrixColCounter] = 0
        matrixColCounter += 1
        matrixCounter += 1
        #print matrixCounter

print elementNaMatrixCategoryZero

#make the graph
pcolor(elementNaMatrixCategoryZero)
title("Element Na Category Zero")

#save the graph, has to be saved before the show()
from pylab import savefig
savefig("/home/jon/myplot.png")

#show the graph as a pop up
show()


print naMatrixZeroCordArray[1]
print naMatrixZeroCordArray[190:250]
print ''
print ''
print ''
naMatrixZeroCordArray[:] = (value for value in naMatrixZeroCordArray if value != 0)
#print naMatrixZeroCordArray

# <headingcell level=2>

# Cluster of new Array of Cordinates

# <rawcell>

# http://stackoverflow.com/questions/1157106/remove-all-occurences-of-a-value-from-a-python-list
# 
# http://glowingpython.blogspot.com/2012/04/k-means-clustering-with-scipy.html

# <codecell>

#import in libraries
from pylab import plot,show
from numpy import vstack,array
from numpy.random import rand
from scipy.cluster.vq import kmeans,vq

# data generation
data = vstack(naMatrixZeroCordArray)

# now with K = 3 (3 clusters)
centroids,_ = kmeans(data,3)
idx,_ = vq(data,centroids)

#make plot
plot(data[idx==0,0],data[idx==0,1],'ob',
     data[idx==1,0],data[idx==1,1],'or',
     data[idx==2,0],data[idx==2,1],'og') # third cluster points
plot(centroids[:,0],centroids[:,1],'sm',markersize=8)

#show plot
title("Element Na Category Zero Kmeans 3")
show()

# <headingcell level=2>

# Back to layers from cordinates

# <rawcell>

# Layer One

# <codecell>

matrixColCounter = 0
matrixRowCounter = 0

elementNaMatrixCategoryOne = numpy.random.random((200,200))

numberOfRows = range(0,200)
rowImOn = 0

for rowNumber in numberOfRows:
    matrixColCounter = 0
    rowImOn = elementNaMatrixCategory[rowNumber,:]
    for col in rowImOn: 
        if col == 1:
            elementNaMatrixCategoryOne[rowNumber,matrixColCounter] = col
        else:
            col = 0
            elementNaMatrixCategoryOne[rowNumber,matrixColCounter] = col
        matrixColCounter += 1

print elementNaMatrixCategoryOne

pcolor(elementNaMatrixCategoryOne)
colorbar()
title("Element Na Category One")
show()

# <rawcell>

# Layer Two

# <codecell>

matrixColCounter = 0
matrixRowCounter = 0

elementNaMatrixCategoryTwo = numpy.random.random((200,200))

numberOfRows = range(0,200)
rowImOn = 0

for rowNumber in numberOfRows:
    matrixColCounter = 0
    rowImOn = elementNaMatrixCategory[rowNumber,:]
    for col in rowImOn: 
        if col == 2:
            elementNaMatrixCategoryTwo[rowNumber,matrixColCounter] = 2
        else:
            elementNaMatrixCategoryTwo[rowNumber,matrixColCounter] = 0
        matrixColCounter += 1

print elementNaMatrixCategoryTwo

pcolor(elementNaMatrixCategoryTwo)
title("Element Na Category Two")
show()

# <rawcell>

# Layer Three

# <codecell>

matrixColCounter = 0
matrixRowCounter = 0

elementNaMatrixCategoryThree = numpy.random.random((200,200))

numberOfRows = range(0,200)
rowImOn = 0

for rowNumber in numberOfRows:
    matrixColCounter = 0
    rowImOn = elementNaMatrixCategory[rowNumber,:]
    for col in rowImOn: 
        if col == 3:
            elementNaMatrixCategoryThree[rowNumber,matrixColCounter] = 3
        else:
            elementNaMatrixCategoryThree[rowNumber,matrixColCounter] = 0
        matrixColCounter += 1

print elementNaMatrixCategoryThree

pcolor(elementNaMatrixCategoryThree)
title("Element Na Category Three")
show()

# <rawcell>

# Layer Four

# <codecell>

matrixColCounter = 0
matrixRowCounter = 0

elementNaMatrixCategoryFour = numpy.random.random((200,200))

numberOfRows = range(0,200)
rowImOn = 0

for rowNumber in numberOfRows:
    matrixColCounter = 0
    rowImOn = elementNaMatrixCategory[rowNumber,:]
    for col in rowImOn: 
        if col == 4:
            elementNaMatrixCategoryFour[rowNumber,matrixColCounter] = 4
        else:
            elementNaMatrixCategoryFour[rowNumber,matrixColCounter] = 0
        matrixColCounter += 1

print elementNaMatrixCategoryFour

pcolor(elementNaMatrixCategoryFour)
title("Element Na Category Four")
show()

# <rawcell>

# Layer Five

# <codecell>

matrixColCounter = 0
matrixRowCounter = 0

elementNaMatrixCategoryFive = numpy.random.random((200,200))

numberOfRows = range(0,200)
rowImOn = 0

for rowNumber in numberOfRows:
    matrixColCounter = 0
    rowImOn = elementNaMatrixCategory[rowNumber,:]
    for col in rowImOn: 
        if col == 5:
            elementNaMatrixCategoryFive[rowNumber,matrixColCounter] = 3
        else:
            elementNaMatrixCategoryFive[rowNumber,matrixColCounter] = 0
        matrixColCounter += 1

print elementNaMatrixCategoryFive

pcolor(elementNaMatrixCategoryFive)
title("Element Na Category Five")
show()

# <rawcell>

# Layer Six

# <codecell>

matrixColCounter = 0
matrixRowCounter = 0

elementNaMatrixCategorySix = numpy.random.random((200,200))

numberOfRows = range(0,200)
rowImOn = 0

for rowNumber in numberOfRows:
    matrixColCounter = 0
    rowImOn = elementNaMatrixCategory[rowNumber,:]
    for col in rowImOn: 
        if col >5:
            elementNaMatrixCategorySix[rowNumber,matrixColCounter] = 6
        else:
            elementNaMatrixCategorySix[rowNumber,matrixColCounter] = 0
        matrixColCounter += 1

print elementNaMatrixCategorySix

pcolor(elementNaMatrixCategorySix)
title("Element Na Category Greater then Five")
show()

# <headingcell level=3>

# rough draft without loops

# <codecell>

matrixColCounter = 0
matrixRowCounter = 0

elementNaMatrixCategory = numpy.random.random((200,200))

rowOne = elementNaMatrix[0,:]
rowTwo = elementNaMatrix[1,:]

numberOfRows = range(0,200)
rowImOn = 0

for rowNumber in numberOfRows:
    matrixColCounter = 0
    rowImOn = elementNaMatrix[rowNumber,:]
    for col in rowImOn:
        if col in range(0,6):
            col = 0
            elementNaMatrixCategory[rowNumber,matrixColCounter] = col
        elif col>= 6 and col <=10:
            col = 1
            elementNaMatrixCategory[rowNumber,matrixColCounter] = col
        elif col>= 11 and col <=15:
            col = 2
            elementNaMatrixCategory[rowNumber,matrixColCounter] = col
        elif col>= 16 and col <=20:
            col = 3
            elementNaMatrixCategory[rowNumber,matrixColCounter] = col
        elif col>= 21 and col <=25:
            col = 4
            elementNaMatrixCategory[rowNumber,matrixColCounter] = col
        elif col>= 26 and col <=30:
            col = 5
            elementNaMatrixCategory[rowNumber,matrixColCounter] = col
        elif col>= 31 and col <=35:
            col = 6
            elementNaMatrixCategory[rowNumber,matrixColCounter] = col
        elif col>= 36 and col <=40:
            col = 7
            elementNaMatrixCategory[rowNumber,matrixColCounter] = col
        elif col>= 41 and col <=50:
            col = 8
            elementNaMatrixCategory[rowNumber,matrixColCounter] = col
        elif col>= 51 and col <=55:
            col = 9
            elementNaMatrixCategory[rowNumber,matrixColCounter] = col
        else:
            col = 10
            elementNaMatrixCategory[rowNumber,matrixColCounter] = col
        matrixColCounter += 1
            
print elementNaMatrix
print ""
print ""
print elementNaMatrixCategory

pcolor(elementNaMatrixCategory)
colorbar()
title("Element Na Category")
show()

print ""
print ""
print matrixColCounter
print matrixRowCounter

# <headingcell level=1>

# EXPORT NUMPY ARRAY as RASTER

# <rawcell>

# from http://gis.stackexchange.com/questions/58517/python-gdal-save-array-as-raster-with-projection-from-other-file

# <codecell>

#convert matrix to array
elementNaArray = numpy.asarray(elementNaMatrix)

# <codecell>

pcolor(elementNaArray)
colorbar()
title("Element Na Array")
show()

# <rawcell>

# """Array > Raster
#     Save a raster from a C order array.
# 
#     :param array: ndarray
#     """

# <codecell>

from osgeo import gdal

def array_to_raster(arrayInput,rasterFolderInput,rasterFileInput):

    #LEVEL 0
    #where I am saving the file
    rasterFolder = rasterFolderInput #'/home/jon/'
    rasterFile = rasterFileInput #'elementNaMatrixV20.tiff'
    rasterFolderFile = rasterFolder + rasterFile
    dst_filename = rasterFolderFile

    # You need to get those values like you did.
    x_pixels = pixelWidth  # number of pixels in x
    y_pixels = pixelHeight  # number of pixels in y
    
    # size of the pixel
    PIXEL_SIZE = 2          
    
    # x_min & y_max are like the "top left" corner.
    x_min = 0  
    y_max = 0  
    
    wkt_projection = 'a projection in wkt that you got from other file'

    #LEVEL 1 of 4
    driver = gdal.GetDriverByName('GTiff')

    #LEVEL 2 of 4
    dataset = driver.Create(
        dst_filename,
        x_pixels,
        y_pixels,
        1,
        gdal.GDT_Float32) 

    #LEVEL 3 of 4
    dataset.SetGeoTransform((
        x_min,    # 0
        PIXEL_SIZE,  # 1
        0,                      # 2
        y_max,    # 3
        0,                      # 4
        -PIXEL_SIZE))  

    #LEVEL 4 of 4
    dataset.SetProjection(wkt_projection)
    dataset.GetRasterBand(1).WriteArray(arrayInput)
    
    # Write to disk.
    dataset.FlushCache() 
    
    #If you need to return, 
    #remenber to return  also the dataset 
    #because the band don`t live without dataset.
    return dataset, dataset.GetRasterBand(1)  

array_to_raster(elementNaArray,'/home/jon/','elementNaMatrixV20.tiff')

# <headingcell level=2>

# Import in the exported TIFF

# <rawcell>

# http://www.gis.usu.edu/~chrisg/python/2008/os5_slides.pdf

# <codecell>

import gdal
from gdalconst import *

rasterFolder = '/home/jon/'
rasterFile = 'elementNaMatrixV20.tiff'
rasterFolderFile = rasterFolder + rasterFile
#savedRaster = osgeo.gdal.Open(rasterFolderFile)
savedRasterDataset = gdal.Open(rasterFolderFile,GA_ReadOnly)

cols = savedRasterDataset.RasterXSize
rows = savedRasterDataset.RasterYSize
bandCount = savedRasterDataset.RasterCount

band = savedRasterDataset.GetRasterBand(1)

xOffset = 0
yOffset = 0

#clear earlier results
savedRasterDatasetArray = [0]
savedRasterDatasetPixel = [0]

savedRasterDatasetArray = band.ReadAsArray(xOffset,yOffset,1,1)
savedRasterDatasetPixel = data[0,0]

print cols
print rows
print bandCount
print band
print savedRasterDatasetArray

#Error Message, says only cordinate 0,0 has info. yet says it has 200 cols and 200 rows
print savedRasterDatasetPixel

# <codecell>


