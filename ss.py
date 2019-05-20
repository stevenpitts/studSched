import tkinter as tk
from datetime import datetime
from tkinter import filedialog, simpledialog
import asyncio
import traceback


BFS = 10  # base font size
DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                "Saturday", "Sunday"]


class Application(tk.Frame):
    def __init__(self, root=None, *args, **kwargs):
        tk.Frame.__init__(self, root, borderwidth=20, relief='ridge',
                          *args, **kwargs)
        self.employee_dict = load_people_file(self)
        self.location_description = simpledialog.askstring(
            "Location",
            r'Please enter a description of this schedule, such as "Library"')
        self.here_now_frame = PeopleFrame(root=self,
                                          title="Here now:")
        self.leaving_soon_frame = PeopleFrame(root=self,
                                              title="Leaving soon:")
        self.arriving_soon_frame = PeopleFrame(root=self,
                                               title="Arriving soon:")
        self.time_label = tk.Label(self, text="", font=("fixedsys", BFS*3))
        self.description_label = tk.Label(self, text=self.location_description,
                                          font=("Helvetica", BFS*4))
        self.here_now_frame.grid(row=2, column=0, rowspan=2, padx=10, pady=50,
                                 sticky='N')
        self.leaving_soon_frame.grid(row=2, column=1, padx=10, pady=50)
        self.arriving_soon_frame.grid(row=3, column=1, padx=10, pady=50)
        self.time_label.grid(row=1, column=0, columnspan=3, padx=5, pady=15,
                             sticky="N")
        self.time_label.config(borderwidth=10)
        self.description_label.grid(row=0, column=0, columnspan=3, padx=5,
                                    pady=10, sticky="N")
        self.master.geometry('800x800')
        self.pack(side='left')
        print("Steven Pitts\nMade for the TechSpot\nMaku")

    async def always_update(self):
        while True:
            try:
                self.update_idletasks()
                self.update()
                self.time_changed()
                self.time_label['text'] = datetime.strftime(datetime.now(),
                                                            '%a %I:%M:%S %p')
            except tk.TclError:
                return

    def time_changed(self):
        now = datetime.now()
        current_time = now.hour + now.minute/60
        current_day = DAYS_OF_WEEK[datetime.today().weekday()]
        here_now_list = []
        leaving_soon_list = []
        arriving_soon_list = []
        # If they're leaving soon, don't include in "here now".
        for person, person_schedule in self.employee_dict.items():
            if current_day not in person_schedule:
                continue
            person_times = person_schedule[current_day]
            for timerange in person_times:
                if timerange[0] < current_time < timerange[1]:
                    if timerange[1] - current_time > 0.5:
                        here_now_list.append(person)
                    else:
                        leaving_soon_list.append(person)
                    break
                elif timerange[0] > current_time > timerange[0] - 0.5:
                    arriving_soon_list.append(person)
        self.here_now_frame.set_people_list(here_now_list)
        self.leaving_soon_frame.set_people_list(leaving_soon_list)
        self.arriving_soon_frame.set_people_list(arriving_soon_list)


