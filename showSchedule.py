import tkinter as tk
import datetime
import time
import _thread
from tkinter import filedialog
class Application(tk.Frame):
    def __init__(self,root=tk.Tk(),*args,**kwargs):
        tk.Frame.__init__(self,root,*args,**kwargs)
        self.employeeDict = loadPeopleFile(self)
        self.weekday = getWeekdayAsChar()
        self.currentTime = getTimeAsHalfInt()
        self.hereNowFrame = PeopleFrame(root=self,title="Here now:")
        self.leavingSoonFrame = PeopleFrame(root=self,title="Leaving soon:")
        self.arrivingSoonFrame = PeopleFrame(root=self,title="Arriving soon:")
        self.timeFrame = TimeFrame(root=self)
        self.hereNowFrame.grid(row=1,column=0,rowspan=2,padx=20,pady=20,sticky='N')
        self.leavingSoonFrame.grid(row=1,column=1,padx=20,pady=20)
        self.arrivingSoonFrame.grid(row=2,column=1,padx=20,pady=20)
        self.timeFrame.grid(row=0,column=1,columnspan=3,padx=20,pady=20,sticky="NE")
        self.timeFrame.config(borderwidth=10)
        _thread.start_new_thread(self.alwaysUpdate,tuple())
        self.timeChanged()
        self.master.geometry('{}x{}'.format(800,800))
        self.master.configure(background="#a1dbcd")
        
        self.pack()
    def alwaysUpdate(self):
        while True:
            newTime = getTimeAsHalfInt()
            timeDifferent = not (self.currentTime == newTime)
            if timeDifferent:
                self.weekday = getWeekdayAsChar()
                self.currentTime = getTimeAsHalfInt()
                self.timeChanged()
            self.timeFrame.updateTimeFrame()
            time.sleep(1)
    def timeChanged(self):
        #print("Time has changed")
        timeTuple = (self.weekday,self.currentTime)
        nextTimeTuple = (self.weekday,self.currentTime + 0.5)
        hereNowList = []
        leavingSoonList = []
        arrivingSoonList = []
        #If they're leaving soon, don't include in "here now".
        for person in self.employeeDict.keys():
            personTimes = self.employeeDict[person]
            personHereNow = timeTuple in personTimes
            personHereNext = nextTimeTuple in personTimes
            if personHereNow and personHereNext:
                hereNowList.append(person)
            elif personHereNow and not personHereNext:
                leavingSoonList.append(person)
            elif personHereNext and not personHereNow:
                arrivingSoonList.append(person)
        self.hereNowFrame.setPeopleList(hereNowList)
        self.leavingSoonFrame.setPeopleList(leavingSoonList)
        self.arrivingSoonFrame.setPeopleList(arrivingSoonList)
class PeopleFrame(tk.Frame):
    def __init__(self,root=None,title="",*args,**kwargs):
        tk.Frame.__init__(self,root,*args,**kwargs)
        self.title = title
        tk.Label(self,text=title,font=("Helvetica", 16)).pack()
        self.peopleLabels = []
    def setPeopleList(self,peopleList): #edit for optimality later
        for label in self.peopleLabels:
            label.pack_forget()
        for person in peopleList:
            label = tk.Label(self,text=person)
            self.peopleLabels.append(label)
            label.pack()
class TimeFrame(tk.Frame):
    def __init__(self,root=None,title="",*args,**kwargs):
        tk.Frame.__init__(self,root,*args,**kwargs)
        self.master = root
        self.dayOfWeekVar = tk.StringVar()
        self.timeVar = tk.StringVar()
        self.dayOfWeekLabel = tk.Label(self,textvariable=self.dayOfWeekVar,font=("Helvetica",26))
        self.timeLabel = tk.Label(self,textvariable=self.timeVar,font=("Helvetica",16))
        self.dayOfWeekLabel.pack()
        self.timeLabel.pack()
    def updateTimeFrame(self):
        dayOfWeekPretty,timePretty = getPrettyTime()
        self.dayOfWeekVar.set(dayOfWeekPretty)
        self.timeVar.set(timePretty)
            
def getTimeAsHalfInt():
    now = datetime.datetime.now()
    overHalf = (now.minute > 30)
    hour = now.hour
    if overHalf: hour+=0.5
    return hour
def getWeekdayAsChar():
    intVersion = datetime.datetime.today().weekday()
    weekdays = ['M','T','W','R','F','S','U']
    return weekdays[intVersion]
def loadPeopleFile(root):
    filename = filedialog.askopenfilename(parent=root,title="Please open the txt file of the employees.",filetypes=(("Text files","*.txt"),("All files","*.*")))
    with open(filename) as f:
        return eval(f.read())
def getPrettyTime():
    now = datetime.datetime.now()
    longTime = str(now.hour)+":"+str(now.minute)+":"+str(now.second)
    dayOfWeekInt = datetime.datetime.today().weekday()
    weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    longWeekDay = weekdays[dayOfWeekInt]
    return (longWeekDay,longTime)
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
thing = Application()
tk.mainloop()