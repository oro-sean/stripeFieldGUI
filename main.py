import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import logging
import datetime

logging.basicConfig(filename='stripeField.log', encoding='utf-8', level=logging.DEBUG)
logging.info('Veering Image Loader Opened')

global ROOT_DIR
global PROJECT_DIR
global FILTER_TYPE
global FILTER_PATH

global PORT_MAIN_CHECK
global STB_MAIN_CHECK
global PORT_JIB_CHECK
global STB_JIB_CHECK
global LOG_CHECK
global EVENT_CHECK

ROOT_DIR = "Mo Directory Selected"
PROJECT_DIR = "No Directory Selected"

class   Make_Project_Directory_Window():
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Make Project Directory")
        self.window.geometry("600x350")
        self.port_main_check_bool = tk.BooleanVar()
        self.stb_main_check_bool = tk.BooleanVar()
        self.port_jib_check_bool = tk.BooleanVar()
        self.stb_jib_check_bool = tk.BooleanVar()
        self.log_check_bool = tk.BooleanVar()
        self.event_check_bool = tk.BooleanVar()
        self.today = datetime.date.today()
        self.year = str(self.today.year)
        self.month = str(self.today.month)
        self.day = str(self.today.day)
        self.root_dir = ROOT_DIR

        ## defne stringVars
        self.root_dir_stringVar = tk.StringVar()
        self.root_dir_stringVar.set("No Directory Selected")

        ## define buttons
        self.close_button = tk.Button(self.window, text="Close", command=self.window.destroy)
        self.create_directory_button = tk.Button(self.window, text="Create Directory", command=self.create_directory)
        self.select_root_dir_button = tk.Button(self.window, text="Select Root Directory", command=self.On_Select_Root_Dir)

        ## define labels
        self.Select_Folders = tk.Label(self.window, text="Select Folders to Generate", font='none 12 bold')
        self.Select_Date = tk.Label(self.window, text="Select Project Date", font='none 12')
        self.Year_label = tk.Label(self.window, text="Year", font='none 12')
        self.Month_label = tk.Label(self.window, text="Month", font='none 12')
        self.Day_label = tk.Label(self.window, text="Day", font='none 12')
        self.root_dir_label = tk.Label(self.window, text="Root Directory", font='none 12 bold')
        self.root_dir_txt = tk.Label(self.window, textvariable=self.root_dir_stringVar, font='none 12')

        ## define combo box
        self.year_strVar = tk.StringVar()
        self.year_combobox = ttk.Combobox(self.window, textvariable=self.year_strVar)
        self.year_combobox['values'] = ('2024', '2025')
        self.year_combobox.state(["readonly"])
        self.year_combobox.current(1)
        self.month_strVar = tk.StringVar()
        self.month_combobox = ttk.Combobox(self.window, textvariable=self.month_strVar)
        self.month_combobox['values'] = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12')
        self.month_combobox.state(["readonly"])
        self.month_combobox.current(int(self.month)-1)
        self.day_strVar = tk.StringVar()
        self.day_combobox = ttk.Combobox(self.window, textvariable=self.day_strVar)
        self.day_combobox['values'] = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31')
        self.day_combobox.state(["readonly"])
        self.day_combobox.current(int(self.day)-1)



        ## define check buttons
        self.port_main_check = tk.Checkbutton(self.window, text="Port Main", variable=self.port_main_check_bool, onvalue=True, offvalue=False)
        self.port_main_check.select()
        self.stb_main_check = tk.Checkbutton(self.window, text=" STB Main", variable=self.stb_main_check_bool, onvalue=True, offvalue=False)
        self.stb_main_check.select()
        self.port_jib_check = tk.Checkbutton(self.window, text="   Port Jib", variable=self.port_jib_check_bool, onvalue=True, offvalue=False)
        self.port_jib_check.select()
        self.stb_jib_check = tk.Checkbutton(self.window, text="    STB Jib", variable=self.stb_jib_check_bool, onvalue=True, offvalue=False)
        self.stb_jib_check.select()
        self.log_check = tk.Checkbutton(self.window, text="        Log", variable=self.log_check_bool, onvalue=True, offvalue=False)
        self.log_check.select()
        self.event_check = tk.Checkbutton(self.window, text="      Event", variable=self.event_check_bool, onvalue=True, offvalue=False)
        self.event_check.select()


        ## grid buttons
        self.root_dir_label.grid(row=0, column=0, padx=10, pady=10)
        self.Select_Folders.grid(row=1, column=0, padx=10, pady=10)
        self.port_main_check.grid(row=2, column=0, padx=10, pady=5)
        self.stb_main_check.grid(row=3, column=0, padx=10, pady=5)
        self.port_jib_check.grid(row=4, column=0, padx=10, pady=5)
        self.stb_jib_check.grid(row=5, column=0, padx=10, pady=5)
        self.log_check.grid(row=6, column=0, padx=10, pady=5)
        self.event_check.grid(row=7, column=0, padx=10, pady=5)
        self.close_button.grid(row=8, column=0)

        self.root_dir_txt.grid(row=0, column=1, padx=10, pady=10)
        self.Select_Date.grid(row=1, column=1, padx=10, pady=10)

        self.Year_label.grid(row=3, column=1, padx=10, pady=5)
        self.Month_label.grid(row=4, column=1, padx=10, pady=5)
        self.Day_label.grid(row=5, column=1, padx=10, pady=5)

        self.create_directory_button.grid(row=8, column=1)

        self.select_root_dir_button.grid(row=0, column=2)
        self.year_combobox.grid(row=3, column=2, padx=10, pady=5)
        self.month_combobox.grid(row=4, column=2, padx=10, pady=5)
        self.day_combobox.grid(row=5, column=2, padx=10, pady=5)

    def create_directory(self):
        print("port main = "+(str(self.port_main_check_bool.get())))
        print("stb main = " + (str(self.stb_main_check_bool.get())))
        print("port jib = " + (str(self.port_jib_check_bool.get())))
        print("stb jib = " + (str(self.stb_jib_check_bool.get())))
        print("log = " + (str(self.log_check_bool.get())))
        print("event = " + (str(self.event_check_bool.get())))

    def On_Select_Root_Dir(self):
            self.root_dir = filedialog.askdirectory()
            self.root_dir_stringVar.set(self.root_dir)
            ROOT_DIR = self.root_dir


