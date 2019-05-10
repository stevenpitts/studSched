import tkinter as tk
import datetime
import time
from tkinter import filedialog, simpledialog
from tkinter import messagebox
import asyncio
import math
import traceback


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
        self.here_now_frame.grid(row=2,column=0,rowspan=2,padx=10,pady=50,sticky='N')
        self.leaving_soon_frame.grid(row=2,column=1,padx=10,pady=50)
        self.arriving_soon_frame.grid(row=3,column=1,padx=10,pady=50)
        self.time_frame.grid(row=1,column=0,columnspan=3,padx=5,pady=15,sticky="N")
        self.time_frame.config(borderwidth=10)
        self.description_frame.grid(row=0,column=0,columnspan=3, padx=5, pady=10, sticky="N")
        self.master.geometry('{}x{}'.format(800,800))
        self.pack()
        print("Steven Pitts\nMade for the TechSpot\nMaku")

    async def always_update(self):
        while True:
            await asyncio.sleep(0.2)
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













class MainFrame(tk.Frame):
    def __init__(self,root=None,*args,**kwargs):
        tk.Frame.__init__(self,root,*args,**kwargs)
        self.file_loaded_string = tk.StringVar()
        self.file_loaded_string.set("No file loaded")
        self.file_loaded_label = tk.Label(self,textvariable=self.file_loaded_string)
        self.master = root
        self.employees_dict = None #Dict of employees that map to a list of tuples of (weekday,timenum) eg ('M',7.5)
        self.load_file_button = tk.Button(self,text="Load People File",command=self.loadPeopleFile)
        self.new_file_button = tk.Button(self,text="Create new People file", command=self.new_people_file)
        self.delete_employee_button = tk.Button(self,text="Remove employee",command=self.removeEmployee)  #delete employee record
        self.employees_filename = None
        self.load_file_button.pack()
        self.new_file_button.pack()
        self.delete_employee_button.pack()
        self.new_employee_button = tk.Button(self,text="New employee",command=self.create_new_employee)
        self.employee_button_frame = tk.Frame(self)
        self.edit_employee_button= tk.Button(self,text="Edit employee hours",command=self.employee_button_frame.pack)
        self.master.geometry('{}x{}'.format(800,800))
        self.save_button = tk.Button(self,text="Save file",command=self.save)
        self.save_and_quit_button = tk.Button(self,text="Save and exit",command=self.save_and_quit)
        self.pack()
    def loadPeopleFile(self): #return (or set variable) to dict if success, else keep as none and throw an error
        filename = filedialog.askopenfilename(parent=self,title="Please open the txt file of the employees.",filetypes=(("Text files","*.txt"),("All files","*.*")))
        if not filename:
            tk.messagebox.showerror('Error', "No file specified")
        with open(filename) as f:
            self.employees_dict = eval(f.read())
        self.employees_filename = filename
        self.load_file_button.pack_forget()
        self.new_file_button.pack_forget()
        buttons = [tk.Button(self.employee_button_frame,text=name,command=lambda name=name:self.edit_employee_hours(name)) for name in self.employees_dict.keys()]
        for button in buttons: button.pack()
        self.new_employee_button.pack()
        self.edit_employee_button.pack()
        self.save_button.pack()
    def new_people_file(self):
        filename = filedialog.asksaveasfilename(title="Where should it be saved?",filetypes=(("Text files","*.txt"),("All files","*.*")))
        self.employees_dict = dict()
        self.employees_filename = filename
        self.load_file_button.pack_forget()
        self.new_file_button.pack_forget()
        self.new_employee_button.pack()
        self.edit_employee_button.pack()
        self.save_button.pack()
    def create_new_employee(self):
        if(self.employees_dict == None):
            tk.messagebox.showwarning("Warning","No file is open")
            return
        name = simpledialog.askstring("Employee name","Please enter the name of the employee")
        self.employees_dict[name] = []
        self.edit_employee_hours(name)
        tk.Button(self.employee_button_frame,text=name,command=lambda:self.edit_employee_hours(name)).pack()
    def removeEmployee(self):#TODO: depricated. remove dictionary enrty
        employee_name = simpledialog.askstring("Employee name","Please enter the name of the employee")
        try:
            for name in employees_dict:
                if name==employee_name:
                    del self.employees_dict[employee_name]
            print("Employee removed")
        except:
            print("employee not found")
    def edit_employee_hours(self,employee_name):
        self.employee_button_frame.pack_forget()
        employee_input_boxes = InputBoxes(self,prev_range_lists_dict=self.employees_dict[employee_name])
        employee_input_boxes.pack()
        close_button = tk.Button(self,text="Save employee hours",command=lambda:self.save_employee_hours(employee_name,employee_input_boxes,close_button)) #Can I pass the button here?
        close_button.pack()
        self.edit_employee_button.pack_forget()
        self.new_employee_button.pack_forget()
    def save_employee_hours(self,employee_name,employee_input_boxes,close_button):
        self.employees_dict[employee_name] = employee_input_boxes.as_range_lists_dict()
        employee_input_boxes.pack_forget()
        close_button.pack_forget()
        self.edit_employee_button.pack()
        self.new_employee_button.pack()
    def save(self):
        with open(self.employees_filename,'w') as f:
            f.write(str(self.employees_dict))
    def save_and_quit(self):
        self.save()
        self.master.quit()
