try:
    import osgeo.gdal as gdal
    import osgeo.osr as osr
except:
    import gdal
    import osr
from numpy import *


class ValueAlreadySet(Exception):
    def __init__(self,val):
        self.val = val
    def __str__(self):
        return repr(self.val)

class CreateTiff:
    ##
    # Create a new tiff file with a WGS84 Projection
    # @param filename Name of the file to create
    # @param xSize X Size of the data set in pixels (longitude)
    # @param ySize Y Size of the data set in pixels (latitude) 
    # @param Number of bands the image will contain (1 -> Machine Limit)
    def __init__(self, filename, xSize, ySize, bands):
        driver = gdal.GetDriverByName("GTiff")
        self.dataset = driver.Create(filename,
                                     xSize, #x size of the image
                                     ySize, #y size of the image
                                     bands,   #number of bands
                                     gdal.GDT_Float32)
        self.srs = osr.SpatialReference()
        self.srs.SetWellKnownGeogCS('WGS84')
        self.dataset.SetProjection(self.srs.ExportToWkt())
        self.ds = zeros((ySize,xSize), float32)


    ##
    # Sets the datasets geotransform (geotransform defined by [Long Tilt (usually 0), 
    # Long Pixel Size, uCorner Long, Lat Tilt (Usually 0), Lat Pixel Size, 
    # uCorner Lat]
    # @param geoTrans Holds the user specified Geotransform
    def SetGeotransform(self, geoTrans):
        self.dataset.SetGeoTransform(geoTrans)
        self.geoTransform = geoTrans

    ## LatLongToPixel
    # Takes a point and converts it to (x,y) pixel coordinates
    # @param point A (lat,long) tuple containing the point of interest
    # @return (x,x) tuple containing map coordinates for the point
    def LatLongToPixel(self,point):
        lat = point[0]
        lon = point[1]
        try:
            x = (lon - self.geoTransform[0]) / self.geoTransform[1]
        except:
            x = 0.0
        try:
            y = (lat - self.geoTransform[3]) / self.geoTransform[5]
        except:
            y = 0.0
        x = int(x)
        y = int(y)
        return (x,y)

    ##
    # Writes a single point to an internal storage array. When flush is called
    # this storage array is written to disk.
    # @param lat Latitude of the point 
    # @param lon Longitude of the point
    # @param data Value at that point
    def WritePoint(self, lat, lon, data):
        val = self.LatLongToPixel([lat,lon])
        if self.ds[val[1]][val[0]] == 0.0:
            self.ds[val[1]][val[0]] = data
        else:
            raise ValueAlreadySet("Value already set for point at " + str(lat) + ", " + str(lon))
    ##
    # Write band to disk and close
    def Close(self):
        self.dataset.GetRasterBand(1).WriteArray(self.ds)
        self.dataset = None