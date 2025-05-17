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

ROOT_DIR = "No Directory Selected"
PROJECT_DIR = "No Directory Selected"

PORT_MAIN_CHECK = True
STB_MAIN_CHECK = True
PORT_JIB_CHECK = True
STB_JIB_CHECK = True
LOG_CHECK = True
EVENT_CHECK = True

class   Make_Project_Directory_Window():
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Make Project Directory")
        self.window.geometry("600x350")

        ## define boolean variables
        self.port_main_check_bool = tk.BooleanVar()
        self.stb_main_check_bool = tk.BooleanVar()
        self.port_jib_check_bool = tk.BooleanVar()
        self.stb_jib_check_bool = tk.BooleanVar()
        self.log_check_bool = tk.BooleanVar()
        self.event_check_bool = tk.BooleanVar()

        ## define today's date
        self.today = datetime.date.today()
        self.year = str(self.today.year)
        self.month = str(self.today.month)
        self.day = str(self.today.day)

        ## define directory variables
        self.root_dir = ROOT_DIR
        self.project_dir = PROJECT_DIR
        self.root_dir_selected = False

        ## define stringVars
        self.root_dir_stringVar = tk.StringVar()
        self.root_dir_stringVar.set("No Directory Selected")
        self.year_strVar = tk.StringVar()
        self.month_strVar = tk.StringVar()
        self.day_strVar = tk.StringVar()
        self.project_dir_success_stringVar = tk.StringVar()
        self.project_dir_success_stringVar.set("")

        ## define buttons
        self.close_button = tk.Button(self.window, text="Close", command=self.window.destroy)
        self.create_directory_button = tk.Button(self.window, text="Create Directory", command=self.Create_Directory)
        self.select_root_dir_button = tk.Button(self.window, text="Select Root Directory", command=self.On_Select_Root_Dir)

        ## define labels
        self.root_dir_label = tk.Label(self.window, text="Root Directory", font='none 12 bold')
        self.root_dir_txt = tk.Label(self.window, textvariable=self.root_dir_stringVar, font='none 12')
        self.Select_Folders = tk.Label(self.window, text="Select Folders to Generate", font='none 12 bold')
        self.Select_Date = tk.Label(self.window, text="Select Project Date", font='none 12 bold')
        self.Year_label = tk.Label(self.window, text="Year", font='none 12')
        self.Month_label = tk.Label(self.window, text="Month", font='none 12')
        self.Day_label = tk.Label(self.window, text="Day", font='none 12')
        self.success_label = tk.Label(self.window, textvariable=self.project_dir_success_stringVar, font='none 12 bold')

        ## define combo box

        self.year_combobox = ttk.Combobox(self.window, textvariable=self.year_strVar)
        self.year_combobox['values'] = ('24', '25')
        self.year_combobox.state(["readonly"])
        self.year_combobox.current(1)

        self.month_combobox = ttk.Combobox(self.window, textvariable=self.month_strVar)
        self.month_combobox['values'] = ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12')
        self.month_combobox.state(["readonly"])
        self.month_combobox.current(int(self.month)-1)

        self.day_combobox = ttk.Combobox(self.window, textvariable=self.day_strVar)
        self.day_combobox['values'] = ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31')
        self.day_combobox.state(["readonly"])
        self.day_combobox.current(int(self.day)-1)

        ## define check buttons
        self.port_main_check = tk.Checkbutton(self.window, text="Port Main", variable=self.port_main_check_bool, onvalue=True, offvalue=False)
        if PORT_MAIN_CHECK:
            self.port_main_check.select()
        self.stb_main_check = tk.Checkbutton(self.window, text=" STB Main", variable=self.stb_main_check_bool, onvalue=True, offvalue=False)
        if STB_MAIN_CHECK:
            self.stb_main_check.select()
        self.port_jib_check = tk.Checkbutton(self.window, text="   Port Jib", variable=self.port_jib_check_bool, onvalue=True, offvalue=False)
        if PORT_JIB_CHECK:
            self.port_jib_check.select()
        self.stb_jib_check = tk.Checkbutton(self.window, text="    STB Jib", variable=self.stb_jib_check_bool, onvalue=True, offvalue=False)
        if STB_JIB_CHECK:
            self.stb_jib_check.select()
        self.log_check = tk.Checkbutton(self.window, text="        Log", variable=self.log_check_bool, onvalue=True, offvalue=False)
        if LOG_CHECK:
            self.log_check.select()
        self.event_check = tk.Checkbutton(self.window, text="      Event", variable=self.event_check_bool, onvalue=True, offvalue=False)
        if EVENT_CHECK:
            self.event_check.select()

        ## grid all
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

        self.success_label.grid(row=8, column=2, padx=10, pady=5)

    ## define functions

    def Create_Directory(self):
        global PROJECT_DIR
        global PORT_MAIN_CHECK
        global STB_MAIN_CHECK
        global PORT_JIB_CHECK
        global STB_JIB_CHECK
        global LOG_CHECK
        global EVENT_CHECK
        ## if no root directory selected promt to choose one
        while self.root_dir_selected == False:
            self.On_Select_Root_Dir()
        ## once root directory selected define project folder name
        try:
            self.project_dir = str(self.year_strVar.get())+str(self.month_strVar.get()+str(self.day_strVar.get())) # get project date
            self.path_project_dir = os.path.join(self.root_dir, self.project_dir) # make path combining new folder and root dir
            os.mkdir(self.path_project_dir) # make folder

            self.folder_bool = [self.port_main_check_bool.get(), self.stb_main_check_bool.get(), self.port_jib_check_bool.get(),self.stb_jib_check_bool.get(), self.log_check_bool.get(), self.event_check_bool.get()] # list with true false to create
            self.folder_names = ['portMain', 'stbMain', 'portJib', 'stbJib', 'log', 'event'] # list with folder names
            self.folder_toBuild = [] # list to append folders to make
            for i in range(len(self.folder_names)): # iterate over folders and make "tobuild" list
                if self.folder_bool[i] == True:
                    self.folder_toBuild.append(self.folder_names[i])

            for folder in self.folder_toBuild: # iterate over folders to build and make directories
                os.mkdir(os.path.join(self.path_project_dir, folder))

            PROJECT_DIR = self.path_project_dir # set project dir globally
            PORT_MAIN_CHECK = self.stb_main_check_bool.get()
            STB_MAIN_CHECK = self.stb_main_check_bool.get()
            PORT_JIB_CHECK = self.port_jib_check_bool.get()
            STB_JIB_CHECK = self.stb_jib_check_bool.get()
            LOG_CHECK = self.log_check_bool.get()
            EVENT_CHECK = self.event_check_bool.get()

            self.project_dir_success_stringVar.set("Project Directory Created Successfully")

        except FileExistsError:
            self.project_dir_success_stringVar.set("Project Directory Already Exists")

        except Exception as e:
            logging.error(e)
            logging.error('Failed to create directory')

    def On_Select_Root_Dir(self):
        global ROOT_DIR

        try:
            self.root_dir = filedialog.askdirectory()
            self.root_dir_stringVar.set(self.root_dir)
            ROOT_DIR = self.root_dir
            self.root_dir_selected = True

        except Exception as e:
            logging.error(e)
            logging.error('Failed to set project root directory in make project directory')