class TopFrame():
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)

        ## define class variables
        self.project_dir = PROJECT_DIR

        ## define buttons
        self.select_project_button = tk.Button(self.frame, width=20, text="Select Project Directory", font='none 12 bold', command=self.On_Select_Project_Dir)
        self.make_project_dir_button = tk.Button(self.frame, width=20, text="Make Project Directory", font='none 12 bold', command=self.Open_Make_Project_Dir)

        ## defne stringVars
        self.project_dir_stringVar = tk.StringVar()
        self.project_dir_stringVar.set("No Directory Selected")

        ## define labels
        self.project_dir_label = tk.Label(self.frame, text="Project Directory", font='none 12 bold')
        self.project_dir_txt = tk.Label(self.frame, textvariable=self.project_dir_stringVar, font='none 12')

        ## grid elements
        self.project_dir_label.grid(row=0, column=0)
        self.project_dir_txt.grid(row=0, column=1)
        self.make_project_dir_button.grid(row=0, column=2)
        self.select_project_button.grid(row=0, column=3)

        ## define class functions

    def On_Select_Project_Dir(self):
        try:
            self.project_dir = filedialog.askdirectory()
            self.project_dir_stringVar.set(self.project_dir)
            PROJECT_DIR = self.project_dir

        except Exception as e:
            logging.error(e)
            logging.error('Failed to set project directory')

    def Open_Make_Project_Dir(self):
        Make_Project_Directory_Window()



class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Veering Stripe Field')
        self.geometry('1100x1000')
        self.mainframe = tk.Frame(self)
        self.mainframe.grid(column=0, row=0, sticky='N,W,S,E')
        self.top_frame = TopFrame(self.mainframe)
        self.top_frame.frame.grid(column=0, row=0)

if __name__ == "__main__":
    app = App()
    app.mainloop()

