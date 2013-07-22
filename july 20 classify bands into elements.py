# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import numpy

# <codecell>

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

# <codecell>

atomicLookUp

# <codecell>

atomicLookUpLabelsNot = atomicLookUp[:,1]
atomicLookUpLabels = atomicLookUpLabelsNot[1:]
print atomicLookUpLabels

# <codecell>

atomicLookUpLow = atomicLookUp[:,2]
print atomicLookUpLow 
atomicLookUpLowVTwo = atomicLookUpLow[1:]
print atomicLookUpLowVTwo
atomicLookUpLowVThree = map(float, atomicLookUpLowVTwo)
print atomicLookUpLowVThree

# <codecell>

atomicLookUpHi = atomicLookUp[:,3]
atomicLookUpHi
atomicLookUpHiVTwo = atomicLookUpHi[1:]
print atomicLookUpHiVTwo
atomicLookUpHiVThree = map(float, atomicLookUpHiVTwo)
print atomicLookUpHiVThree

# <codecell>

kevBandWidth = 0.01953125
sampleImageBands = 512

# <codecell>

bandRangeMatrix = [0]*sampleImageBands
for x in range(sampleImageBands):
    bandRangeMatrix[x] = kevBandWidth*x
bandRangeMatrix

# <codecell>

len(bandRangeMatrix)

# <headingcell level=3>

# Why doesnt this for loop work? but hand typing in all of the elif statments does?

# <codecell>

labels512v2 = [0]*512

for x in range(512):
    for aaa in range(64):
        if bandRangeMatrix[x] >= atomicLookUpLowVThree[aaa] and bandRangeMatrix[x] <= atomicLookUpHiVThree[aaa]:
            labels512v2[x] = atomicLookUpLabels[aaa]
        else:
            labels512v2[x] = 'BACKGROUND'
        
        
print 'test 20'
print labels512v2

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
    else:
        labels512[x] = 'BACKGROUND'

print 'test 5'
print labels512 

# <codecell>


