import gzip
import os
import tkFileDialog

import xlsxwriter

import Tkinter as tk
import numpy as np


class TemporalMeanFrame(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("Temporal Mean Calculation")
        self.pack(fill=tk.BOTH, expand=1)

        inputgracedirlbl = tk.Label(self.master, text="Raw Data Directory")
        inputgracedirlbl.place(x=20, y=50)

        self.inputgracedirtxtfield = tk.Text(self.master, height=1, width=50)
        self.inputgracedirtxtfield.place(x=130, y=50)

        inputgracedirbtn = tk.Button(self.master, text="Browse", command=self.selectgracerawdatadir)
        inputgracedirbtn.place(x=540, y=47)

        self.startcalculatingtemporalmeanbtn = tk.Button(self.master, text="Calculate Temporal Mean",
                                                         command=self.calculatetemporalmean)
        self.startcalculatingtemporalmeanbtn.place(x=450, y=200)
        self.cancelbtn = tk.Button(self.master, text="Cancel", command=self.exit)
        self.cancelbtn.place(x=400, y=200)

        self.opentemporalmeanbtn = tk.Button(self.master, text="Open Temporal Mean", command=self.opentemporalmean)
        self.opentemporalmeanbtn.place(x=50, y=200)
        self.opentemporalmeanbtn.config(state="disabled")

    def exit(self):
        self.master.destroy()

    def selectgracerawdatadir(self):
        self.inputfilespath = tkFileDialog.askdirectory(initialdir="/", title="Select GRACE Raw Data Directory")
        self.files = os.listdir(self.inputfilespath)
        nooffiles = "No of Files= " + str(len(self.files))
        self.nooffileslbl = tk.Label(self.master, text=nooffiles)
        self.nooffileslbl.place(x=20, y=100)

    def calculatetemporalmean(self):
        self.cancelbtn.config(state="disabled")
        self.startcalculatingtemporalmeanbtn.config(state="disabled")

        # Creating clm_all & slm_all container (degree x order x num_of_files)
        grace_base = 60  # grace base either 60 or 96
        max_files = 200  # maximum number of files used expected
        clm_all = np.zeros(dtype='f', shape=[grace_base + 1, grace_base + 1, max_files])
        slm_all = np.zeros(dtype='f', shape=[grace_base + 1, grace_base + 1, max_files])
        index = -1
        filenames = []
        if not os.path.exists(self.inputfilespath + '/raw/'):
            os.makedirs(self.inputfilespath + '/raw/')

        if not os.path.exists(self.inputfilespath + '/processed/'):
            os.makedirs(self.inputfilespath + '/processed/')

        workbook = xlsxwriter.Workbook(self.inputfilespath + '/raw/' + 'GRACE Raw Data.xlsx')
        worksheet = workbook.add_worksheet()
        # Header
        # worksheet.write(0, 0, 'Coefficient')
        # worksheet.write(0, 1, 'Degree')
        worksheet.write(0, 0, 'Order')
        worksheet.write(0, 1, 'Degree')
        worksheet.write(0, 2, 'Clm Mean')
        worksheet.write(0, 3, 'Slm Mean')

        for x in self.files:
            if ".gz" in x:
                try:
                    filename = x.split('.')[0]  # File Name without extension
                    filenames.append(filename)
                    with gzip.open(self.inputfilespath + '/' + x, 'rb') as f:
                        file_content = f.read()
                    o = open(self.inputfilespath + '/raw/' + filename + '.txt', 'w')
                    o.write(file_content)
                    o.close()
                except Exception as e:
                    print(e)
                    print "Could not read " + x
                    continue
            else:
                print("File " + x + " is not a .gz file")
                continue

        for x in self.files:
            # print x[6:26]
            if ".gz" in x:
                index += 1
                print "Starting in file:" + x[6:26]
                try:
                    f = gzip.GzipFile(self.inputfilespath + '/' + x, "r")
                    data = f.readlines()[7:]  # read from the line no 7.. you should later add the coeff. (0,0) values

                    for entry in data:
                        tmp = entry.split(' ')
                        m = []
                        for n in tmp:
                            if n != '':
                                m.append(n)
                        clm_all[int(m[1]), int(m[2]), index] = float(m[3])
                        slm_all[int(m[1]), int(m[2]), index] = float(m[4])

                    f.close()

                except:
                    print "Could not open " + x
                    continue

        print index  # counter for num of files processed
        print clm_all.shape
        print slm_all.shape
        # delete all empty layers (more than 163 will be deleted)
        # clm & slm are filled, num of layers = index
        clm_all = clm_all[:, :, 0:index + 1]
        slm_all = slm_all[:, :, 0:index + 1]
        # calculate mean for clm and slm
        clm_mean = np.mean(clm_all, axis=2)
        slm_mean = np.mean(slm_all, axis=2)
        # subtract mean from each layer in clm and slm
        clm_cleaned = np.zeros(dtype='f', shape=[grace_base + 1, grace_base + 1, index + 1])
        slm_cleaned = np.zeros(dtype='f', shape=[grace_base + 1, grace_base + 1, index + 1])

        for layer in range(index + 1):
            clm_cleaned[:, :, layer] = clm_all[:, :, layer] - clm_mean
            slm_cleaned[:, :, layer] = slm_all[:, :, layer] - slm_mean

        count = 1
        for xx in range(0, grace_base + 1):
            for yy in range(0, xx + 1):
                # print "[" + str(xx) + ", " + str(yy) + "]"
                worksheet.write(count, 0, xx)
                worksheet.write(count, 1, yy)
                worksheet.write(count, 2, clm_mean[xx, yy])
                worksheet.write(count, 3, slm_mean[xx, yy])
                count += 1
        workbook.close()

        for i in range(index + 1):
            try:
                o = open(self.inputfilespath + '/processed/' + "filtered.month." + str(i).zfill(3) + '.txt', 'w')
                # o = open(self.inputfilespath + '/processed/' + filenames[i] + '.txt', 'w')
                for xx in range(0, grace_base + 1):
                    for yy in range(0, xx + 1):
                        o.write('{0:6d}'.format(xx) + "  " + '{0:6d}'.format(yy) + "    " + (
                                    '%.8E' % clm_cleaned[xx, yy, i]) + "  " + ('%.8E' % slm_cleaned[xx, yy, i]) + "\n")
                o.close()
            except Exception as e:
                print(e)
                print "Could not read " + x
                continue
        #########################################

        #########################################

        self.opentemporalmeanbtn.config(state="active")
        self.cancelbtn.config(state="active")

    def opentemporalmean(self):
        os.chdir(self.inputfilespath)
        os.system('start excel.exe "%s/raw/GRACE Raw Data.xlsx"' % (self.inputfilespath,))
        # os.system('start excel.exe "%s\\MonthIndex.xlsx"' % (self.inputfilespath,))
