import numpy
from qgis.core import QgsRasterLayer
import os
import glob

#Note that this requires the coordinate system to be identical
#The pixel size must also be nearly identical

"""
##########################################################
User options
"""

#That raster that is to be snapped
inputRaster     = 'C:/Temp/InputRaster.tif'

#The raster to snap to
snapRaster      = 'C:/Temp/SnapRaster.tif'

#The output raster to be created
outputRaster    = 'C:/Temp/InputRasterSnapped.tif'

#Options for output compression
compressOptions = 'COMPRESS=LZW|PREDICTOR=1|NUM_THREADS=ALL_CPUS|BIGTIFF=IF_SAFER|TILED=YES'

"""
##############################################################
Input raster info
"""

inputRas = QgsRasterLayer(inputRaster) 
pixelSizeXInputRas = inputRas.rasterUnitsPerPixelX()
pixelSizeYInputRas = inputRas.rasterUnitsPerPixelY()
inputRasterHeight = inputRas.height()
inputRasterWidth = inputRas.width()

inputRasBounds = inputRas.extent() 
xminInputRas = inputRasBounds.xMinimum()
xmaxInputRas = inputRasBounds.xMaximum()
yminInputRas = inputRasBounds.yMinimum()
ymaxInputRas = inputRasBounds.yMaximum()
coordsInputRas = "%f %f %f %f" %(xminInputRas, ymaxInputRas, xmaxInputRas, yminInputRas)
print(coordsInputRas)

"""
##############################################################
Snap raster info
"""

snapRas = QgsRasterLayer(snapRaster) 
pixelSizeXSnapRas = snapRas.rasterUnitsPerPixelX()
pixelSizeYSnapRas = snapRas.rasterUnitsPerPixelY()
coordinateSystemSnapRas = snapRas.crs().authid()
snapRasterHeight = snapRas.height()
snapRasterWidth = snapRas.width()

snapRasBounds = snapRas.extent()
xminSnapRas = snapRasBounds.xMinimum()
xmaxSnapRas = snapRasBounds.xMaximum()
yminSnapRas = snapRasBounds.yMinimum()
ymaxSnapRas = snapRasBounds.yMaximum()
coordsSnapRas = "%f %f %f %f" %(xminSnapRas, ymaxSnapRas, xmaxSnapRas, yminSnapRas)
print(coordsSnapRas)


"""
##############################################################
Find the bounds which define the snap grid
"""

totalXMin = min(xminSnapRas, xminInputRas)
totalXMax = max(xmaxSnapRas, xmaxInputRas)
totalYMin = min(yminSnapRas, yminInputRas)
totalYMax = max(ymaxSnapRas, ymaxInputRas)

#Determine where the lower left corner of the snap grid is
nextXCoord = xminSnapRas
while nextXCoord > (totalXMin - pixelSizeXSnapRas):
    nextXCoord = nextXCoord - pixelSizeXSnapRas
nextYCoord = yminSnapRas
while nextYCoord > (totalYMin - pixelSizeYSnapRas):
    nextYCoord = nextYCoord - pixelSizeYSnapRas


"""
##############################################################
Get a list of possible snap coordinates in the grid
"""

listOfXCoords = []
while nextXCoord < (totalXMax + pixelSizeXSnapRas):
    nextXCoord = nextXCoord + pixelSizeXSnapRas
    listOfXCoords.append(nextXCoord)
print(str(listOfXCoords[:10]) + '...')


listOfYCoords = []
while nextYCoord < (totalYMax + pixelSizeYSnapRas):
    nextYCoord = nextYCoord + pixelSizeYSnapRas
    listOfYCoords.append(nextYCoord)
print(str(listOfYCoords[:10]) + '...')


"""
##############################################################
Determine what the delta X & Y needs to be, then transform
"""

#We'll aim to first snap the top left corner (highest y val, lowest x val)
closestXCoordinate = min(listOfXCoords, key=lambda x:abs(x-xminInputRas))
closestYCoordinate = min(listOfYCoords, key=lambda x:abs(x-ymaxInputRas))

shiftX = closestXCoordinate - xminInputRas
shiftY = closestYCoordinate - ymaxInputRas

#Here we are snapping the image onto the snap raster pixel by pixel, regardless of where the input bottom right corner is
outputLeftCoord = str(xminInputRas + shiftX)
outputTopCoord = str(ymaxInputRas + shiftY)
outputRightCoord = str(xminInputRas + shiftX + (inputRasterWidth * pixelSizeXSnapRas))
outputBottomCoord = str(ymaxInputRas + shiftY - (inputRasterHeight * pixelSizeYSnapRas))

shiftParameter = '-a_ullr ' + outputLeftCoord + ' ' + outputTopCoord + ' ' + outputRightCoord + ' ' + outputBottomCoord

processing.run("gdal:translate", {'INPUT':inputRaster,'TARGET_CRS':None,'NODATA':None,'COPY_SUBDATASETS':False,'OPTIONS':compressOptions,'EXTRA':shiftParameter,'DATA_TYPE':0,'OUTPUT':outputRaster})
