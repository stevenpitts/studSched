import tkinter as tk
import math
class ScheduleGrid(tk.Frame):
    def __init__(self,root=tk.Tk(),*args,**kwargs):
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
        self.pack()
        tk.mainloop()
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

thing = ScheduleGrid()