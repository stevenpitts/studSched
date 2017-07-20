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
        self.hereNowFrame.pack()
        self.leavingSoonFrame.pack()
        self.arrivingSoonFrame.pack()
        _thread.start_new_thread(self.alwaysUpdate,tuple())
        self.timeChanged()
        self.pack()
    def alwaysUpdate(self):
        while True:
            newTime = getTimeAsHalfInt()
            timeDifferent = not (self.currentTime == newTime)
            if timeDifferent:
                self.weekday = getWeekdayAsChar()
                self.currentTime = getTimeAsHalfInt()
                self.timeChanged()
            time.sleep(1000)
    def timeChanged(self):
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
        tk.Label(self,text=title).pack()
        self.peopleLabels = []
    def setPeopleList(self,peopleList): #edit for optimality later
        for label in self.peopleLabels:
            label.forget_pack()
        for person in peopleList:
            label = tk.Label(self,text=person)
            self.peopleLabels.append(label)
            label.pack()
            
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
        
thing = Application()
tk.mainloop()