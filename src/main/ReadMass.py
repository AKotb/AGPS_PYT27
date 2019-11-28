import exceptions
import os

class FileNotFound(Exception):
    def __init__(self,val):
        self.val = val
    def __str__(self):
        return repr(self.val)

class ReadMonthlyMass:
    ##
    # Initialize the monthly mass constructor 
    # @param filename Filename for the monthly mass file to read
    def __init__(self, filename):
        self.filename = filename ##< Filename of the monthly mass file
        self.topCorner = [9999,-9999] ##< X,Y postion of the top corner point 
    ##
    # Reads the data in the monthly mass file
    def Read(self):
        data = [] ## < Stores file data as a list of lines in the text file

        #if the file exists, read it and store information in data.
        if os.path.exists(self.filename):
            f = open(self.filename,"r")
            data = f.readlines()
            f.close()
        #if it does not exists, throw a FileNotFound Exception
        else:
            raise FileNotFound("Could not find file " + self.filename)
        
        #Parse the file data and return the result
        return self.ParseFile(data)

    ##
    # Parses the data in the file and generates an object with all of the file
    # data to return to the caller
    # @param data Data contained 
    def ParseFile(self,data):
        dataDict = {}
        #for each line in the data file
        for line in data:
            #Check to see if it is a valid line based on our schema
            if self.CheckLine(line) == False:
                #line not valid, continue to next line in file
                continue 
 
            dataDict[str(self.x) + "," + str(self.y)] = self.z
            if self.x < self.topCorner[0] and self.y > self.topCorner[1]:
                self.topCorner = [self.x,self.y]
        return dataDict

            
    ##
    # Checks the validity of a line from the file 
    # @param line A line to check 
    # @return True if the line is valid, false if not valid
    def CheckLine(self,line):
        tmpData = line.split(" ")
        data = []
        for x in tmpData:
            if x != "":
                data.append(x.strip())
        try:
            if len(data) == 3:
                self.x = float(data[0])
                self.y = float(data[1])
                self.z = float(data[2])
                return True
            else:
                return False
        except:
            pass
        return False

#Testing
if __name__ == "__main__":
    testFile = "mass.month.017"
    m = ReadMonthlyMass(testFile)
    d = m.Read()
    assert(d[str(81.500) + "," + str(43.000)] == float("0.39887E+01"))
    

    
        
