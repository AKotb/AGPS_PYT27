import os
from subprocess import *
import subprocess
import tkFileDialog

import Tkinter as tk


class ZonalStatistics(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("Zonal Statistics")
        self.pack(fill=tk.BOTH, expand=1)
        
        inputrasterdatadirlbl = tk.Label(self.master, text="Input Raster Data")
        inputrasterdatadirlbl.place(x=20, y=50)
        self.inputrasterdatadirtxtfield = tk.Text(self.master, height=1, width=50)
        self.inputrasterdatadirtxtfield.place(x=130, y=50)
        inputrasterdatadirbtn = tk.Button(self.master, text="Browse", command=self.selectrasterdatadir)
        inputrasterdatadirbtn.place(x=540, y=47)
        
        outputtabledatadirlbl = tk.Label(self.master, text="Output Table")
        outputtabledatadirlbl.place(x=20, y=100)
        self.outputtabledatadirtxtfield = tk.Text(self.master, height=1, width=50)
        self.outputtabledatadirtxtfield.place(x=130, y=100)
        outputtabledatadirbtn = tk.Button(self.master, text="Browse", command=self.selectoutputtabledatadir)
        outputtabledatadirbtn.place(x=540, y=97)
        
        featurezonelbl = tk.Label(self.master, text="Feature Zone")
        featurezonelbl.place(x=20, y=150)
        self.featurezonetxtfield = tk.Text(self.master, height=1, width=50)
        self.featurezonetxtfield.place(x=130, y=150)
        featurezonebtn = tk.Button(self.master, text="Browse", command=self.selectfeaturezone)
        featurezonebtn.place(x=540, y=147)

        self.startbtn = tk.Button(self.master, text="Start", command=self.startzonalstatistics)
        self.startbtn.place(x=500, y=200)
        self.cancelbtn = tk.Button(self.master, text="Cancel", command=self.exit)
        self.cancelbtn.place(x=540, y=200)

    def exit(self):
        self.master.destroy()

    def selectrasterdatadir(self):
        self.inputrasterdatapath = tkFileDialog.askdirectory(initialdir="/", title="Select Raster Data Directory")
        self.inputrasterdatadirtxtfield.delete(1.0, tk.END)
        self.inputrasterdatadirtxtfield.insert(tk.END, self.inputrasterdatapath)
        
    def selectoutputtabledatadir(self):
        self.outputtablepath = tkFileDialog.askdirectory(initialdir="/", title="Select Output Table Directory")
        self.outputtabledatadirtxtfield.delete(1.0, tk.END)
        self.outputtabledatadirtxtfield.insert(tk.END, self.outputtablepath)
        
    def selectfeaturezone(self):
        self.featurezonepath = tkFileDialog.askopenfilename(initialdir="/", title="Select Feature Zone",
                                                        filetypes=(("Shp Files", "*.shp"), ("All Files", "*.*")))
        self.featurezonetxtfield.delete(1.0, tk.END)
        self.featurezonetxtfield.insert(tk.END, self.featurezonepath)

    def startzonalstatistics(self):
        inputrasterdata = self.inputrasterdatadirtxtfield.get("1.0", tk.END)
        inputrasterdata = "-i "+inputrasterdata
        inputrasterdata = '"'+inputrasterdata+'"'
        print "inputrasterdata: "+inputrasterdata
        outputtable = self.outputtabledatadirtxtfield.get("1.0", tk.END)
        outputtable = "-o "+outputtable
        outputtable = '"'+outputtable+'"'
        print "outputtable: "+outputtable
        featurezone = self.featurezonetxtfield.get("1.0", tk.END)
        featurezone = "-f "+featurezone
        featurezone = '"'+featurezone+'"'
        print "featurezone: "+featurezone
     
#         batfilepath = r'C:\Users\ahmed.kotb\workspace\AGPS_PYT27\resources\zonalstatistics.bat'
#         item = subprocess.Popen([batfilepath ["-i "+inputrasterdata ["-o "+outputtable ["-f "+featurezone]]]], shell=True, stdout=subprocess.PIPE)
#         for line in item.stdout:
#             print line
            
        
        p = Popen([r'C:\Users\ahmed.kotb\workspace\AGPS_PYT27\resources\zonalstatistics.bat', inputrasterdata, outputtable, featurezone], stdout=PIPE, stderr=PIPE, stdin=PIPE)
        output, errors = p.communicate()
        p.wait()
        print('after calling bat file')
        print('============================================')
        print (output)
        print('============================================')
        print (errors)
        print('============================================')
            
