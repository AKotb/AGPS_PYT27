import os
import tkFileDialog
import Tkinter as tk
from pymatbridge import Matlab


class NCtoTiff(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        # window title in the title bar
        self.master.title("Convert NC File to TIFF Images")
        
        # window title label
        windowlbl = tk.Label(self.master, text="Convert NC File to TIFF Images")
        windowlbl.grid(padx=10, pady=10, row=0, column=0, columnspan=4)
        
        # NC file
        inputncdirlbl = tk.Label(self.master, text="NC File")
        inputncdirlbl.grid(sticky='W', padx=10, pady=10, row=1, column=0)

        self.inputncdirtxtfield = tk.Text(self.master, height=1, width=45)
        self.inputncdirtxtfield.grid(sticky='W', padx=10, pady=10, row=1, column=1, columnspan=2)

        inputncdirbtn = tk.Button(self.master, text="Browse", command=self.selectncdir)
        inputncdirbtn.grid(sticky='W', padx=10, pady=10, row=1, column=3)

        # TIFF Output Data Directory
        outputtiffdirlbl = tk.Label(self.master, text="Output TIFF Directory")
        outputtiffdirlbl.grid(sticky='W', padx=10, pady=10, row=2, column=0)

        self.outputtiffdirtxtfield = tk.Text(self.master, height=1, width=45)
        self.outputtiffdirtxtfield.grid(sticky='W', padx=10, pady=10, row=2, column=1, columnspan=2)

        outputtiffdirbtn = tk.Button(self.master, text="Browse", command=self.selectoutputtiffdatadir)
        outputtiffdirbtn.grid(sticky='W', padx=10, pady=10, row=2, column=3)
        
        # NC Variable
        ncvarlbl = tk.Label(self.master, text="NC Variable")
        ncvarlbl.grid(sticky='W', padx=10, pady=10, row=3, column=0)

        self.ncvartxtfield = tk.Text(self.master, height=1, width=30)
        self.ncvartxtfield.grid(sticky='W', padx=10, pady=10, row=3, column=1, columnspan=2)
        
        # NC Times
        nctimeslbl = tk.Label(self.master, text="NC Times")
        nctimeslbl.grid(sticky='W', padx=10, pady=10, row=4, column=0)

        self.nctimestxtfield = tk.Text(self.master, height=1, width=10)
        self.nctimestxtfield.grid(sticky='W', padx=10, pady=10, row=4, column=1, columnspan=2)

        # control buttons
        self.startconvertingnctotiffbtn = tk.Button(self.master, text="Start", width=15, command=self.convertnctotiff)
        self.startconvertingnctotiffbtn.grid(sticky='E', padx=10, pady=10, row=5, column=1)
        self.cancelbtn = tk.Button(self.master, text="Cancel", width=15, command=self.exit)
        self.cancelbtn.grid(sticky='W', padx=10, pady=10, row=5, column=2)

    def exit(self):
        self.master.destroy()

    def selectncdir(self):
        self.ncfilepath = tkFileDialog.askopenfilename(initialdir="/", title="Select NC File", filetypes=(("NetCDF File", "*.nc"), ("All Files", "*.*")))
        self.inputncdirtxtfield.delete(1.0, tk.END)
        self.inputncdirtxtfield.insert(tk.END, self.ncfilepath)

    def selectoutputtiffdatadir(self):
        self.outputtifffilesdatapath = tkFileDialog.askdirectory(initialdir="/", title="Select Output TIFF Files Directory")
        self.outputtiffdirtxtfield.delete(1.0, tk.END)
        self.outputtiffdirtxtfield.insert(tk.END, self.outputtifffilesdatapath)
        
    def convertnctotiff(self):
        self.cancelbtn.config(state="disabled")
        
        matlabpath= "\"C:/Program Files/MATLAB/R2016b/bin/matlab\""
        mlab = Matlab(executable= matlabpath)
        
        ncfilefullpath = self.inputncdirtxtfield.get("1.0", tk.END).encode("ascii")
        ncfilefullpath = ncfilefullpath[0:-1]
        #ncfilefullpathst = 'D:/NARSS/Research Project/2018-2019/01-01-2020/Task_NC-2-TIFF/input/GRCTellus.JPL.200204_201603.GLO.RL05M_1.MSCNv02CRIv02.nc'
        #print('ncfilefullpathdyn: '+ncfilefullpath, type(ncfilefullpath))
        
        tiffoutputdir = self.outputtiffdirtxtfield.get("1.0", tk.END).encode("ascii")
        tiffoutputdir = tiffoutputdir[0:-1]
        tiffoutputdir = os.path.join(tiffoutputdir, '')
        #tiffoutputdirst = 'D:/NARSS/Research Project/2018-2019/01-01-2020/Task_NC-2-TIFF/output/'
        #print('tiffoutputdir: '+tiffoutputdir, type(tiffoutputdir))
        
        
        ncvar = self.ncvartxtfield.get("1.0", tk.END).encode("ascii")
        ncvar = ncvar[0:-1]
        #ncvar = 'lwe_thickness'
        #print('ncvar: '+ncvar, type(ncvar))
        
        
        nctimes = self.nctimestxtfield.get("1.0", tk.END)
        nctimes = int(nctimes)
        #nctimes = 152
        #print('nctimes: '+nctimes, type(nctimes))
        
        
        mlab.start()
        
        mlab.run_func('C:/Users/ahmed.kotb/workspace/AGPS_PYT27/resources/netcdf_to_tiff.m', {'arg1': ncfilefullpath, 'arg2': ncvar, 'arg3': nctimes, 'arg4': tiffoutputdir})
        
        #self.conversionstartedlbl.grid_forget()
        self.startconvertingnctotiffbtn.grid_forget()
        self.cancelbtn.grid_forget()
        
        # task status
        self.conversioncompletedlbl = tk.Label(self.master, text="Conversion Completed")
        self.conversioncompletedlbl.grid(sticky='W', padx=10, pady=10, row=5, column=1)
        self.closebtn = tk.Button(self.master, text="Close", width=15, command=self.exit)
        self.closebtn.grid(sticky='E', padx=10, pady=10, row=5, column=2)
        mlab.stop()
        