# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Goals: Look at an image, save its 512 bands, sum the bands by element, save images of the elements

# <headingcell level=3>

# Import in the libraries

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

# <rawcell>

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
    
    
    print 'this is the matrix in the enviMatrix()',' for band ',bandNumber
    matrixForAllBands[bandNumber] = matrix
    print matrix

# <rawcell>

# the for loop to run the function

# <codecell>

counter = 0
bandVectorPlus = range(1,sampleImageBands)
for x in bandVectorPlus:
	bandNumber = x
	sampleEnviMatrix = enviMatrix(widthCordinate,heightCordinate,pixelWidth,pixelHeight)
        counter += 1

# <codecell>

print matrixForAllBands

# <headingcell level=3>

# List of element values

# <codecell>

import numpy
atomicLookUp = numpy.array([ ['atomic number','element abr','kev low','kev hi'],
[5,'B',0.125,0.242],
[6,'C',0.218,0.337],
[7,'N',0.332,0.452],
[8,'O',0.464,0.587],
[9,'F',0.615,0.739],
[11,'Na',0.976,1.106],
[12,'Mg',1.188,1.32],
[13,'Al',1.419,1.554],
[14,'Si',1.671,1.809],
[39,'Y',1.852,1.993],
[15,'P',1.943,2.085],
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
[30,'Zn',8.535,8.743],
[75,'Re',8.548,8.757],
[76,'Os',8.807,9.017],
[77,'Ir',9.069,9.282],
[31,'Ga',9.145,9.359],
[78,'Pt',9.335,9.55],
[79,'Au',9.605,9.822],
[32,'Ge',9.777,9.996],
[80,'Hg',9.879,10.099],
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

# <headingcell level=3>

# Make an Array labeling the 512 bands based on their elements

# <codecell>

labels512 = [0]*512

for x in range(512):
    if bandRangeMatrix[x] >= atomicLookUpLowVThree[0] and bandRangeMatrix[x] <= atomicLookUpHiVThree[0]:
        labels512[x] = atomicLookUpLabels[0]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[1] and bandRangeMatrix[x] <= atomicLookUpHiVThree[1]:
        labels512[x] = atomicLookUpLabels[1]
    elif bandRangeMatrix[x] >= atomicLookUpLowVThree[2] and bandRangeMatrix[x] <= atomicLookUpHiVThree[2]:
        labels512[x] = atomicLookUpLabels[2]
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
    
    else:
        labels512[x] = 'BACKGROUND'

print 'List of Elements for the 512 Bands'
print labels512 

# <headingcell level=3>

# Find out the index number for the element

# <codecell>

for x in atomicLookUpLabels:
    i = labels512.index(x)
    print 'for element ',x,' band is ',i

# <codecell>

i = labels512.index('Fe')
print 'for element ','Fe',' band is ',i

# <codecell>

i = labels512.index('Pt')
print i

# <codecell>

for element in labels512:
    for x in atomicLookUpLabels:
        zeroOne = element.find(x)
        if zeroOne == 0:
            print 'Here is ',x

# <headingcell level=3>

# Plot the Matricies.  AND save the plots as PNG or JPG

# <rawcell>

# PROBLEM: NOT saving the PLOT saving WHITE IMAGE

# <codecell>

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# <headingcell level=4>

# Show Map of Element B

# <codecell>

plt.clf()

elementBMatrix = [0]

bBands =[7,8,9,10,11,12]

for x in bBands:
    elementBMatrix += matrixForAllBands[x]

#elementBMatrix = matrixForAllBands[7]\
#+ matrixForAllBands[8]\
#+ matrixForAllBands[9]\
#+ matrixForAllBands[10]\
#+ matrixForAllBands[11]\
#+ matrixForAllBands[12]

img = plt.imshow(elementBMatrix)

plt.show()

print elementBMatrix

# <headingcell level=4>

# Show map of Element C

# <codecell>

plt.clf()
elementCMatrix = [0]

cBands =[13,14,15,16,17]

for x in cBands:
    elementCMatrix += matrixForAllBands[x]
    
#elementCMatrix = matrixForAllBands[13]\
#+ matrixForAllBands[14]\
#+ matrixForAllBands[15]\
#+ matrixForAllBands[16]\
#+ matrixForAllBands[17]

#One way to show a matrix
#img = plt.imshow(elementCMatrix)
#plt.show()

from pylab import pcolor, show, colorbar, xticks, yticks, savefig
pcolor(elementCMatrix)
colorbar()
show()

savefig('/home/jon/Documents/githubipython/elementCMatrixV1.png')

print elementCMatrix

# <headingcell level=4>

# Show a matrix of Iron

# <codecell>

plt.clf()
elementFeMatrix = [0]

feBands =[324,325,326,327,328,329,330,331,332]

for x in feBands:
    elementFeMatrix += matrixForAllBands[x]
    
img = plt.imshow(elementFeMatrix)

plt.show()

print elementFeMatrix

# <rawcell>

# Not working to save here. problem between plt.imshow and plt.figure

# <codecell>

#fileName = 'elementBMatrix'
#png = '.png'
#jpg = '.jpg'
#fileNameAndExt = fileName + jpg

#fig = plt.figure()
# generate your plot
#fig.savefig(fileNameAndExt,dpi=600)

