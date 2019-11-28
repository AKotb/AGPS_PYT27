import os
import time
import tkFileDialog

from ReadMass import *
import Tkinter as tk
from main import CreateTiff_Global


class NCtoTiff(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("Convert NC File to TIFF Images")
        self.pack(fill=tk.BOTH, expand=1)

        # NC file
        inputncdirlbl = tk.Label(self.master, text="NC File")
        inputncdirlbl.place(x=10, y=50)

        self.inputncdirtxtfield = tk.Text(self.master, height=1, width=45)
        self.inputncdirtxtfield.place(x=180, y=50)

        inputncdirbtn = tk.Button(self.master, text="Browse", command=self.selectncdir)
        inputncdirbtn.place(x=540, y=47)

        # TIFF Output Data Directory
        outputtiffdirlbl = tk.Label(self.master, text="Output TIFF Directory")
        outputtiffdirlbl.place(x=10, y=80)

        self.outputtiffdirtxtfield = tk.Text(self.master, height=1, width=45)
        self.outputtiffdirtxtfield.place(x=180, y=80)

        outputtiffdirbtn = tk.Button(self.master, text="Browse", command=self.selectoutputtiffdatadir)
        outputtiffdirbtn.place(x=540, y=77)

        self.conversioncompletedlbl = tk.Label(self.master, text="Conversion Completed")
        self.conversionstartedlbl = tk.Label(self.master, text="Conversion Started ...")

        self.startconvertingnctotiffbtn = tk.Button(self.master, text="Start", command=self.convertnctotiff)
        self.startconvertingnctotiffbtn.place(x=500, y=200)
        self.cancelbtn = tk.Button(self.master, text="Cancel", command=self.exit)
        self.cancelbtn.place(x=450, y=200)


    def exit(self):
        self.master.destroy()

    def selectncdir(self):
        self.twsfilesdatapath = tkFileDialog.askdirectory(initialdir="/", title="Select NC File")
        self.inputncdirtxtfield.delete(1.0, tk.END)
        self.inputncdirtxtfield.insert(tk.END, self.twsfilesdatapath)

    def selectoutputtiffdatadir(self):
        self.outputtifffilesdatapath = tkFileDialog.askdirectory(initialdir="/", title="Select Output TIFF Files Directory")
        self.outputtiffdirtxtfield.delete(1.0, tk.END)
        self.outputtiffdirtxtfield.insert(tk.END, self.outputtifffilesdatapath)

    def convertnctotiff(self):
        print ('convertnctotiff')
        self.conversionstartedlbl.place(x=20, y=150)
        myfilesList = os.listdir(self.twsfilesdatapath)
        for f in myfilesList:
            testFile = self.twsfilesdatapath + '\\' + f
            outputtifffile=self.outputtifffilesdatapath + '\\' + f
            m = ReadMonthlyMass(testFile)
            d = m.Read()
            t = CreateTiff_Global(outputtifffile + '.tif', 717, 357, 1)
            t.SetGeotransform([-179.25, 0.5, 0.0, 89.25, 0.0, -0.5])
            for x in d.keys():
                tmp = x.split(",")
                t.WritePoint(float(tmp[1]), float(tmp[0]), d[x])
            t.Close()
        self.conversioncompletedlbl.place(x=200, y=150)