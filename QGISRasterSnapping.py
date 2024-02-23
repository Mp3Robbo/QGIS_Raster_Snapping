import numpy
from qgis.core import QgsRasterLayer
import os
import glob


"""
##########################################################
User options
"""

#That raster that is to be snapped
inputRaster     = 'C:/Temp/SmallerImage.tif'

#The raster to snap to
snapRaster      = 'C:/Temp/BiggerImage.tif'

#The output raster to be created
outputRaster    = 'C:/Temp/SmallerImageSnapped.tif'

#Options for output compression
compressOptions = 'COMPRESS=LZW|PREDICTOR=1|NUM_THREADS=ALL_CPUS|BIGTIFF=IF_SAFER|TILED=YES'

"""
##############################################################
Input raster info
"""

inputRas = QgsRasterLayer(inputRaster) 
pixelSizeXInputRas = inputRas.rasterUnitsPerPixelX()
pixelSizeYInputRas = inputRas.rasterUnitsPerPixelY()

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
snapRasterHeightSnapRas = snapRas.height()
snapRasterWidthSnapRas = snapRas.width()

snapRasBounds = snapRas.extent()
xminSnapRas = snapRasBounds.xMinimum()
xmaxSnapRas = snapRasBounds.xMaximum()
yminSnapRas = snapRasBounds.yMinimum()
ymaxSnapRas = snapRasBounds.yMaximum()
coordsSnapRas = "%f %f %f %f" %(xminSnapRas, ymaxSnapRas, xmaxSnapRas, yminSnapRas)
print(coordsSnapRas)

"""
##############################################################
Get a list of possible snap coordinates
"""

listOfXCoords = []
nextXCoord = xminSnapRas

while nextXCoord < xmaxSnapRas:
    nextXCoord = nextXCoord + pixelSizeXSnapRas
    listOfXCoords.append(nextXCoord)
print(str(listOfXCoords[:10]) + '...')


listOfYCoords = []
nextYCoord = yminSnapRas

while nextYCoord < ymaxSnapRas:
    nextYCoord = nextYCoord + pixelSizeYSnapRas
    listOfYCoords.append(nextYCoord)
print(str(listOfYCoords[:10]) + '...')


"""
##############################################################
Determine what the delta X & Y needs to be
"""

#We'll aim to snap the top left corner (highest y val, lowest x val)
closestXCoordinate = min(listOfXCoords, key=lambda x:abs(x-xminInputRas))
closestYCoordinate = min(listOfYCoords, key=lambda x:abs(x-ymaxInputRas))

shiftX = closestXCoordinate - xminInputRas
shiftY = closestYCoordinate - ymaxInputRas

shiftParameter = '-a_ullr ' + str(xminInputRas + shiftX) + ' ' + str(ymaxInputRas + shiftY) + ' ' + str(xmaxInputRas + shiftX) + ' ' + str(yminInputRas + shiftY)

processing.run("gdal:translate", {'INPUT':inputRaster,'TARGET_CRS':None,'NODATA':None,'COPY_SUBDATASETS':False,'OPTIONS':compressOptions,'EXTRA':shiftParameter,'DATA_TYPE':0,'OUTPUT':outputRaster})