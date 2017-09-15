import tkinter as tk
import datetime
import time
import _thread
from tkinter import filedialog, simpledialog
from tkinter import messagebox
#import conf.py


bfs=10 #base font size

class Application(tk.Frame):
    def __init__(self,root=None,*args,**kwargs):
        tk.Frame.__init__(self,root,*args,**kwargs)
        self.employeeDict = loadPeopleFile(self)
        self.locationDesc = simpledialog.askstring("Location","Please enter a description of this schedule, such as \"Library\"")
        self.weekday = getWeekdayAsChar()
        self.currentTime = getTimeAsHalfInt()
        self.hereNowFrame = PeopleFrame(root=self,title="Here now:")
        self.leavingSoonFrame = PeopleFrame(root=self,title="Leaving soon:")
        self.arrivingSoonFrame = PeopleFrame(root=self,title="Arriving soon:")
        self.timeFrame = TimeFrame(root=self)
        self.descriptionFrame = DescriptionFrame(root=self)
        self.hereNowFrame.grid(row=2,column=0,rowspan=2,padx=50,pady=50,sticky='N')
        self.leavingSoonFrame.grid(row=2,column=1,padx=50,pady=50)
        self.arrivingSoonFrame.grid(row=3,column=1,padx=50,pady=50)
        self.timeFrame.grid(row=1,column=0,columnspan=3,padx=15,pady=15,sticky="N")
        self.timeFrame.config(borderwidth=10)
        self.descriptionFrame.grid(row=0,column=0,columnspan=3, padx=10, pady=10, sticky="N")
        
        
        
        #self.infoButtonCommand = showAboutBox
        #self.infoButtonFrame = tk.Frame(self)
        #self.infoButton = tk.Button(self.infoButtonFrame,text="?", command=lambda:print("8313"))
        #self.infoButtonFrame.grid(row=3,column=1)
        #self.infoButton.pack()
        #print("1")
        _thread.start_new_thread(self.alwaysUpdate,tuple())
        self.timeChanged()
        self.master.geometry('{}x{}'.format(800,800))
        self.pack()
        print("Steven Pitts\nMade for the TechSpot\nMaku")
        #print("2")
    #def showInfoBox(self):
    #    print("ihewofa")
    #    #messagebox.showinfo("About","Steven Pitts\nMade for the TechSpot\nMaku")
        
    def alwaysUpdate(self):
        while True:
            newTime = getTimeAsHalfInt()
            timeDifferent = not (self.currentTime == newTime)
            if timeDifferent:
                self.weekday = getWeekdayAsChar()
                self.currentTime = getTimeAsHalfInt()
                self.timeChanged()
            self.timeFrame.updateTimeFrame()
            time.sleep(0.1)
    def timeChanged(self):
        print("Time has changed")
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
        self.title = tk.StringVar()
        self.title.set(title)
        tk.Label(self,textvariable=self.title,font=("Helvetica", bfs*3)).pack()
        self.peopleLabels = []
    def setPeopleList(self,peopleList): #edit for optimality later
        for label in self.peopleLabels:
            label.pack_forget()
        for person in peopleList:
            label = tk.Label(self,text=person,font=("Courier", bfs*2))
            self.peopleLabels.append(label)
            label.pack()
class DescriptionFrame(tk.Frame):
    def __init__(self,root=None,title="",*args,**kwargs):
        tk.Frame.__init__(self,root,*args,**kwargs)
        self.master = root
        self.descLabel = tk.Label(self,text=self.master.locationDesc,font=("Helvetica", bfs*4))
        self.descLabel.pack()
    
class TimeFrame(tk.Frame):
    def __init__(self,root=None,title="",*args,**kwargs):
        tk.Frame.__init__(self,root,*args,**kwargs)
        self.master = root
        self.dayOfWeekVar = tk.StringVar()
        self.timeVar = tk.StringVar()
        self.dayOfWeekLabel = tk.Label(self,textvariable=self.dayOfWeekVar,font=("Helvetica", bfs*4))
        self.timeLabel = tk.Label(self,textvariable=self.timeVar,font=("fixedsys",bfs*3) )
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
def main():
    root=tk.Tk()
    thing = Application(root=root)
    #print("3")
    root.mainloop()
    #print("4")
if  __name__ =='__main__':main()