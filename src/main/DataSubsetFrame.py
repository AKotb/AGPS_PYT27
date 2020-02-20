import tkFileDialog
import Tkinter as tk
from shutil import copy2
import glob2
import os


class DataSubsetFrame(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("Data Subset")
        self.pack(fill=tk.BOTH, expand=1)

        # Input Data Dir
        inputdatadirlbl = tk.Label(self.master, text="Input Directory")
        inputdatadirlbl.place(x=20, y=50)

        self.inputdatadirtxtfield = tk.Text(self.master, height=1, width=50)
        self.inputdatadirtxtfield.place(x=130, y=50)

        inputdatadirbtn = tk.Button(self.master, text="Browse", command=self.selectinputdatadir)
        inputdatadirbtn.place(x=540, y=47)
        
        # Filter File
        inputfilefilterlbl = tk.Label(self.master, text="Filter File")
        inputfilefilterlbl.place(x=20, y=100)

        self.inputfilefiltertxtfield = tk.Text(self.master, height=1, width=50)
        self.inputfilefiltertxtfield.place(x=130, y=100)

        inputfilefilterbtn = tk.Button(self.master, text="Browse", command=self.selectfilterfile)
        inputfilefilterbtn.place(x=540, y=97)
        
        # Input Band Number
        inputbandnumberlbl = tk.Label(self.master, text="Selected Band")
        inputbandnumberlbl.place(x=20, y=150)

        self.inputbandnumbertxtfield = tk.Text(self.master, height=1, width=10)
        self.inputbandnumbertxtfield.place(x=130, y=150)
        
        # output Data Dir
        outputdatadirlbl = tk.Label(self.master, text="Output Directory")
        outputdatadirlbl.place(x=20, y=200)

        self.outputdatadirtxtfield = tk.Text(self.master, height=1, width=50)
        self.outputdatadirtxtfield.place(x=130, y=200)

        outputdatadirbtn = tk.Button(self.master, text="Browse", command=self.selectoutputdatadir)
        outputdatadirbtn.place(x=540, y=197)

        # Control Buttons
        self.startdatasubsetbtn = tk.Button(self.master, text="Start Subset", command=self.startsubsetingdata)
        self.startdatasubsetbtn.place(x=250, y=250)
        self.cancelbtn = tk.Button(self.master, text="Cancel", command=self.exit)
        self.cancelbtn.place(x=350, y=250)
        
        
    def exit(self):
        self.master.destroy()

    def selectinputdatadir(self):
        self.inputdatadirpath = tkFileDialog.askdirectory(initialdir="/", title="Select Input Data Directory")
        self.inputdatadirtxtfield.delete(1.0, tk.END)
        self.inputdatadirtxtfield.insert(tk.END, self.inputdatadirpath)
        
    def selectfilterfile(self):
        self.filterfilepath = tkFileDialog.askopenfilename(initialdir="/", title="Select Filter File", filetypes=(("Text File", "*.txt"), ("All Files", "*.*")))
        self.inputfilefiltertxtfield.delete(1.0, tk.END)
        self.inputfilefiltertxtfield.insert(tk.END, self.filterfilepath)
        
    def selectoutputdatadir(self):
        self.outputdatadirpath = tkFileDialog.askdirectory(initialdir="/", title="Select Output Data Directory")
        self.outputdatadirtxtfield.delete(1.0, tk.END)
        self.outputdatadirtxtfield.insert(tk.END, self.outputdatadirpath)
        
    def startsubsetingdata(self):
        print("Filter File: "+self.filterfilepath)
        print("Input Data Directory: "+self.inputdatadirpath)
        print("Output Data Directory: "+self.outputdatadirpath)
        print("Selected Band Number: "+self.inputbandnumbertxtfield.get(1.0, tk.END))
        self.copy_subset_data(self.filterfilepath, self.inputdatadirpath, self.outputdatadirpath, self.inputbandnumbertxtfield.get(1.0, tk.END))
        
    
    def copy_subset_data(self, filter_path, data_source, data_output, band):
        print("I am in copy_subset_data")
        
        print("Passed Filter File: "+filter_path)
        print("Passed Input Data Directory: "+data_source)
        print("Passed Output Data Directory: "+data_output)
        print("Passed Selected Band Number: "+band)
        
        index = 0
        band_str = '*_b0' + str(band) + '*'
        #tiff_list = glob2.iglob(data_source + '/' + band_str + '.tif')
        tiff_list = []
        #print(os.listdir(data_source))
        for file in os.listdir(data_source):
            if file.endswith(".tif") and ("_b0"+str(band)) in file:
                tiff_list.append(file)
                print (file)
        
        print(tiff_list)
        filter = open(filter_path).readlines()
        filter_ids = []
        print("Before First For Loop")
        for i in range(0, len(filter), 4):
            filter_ids.append(filter[i][:7] + '_' + filter[i][8:16] + '_' + filter[i][17:23] + '_' + filter[i][24:27] + '_' + filter[i][28:41])
        print("After First For Loop")
        for i in range(len(tiff_list)):
            if tiff_list[i][1+len(data_source):42+len(data_source)] in filter_ids:
                index += 1
                print index, 'copy band ' + str(band) + ' to: ', data_output + '/' + tiff_list[i][1+len(data_source):25+len(data_source)] + tiff_list[i][86+len(data_source):89+len(data_source)] + '.tif'
                copy2(tiff_list[i],
                      data_output + '/' + tiff_list[i][1 + len(data_source):25 + len(data_source)] + tiff_list[i][86 + len(data_source):89 + len(data_source)] + '.tif')
                
        print(index)
        print("End")