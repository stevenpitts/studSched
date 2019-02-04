import tkinter as tk
from tkinter import filedialog, simpledialog
import math
class MainFrame(tk.Frame):
    def __init__(self,root=tk.Tk(),*args,**kwargs):
        tk.Frame.__init__(self,root,*args,**kwargs)
        self.fileLoadedString = tk.StringVar()
        self.fileLoadedString.set("No file loaded")
        self.fileLoadedLabel = tk.Label(self,textvariable=self.fileLoadedString)
        self.master = root
        self.employeesDict = None #Dict of employees that map to a list of tuples of (weekday,timenum) eg ('M',7.5)
        self.loadFileButton = tk.Button(self,text="Load People File",command=self.loadPeopleFile)
        self.newFileButton = tk.Button(self,text="Create new People file", command=self.newPeopleFile)
        self.deleteEmployeeButton = tk.Button(self,text="Remove employee",command=self.removeEmployee)  #delete employee record
        self.employeesFileName = None
        self.loadFileButton.pack()
        self.newFileButton.pack()
        self.deleteEmployeeButton.pack()
        self.newEmployeeButton = tk.Button(self,text="New employee",command=self.createNewEmployee)
        self.employeeButtonFrame = tk.Frame(self)
        self.editEmployeeButton= tk.Button(self,text="Edit employee hours",command=self.employeeButtonFrame.pack)
        self.master.geometry('{}x{}'.format(800,800))
        self.saveButton = tk.Button(self,text="Save file",command=self.save)
        self.saveAndQuitButton = tk.Button(self,text="Save and exit",command=self.saveAndQuit)
        self.pack()
    def loadPeopleFile(self): #return (or set variable) to dict if success, else keep as none and throw an error
        filename = filedialog.askopenfilename(parent=self,title="Please open the txt file of the employees.",filetypes=(("Text files","*.txt"),("All files","*.*")))
        with open(filename) as f:
            self.employeesDict = eval(f.read())
        self.employeesFileName = filename
        self.loadFileButton.pack_forget()
        self.newFileButton.pack_forget()
        buttons = [tk.Button(self.employeeButtonFrame,text=name,command=lambda name=name:self.editEmployeeHours(name)) for name in self.employeesDict.keys()]
        for button in buttons: button.pack()
        self.newEmployeeButton.pack()
        self.editEmployeeButton.pack()
        self.saveButton.pack()
    def newPeopleFile(self):
        filename = filedialog.asksaveasfilename(title="Where should it be saved?",filetypes=(("Text files","*.txt"),("All files","*.*")))
        self.employeesDict = dict()
        self.employeesFileName = filename
        self.loadFileButton.pack_forget()
        self.newFileButton.pack_forget()
        self.newEmployeeButton.pack()
        self.editEmployeeButton.pack()
        self.saveButton.pack()
    def createNewEmployee(self):
        if(self.employeesDict == None):
            tk.messagebox.showwarning("Warning","No file is open")
            return
        name = simpledialog.askstring("Employee name","Please enter the name of the employee")
        self.employeesDict[name] = []
        self.editEmployeeHours(name)
        tk.Button(self.employeeButtonFrame,text=name,command=lambda:self.editEmployeeHours(name)).pack()
    def removeEmployee(self):#TODO: depricated. remove dictionary enrty
        employeeName = simpledialog.askstring("Employee name","Please enter the name of the employee")
        try:
            for name in employeesDict:
                if name==employeeName:
                    del self.employeesDict[employeeName]
            print("Employee removed")
        except:
            print("employee not found")
    def editEmployeeHours(self,employeeName):
        print(str(employeeName)+" "+str(self.employeesDict[employeeName]))
        self.employeeButtonFrame.pack_forget()
        employeeGrid = InputBoxes(self,employeeName=employeeName,employeeList=self.employeesDict[employeeName])
        employeeGrid.pack()
        closeButton = tk.Button(self,text="Save employee hours",command=lambda:self.saveEmployeeHours(employeeName,employeeGrid,closeButton)) #Can I pass the button here?
        closeButton.pack()
        self.editEmployeeButton.pack_forget()
        self.newEmployeeButton.pack_forget()
    def saveEmployeeHours(self,employeeName,InputBoxes,closeButton):
        self.employeesDict[employeeName] = InputBoxes.asList()
        InputBoxes.pack_forget()
        closeButton.pack_forget()
        self.editEmployeeButton.pack()
        self.newEmployeeButton.pack()
    def save(self):
        with open(self.employeesFileName,'w') as f:
            f.write(str(self.employeesDict))
    def saveAndQuit(self):
        self.save()
        self.master.quit()
class InputBoxes(tk.Frame):   #input start/end times for shift
    def __init__(self,root,employeeName=None,employeeList=[],*args,**kwargs):
        tk.Frame.__init__(self,root,*args,**kwargs)
        self.master = root
        self.daysOfWeek = ["Monday","Tuesday","Wednesday","Thursday","Friday"]
        self.daysOfWeekShort = ['M','T','W','R','F']
        self.entryBoxes= {day:tk.Entry(self)for day in self.daysOfWeek}
        for day in self.daysOfWeek:
            tk.Label(self,text=day+": ").pack()
            self.entryBoxes[day].pack()
    def timesList(self,timesString):
        startTime,endTime=timesString.split('-')#splits start and end times
        startHourTemp,startMin=startTime.split(':')#splits start time into hours and minutes
        startSuffix=startMin[-2:]
        startMin=float(startMin[:-2])
        endHourTemp,endMin=endTime.split(':')
        endSuffix=endMin[-2:]
        endMin=float(endMin[:-2])
        startHour=float(startHourTemp)#converts start hours into int
        endHour=float(endHourTemp)
        shiftStart=self.timeConversion(startHour,startMin,startSuffix)
        shiftEnd=self.timeConversion(endHour,endMin,endSuffix)
        shiftDuration=shiftEnd-shiftStart
        shiftDec=startHour+(startMin/60)#time shift begins in decimal format, i.e.: 8:30am=8.5
        shiftList=[shiftDec]#list of start times for each half-hour segment of a shift
        while (shiftDuration>0):
            shiftDuration-=30
            shiftDec+=0.5
            shiftList.append(shiftDec)
        return shiftList
    def timeConversion(self,hour,minute,suffix):#simplifies process of calculating shift times
        if (suffix=="PM"):
            hour+=12
        timeStamp=(hour*60)+minute
        return timeStamp
    def asList(self):
        full_list = []
        for day_of_week_index,day_of_week in enumerate(self.daysOfWeek):
            short_day_of_week = self.daysOfWeekShort[day_of_week_index]
            day_of_week_blocks = self.timesList(self.entryBoxes[day_of_week].get())
            for block in day_of_week_blocks:
                full_list.append((short_day_of_week,block))
        return full_list
    
    

mainframe = MainFrame()
tk.mainloop()



#Maybe do a dict of day of week to a list of values?