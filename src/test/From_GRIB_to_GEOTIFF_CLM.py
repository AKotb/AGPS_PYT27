# Code to convert ".grb" files to geotiff files.
# Coded by Mohamed Ahmed
# Change the processed years and path to the input data
 
import os


namesCLM = ["NSWRS", "NLWRS", "LHTFL", "SHTFL","var155","var131","var132","EVP","var235","var234","SNOM","var138","WEASD","TSOIL_1","TSOIL_2","TSOIL_3","TSOIL_4","TSOIL_5","TSOIL_6","TSOIL_7","TSOIL_8","TSOIL_9","TSOIL_10","SOILM_1","SOILM_2","SOILM_3","SOILM_4","SOILM_5","SOILM_6","SOILM_7","SOILM_8","SOILM_9","SOILM_10","TCDC","WIND","TMP","SPFH","PRES","var204","var205"]
namesNOAH = ["NSWRS", "NLWRS", "LHTFL", "SHTFL","var155","var131","var132","EVP","var235","var234","SNOM","var138","WEASD","TSOIL_1","TSOIL_2","TSOIL_3","TSOIL_4","SOILM_1","SOILM_2","SOILM_3","SOILM_4","TCDC","WIND","TMP","SPFH","PRES","var204","var205"]
namesVIC = ["var131","var132","EVP","SSRUN","BGRUN", "SNOM", "WEASD","SOILM_1","SOILM_2","SOILM_3","TCDC","WIND","TMP","SPFH","PRES","DSWRF", "DLWRF"]
namesMOSAIC = ["NSWRS", "NLWRS", "LHTFL", "SHTFL","var155","var131","var132","EVP","var235","var234","SNOM","var138","TSOIL_1","WEASD","SOILM_1","SOILM_2","SOILM_3","TCDC","WIND","TMP","SPFH","PRES","var204","var205"]

# Change the processed years and path to the input data
for year in range(2002, 2018):
	os.chdir("F:\\Gldas_Model\\GLDAS_CLM10_M\\"+str(year))	
	for file in os.listdir(os.getcwd()):
	# Change the model name
		for x in range(len(namesCLM)):
			if(file[-3:] == "grb"):
			# Change the model name
				outName = file[:-4]+"_"+namesCLM[x]+".tif"
				os.system("gdal_translate -b "+str(x+1)+" -of GTiff "+file+" "+outName)
				

				
				
				
