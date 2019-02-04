import tkinter as tk
import datetime
import time
from tkinter import filedialog, simpledialog
from tkinter import messagebox
import asyncio


bfs=10 #base font size

class Application(tk.Frame):
    def __init__(self,root=None,*args,**kwargs):
        tk.Frame.__init__(self,root,*args,**kwargs)
        self.employee_dict = load_people_file(self)
        self.location_description = simpledialog.askstring("Location","Please enter a description of this schedule, such as \"Library\"")
        self.here_now_frame = PeopleFrame(root=self,title="Here now:")
        self.leaving_soon_frame = PeopleFrame(root=self,title="Leaving soon:")
        self.arriving_soon_frame = PeopleFrame(root=self,title="Arriving soon:")
        self.time_frame = time_frame(root=self)
        self.description_frame = DescriptionFrame(root=self)
        self.here_now_frame.grid(row=2,column=0,rowspan=2,padx=50,pady=50,sticky='N')
        self.leaving_soon_frame.grid(row=2,column=1,padx=50,pady=50)
        self.arriving_soon_frame.grid(row=3,column=1,padx=50,pady=50)
        self.time_frame.grid(row=1,column=0,columnspan=3,padx=15,pady=15,sticky="N")
        self.time_frame.config(borderwidth=10)
        self.description_frame.grid(row=0,column=0,columnspan=3, padx=10, pady=10, sticky="N")
        self.master.geometry('{}x{}'.format(800,800))
        self.pack()
        print("Steven Pitts\nMade for the TechSpot\nMaku")
        
    async def always_update(self):
        while True:
            try:
                self.update_idletasks()
                self.update()
                self.time_changed()
                self.time_frame.update_time_frame()
            except tk.TclError:
                return
    def time_changed(self):
        current_time = get_current_time_as_float()
        here_now_list = []
        leaving_soon_list = []
        arriving_soon_list = []
        #If they're leaving soon, don't include in "here now".
        for person in self.employee_dict.keys():
            person_times = self.employee_dict[person]
            person_times_today = person_times[get_current_weekday()]
            for person_timerange_today in person_times_today:
                if person_timerange_today[0] < current_time and person_timerange_today[1] > current_time:
                    if person_timerange_today[1] - current_time > 0.5:
                        here_now_list.append(person)
                        break
                    else:
                        leaving_soon_list.append(person)
                        break
                elif person_timerange_today[0] > current_time and person_timerange_today[0] - current_time < 0.5:
                    arriving_soon_list.append(person)
        self.here_now_frame.set_people_list(here_now_list)
        self.leaving_soon_frame.set_people_list(leaving_soon_list)
        self.arriving_soon_frame.set_people_list(arriving_soon_list)
class PeopleFrame(tk.Frame):
    def __init__(self,root=None,title="",*args,**kwargs):
        tk.Frame.__init__(self,root,*args,**kwargs)
        self.title = tk.StringVar()
        self.title.set(title)
        tk.Label(self,textvariable=self.title,font=("Helvetica", bfs*3)).pack()
        self.people_labels = []
    def set_people_list(self,people_list): #edit for optimality later
        for label in self.people_labels:
            label.pack_forget()
        for person in people_list:
            label = tk.Label(self,text=person,font=("Courier", bfs*2))
            self.people_labels.append(label)
            label.pack()
class DescriptionFrame(tk.Frame):
    def __init__(self,root=None,title="",*args,**kwargs):
        tk.Frame.__init__(self,root,*args,**kwargs)
        self.master = root
        tk.Label(self,text=self.master.location_description,font=("Helvetica", bfs*4)).pack()
    
class time_frame(tk.Frame):
    def __init__(self,root=None,title="",*args,**kwargs):
        tk.Frame.__init__(self,root,*args,**kwargs)
        self.master = root
        self.day_of_week_label = tk.Label(self,text='hi',font=("Helvetica", bfs*4))
        self.time_label = tk.Label(self,text="",font=("fixedsys",bfs*3) )
        self.day_of_week_label.pack()
        self.time_label.pack()
    def update_time_frame(self):
        self.day_of_week_label['text'], self.time_label['text'] = get_pretty_time()
def get_current_time_as_float():
    now = datetime.datetime.now()
    return now.hour + now.minute/60
def get_current_weekday():
    int_version = datetime.datetime.today().weekday()
    weekdays = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    return weekdays[int_version]
def load_people_file(root):
    filename = filedialog.askopenfilename(parent=root,title="Please open the txt file of the employees.",filetypes=(("Text files","*.txt"),("All files","*.*")))
    with open(filename) as f:
        return eval(f.read())
def get_pretty_time():
    now = datetime.datetime.now()
    longTime = str(now.hour)+":"+str(now.minute)+":"+str(now.second)
    return (get_current_weekday(),longTime)
def main():
    root=tk.Tk()
    thing = Application(root=root)
    asyncio.run(thing.always_update())
if  __name__ =='__main__':main()