class InputBoxes(tk.Frame):   #input start/end times for shift
    def __init__(self,root,prev_range_lists_dict={},*args,**kwargs):
        tk.Frame.__init__(self,root,*args,**kwargs)
        self.master = root
        self.days_of_week = ["Monday","Tuesday","Wednesday","Thursday","Friday"]
        self.entry_boxes= {day:tk.Entry(self)for day in self.days_of_week}
        for day in self.days_of_week:
            tk.Label(self,text=day+": ").pack()
            self.entry_boxes[day].pack()
            if day in prev_range_lists_dict:
                self.entry_boxes[day].insert(0,self.ranges_as_times(prev_range_lists_dict[day]))

    def time_floats_from_str(self,times:str):
        start_time,end_time=times.split('-')#splits start and end times
        start_time_float = self.time_str_to_float(start_time)
        end_time_float = self.time_str_to_float(end_time)
        return start_time_float,end_time_float
    def times_list_from_day(self,times:str):
        if not times.strip():
            return []
        return [self.time_floats_from_str(timerange) for timerange in times.split(',')
                if times.strip()]
    def time_str_to_float(self,time:str):
        hour,min_with_suffix = time.split(':')
        pm_modifier = 12 if "pm" in time.lower() and int(hour) != 12 else 0
        hour = int(int(hour)+pm_modifier)
        try:
            minute = int(min_with_suffix[:-2])
        except ValueError:
            minute = int(min_with_suffix)
        return hour+(minute/60)

    def time_float_to_str(self,time_float):
        suffix = "PM" if time_float >= 12 else "AM"
        hour = int(time_float)
        if hour > 12: #12 should NOT be included
            hour -= 12
        minute = int((time_float-int(time_float))*60)
        return "{}:{}{}".format(hour,str(minute).zfill(2),suffix)
    def range_as_str(self,range):
        return "{}-{}".format(self.time_float_to_str(range[0]),self.time_float_to_str(range[1]))
    def ranges_as_times(self,ranges):
        return ','.join([self.range_as_str(range) for range in ranges])

    def as_range_lists_dict(self):
        return {day_of_week:self.times_list_from_day(self.entry_boxes[day_of_week].get().replace(' ','')) for day_of_week in self.days_of_week}






def show_error(self, *args):
    tk.messagebox.showerror('Error', traceback.format_exception(*args))


true_root = tk.Tk()
tk.Tk.report_callback_exception = show_error



def main():
    if tk.messagebox.askyesno("Mode Selection","Are you attempting to edit the schedule? ('No' to show the schedule instead)"):
        mainframe = MainFrame(root=true_root)
        tk.mainloop()
    else:
        thing = Application(root=true_root)
        asyncio.run(thing.always_update())
if  __name__ =='__main__':
    try:
        main()
    except Exception as e:
        tk.messagebox.showerror('Error', ''.join(traceback.format_exception(type(e), e, e.__traceback__)))
