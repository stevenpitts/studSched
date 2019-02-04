import tkinter as tk
from tkinter import filedialog, simpledialog
import math
class MainFrame(tk.Frame):
    def __init__(self,root=tk.Tk(),*args,**kwargs):
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
        employee_input_boxes = InputBoxes(self)
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
    def __init__(self,root,*args,**kwargs):
        tk.Frame.__init__(self,root,*args,**kwargs)
        self.master = root
        self.days_of_week = ["Monday","Tuesday","Wednesday","Thursday","Friday"]
        self.days_of_week_short = ['M','T','W','R','F']
        self.entry_boxes= {day:tk.Entry(self)for day in self.days_of_week}
        for day in self.days_of_week:
            tk.Label(self,text=day+": ").pack()
            self.entry_boxes[day].pack()
    def time_floats_from_str(self,times:str):
        start_time,end_time=times.split('-')#splits start and end times
        start_time_float = self.time_str_to_float(start_time)
        end_time_float = self.time_str_to_float(end_time)
        return start_time_float,end_time_float
        #times_list = [
        #return [my_float for my_float in range(start_time_float,end_time_float-0.25,0.5)]
        # startHourTemp,startMin=startTime.split(':')#splits start time into hours and minutes
        # startSuffix=startMin[-2:]
        # startMin=float(startMin[:-2])
        # endHourTemp,endMin=endTime.split(':')
        # endSuffix=endMin[-2:]
        # endMin=float(endMin[:-2])
        # startHour=float(startHourTemp)#converts start hours into int
        # endHour=float(endHourTemp)
        # shiftStart=self.timeConversion(startHour,startMin,startSuffix)
        # shiftEnd=self.timeConversion(endHour,endMin,endSuffix)
        # shiftDuration=shiftEnd-shiftStart
        # shiftDec=startHour+(startMin/60)#time shift begins in decimal format, i.e.: 8:30am=8.5
        # shiftList=[shiftDec]#list of start times for each half-hour segment of a shift
        # while (shiftDuration>0):
        #     shiftDuration-=30
        #     shiftDec+=0.5
        #     shiftList.append(shiftDec)
        # return shiftList
    def times_list_from_day(self,times:str):
        return [self.time_floats_from_str(timerange) for timerange in times.split(',')]
    def time_str_to_float(self,time:str):
        pm_modifier = 12 if "pm" in time.lower() else 0
        hour,min_with_suffix = time.split(':')
        hour = int(hour)+pm_modifier
        minute = int(min_with_suffix[:-2])
        return hour+(minute/60)
        
    def as_range_lists_dict(self):
        return {day_of_week:self.times_list_from_day(self.entry_boxes[day_of_week].get()) for day_of_week in self.days_of_week}
    # def asList(self):
    #     full_list = []
    #     for day_of_week_index,day_of_week in enumerate(self.daysOfWeek):
    #         short_day_of_week = self.daysOfWeekShort[day_of_week_index]
    #         day_of_week_blocks = self.times_list_from_day(self.entryBoxes[day_of_week].get())
    #         for block in day_of_week_blocks:
    #             full_list.append((short_day_of_week,block))
    #     return full_list
    
    

mainframe = MainFrame()
tk.mainloop()



#Maybe do a dict of day of week to a list of values?