class TopFrame():
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)

        ## define boolean variables
        self.port_main_check_bool = tk.BooleanVar()
        self.stb_main_check_bool = tk.BooleanVar()
        self.port_jib_check_bool = tk.BooleanVar()
        self.stb_jib_check_bool = tk.BooleanVar()
        self.log_check_bool = tk.BooleanVar()
        self.event_check_bool = tk.BooleanVar()



        ## define buttons
        self.select_project_button = tk.Button(self.frame, width=20, text="Select Project Directory", font='none 12 bold', command=self.On_Select_Project_Dir)
        self.make_project_dir_button = tk.Button(self.frame, width=20, text="Make Project Directory", font='none 12 bold', command=self.Open_Make_Project_Dir)
        self.port_main_import_button = tk.Button(self.frame, width=20, text="Select Port Main File", font='none 12 bold', command=lambda: self.On_Import_File(self.port_main_import_path), state=tk.NORMAL)
        self.stb_main_import_button = tk.Button(self.frame, width=20, text="Select STB Main File", font='none 12 bold', command=lambda: self.On_Import_File(self.stb_main_import_path), state=tk.NORMAL)
        self.port_jib_import_button = tk.Button(self.frame, width=20, text="Select Port Jib File", font='none 12 bold', command=lambda: self.On_Import_File(self.port_jib_import_path), state=tk.NORMAL)
        self.stb_jib_import_button = tk.Button(self.frame, width=20, text="Select STB Jib File", font='none 12 bold', command=lambda: self.On_Import_File(self.stb_jib_import_path))
        self.import_sail_mp4_button = tk.Button(self.frame, width=20, text="Import Sail .MP4", font='none 12 bold',command=self.On_Import_Sail)
        self.log_import_button = tk.Button(self.frame, width=20, text="Select Log File", font='none 12 bold',command=lambda: self.On_Import_File(self.log_import_path), state=tk.NORMAL)
        self.event_import_button = tk.Button(self.frame, width=20, text="Select Event File", font='none 12 bold',command=lambda: self.On_Import_File(self.event_import_path), state=tk.NORMAL)
        self.logs_process_button = tk.Button(self.frame, width=20, text="Import Log Files", font='none 12 bold',command=self.On_Import_Logs)

        ## defne stringVars
        self.project_dir_stringVar = tk.StringVar()
        self.project_dir_stringVar.set("No Directory Selected")
        self.port_main_import_path = tk.StringVar()
        self.port_main_import_path.set("No File Selected")
        self.stb_main_import_path = tk.StringVar()
        self.stb_main_import_path.set("No File Selected")
        self.port_jib_import_path = tk.StringVar()
        self.port_jib_import_path.set("No File Selected")
        self.stb_jib_import_path = tk.StringVar()
        self.stb_jib_import_path.set("No File Selected")
        self.log_import_path = tk.StringVar()
        self.log_import_path.set("No File Selected")
        self.event_import_path = tk.StringVar()
        self.event_import_path.set("No File Selected")
        self.timezone_port_main = tk.StringVar()
        self.timezone_stb_main = tk.StringVar()
        self.timezone_port_jib = tk.StringVar()
        self.timezone_stb_jib = tk.StringVar()
        self.timestep_port_main = tk.StringVar()
        self.timestep_stb_main = tk.StringVar()
        self.timestep_port_jib = tk.StringVar()
        self.timestep_stb_jib = tk.StringVar()
        self.origin_port_main = tk.StringVar()
        self.origin_stb_main = tk.StringVar()
        self.origin_port_jib = tk.StringVar()
        self.origin_stb_jib = tk.StringVar()
        self.timezone_log = tk.StringVar()
        self.timezone_event = tk.StringVar()
        self.log_type = tk.StringVar()

        ## define combobox
        self.timezone_port_main_combobox = ttk.Combobox(self.frame, textvariable=self.timezone_port_main, width=6)
        self.timezone_stb_main_combobox = ttk.Combobox(self.frame, textvariable=self.timezone_stb_main, width=6)
        self.timezone_port_jib_combobox = ttk.Combobox(self.frame, textvariable=self.timezone_port_jib, width=6)
        self.timezone_stb_jib_combobox = ttk.Combobox(self.frame, textvariable=self.timezone_stb_jib, width=6)
        tz_combo_list = ['-11', '-10', '-09', '-08', '-07', '-06', '-05', '-04', '-03', '-02', '-01', '+00', '+01', '+02', '+03', '+04', '+05', '+06', '+07', '+08', '+09', '+10', '+11']
        self.timezone_port_main_combobox['values'] = tz_combo_list
        self.timezone_port_main_combobox.state(["readonly"])
        self.timezone_port_main_combobox.current(11)
        self.timezone_stb_main_combobox['values'] = tz_combo_list
        self.timezone_stb_main_combobox.state(["readonly"])
        self.timezone_stb_main_combobox.current(11)
        self.timezone_port_jib_combobox['values'] = tz_combo_list
        self.timezone_port_jib_combobox.state(["readonly"])
        self.timezone_port_jib_combobox.current(11)
        self.timezone_stb_jib_combobox['values'] = tz_combo_list
        self.timezone_stb_jib_combobox.state(["readonly"])
        self.timezone_stb_jib_combobox.current(11)
        self.timezone_log_combobox = ttk.Combobox(self.frame, textvariable=self.timezone_log, width=6)
        self.timezone_log_combobox['values'] = tz_combo_list
        self.timezone_log_combobox.state(["readonly"])
        self.timezone_log_combobox.current(11)
        self.timezone_event_combobox = ttk.Combobox(self.frame, textvariable=self.timezone_log, width=6)
        self.timezone_event_combobox['values'] = tz_combo_list
        self.timezone_event_combobox.state(["readonly"])
        self.timezone_event_combobox.current(11)

        self.timestep_port_main_combobox = ttk.Combobox(self.frame, textvariable=self.timestep_port_main, width=6)
        self.timestep_stb_main_combobox = ttk.Combobox(self.frame, textvariable=self.timestep_stb_main, width=6)
        self.timestep_port_jib_combobox = ttk.Combobox(self.frame, textvariable=self.timestep_port_jib, width=6)
        self.timestep_stb_jib_combobox = ttk.Combobox(self.frame, textvariable=self.timestep_stb_jib, width=6)
        ts_combo_list = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '15', '20', '30']
        self.timestep_port_main_combobox['values'] = ts_combo_list
        self.timestep_port_main_combobox.state(["readonly"])
        self.timestep_port_main_combobox.current(5)
        self.timestep_stb_main_combobox['values'] = ts_combo_list
        self.timestep_stb_main_combobox.state(["readonly"])
        self.timestep_stb_main_combobox.current(5)
        self.timestep_port_jib_combobox['values'] = ts_combo_list
        self.timestep_port_jib_combobox.state(["readonly"])
        self.timestep_port_jib_combobox.current(5)
        self.timestep_stb_jib_combobox['values'] = ts_combo_list
        self.timestep_stb_jib_combobox.state(["readonly"])
        self.timestep_stb_jib_combobox.current(5)

        self.origin_port_main_combobox = ttk.Combobox(self.frame, textvariable=self.origin_port_main, width=8)
        self.origin_stb_main_combobox = ttk.Combobox(self.frame, textvariable=self.origin_stb_main, width=8)
        self.origin_port_jib_combobox = ttk.Combobox(self.frame, textvariable=self.origin_port_jib, width=8)
        self.origin_stb_jib_combobox = ttk.Combobox(self.frame, textvariable=self.origin_stb_jib, width=8)
        origin_combo_list = ['EXIF', 'File Name']
        self.origin_port_main_combobox['values'] = origin_combo_list
        self.origin_port_main_combobox.state(["readonly"])
        self.origin_port_main_combobox.current(0)
        self.origin_stb_main_combobox['values'] = origin_combo_list
        self.origin_stb_main_combobox.state(["readonly"])
        self.origin_stb_main_combobox.current(0)
        self.origin_port_jib_combobox['values'] = origin_combo_list
        self.origin_port_jib_combobox.state(["readonly"])
        self.origin_port_jib_combobox.current(1)
        self.origin_stb_jib_combobox['values'] = origin_combo_list
        self.origin_stb_jib_combobox.state(["readonly"])
        self.origin_stb_jib_combobox.current(1)

        self.log_type_combobox = ttk.Combobox(self.frame, textvariable=self.log_type, width=8)
        self.log_type_combobox['values'] = ['Expedition','CSV']
        self.log_type_combobox.state(["readonly"])
        self.log_type_combobox.current(0)

        ## define labels
        self.project_dir_label = tk.Label(self.frame, text="Project Directory", font='none 12 bold')
        self.project_dir_txt = tk.Label(self.frame, textvariable=self.project_dir_stringVar, font='none 12')
        self.port_main_import_label = tk.Label(self.frame, textvariable=self.port_main_import_path, font='none 12')
        self.stb_main_import_label = tk.Label(self.frame, textvariable=self.stb_main_import_path, font='none 12')
        self.port_jib_import_label = tk.Label(self.frame, textvariable=self.port_jib_import_path, font='none 12')
        self.stb_jib_import_label = tk.Label(self.frame, textvariable=self.stb_jib_import_path, font='none 12')
        self.log_import_label = tk.Label(self.frame, textvariable=self.log_import_path, font='none 12')
        self.event_import_label = tk.Label(self.frame, textvariable=self.event_import_path, font='none 12')
        self.sail_header_label_1 = tk.Label(self.frame, text="Sail", font='none 12 bold')
        self.sail_header_label_2 = tk.Label(self.frame, text="Path", font='none 12 bold')
        self.sail_header_label_3 = tk.Label(self.frame, text="Select File", font='none 12 bold')
        self.sail_header_label_4 = tk.Label(self.frame, text="Time Zone (0 if in local time)", font='none 12 bold')
        self.sail_header_label_5 = tk.Label(self.frame, text="Time Step", font='none 12 bold')
        self.sail_header_label_6 = tk.Label(self.frame, text="Time Stepping Origin", font='none 12 bold')
        self.log_header_label_1 = tk.Label(self.frame, text="Log File Type", font='none 12 bold')
        self.log_header_label_2 = tk.Label(self.frame, text="Log File Path", font='none 12 bold')
        self.log_header_label_3 = tk.Label(self.frame, text="Select File", font='none 12 bold')
        self.log_header_label_4 = tk.Label(self.frame, text="Time Zone", font='none 12 bold')

        ## define checkbuttons
        self.port_main_check = tk.Checkbutton(self.frame, text="Port Main", variable=self.port_main_check_bool, onvalue=True, offvalue=False, command=lambda: self.Set_Sources_Used_Togle(0))
        if PORT_MAIN_CHECK:
            self.port_main_check.select()
        self.stb_main_check = tk.Checkbutton(self.frame, text=" STB Main", variable=self.stb_main_check_bool, onvalue=True, offvalue=False, command=lambda: self.Set_Sources_Used_Togle(1))
        if STB_MAIN_CHECK:
            self.stb_main_check.select()
        self.port_jib_check = tk.Checkbutton(self.frame, text="   Port Jib", variable=self.port_jib_check_bool, onvalue=True, offvalue=False, command=lambda: self.Set_Sources_Used_Togle(2))
        if PORT_JIB_CHECK:
            self.port_jib_check.select()
        self.stb_jib_check = tk.Checkbutton(self.frame, text="    STB Jib", variable=self.stb_jib_check_bool, onvalue=True, offvalue=False, command=lambda: self.Set_Sources_Used_Togle(3))
        if STB_JIB_CHECK:
            self.stb_jib_check.select()
        self.log_check = tk.Checkbutton(self.frame, text="        Log", variable=self.log_check_bool, onvalue=True, offvalue=False, command=lambda: self.Set_Sources_Used_Togle(4))
        self.log_check.select()
        self.event_check = tk.Checkbutton(self.frame, text="      Event", variable=self.event_check_bool, onvalue=True, offvalue=False, command=lambda: self.Set_Sources_Used_Togle(5))
        self.event_check.select()

        ## grid elements
        self.project_dir_label.grid(row=1, column=0, padx=10, pady=5)
        self.project_dir_txt.grid(row=1, column=1, padx=10, pady=5)
        self.select_project_button.grid(row=1, column=2, padx=10, pady=5)
        self.make_project_dir_button.grid(row=1, column=3, padx=10, pady=5)

        self.sail_header_label_1.grid(row=2, column=0, padx=10, pady=5)
        self.sail_header_label_2.grid(row=2, column=1, padx=10, pady=5)
        self.sail_header_label_3.grid(row=2, column=2, padx=10, pady=5)
        self.sail_header_label_4.grid(row=2, column=3, padx=10, pady=5)
        self.sail_header_label_5.grid(row=2, column=4, padx=10, pady=5)
        self.sail_header_label_6.grid(row=2, column=5, padx=10, pady=5)

        self.port_main_check.grid(row=3, column=0, padx=10, pady=5)
        self.port_main_import_label.grid(row=3, column=1, padx=10, pady=5)
        self.port_main_import_button.grid(row=3, column=2, padx=10, pady=5)
        self.timezone_port_main_combobox.grid(row=3, column=3, padx=10, pady=5)
        self.timestep_port_main_combobox.grid(row=3, column=4, padx=10, pady=5)
        self.origin_port_main_combobox.grid(row=3, column=5, padx=10, pady=5)

        self.stb_main_check.grid(row=4, column=0, padx=10, pady=5)
        self.stb_main_import_label.grid(row=4, column=1, padx=10, pady=5)
        self.stb_main_import_button.grid(row=4, column=2, padx=10, pady=5)
        self.timezone_stb_main_combobox.grid(row=4, column=3, padx=10, pady=5)
        self.timestep_stb_main_combobox.grid(row=4, column=4, padx=10, pady=5)
        self.origin_stb_main_combobox.grid(row=4, column=5, padx=10, pady=5)

        self.port_jib_check.grid(row=5, column=0, padx=10, pady=5)
        self.port_jib_import_label.grid(row=5, column=1, padx=10, pady=5)
        self.port_jib_import_button.grid(row=5, column=2, padx=10, pady=5)
        self.timezone_port_jib_combobox.grid(row=5, column=3, padx=10, pady=5)
        self.timestep_port_jib_combobox.grid(row=5, column=4, padx=10, pady=5)
        self.origin_port_jib_combobox.grid(row=5, column=5, padx=10, pady=5)

        self.stb_jib_check.grid(row=6, column=0, padx=10, pady=5)
        self.stb_jib_import_label.grid(row=6, column=1, padx=10, pady=5)
        self.stb_jib_import_button.grid(row=6, column=2, padx=10, pady=5)
        self.timezone_stb_jib_combobox.grid(row=6, column=3, padx=10, pady=5)
        self.timestep_stb_jib_combobox.grid(row=6, column=4, padx=10, pady=5)
        self.origin_stb_jib_combobox.grid(row=6, column=5, padx=10, pady=5)

        self.import_sail_mp4_button.grid(row=7, column=3, padx=10, pady=5)

        self.log_header_label_1.grid(row=8, column=0, padx=10, pady=5)
        self.log_header_label_2.grid(row=8, column=1, padx=10, pady=5)
        self.log_header_label_3.grid(row=8, column=2, padx=10, pady=5)
        self.log_header_label_4.grid(row=8, column=3, padx=10, pady=5)

        self.log_check.grid(row=9, column=0, padx=10, pady=5)
        self.log_import_label.grid(row=9, column=1, padx=10, pady=5)
        self.log_import_button.grid(row=9, column=2, padx=10, pady=5)
        self.timezone_log_combobox.grid(row=9, column=3, padx=10, pady=5)
        self.log_type_combobox.grid(row=9, column=4, padx=10, pady=5)

        self.event_check.grid(row=10, column=0, padx=10, pady=5)
        self.event_import_label.grid(row=10, column=1, padx=10, pady=5)
        self.event_import_button.grid(row=10, column=2, padx=10, pady=5)
        self.timezone_event_combobox.grid(row=10, column=3, padx=10, pady=5)

        self.logs_process_button.grid(row=11, column=3, padx=10, pady=5)

        ## define class functions

    def On_Import_Logs(self):
        print('On_Import_Logs')

    def On_Import_Sail(self):
        print("On_Import_Sail")


    def Set_Sources_Used_Togle(self,source):
        global PORT_MAIN_CHECK
        global STB_MAIN_CHECK
        global PORT_JIB_CHECK
        global STB_JIB_CHECK
        global LOG_CHECK
        global EVENT_CHECK

        globalChecks = [PORT_MAIN_CHECK, STB_MAIN_CHECK, PORT_JIB_CHECK, STB_JIB_CHECK, LOG_CHECK, EVENT_CHECK]
        toggles = [self.port_main_check_bool, self.stb_main_check_bool, self.port_jib_check_bool, self.stb_jib_check_bool, self.log_check_bool, self.event_check_bool]
        texts = [self.port_main_import_path, self.stb_main_import_path, self.port_jib_import_path, self.stb_jib_import_path, self.log_import_path, self.event_import_path]
        comboboxes = [[ self.timezone_port_main_combobox, self.timestep_port_main_combobox,self.origin_port_main_combobox],
                      [self.timezone_stb_main_combobox, self.timestep_stb_main_combobox,self.origin_stb_main_combobox],
                      [self.timezone_port_jib_combobox, self.timestep_port_jib_combobox,self.origin_port_jib_combobox],
                      [self.timezone_stb_jib_combobox, self.timestep_stb_jib_combobox,self.origin_stb_jib_combobox],
                      [self.timezone_log_combobox, self.log_type_combobox],
                      [self.timezone_event_combobox]]
        buttons = [self.port_main_import_button, self.stb_main_import_button, self.port_jib_import_button, self.stb_jib_import_button, self.log_import_button, self.event_import_button]

        if toggles[source].get() == False:
            texts[source].set("Disabled")
            globalChecks[source] = False
            buttons[source]['state'] = tk.DISABLED
            for combo in comboboxes[source]:
                combo.state(statespec=["disabled"])
        else:
            texts[source].set("No File Selected")
            globalChecks[source] = True
            buttons[source]['state'] = tk.NORMAL
            for combo in comboboxes[source]:
                combo.state(statespec=["!disabled"])


    def On_Import_File(self,source):
        try:
            self.file_path = filedialog.askdirectory(initialdir='/Users/sean/Downloads')
            if self.file_path:
                source.set(self.file_path)

        except Exception as e:
            logging.error(e)
            logging.error('Failed to set project directory')


    def On_Select_Project_Dir(self):
        global PROJECT_DIR
        global ROOT_DIR

        try:
            if PROJECT_DIR == "No Directory Selected":
                self.project_dir = filedialog.askdirectory()
                if self.project_dir:
                    self.project_dir_stringVar.set(self.project_dir)
                    PROJECT_DIR = self.project_dir

            else:
                self.project_dir = filedialog.askdirectory(initialdir=PROJECT_DIR)
                if self.project_dir:
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

