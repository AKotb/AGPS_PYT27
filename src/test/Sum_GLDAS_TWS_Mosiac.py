# This code will sum the Snow storage, Canopy water storage, and Soil Moisture storage  of the GLDAS model in one GeoTIFF image.
# The resultant image will represnet the GLDAS-derived TWS.
# The input images and the code should be in one folder
# GLDAS model version: MOSAIC
# Coded: Mohamed Ahmed

import os

from numpy import *
from osgeo import gdal

files = os.listdir(".")
#monthNum = 1
index = 0
no_data_value = 0.0 #9.99900e+20
for year in range(2002, 2018):
	for month in range(1,13):
		index += 1
		monthStr = str(year)+"%02d" % (month,)
		s1 = gdal.Open("GLDAS_MOS10_M.A"+ monthStr+".001_SOILM_1.tif")
		ref = s1
		s1 = s1.ReadAsArray()
		s2 = gdal.Open("GLDAS_MOS10_M.A"+ monthStr+".001_SOILM_2.tif")
		s2 = s2.ReadAsArray()
		s3 = gdal.Open("GLDAS_MOS10_M.A"+ monthStr+".001_SOILM_3.tif")
		s3 = s3.ReadAsArray()
		s11 = gdal.Open("GLDAS_MOS10_M.A"+ monthStr+".001_WEASD.tif")
		s11 = s11.ReadAsArray()
		s12 = gdal.Open("GLDAS_MOS10_M.A"+ monthStr+".001_TCDC.tif")
		s12 = s12.ReadAsArray()
		out = s1+s2+s3+s11+s12
		out[out >= 9999.0] = no_data_value

		geo = ref.GetGeoTransform()  # get the datum
		proj = ref.GetProjection()   # get the projection
		shape = s1.shape        # get the image dimensions - format (row, col)
		driver = gdal.GetDriverByName('GTiff')
		dst_ds = driver.Create( "month_MOSAIC_"+str(index)+".tif", shape[1], shape[0], 1, gdal.GDT_Float32)
																 # here we set the variable dst_ds with
																 # destination filename, number of columns and rows
																 # 1 is the number of bands we will write out
																 # gdal.GDT_Float32 is the data type - decimals
		dst_ds.SetGeoTransform( geo ) # set the datum
		dst_ds.SetProjection( proj )  # set the projection
		dst_ds.GetRasterBand(1).WriteArray( out)  # write numpy array band1 as the first band of the multiTiff - this is the blue band
		dst_ds.GetRasterBand(1).SetNoDataValue(no_data_value)
		print (year,month,out.shape)
		stat = dst_ds.GetRasterBand(1).GetStatistics(1,1)  # get the band statistics (min, max, mean, standard deviation)
		dst_ds.GetRasterBand(1).SetStatistics(stat[0], stat[1], stat[2], stat[3]) # set the stats we just got to the band                                   


'''
#image = gdal.Open(pathout2 + x , gdal.GA_ReadOnly)


		#data = image.ReadAsArray(0, 0, image.RasterXSize, image.RasterYSize)
		#wite to file
		#monthNumStr = "month."+"%03d" %(monthNum,)
		#f = open(pathout2+monthNumStr, "wb")
		#f = open("month_MOSAIC."+str(totMonths).zfill(3), "wb")
		y_lat = -59.5
		for i in reversed(out):    
			x_long = 180.5
			for j in i:               
				long = x_long
				lat = y_lat
				value = "%.5e" %j
				
				if value.find("9.99900e+20") > -1:
					#print value
					value = value.replace("9.99900e+20", "0.00000e+00")
					#print("replaced")

				value = "%+13s" %value
				long = ("%.4f" % long)
				lat = ("%.4f" % lat)
				long = ("%+8s" % long)
				lat = ("%+9s" % lat)
				out = long + lat + value + '\n'                        
				#f.write(out)
				x_long+=1
				if (x_long > 360):
					x_long = 0.5
			y_lat+=1
		#f.close()
		#print "printing file",monthNum
		monthNum+=1
'''