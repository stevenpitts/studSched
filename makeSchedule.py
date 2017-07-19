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
        self.employeesFileName = None
        self.loadFileButton.pack()
        self.newFileButton.pack()
        self.newEmployeeButton = tk.Button(self,text="New employee",command=self.createNewEmployee)
        self.employeeButtonFrame = tk.Frame(self)
        self.editEmployeeButton= tk.Button(self,text="Edit employee hours",command=self.employeeButtonFrame.pack)
        self.master.geometry('{}x{}'.format(800,800))
        self.saveButton = tk.Button(self,text="Save file",command=self.save)
        self.pack()
    def loadPeopleFile(self): #return (or set variable) to dict if success, else keep as none and throw an error
        filename = filedialog.askopenfilename(parent=self,title="Please open the txt file of the employees.",filetypes=(("Text files","*.txt"),("All files","*.*")))
        with open(filename) as f:
            self.employeesDict = eval(f.read())
        self.employeesFileName = filename
        self.loadFileButton.pack_forget()
        self.newFileButton.pack_forget()
        buttons = [tk.Button(self.employeeButtonFrame,text=name,command=lambda name=name:self.editEmployeeHours(name)) for name in self.employeesDict.keys()]
        for button in buttons:
            button.pack()
        self.newEmployeeButton.pack()
        self.editEmployeeButton.pack()
        self.saveButton.pack()
        #print(self.employeesDict)
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
    def editEmployeeHours(self,employeeName):
        print(str(employeeName)+" "+str(self.employeesDict[employeeName]))
        self.employeeButtonFrame.pack_forget()
        employeeGrid = ScheduleGrid(self,employeeName=employeeName,employeeList=self.employeesDict[employeeName])
        employeeGrid.pack()
        closeButton = tk.Button(self,text="Save employee hours",command=lambda:self.saveEmployeeHours(employeeName,employeeGrid,closeButton)) #Can I pass the button here?
        closeButton.pack()
        self.editEmployeeButton.pack_forget()
        self.newEmployeeButton.pack_forget()
    def saveEmployeeHours(self,employeeName,scheduleGrid,closeButton):
        self.employeesDict[employeeName] = scheduleGrid.asList()
        scheduleGrid.pack_forget()
        closeButton.pack_forget()
        self.editEmployeeButton.pack()
        self.newEmployeeButton.pack()
    def save(self):
        with open(self.employeesFileName,'w') as f:
            f.write(str(self.employeesDict))
class ScheduleGrid(tk.Frame):
    def __init__(self,root,employeeName=None,employeeList=[],*args,**kwargs):
        tk.Frame.__init__(self,root,*args,**kwargs)
        self.master = root
        self.daysOfWeek = ["Monday","Tuesday","Wednesday","Thursday","Friday"]
        self.daysOfWeekShort = ['M','T','W','R','F']
        self.daysOfWeekLabels = [tk.Label(self,text=dayOfWeek) for dayOfWeek in self.daysOfWeekShort]
        self.times = [float(x)/2 for x in range(14,38)]
        self.timesLabels = [tk.Label(self,text=strFromTime(time)) for time in self.times]
        self.boxes = {(col,row):BoxThing(self,col=col,row=row) for row in range(len(self.times)) for col in range(len(self.daysOfWeek))}
        for i in range(len(self.timesLabels)):
            timeLabel = self.timesLabels[i]
            timeLabel.grid(row=i+1,column=0)
        for i in range(len(self.daysOfWeekLabels)):
            dayLabel = self.daysOfWeekLabels[i]
            dayLabel.grid(row=0,column=i+1)
        for coords in self.boxes:
            box = self.boxes[coords]
            box.grid()
        for coords in employeeList:
            assert coords[0] in self.daysOfWeekShort
            assert coords[1] in self.times
            self.boxes[(self.daysOfWeekShort.index(coords[0]),self.times.index(coords[1]))].activate()
    def asList(self):
        listThing = []
        for box in self.boxes.values():
            if bool(box):
                listThing.append((self.daysOfWeekShort[box.col],self.times[box.row]))
        return listThing
        
class BoxThing:
    def __init__(self,master,col=-1,row=-1):
        self.row = row
        self.col = col
        self.master = master
        self.checkedVal = tk.IntVar()
        self.checkBox = tk.Checkbutton(self.master,variable=self.checkedVal)
    def __bool__(self):
        return (self.checkedVal.get() == 1)
    def grid(self):
        self.checkBox.grid(row=self.row+1,column=self.col+1)
    def activate(self):
        self.checkBox.select()
        assert self.checkedVal.get() == 1
    def deactivate(self):
        self.checkBox.deselect()
        assert self.checkedVal.get() == 0
def strFromTime(time):
    assert float(time*2).is_integer()
    pm = (time >= 12)
    fullHour = (float(time).is_integer())
    hour = math.floor(time)%12
    if (hour==0):
        hour = 12
    noonSwitchString = "PM" if pm else "AM"
    halfHourString = "00" if fullHour else "30"
    timeString = str(hour) + ":" + halfHourString + " " + noonSwitchString
    return timeString
    
    

mainframe = MainFrame()
tk.mainloop()



#Maybe do a dict of day of week to a list of values?