class PeopleFrame(tk.Frame):
    def __init__(self, root=None, title="", *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.title = tk.StringVar()
        self.title.set(title)
        tk.Label(self, textvariable=self.title,
                 font=("Helvetica", BFS*3)).pack()
        self.people_labels = []

    def set_people_list(self, people_list):  # edit for optimality later
        for label in self.people_labels:
            label.pack_forget()
            label.destroy()
        self.people_labels = []
        for person in people_list:
            label = tk.Label(self, text=person, font=("Courier", BFS*2))
            self.people_labels.append(label)
            label.pack()


def get_current_time_as_float():
    now = datetime.now()
    return now.hour + now.minute/60


def load_people_file(root):
    filename = filedialog.askopenfilename(
        parent=root, title="Please open the txt file of the employees.",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    with open(filename) as f:
        return eval(f.read())


class MainFrame(tk.Frame):
    def __init__(self, root=None, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.file_loaded_string = tk.StringVar()
        self.file_loaded_string.set("No file loaded")
        self.file_loaded_label = tk.Label(self,
                                          textvariable=self.file_loaded_string)
        self.master = root
        self.employees_dict = None
        # Dict of employees : tuples of (day, time) eg ('M',7.5)
        self.load_file_button = tk.Button(self, text="Load People File",
                                          command=self.load_people_file)
        self.new_file_button = tk.Button(self, text="Create new People file",
                                         command=self.new_people_file)
        self.delete_employee_button = tk.Button(self, text="Remove employee",
                                                command=self.remove_employee)
        self.employees_filename = None
        self.load_file_button.pack()
        self.new_file_button.pack()
        self.delete_employee_button.pack()
        self.new_employee_button = tk.Button(self, text="New employee",
                                             command=self.create_new_employee)
        self.employee_button_frame = tk.Frame(self)
        self.edit_employee_button = tk.Button(
            self, text="Edit employee hours",
            command=self.employee_button_frame.pack)
        self.master.geometry('800x800')
        self.save_button = tk.Button(self,
                                     text="Save file", command=self.save)
        self.save_and_quit_button = tk.Button(self, text="Save and exit",
                                              command=self.save_and_quit)
        self.pack()

    def load_people_file(self):
        filename = filedialog.askopenfilename(
            parent=self, title="Please open the txt file of the employees.",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if not filename:
            tk.messagebox.showerror('Error', "No file specified")
        with open(filename) as f:
            self.employees_dict = eval(f.read())
        self.employees_filename = filename
        self.load_file_button.pack_forget()
        self.new_file_button.pack_forget()
        buttons = [tk.Button(self.employee_button_frame, text=name,
                             command=lambda name=name: self.edit_hours(name))
                   for name in self.employees_dict.keys()]
        for button in buttons:
            button.pack()
        self.new_employee_button.pack()
        self.edit_employee_button.pack()
        self.save_button.pack()

    def new_people_file(self):
        filename = filedialog.asksaveasfilename(
            title="Where should it be saved?",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        self.employees_dict = dict()
        self.employees_filename = filename
        self.load_file_button.pack_forget()
        self.new_file_button.pack_forget()
        self.new_employee_button.pack()
        self.edit_employee_button.pack()
        self.save_button.pack()

    def create_new_employee(self):
        if self.employees_dict is None:
            tk.messagebox.showwarning("Warning", "No file is open")
            return
        name = simpledialog.askstring("Employee name",
                                      "Please enter the name of the employee")
        self.employees_dict[name] = []
        self.edit_hours(name)
        tk.Button(self.employee_button_frame,
                  text=name, command=lambda: self.edit_hours(name)
                  ).pack()

    def remove_employee(self):
        employee_name = simpledialog.askstring(
            "Employee name",
            "Please enter the name of the employee")
        for name in self.employees_dict:
            if name == employee_name:
                self.employees_dict.remove(employee_name)
        print("Employee removed")

    def edit_hours(self, employee_name):
        self.employee_button_frame.pack_forget()
        employee_input_boxes = InputBoxes(
            self, prev_range_lists_dict=self.employees_dict[employee_name])
        employee_input_boxes.pack()
        close_button = tk.Button(self, text="Save employee hours",
                                 command=lambda: self.save_employee_hours(
                                     employee_name, employee_input_boxes,
                                     close_button))
        close_button.pack()
        self.edit_employee_button.pack_forget()
        self.new_employee_button.pack_forget()

    def save_employee_hours(self, employee_name, employee_boxes,
                            close_button):
        self.employees_dict[employee_name] = employee_boxes.as_dict()
        employee_boxes.pack_forget()
        close_button.pack_forget()
        self.edit_employee_button.pack()
        self.new_employee_button.pack()

    def save(self):
        with open(self.employees_filename, 'w') as f:
            f.write(str(self.employees_dict))

    def save_and_quit(self):
        self.save()
        self.master.quit()


class InputBoxes(tk.Frame):  # input start/end times for shift
    def __init__(self, root, prev_range_lists_dict={}, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.master = root
        self.entry_boxes = {day: tk.Entry(self) for day in DAYS_OF_WEEK}
        for day in DAYS_OF_WEEK:
            tk.Label(self, text=day+": ").pack()
            self.entry_boxes[day].pack()
            if day in prev_range_lists_dict:
                self.entry_boxes[day].insert(0, ranges_as_times(
                    prev_range_lists_dict[day]))

    def as_dict(self):
        return {day_of_week:
                times_list_from_day(
                    self.entry_boxes[day_of_week].get().replace(' ', ''))
                for day_of_week in DAYS_OF_WEEK}


def times_list_from_day(times: str):
    if not times.strip():
        return []
    return [time_floats_from_str(timerange)
            for timerange in times.split(',')
            if times.strip()]


def time_floats_from_str(times: str):
    start_time, end_time = times.split('-')  # splits start and end times
    start_time_float = time_str_to_float(start_time)
    end_time_float = time_str_to_float(end_time)
    return start_time_float, end_time_float


def time_str_to_float(timestr: str):
    #  Naming it timestr cuz time is taken. Sue me.
    hour, min_with_suffix = timestr.split(':')
    pm_modifier = 12 if "pm" in timestr.lower() and int(hour) != 12 else 0
    hour = int(int(hour)+pm_modifier)
    try:
        minute = int(min_with_suffix[:-2])
    except ValueError:
        minute = int(min_with_suffix)
    return hour+(minute/60)


def ranges_as_times(ranges):
    return ','.join([range_as_str(range) for range in ranges])


def range_as_str(timespan):
    return "{}-{}".format(time_float_to_str(timespan[0]),
                          time_float_to_str(timespan[1]))


def time_float_to_str(time_float):
    suffix = "PM" if time_float >= 12 else "AM"
    hour = int(time_float)
    if hour > 12:  # 12 should NOT be included
        hour -= 12
    minute = int((time_float-int(time_float))*60)
    return "{}:{}{}".format(hour, str(minute).zfill(2), suffix)


def show_error(_, *args):
    tk.messagebox.showerror('Error', traceback.format_exception(*args))


TRUE_ROOT = tk.Tk()
tk.Tk.report_callback_exception = show_error


def main():
    if tk.messagebox.askyesno("Mode Selection",
                              ("Are you attempting to edit the schedule? "
                               "('No' to show the schedule instead)")):
        MainFrame(root=TRUE_ROOT)
        tk.mainloop()
    else:
        num_screens = simpledialog.askinteger("How many files?",
                                              "How many locations are there?",
                                              minvalue=1, maxvalue=5)
        if not num_screens:
            tk.messagebox.showerror("Error", "Invalid response")
            return
        screens = [Application(root=TRUE_ROOT) for _ in range(num_screens)]

        async def wait_for_application_end():
            screen_tasks = [screen.always_update() for screen in screens]
            await asyncio.gather(*screen_tasks)
        asyncio.run(wait_for_application_end())


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        tk.messagebox.showerror('Error', ''.join(
            traceback.format_exception(type(e), e, e.__traceback__)))
