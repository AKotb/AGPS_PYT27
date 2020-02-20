import os
import subprocess
import tkFileDialog

try:
    import osgeo.gdal as gdal
    import osgeo.osr as osr
except:
    import gdal
    import osr

import Tkinter as tk


class LSMProcessing(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        
        self.namesCLM = ["NSWRS", "NLWRS", "LHTFL", "SHTFL", "var155", "var131", "var132", "EVP", "var235", "var234", "SNOM", "var138", "WEASD", "TSOIL_1", "TSOIL_2", "TSOIL_3", "TSOIL_4", "TSOIL_5", "TSOIL_6", "TSOIL_7", "TSOIL_8", "TSOIL_9", "TSOIL_10", "SOILM_1", "SOILM_2", "SOILM_3", "SOILM_4", "SOILM_5", "SOILM_6", "SOILM_7", "SOILM_8", "SOILM_9", "SOILM_10", "TCDC", "WIND", "TMP", "SPFH", "PRES", "var204", "var205"]
        self.namesNOAH = ["NSWRS", "NLWRS", "LHTFL", "SHTFL", "var155", "var131", "var132", "EVP", "var235", "var234", "SNOM", "var138", "WEASD", "TSOIL_1", "TSOIL_2", "TSOIL_3", "TSOIL_4", "SOILM_1", "SOILM_2", "SOILM_3", "SOILM_4", "TCDC", "WIND", "TMP", "SPFH", "PRES", "var204", "var205"]
        self.namesVIC = ["var131", "var132", "EVP", "SSRUN", "BGRUN", "SNOM", "WEASD", "SOILM_1", "SOILM_2", "SOILM_3", "TCDC", "WIND", "TMP", "SPFH", "PRES", "DSWRF", "DLWRF"]
        self.namesMOSAIC = ["NSWRS", "NLWRS", "LHTFL", "SHTFL", "var155", "var131", "var132", "EVP", "var235", "var234", "SNOM", "var138", "TSOIL_1", "WEASD", "SOILM_1", "SOILM_2", "SOILM_3", "TCDC", "WIND", "TMP", "SPFH", "PRES", "var204", "var205"]
        
        # window title in the title bar
        self.master.title("LSM Processing")
        
        # window title label
        windowlbl = tk.Label(self.master, text="Land Surface Models Processing Tasks")
        windowlbl.grid(padx=10, pady=10, row=0, column=0, columnspan=4)

        # select gldas model version
        gldasmodelversionlbl = tk.Label(self.master, text="GLDAS Model")
        gldasmodelversionlbl.grid(sticky='W', padx=10, pady=10, row=1, column=0)
        self.gldasmodelversionvar = tk.StringVar(self.master)
        self.gldasmodelversionvar.set("Select Model")
        gldasmodelversionw = tk.OptionMenu(self.master, self.gldasmodelversionvar, "Select Model", "CLM", "Mosaic", "Noah", "VIC", command=self.modelchanged)
        gldasmodelversionw.grid(sticky='W', padx=10, pady=10, row=1, column=1, columnspan=3)
        
        # select task to process
        lsmtasklbl = tk.Label(self.master, text="Task to Process")
        lsmtasklbl.grid(sticky='W', padx=10, pady=10, row=2, column=0)
        self.lsmtaskvar = tk.StringVar(self.master)
        self.lsmtaskvar.set("Select Task")
        lsmtaskw = tk.OptionMenu(self.master, self.lsmtaskvar, "Select Task", "GRB-to-GeoTIFF", "Sum GLDAS-derived TWS", command=self.taskchanged)
        lsmtaskw.grid(sticky='W', padx=10, pady=10, row=2, column=1, columnspan=3)

        # first year
        self.firstyearlbl = tk.Label(self.master, text="First Year")
        self.firstyearlbl.grid(sticky='W', padx=10, pady=10, row=3, column=0)
        self.firstyeartxtfeld = tk.Text(self.master, height=1, width=10)
        self.firstyeartxtfeld.grid(sticky='W', padx=10, pady=10, row=3, column=1)
        
        # last year
        self.lastyearlbl = tk.Label(self.master, text="Last Year")
        self.lastyearlbl.grid(sticky='W', padx=10, pady=10, row=3, column=2)
        self.lastyeartxtfeld = tk.Text(self.master, height=1, width=10)
        self.lastyeartxtfeld.grid(sticky='W', padx=10, pady=10, row=3, column=3)
        
        # input grb files 
        inputgrbtiffdirlbl = tk.Label(self.master, text="Input Files")
        inputgrbtiffdirlbl.grid(sticky='W', padx=10, pady=10, row=4, column=0)
        self.inputgrbtiffdirtxtfield = tk.Text(self.master, height=1, width=50)
        self.inputgrbtiffdirtxtfield.grid(sticky='W', padx=10, pady=10, row=4, column=1, columnspan=2)
        inputgrbtiffdirbtn = tk.Button(self.master, text="Browse", command=self.selectgrbtiffdatadir)
        inputgrbtiffdirbtn.grid(sticky='W', padx=10, pady=10, row=4, column=3)
        
        # output tiff directory
        outputtiffdirlbl = tk.Label(self.master, text="Output Files")
        outputtiffdirlbl.grid(sticky='W', padx=10, pady=10, row=5, column=0)
        self.outputtiffdirtxtfield = tk.Text(self.master, height=1, width=50)
        self.outputtiffdirtxtfield.grid(sticky='W', padx=10, pady=10, row=5, column=1, columnspan=2)
        outputtiffdirbtn = tk.Button(self.master, text="Browse", command=self.selecttiffdatadir)
        outputtiffdirbtn.grid(sticky='W', padx=10, pady=10, row=5, column=3)

        # control buttons
        self.startbtn = tk.Button(self.master, text="Start", command=self.startprocessingtask)
        self.startbtn.grid(sticky='E', padx=10, pady=10, row=6, column=1)
        self.cancelbtn = tk.Button(self.master, text="Cancel", command=self.exit)
        self.cancelbtn.grid(sticky='W', padx=10, pady=10, row=6, column=2)

    def exit(self):
        self.master.destroy()
        
    def modelchanged(self, dummy):
        print(self.gldasmodelversionvar.get())
    
    def taskchanged(self, dummy):
        print(self.lsmtaskvar.get())

    def selectgrbtiffdatadir(self):
        self.inputfilespath = tkFileDialog.askdirectory(initialdir="/", title="Select GRB Files Directory")
        self.inputgrbtiffdirtxtfield.delete(1.0, tk.END)
        self.inputgrbtiffdirtxtfield.insert(tk.END, self.inputfilespath)
        
    def selecttiffdatadir(self):
        self.outputtiffpath = tkFileDialog.askdirectory(initialdir="/", title="Select TIFF Files Directory")
        self.outputtiffdirtxtfield.delete(1.0, tk.END)
        self.outputtiffdirtxtfield.insert(tk.END, self.outputtiffpath)

    def startprocessingtask(self): 
        firstyear = self.firstyeartxtfeld.get("1.0", tk.END)
        lastyear = self.lastyeartxtfeld.get("1.0", tk.END)
        if self.lsmtaskvar.get() == "GRB-to-GeoTIFF":
            if self.gldasmodelversionvar.get() == "CLM":
                self.From_GRIB_to_GEOTIFF(self.inputfilespath, self.namesCLM, self.outputtiffpath)
            if self.gldasmodelversionvar.get() == "Mosaic":
                self.From_GRIB_to_GEOTIFF(self.inputfilespath, self.namesMOSAIC, self.outputtiffpath)
            if self.gldasmodelversionvar.get() == "Noah":
                self.From_GRIB_to_GEOTIFF(self.inputfilespath, self.namesNOAH, self.outputtiffpath)
            if self.gldasmodelversionvar.get() == "VIC":
                self.From_GRIB_to_GEOTIFF(self.inputfilespath, self.namesVIC, self.outputtiffpath)
                
        if self.lsmtaskvar.get() == "Sum GLDAS-derived TWS":
            if self.gldasmodelversionvar.get() == "CLM":
                self.Sum_GLDAS_TWS_CLM(self.inputfilespath, self.outputtiffpath, firstyear, lastyear)
            if self.gldasmodelversionvar.get() == "Mosaic":
                self.Sum_GLDAS_TWS_Mosiac(self.inputfilespath, self.outputtiffpath, firstyear, lastyear)
            if self.gldasmodelversionvar.get() == "Noah":
                self.Sum_GLDAS_TWS_Noah(self.inputfilespath, self.outputtiffpath, firstyear, lastyear)
            if self.gldasmodelversionvar.get() == "VIC":
                self.Sum_GLDAS_TWS_VIC(self.inputfilespath, self.outputtiffpath, firstyear, lastyear)
    
    
    # method to convert all provided grb files into geotiff files    
    def From_GRIB_to_GEOTIFF(self, inputdatadir, names, outputtiffdir):
        os.chdir(inputdatadir)    
        for filename in os.listdir(os.getcwd()):
            for x in range(len(names)):
                if(filename[-3:] == "grb"):
                    outName = filename[:-4] + "_" + names[x] + ".tif"
                    os.system("gdal_translate -b " + str(x + 1) + " -of GTiff " + filename + " " + "\""+outputtiffdir+'/'+outName+"\"")
        
        # task status
        self.startbtn.grid_forget()
        self.cancelbtn.grid_forget()
        self.conversioncompletedlbl = tk.Label(self.master, text="Conversion Completed")
        self.conversioncompletedlbl.grid(sticky='W', padx=10, pady=10, row=6, column=1)
        self.closebtn = tk.Button(self.master, text="Close", width=15, command=self.exit)
        self.closebtn.grid(sticky='E', padx=10, pady=10, row=6, column=2)
        
                        
    def Sum_GLDAS_TWS_CLM(self, inputdatadir, outputtiffpath, firstyear, lastyear):
        monthNum=1
        totMonths = 0
        no_data_value = 0.0  # 9.99900e+20
        for year in range(int(firstyear), int(lastyear)+1):
            for month in range(1, 13):
                if monthNum>186:
                    print ("Invalid Month Number!")
                else:
                    totMonths += 1
                    if (month < 10):
                        monthStr = str(year) + "0" + str(month)
                    else:
                        monthStr = str(year) + str(month)
                    s1 = gdal.Open(inputdatadir + "/GLDAS_CLM10_M.A" + monthStr + ".001_SOILM_1.tif")
                    ref = s1
                    s1 = s1.ReadAsArray()
                    s2 = gdal.Open(inputdatadir + "/GLDAS_CLM10_M.A" + monthStr + ".001_SOILM_2.tif")
                    s2 = s2.ReadAsArray()
                    s3 = gdal.Open(inputdatadir + "/GLDAS_CLM10_M.A" + monthStr + ".001_SOILM_3.tif")
                    s3 = s3.ReadAsArray()
                    s4 = gdal.Open(inputdatadir + "/GLDAS_CLM10_M.A" + monthStr + ".001_SOILM_4.tif")
                    s4 = s4.ReadAsArray()
                    s5 = gdal.Open(inputdatadir + "/GLDAS_CLM10_M.A" + monthStr + ".001_SOILM_5.tif")
                    s5 = s5.ReadAsArray()
                    s6 = gdal.Open(inputdatadir + "/GLDAS_CLM10_M.A" + monthStr + ".001_SOILM_6.tif")
                    s6 = s6.ReadAsArray()
                    s7 = gdal.Open(inputdatadir + "/GLDAS_CLM10_M.A" + monthStr + ".001_SOILM_7.tif")
                    s7 = s7.ReadAsArray()
                    s8 = gdal.Open(inputdatadir + "/GLDAS_CLM10_M.A" + monthStr + ".001_SOILM_8.tif")
                    s8 = s8.ReadAsArray()
                    s9 = gdal.Open(inputdatadir + "/GLDAS_CLM10_M.A" + monthStr + ".001_SOILM_9.tif")
                    s9 = s9.ReadAsArray()
                    s10 = gdal.Open(inputdatadir + "/GLDAS_CLM10_M.A" + monthStr + ".001_SOILM_10.tif")
                    s10 = s10.ReadAsArray()
                    s11 = gdal.Open(inputdatadir + "/GLDAS_CLM10_M.A" + monthStr + ".001_WEASD.tif")
                    s11 = s11.ReadAsArray()
                    s12 = gdal.Open(inputdatadir + "/GLDAS_CLM10_M.A" + monthStr + ".001_TCDC.tif")
                    s12 = s12.ReadAsArray()
                    out = s1 + s2 + s3 + s4 + s5 + s6 + s7 + s8 + s9 + s10 + s11 + s12
                    out[out >= 9999.0] = no_data_value
                    geo = ref.GetGeoTransform()  # get the datum
                    proj = ref.GetProjection()  # get the projection
                    shape = s1.shape  # get the image dimensions - format (row, col)
                    driver = gdal.GetDriverByName('GTiff')
                    # here we set the variable dst_ds with destination filename, number of columns and rows, 1 is the number of bands we will write out, gdal.GDT_Float32 is the data type - decimals
                    dst_ds = driver.Create(outputtiffpath + "/month_CLM1_" + str(totMonths) + ".tif", shape[1], shape[0], 1, gdal.GDT_Float32)
                    dst_ds.SetGeoTransform(geo)  # set the datum
                    dst_ds.SetProjection(proj)  # set the projection
                    dst_ds.GetRasterBand(1).WriteArray(out)  # write numpy array band1 as the first band of the multiTiff - this is the blue band
                    stat = dst_ds.GetRasterBand(1).GetStatistics(1, 1)  # get the band statistics (min, max, mean, standard deviation)
                    dst_ds.GetRasterBand(1).SetStatistics(stat[0], stat[1], stat[2], stat[3])  # set the stats we just got to the band
                    y_lat = -59.5
                    for i in reversed(out):
                        x_long = 180.5
                        for j in i:
                            long = x_long
                            lat = y_lat
                            value = "%.5e" % j
                            if value.find("9.99900e+20") > -1:
                                value = value.replace("9.99900e+20", "0.00000e+00")
                            value = "%+13s" % value
                            long = ("%.4f" % long)
                            lat = ("%.4f" % lat)
                            long = ("%+8s" % long)
                            lat = ("%+9s" % lat)
                            out = long + lat + value + '\n'
                            x_long += 1
                            if (x_long > 360):
                                x_long = 0.5
                        y_lat += 1
                    monthNum += 1
                
        # task status
        self.startbtn.grid_forget()
        self.cancelbtn.grid_forget()
        self.summationcompletedlbl = tk.Label(self.master, text="Summation Completed")
        self.summationcompletedlbl.grid(sticky='W', padx=10, pady=10, row=6, column=1)
        self.closebtn = tk.Button(self.master, text="Close", width=15, command=self.exit)
        self.closebtn.grid(sticky='E', padx=10, pady=10, row=6, column=2)
             
                
    def Sum_GLDAS_TWS_Mosiac(self, inputdatadir, outputtiffpath, firstyear, lastyear):
        monthNum = 1
        index = 0
        no_data_value = 0.0  # 9.99900e+20
        for year in range(int(firstyear), int(lastyear)+1):
            for month in range(1, 13):
                if monthNum>186:
                    print ("Invalid Month Number!")
                else:
                    index += 1
                    monthStr = str(year) + "%02d" % (month,)
                    s1 = gdal.Open(inputdatadir + "/GLDAS_MOS10_M.A" + monthStr + ".001_SOILM_1.tif")
                    ref = s1
                    s1 = s1.ReadAsArray()
                    s2 = gdal.Open(inputdatadir + "/GLDAS_MOS10_M.A" + monthStr + ".001_SOILM_2.tif")
                    s2 = s2.ReadAsArray()
                    s3 = gdal.Open(inputdatadir + "/GLDAS_MOS10_M.A" + monthStr + ".001_SOILM_3.tif")
                    s3 = s3.ReadAsArray()
                    s11 = gdal.Open(inputdatadir + "/GLDAS_MOS10_M.A" + monthStr + ".001_WEASD.tif")
                    s11 = s11.ReadAsArray()
                    s12 = gdal.Open(inputdatadir + "/GLDAS_MOS10_M.A" + monthStr + ".001_TCDC.tif")
                    s12 = s12.ReadAsArray()
                    out = s1 + s2 + s3 + s11 + s12
                    out[out >= 9999.0] = no_data_value
            
                    geo = ref.GetGeoTransform()  # get the datum
                    proj = ref.GetProjection()  # get the projection
                    shape = s1.shape  # get the image dimensions - format (row, col)
                    driver = gdal.GetDriverByName('GTiff')
                    # here we set the variable dst_ds with destination filename, number of columns and rows, 1 is the number of bands we will write out, gdal.GDT_Float32 is the data type - decimals
                    dst_ds = driver.Create(outputtiffpath + "/month_MOSAIC_" + str(index) + ".tif", shape[1], shape[0], 1, gdal.GDT_Float32)
                    dst_ds.SetGeoTransform(geo)  # set the datum
                    dst_ds.SetProjection(proj)  # set the projection
                    dst_ds.GetRasterBand(1).WriteArray(out)  # write numpy array band1 as the first band of the multiTiff - this is the blue band
                    dst_ds.GetRasterBand(1).SetNoDataValue(no_data_value)
                    print (year, month, out.shape)
                    stat = dst_ds.GetRasterBand(1).GetStatistics(1, 1)  # get the band statistics (min, max, mean, standard deviation)
                    dst_ds.GetRasterBand(1).SetStatistics(stat[0], stat[1], stat[2], stat[3])  # set the stats we just got to the band
                    y_lat = -59.5
                    for i in reversed(out):
                        x_long = 180.5
                        for j in i:
                            long = x_long
                            lat = y_lat
                            value = "%.5e" % j
                            if value.find("9.99900e+20") > -1:
                                value = value.replace("9.99900e+20", "0.00000e+00")
                            value = "%+13s" % value
                            long = ("%.4f" % long)
                            lat = ("%.4f" % lat)
                            long = ("%+8s" % long)
                            lat = ("%+9s" % lat)
                            out = long + lat + value + '\n'
                            x_long += 1
                            if (x_long > 360):
                                x_long = 0.5
                        y_lat += 1
                    print "printing file",monthNum
                    monthNum += 1                                
        
        # task status
        self.startbtn.grid_forget()
        self.cancelbtn.grid_forget()
        self.summationcompletedlbl = tk.Label(self.master, text="Summation Completed")
        self.summationcompletedlbl.grid(sticky='W', padx=10, pady=10, row=6, column=1)
        self.closebtn = tk.Button(self.master, text="Close", width=15, command=self.exit)
        self.closebtn.grid(sticky='E', padx=10, pady=10, row=6, column=2)

        
    def Sum_GLDAS_TWS_Noah(self, inputdatadir, outputtiffpath, firstyear, lastyear):
        monthNum = 1
        totMonths = 0
        no_data_value = 0.0  # 9.99900e+20
        for year in range(int(firstyear), int(lastyear)+1):
            for month in range(1, 13):
                if monthNum>186:
                    print ("Invalid Month Number!")
                else:
                    totMonths = totMonths + 1
                    if (month < 10):
                        monthStr = str(year) + "0" + str(month)
                    else:
                        monthStr = str(year) + str(month)
                    s1 = gdal.Open(inputdatadir + "/GLDAS_NOAH10_M.A" + monthStr + ".001_SOILM_1.tif")
                    ref = s1
                    s1 = s1.ReadAsArray()
                    s2 = gdal.Open(inputdatadir + "/GLDAS_NOAH10_M.A" + monthStr + ".001_SOILM_2.tif")
                    s2 = s2.ReadAsArray()
                    s3 = gdal.Open(inputdatadir + "/GLDAS_NOAH10_M.A" + monthStr + ".001_SOILM_3.tif")
                    s3 = s3.ReadAsArray()
                    s4 = gdal.Open(inputdatadir + "/GLDAS_NOAH10_M.A" + monthStr + ".001_SOILM_4.tif")
                    s4 = s4.ReadAsArray()
                    s5 = gdal.Open(inputdatadir + "/GLDAS_NOAH10_M.A" + monthStr + ".001_WEASD.tif")
                    s5 = s5.ReadAsArray()
                    s6 = gdal.Open(inputdatadir + "/GLDAS_NOAH10_M.A" + monthStr + ".001_TCDC.tif")
                    s6 = s6.ReadAsArray()
                    out = s1 + s2 + s3 + s4 + s5 + s6
                    out[out >= 9999.0] = no_data_value
                    geo = ref.GetGeoTransform()  # get the datum
                    proj = ref.GetProjection()  # get the projection
                    shape = s1.shape  # get the image dimensions - format (row, col)
                    driver = gdal.GetDriverByName('GTiff')
                    # here we set the variable dst_ds with destination filename, number of columns and rows, 1 is the number of bands we will write out, gdal.GDT_Float32 is the data type - decimals
                    dst_ds = driver.Create(outputtiffpath + "/month_NOAH_" + str(totMonths) + ".tif", shape[1], shape[0], 1, gdal.GDT_Float32)
                    dst_ds.SetGeoTransform(geo)  # set the datum
                    dst_ds.SetProjection(proj)  # set the projection
                    dst_ds.GetRasterBand(1).WriteArray(out)  # write numpy array band1 as the first band of the multiTiff - this is the blue band
                    stat = dst_ds.GetRasterBand(1).GetStatistics(1, 1)  # get the band statistics (min, max, mean, standard deviation)
                    dst_ds.GetRasterBand(1).SetStatistics(stat[0], stat[1], stat[2], stat[3])  # set the stats we just got to the band
                    y_lat = -59.5
                    for i in reversed(out):
                        x_long = 180.5
                        for j in i:
                            long = x_long
                            lat = y_lat
                            value = "%.5e" % j
                            if value.find("9.99900e+20") > -1:
                                value = value.replace("9.99900e+20", "0.00000e+00")
                            value = "%+13s" % value
                            long = ("%.4f" % long)
                            lat = ("%.4f" % lat)
                            long = ("%+8s" % long)
                            lat = ("%+9s" % lat)
                            out = long + lat + value + '\n'
                            x_long += 1
                            if (x_long > 360):
                                x_long = 0.5
                        y_lat += 1
                    print "printing file",monthNum
                    monthNum += 1
        
        # task status
        self.startbtn.grid_forget()
        self.cancelbtn.grid_forget()
        self.summationcompletedlbl = tk.Label(self.master, text="Summation Completed")
        self.summationcompletedlbl.grid(sticky='W', padx=10, pady=10, row=6, column=1)
        self.closebtn = tk.Button(self.master, text="Close", width=15, command=self.exit)
        self.closebtn.grid(sticky='E', padx=10, pady=10, row=6, column=2)


    def Sum_GLDAS_TWS_VIC(self, inputdatadir, outputtiffpath, firstyear, lastyear):
        monthNum = 1
        totMonths = 0
        no_data_value = 0.0  # 9.99900e+20
        for year in range(int(firstyear), int(lastyear)+1):
            for month in range(1, 13):
                if monthNum>186:
                    print ("Invalid Month Number!")
                else:
                    totMonths = totMonths + 1
                    if (month < 10):
                        monthStr = str(year) + "0" + str(month)
                    else:
                        monthStr = str(year) + str(month)
                    s1 = gdal.Open(inputdatadir + "/GLDAS_VIC10_M.A" + monthStr + ".001_SOILM_1.tif")
                    ref = s1
                    s1 = s1.ReadAsArray()
                    s2 = gdal.Open(inputdatadir + "/GLDAS_VIC10_M.A" + monthStr + ".001_SOILM_2.tif")
                    s2 = s2.ReadAsArray()
                    s3 = gdal.Open(inputdatadir + "/GLDAS_VIC10_M.A" + monthStr + ".001_SOILM_3.tif")
                    s3 = s3.ReadAsArray()
                    s11 = gdal.Open(inputdatadir + "/GLDAS_VIC10_M.A" + monthStr + ".001_WEASD.tif")
                    s11 = s11.ReadAsArray()
                    s12 = gdal.Open(inputdatadir + "/GLDAS_VIC10_M.A" + monthStr + ".001_TCDC.tif")
                    s12 = s12.ReadAsArray()
                    out = s1 + s2 + s3 + s11 + s12
                    out[out >= 9999.0] = no_data_value
                    geo = ref.GetGeoTransform()  # get the datum
                    proj = ref.GetProjection()  # get the projection
                    shape = s1.shape  # get the image dimensions - format (row, col)
                    driver = gdal.GetDriverByName('GTiff')
                    # here we set the variable dst_ds with destination filename, number of columns and rows, 1 is the number of bands we will write out, gdal.GDT_Float32 is the data type - decimals
                    dst_ds = driver.Create(outputtiffpath + "/month_VIC_" + str(totMonths) + ".tif", shape[1], shape[0], 1, gdal.GDT_Float32)
                    dst_ds.SetGeoTransform(geo)  # set the datum
                    dst_ds.SetProjection(proj)  # set the projection
                    dst_ds.GetRasterBand(1).WriteArray(out)  # write numpy array band1 as the first band of the multiTiff - this is the blue band
                    stat = dst_ds.GetRasterBand(1).GetStatistics(1, 1)  # get the band statistics (min, max, mean, standard deviation)
                    dst_ds.GetRasterBand(1).SetStatistics(stat[0], stat[1], stat[2], stat[3])  # set the stats we just got to the band                                   
                    y_lat = -59.5
                    for i in reversed(out):
                        x_long = 180.5
                        for j in i:
                            long = x_long
                            lat = y_lat
                            value = "%.5e" % j
                            if value.find("9.99900e+20") > -1:
                                value = value.replace("9.99900e+20", "0.00000e+00")
                            value = "%+13s" % value
                            long = ("%.4f" % long)
                            lat = ("%.4f" % lat)
                            long = ("%+8s" % long)
                            lat = ("%+9s" % lat)
                            out = long + lat + value + '\n'
                            x_long += 1
                            if (x_long > 360):
                                x_long = 0.5
                        y_lat += 1
                    print "printing file",monthNum
                    monthNum += 1
        
        # task status
        self.startbtn.grid_forget()
        self.cancelbtn.grid_forget()
        self.summationcompletedlbl = tk.Label(self.master, text="Summation Completed")
        self.summationcompletedlbl.grid(sticky='W', padx=10, pady=10, row=6, column=1)
        self.closebtn = tk.Button(self.master, text="Close", width=15, command=self.exit)
        self.closebtn.grid(sticky='E', padx=10, pady=10, row=6, column=2)