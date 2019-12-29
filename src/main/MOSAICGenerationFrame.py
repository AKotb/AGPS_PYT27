import os
import tkFileDialog

import xlsxwriter

import Tkinter as tk


class MOSAICGenerationFrame(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("MOSAIC Generation")
        self.pack(fill=tk.BOTH, expand=1)

        inputgracedirlbl = tk.Label(self.master, text="Raw Data Directory")
        inputgracedirlbl.place(x=20, y=50)

        self.inputgracedirtxtfield = tk.Text(self.master, height=1, width=50)
        self.inputgracedirtxtfield.place(x=130, y=50)

        inputgracedirbtn = tk.Button(self.master, text="Browse", command=self.selectgracerawdatadir)
        inputgracedirbtn.place(x=540, y=47)

        self.startgeneratingmonthindexbtn = tk.Button(self.master, text="Generate Month Index",
                                                      command=self.generatemonthindex)
        self.startgeneratingmonthindexbtn.place(x=450, y=200)
        self.cancelbtn = tk.Button(self.master, text="Cancel", command=self.exit)
        self.cancelbtn.place(x=400, y=200)

        self.openmonthindexbtn = tk.Button(self.master, text="Open Month Index", command=self.openmonthindex)
        self.openmonthindexbtn.place(x=50, y=200)
        self.openmonthindexbtn.config(state="disabled")

    def exit(self):
        self.master.destroy()

    def selectgracerawdatadir(self):
        self.inputfilespath = tkFileDialog.askdirectory(initialdir="/", title="Select GRACE Raw Data Directory")
        self.files = os.listdir(self.inputfilespath)
        nooffiles = "No of Files= " + str(len(self.files))
        self.nooffileslbl = tk.Label(self.master, text=nooffiles)
        self.nooffileslbl.place(x=20, y=100)

    def generatemonthindex(self):
        self.cancelbtn.config(state="disabled")
        self.startgeneratingmonthindexbtn.config(state="disabled")
        row = 0;
        self.nextmonth = 'Null';
        self.previousmonth = 'Null';
        self.lastmonth = 'Null';
        workbook = xlsxwriter.Workbook(self.inputfilespath + '/' + 'MonthIndex.xlsx')
        worksheet = workbook.add_worksheet()
        # Add some cell formats.
        format = workbook.add_format()
        format.set_bg_color('#F9F90E')
        # Header
        worksheet.write(0, 0, 'File Name')
        worksheet.write(0, 1, 'From Day')
        worksheet.write(0, 2, 'To Day')
        worksheet.write(0, 3, 'No Of Days')
        worksheet.write(0, 4, 'Month-Year')
        for x in self.files:
            self.successful = False
            while not self.successful:
                if ".gz" in x:
                    row = row + 1
                    try:
                        filename = x.split('.')[0]  # File Name without extension
                        # Data
                        filenameparts = filename.split('_')
                        noofdays = filenameparts[2]  # No of Days
                        fromtodays = filenameparts[1]
                        fromtodaysparts = fromtodays.split('-')
                        fromdaystr = fromtodaysparts[0]
                        fromday = fromdaystr[-3:]  # From Day
                        toDaystr = fromtodaysparts[1]
                        toDay = toDaystr[-3:]  # To Day
                        year = fromdaystr[:-3]  # Year
                        month = 'NaN'
                        fromdayint = int(fromday)
                        todayint = int(toDay)
                        # yearint = int(year)
                        if (fromdayint >= 1) & (todayint <= 34):
                            month = 'Jan'
                        if (fromdayint >= 29) & (todayint <= 60):
                            month = 'Feb'
                        if (fromdayint >= 60) & (todayint <= 104):
                            month = 'Mar'
                        if (fromdayint >= 80) & (todayint <= 131):
                            month = 'Apr'
                        if (fromdayint >= 120) & (todayint <= 152):
                            month = 'May'
                        if (fromdayint >= 143) & (todayint <= 182):
                            month = 'Jun'
                        if (fromdayint >= 180) & (todayint <= 213):
                            month = 'Jul'
                        if (fromdayint >= 211) & (todayint <= 247):
                            month = 'Aug'
                        if (fromdayint >= 242) & (todayint <= 274):
                            month = 'Sep'
                        if (fromdayint >= 273) & (todayint <= 305):
                            month = 'Oct'
                        if (fromdayint >= 289) & (todayint <= 345):
                            month = 'Nov'
                        if (fromdayint >= 333) & (todayint <= 366):
                            month = 'Dec'
                        monthyear = month + '/' + year
                        currentmonth = month
                        # print('Current Month: ' + currentmonth)
                        self.previousmonth = self.getpreviousmonth(currentmonth);
                        # print('Previous Month: '+self.previousmonth)
                        # print('Last Month: ' + self.lastmonth)
                        if row != 1:  # First Record
                            if self.lastmonth == self.previousmonth:
                                worksheet.write(row, 0, filename)
                                worksheet.write(row, 1, fromday)
                                worksheet.write(row, 2, toDay)
                                worksheet.write(row, 3, noofdays)
                                worksheet.write(row, 4, monthyear)
                                self.lastmonth = month;
                                self.successful = True
                            else:
                                if currentmonth == self.lastmonth:  # Duplicated Record
                                    worksheet.write(row, 0, filename)
                                    worksheet.write(row, 1, fromday)
                                    worksheet.write(row, 2, toDay)
                                    worksheet.write(row, 3, noofdays)
                                    worksheet.write(row, 4, monthyear)
                                    self.lastmonth = month;
                                    self.successful = True
                                else:
                                    worksheet.write(row, 0, '', format)
                                    worksheet.write(row, 1, '', format)
                                    worksheet.write(row, 2, '', format)
                                    worksheet.write(row, 3, '', format)
                                    self.nextmonth = self.getnextmonth(self.lastmonth)
                                    if (currentmonth == 'Jan') & (self.lastmonth == 'Nov'):
                                        yearint = int(year)
                                        year = yearint - 1
                                        worksheet.write(row, 4, self.nextmonth + '/' + str(year), format)
                                    else:
                                        worksheet.write(row, 4, self.nextmonth + '/' + year, format)
                                    self.lastmonth = self.nextmonth;
                        else:
                            worksheet.write(row, 0, filename)
                            worksheet.write(row, 1, fromday)
                            worksheet.write(row, 2, toDay)
                            worksheet.write(row, 3, noofdays)
                            worksheet.write(row, 4, monthyear)
                            self.lastmonth = month;
                            self.successful = True
                    except Exception as e:
                        print(e)
                        print "Could not read " + x
                        # continue
                else:
                    print("File " + x + " is not a .gz file")
                    continue
        workbook.close()
        self.openmonthindexbtn.config(state="active")
        self.cancelbtn.config(state="active")

    def getnextmonth(self, currentmonth):
        if (currentmonth == 'Jan'):
            nextmonth = 'Feb'
        if (currentmonth == 'Feb'):
            nextmonth = 'Mar'
        if (currentmonth == 'Mar'):
            nextmonth = 'Apr'
        if (currentmonth == 'Apr'):
            nextmonth = 'May'
        if (currentmonth == 'May'):
            nextmonth = 'Jun'
        if (currentmonth == 'Jun'):
            nextmonth = 'Jul'
        if (currentmonth == 'Jul'):
            nextmonth = 'Aug'
        if (currentmonth == 'Aug'):
            nextmonth = 'Sep'
        if (currentmonth == 'Sep'):
            nextmonth = 'Oct'
        if (currentmonth == 'Oct'):
            nextmonth = 'Nov'
        if (currentmonth == 'Nov'):
            nextmonth = 'Dec'
        if (currentmonth == 'Dec'):
            nextmonth = 'Jan'
        return nextmonth;

    def getpreviousmonth(self, currentmonth):
        if (currentmonth == 'Jan'):
            previousmonth = 'Dec'
        if (currentmonth == 'Feb'):
            previousmonth = 'Jan'
        if (currentmonth == 'Mar'):
            previousmonth = 'Feb'
        if (currentmonth == 'Apr'):
            previousmonth = 'Mar'
        if (currentmonth == 'May'):
            previousmonth = 'Apr'
        if (currentmonth == 'Jun'):
            previousmonth = 'May'
        if (currentmonth == 'Jul'):
            previousmonth = 'Jun'
        if (currentmonth == 'Aug'):
            previousmonth = 'Jul'
        if (currentmonth == 'Sep'):
            previousmonth = 'Aug'
        if (currentmonth == 'Oct'):
            previousmonth = 'Sep'
        if (currentmonth == 'Nov'):
            previousmonth = 'Oct'
        if (currentmonth == 'Dec'):
            previousmonth = 'Nov'
        return previousmonth;

    def openmonthindex(self):
        os.chdir(self.inputfilespath)
        os.system('start excel.exe "%s\\MonthIndex.xlsx"' % (self.inputfilespath,))
