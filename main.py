import os
import tkinter as tk
from tkinter import filedialog, StringVar
from tkinter import ttk
import logging
import datetime
import shutil
from tkinter.constants import ACTIVE

import veeringVideo
import veeringLogs

logging.basicConfig(filename='stripeField.log', encoding='utf-8', level=logging.DEBUG)
logging.info('Veering Image Loader Opened')

class   Make_Project_Directory_Window(tk.Toplevel):
    def __init__(self,master):
        super().__init__(master)
        self.title("Make Project Directory")
        self.geometry("600x350")

        ## define boolean variables
        self.port_main_check_bool = tk.BooleanVar()
        self.stb_main_check_bool = tk.BooleanVar()
        self.port_jib_check_bool = tk.BooleanVar()
        self.stb_jib_check_bool = tk.BooleanVar()
        self.log_check_bool = tk.BooleanVar()
        self.event_check_bool = tk.BooleanVar()
        self.root_dir_selected = tk.BooleanVar()
        self.root_dir_selected.set(False)

        ## define today's date
        self.today = datetime.date.today()
        self.year = str(self.today.year)
        self.month = str(self.today.month)
        self.day = str(self.today.day)

        ## define stringVars
        self.root_dir_stringVar = tk.StringVar()
        self.root_dir_stringVar.set("No Directory Selected")
        self.year_strVar = tk.StringVar()
        self.month_strVar = tk.StringVar()
        self.day_strVar = tk.StringVar()
        self.project_dir_success_stringVar = tk.StringVar()
        self.project_dir_success_stringVar.set("")
        self.project_dir_stringVar = tk.StringVar()

        ## define buttons
        self.close_button = tk.Button(self, text="Close", command=self.destroy)
        self.create_directory_button = tk.Button(self, text="Create Directory", command=self.Create_Directory)
        self.select_root_dir_button = tk.Button(self, text="Select Root Directory", command=self.On_Select_Root_Dir)

        ## define labels
        self.root_dir_label = tk.Label(self, text="Root Directory", font='none 12 bold')
        self.root_dir_txt = tk.Label(self, textvariable=self.root_dir_stringVar, font='none 12')
        self.Select_Folders = tk.Label(self, text="Select Folders to Generate", font='none 12 bold')
        self.Select_Date = tk.Label(self, text="Select Project Date", font='none 12 bold')
        self.Year_label = tk.Label(self, text="Year", font='none 12')
        self.Month_label = tk.Label(self, text="Month", font='none 12')
        self.Day_label = tk.Label(self, text="Day", font='none 12')
        self.success_label = tk.Label(self, textvariable=self.project_dir_success_stringVar, font='none 12 bold')

        ## define combo box
        self.year_combobox = ttk.Combobox(self, textvariable=self.year_strVar)
        self.year_combobox['values'] = ('24', '25')
        self.year_combobox.state(["readonly"])
        self.year_combobox.current(1)

        self.month_combobox = ttk.Combobox(self, textvariable=self.month_strVar)
        self.month_combobox['values'] = ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12')
        self.month_combobox.state(["readonly"])
        self.month_combobox.current(int(self.month)-1)

        self.day_combobox = ttk.Combobox(self, textvariable=self.day_strVar)
        self.day_combobox['values'] = ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31')
        self.day_combobox.state(["readonly"])
        self.day_combobox.current(int(self.day)-1)

        ## define check buttons
        self.port_main_check = tk.Checkbutton(self, text="Port Main", variable=self.port_main_check_bool, onvalue=True, offvalue=False)
        self.port_main_check.select()
        self.stb_main_check = tk.Checkbutton(self, text=" STB Main", variable=self.stb_main_check_bool, onvalue=True, offvalue=False)
        self.stb_main_check.select()
        self.port_jib_check = tk.Checkbutton(self, text="   Port Jib", variable=self.port_jib_check_bool, onvalue=True, offvalue=False)
        self.port_jib_check.select()
        self.stb_jib_check = tk.Checkbutton(self, text="    STB Jib", variable=self.stb_jib_check_bool, onvalue=True, offvalue=False)
        self.stb_jib_check.select()
        self.log_check = tk.Checkbutton(self, text="        Log", variable=self.log_check_bool, onvalue=True, offvalue=False)
        self.log_check.select()
        self.event_check = tk.Checkbutton(self, text="      Event", variable=self.event_check_bool, onvalue=True, offvalue=False)
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
                if self.folder_bool[i]:
                    self.folder_toBuild.append(self.folder_names[i])

            for folder in self.folder_toBuild: # iterate over folders to build and make directories
                os.mkdir(os.path.join(self.path_project_dir, folder))

            self.project_dir_success_stringVar.set("Project Directory Created Successfully")
            self.project_dir_stringVar.set(self.path_project_dir)

        except FileExistsError:
            self.project_dir_success_stringVar.set("Project Directory Already Exists")
            self.project_dir_stringVar.set(self.path_project_dir)

        except Exception as e:
            logging.error(e)
            logging.error('Failed to create directory')

    def On_Select_Root_Dir(self):

        try:
            self.root_dir = filedialog.askdirectory(initialdir='/Users/sean/mbp_storage')
            self.root_dir_stringVar.set(self.root_dir)
            self.root_dir_selected = True

        except Exception as e:
            logging.error(e)
            logging.error('Failed to set project root directory in make project directory')

class   Import_Frame_Header(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.column_min_width = 160
        ## define buttons
        self.select_project_button = tk.Button(self, width=20, text="Select Project Directory", font='none 12 bold', command=self.On_Select_Project_Dir)
        self.make_project_dir_button = tk.Button(self, width=20, text="Make Project Directory", font='none 12 bold', command=self.Open_Make_Project_Dir)

        ## defne stringVars
        self.project_dir_stringVar = tk.StringVar()
        self.project_dir_stringVar.set("No Directory Selected")

        ## define bools
        self.port_main_check_bool = tk.BooleanVar()
        self.port_main_check_bool.set(True)
        self.stb_main_check_bool = tk.BooleanVar()
        self.stb_main_check_bool.set(True)
        self.port_jib_check_bool = tk.BooleanVar()
        self.port_jib_check_bool.set(True)
        self.stb_jib_check_bool = tk.BooleanVar()
        self.stb_jib_check_bool.set(True)
        self.log_check_bool = tk.BooleanVar()
        self.log_check_bool.set(True)
        self.event_check_bool = tk.BooleanVar()
        self.event_check_bool.set(True)

        ## define Labels
        self.import_header_label = tk.Label(self, text="Define Project Directory", font='none 14 bold')
        self.project_dir_label = tk.Label(self, text="Project Directory", font='none 12 bold')
        self.project_dir_txt = tk.Label(self, textvariable=self.project_dir_stringVar, font='none 12')

        ## grid elements
        self.import_header_label.grid(row=0, column=0, columnspan=4)
        self.project_dir_label.grid(row=1, column=0)
        self.project_dir_txt.grid(row=1, column=1)
        self.select_project_button.grid(row=1, column=2)
        self.make_project_dir_button.grid(row=1, column=3)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1, minsize=self.column_min_width)

        ## bind events


    def On_Select_Project_Dir(self):
        try:
            if self.project_dir_stringVar.get() == "No Directory Selected":
                self.project_dir = filedialog.askdirectory(initialdir='/Users/sean/mbp_storage')
                if self.project_dir:
                    self.project_dir_stringVar.set(self.project_dir)
            else:
                self.project_dir = filedialog.askdirectory(initialdir='/Users/sean/mbp_storage')
                if self.project_dir:
                    self.project_dir_stringVar.set(self.project_dir)
        except Exception as e:
            logging.error(e)
            logging.error('Failed to set project directory')


    def Open_Make_Project_Dir(self):
        self.Proj_Window = Make_Project_Directory_Window(self)
        self.Proj_Window.project_dir_stringVar.trace('w', self.Update_From_Proj_window)
        self.Proj_Window.port_main_check_bool.trace('w', self.Update_From_Proj_window)
        self.Proj_Window.stb_main_check_bool.trace('w', self.Update_From_Proj_window)
        self.Proj_Window.port_jib_check_bool.trace('w', self.Update_From_Proj_window)
        self.Proj_Window.stb_jib_check_bool.trace('w', self.Update_From_Proj_window)
        self.Proj_Window.log_check_bool.trace('w', self.Update_From_Proj_window)
        self.Proj_Window.event_check_bool.trace('w', self.Update_From_Proj_window)

    def Update_From_Proj_window(self,*args):
        self.project_dir_stringVar.set(self.Proj_Window.project_dir_stringVar.get())
        self.port_main_check_bool.set(self.Proj_Window.port_main_check_bool.get())
        self.stb_main_check_bool.set(self.Proj_Window.stb_main_check_bool.get())
        self.port_jib_check_bool.set(self.Proj_Window.port_jib_check_bool.get())
        self.stb_jib_check_bool.set(self.Proj_Window.stb_jib_check_bool.get())
        self.log_check_bool.set(self.Proj_Window.log_check_bool.get())
        self.event_check_bool.set(self.Proj_Window.event_check_bool.get())

class   Import_Frame_Source(tk.Frame):
    def __init__(self, master, check_bool_pre, source_name, source_type):
        super().__init__(master)
        ## define grid column width
        self.column_min_width = 160

        ## define bools
        self.check_bool = check_bool_pre

        ## define buttons
        self.import_button = tk.Button(self, width=15, text=str(source_name)+" Select File", font='none 12 bold', command=self.On_Import_File, state=tk.NORMAL)

        ## define stringVars
        self.import_path = tk.StringVar()
        self.import_path.set("No File Selected")
        self.timezone = tk.StringVar()
        self.timestep = tk.StringVar()
        self.origin = tk.StringVar()
        self.file_name_entry = tk.StringVar()
        self.file_name_check_return = tk.StringVar()
        self.file_name_check_return.set("YYMMDD_HHMMSS")
        self.log_type = tk.StringVar()

        ## define combo
        tz_combo_list = ['-11', '-10', '-09', '-08', '-07', '-06', '-05', '-04', '-03', '-02', '-01', '+00', '+01',
                         '+02', '+03', '+04', '+05', '+06', '+07', '+08', '+09', '+10', '+11']
        self.timezone_combobox = self.Create_Combo(text_variable=self.timezone, combo_list=tz_combo_list, state_pre=["readonly"], current_value=11)

        ts_combo_list = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '15', '20', '30']
        self.timestep_combobox = self.Create_Combo(text_variable=self.timestep, combo_list=ts_combo_list, state_pre=["readonly"], current_value=5)

        origin_combo_list = ['EXIF', 'File Name']
        self.origin_combobox = self.Create_Combo(text_variable=self.origin, combo_list=origin_combo_list, state_pre=["readonly"], current_value=0)

        log_type_combo_list = ['Expedition', 'CSV', 'XML']
        self.log_type_combo = self.Create_Combo(text_variable=self.log_type, combo_list=log_type_combo_list, state_pre=["readonly"], current_value=0)

        ## define labels
        self.import_label = tk.Label(self, textvariable=self.import_path, font='none 12', width=20)
        self.import_label.configure(wraplength=self.column_min_width)
        self.file_name_check_label = tk.Label(self, textvariable=self.file_name_check_return, font='none 12')

        ## define checkboxes
        self.check = tk.Checkbutton(self, text=source_name, variable=self.check_bool, onvalue=True, offvalue=False, command=self.Set_Sources_Used_Togle)

        ## define entry box
        self.file_name_entry_box = tk.Entry(self, textvariable=self.file_name_entry, validate='focus', validatecommand=self.Check_Manual_File_Name, width=20)

        ## bind events
        self.origin_combobox.bind('<<ComboboxSelected>>', self.Set_Sources_Used_Togle)
        self.check_bool.trace('w', self.Set_Sources_Used_Togle)
        self.file_name_entry_box.bind('<Key>', self.Check_Manual_File_Name)
        self.file_name_entry_box.bind('<FocusOut>', self.Check_Manual_File_Name)

        ## grid elements
        self.Grid_Elements(source_type)

        self.Set_Sources_Used_Togle()

        ## define functions
    def On_Import_File(self):
        try:
            file_path = filedialog.askopenfilename(initialdir='/Users/sean/Downloads')
            if file_path:
                self.import_path.set(file_path)
        except Exception as e:
            logging.error(e)
            logging.error('Failed to set project directory')

    def Check_Manual_File_Name(self,*args):
        if len(self.file_name_entry.get()) != 15:
            self.file_name_check_return.set("Length Fails")
            return False
        elif not self.file_name_entry.get()[0:8].isdigit():
            self.file_name_check_return.set("Not Digits")
            return False
        elif not self.file_name_entry.get()[9:].isdigit():
            self.file_name_check_return.set("Not Digits")
            return False
        else:
            self.file_name_check_return.set("Valid")
            return True

    def Set_Sources_Used_Togle(self,*args):
        if self.check_bool.get() == False:
            self.import_path.set("Disabled")
            self.import_button.configure(state=tk.DISABLED)
            for combo in [self.timezone_combobox, self.timestep_combobox, self.origin_combobox]:
                combo.configure(state=tk.DISABLED)
            self.file_name_entry_box.configure(state=tk.DISABLED)
            self.file_name_check_return.set("")
        else:
            if self.import_path.get() == "Disabled":
                self.import_path.set("No File Selected")
            self.import_button.configure(state=tk.NORMAL)
            for combo in [self.timezone_combobox, self.timestep_combobox, self.origin_combobox]:
                combo.configure(state=tk.NORMAL)
            if self.origin.get() == "EXIF":
                self.file_name_entry_box.configure(state=tk.DISABLED)
                self.file_name_check_return.set("")
            else:
                self.file_name_entry_box.configure(state=tk.NORMAL)
                self.file_name_check_return.set("YYMMDD_HHMMSS")

    ## define widget builders
    def Create_Combo(self,text_variable, combo_list, state_pre,current_value):
        combo = ttk.Combobox(self, textvariable=text_variable, width=6)
        combo['values'] = combo_list
        combo['state'] = state_pre
        combo.current(current_value)
        return combo

    def Grid_Elements(self, source_type):
        self.check.grid(row=0, column=0)
        self.import_label.grid(row=0, column=1)
        self.import_button.grid(row=0, column=2)
        self.timezone_combobox.grid(row=0, column=3)
        if source_type == "sail":
            self.timestep_combobox.grid(row=0, column=4)
            self.origin_combobox.grid(row=0, column=5)
            self.file_name_entry_box.grid(row=0, column=6)
            self.file_name_check_label.grid(row=0, column=7)
            for i in range(8):
                self.grid_columnconfigure(i, weight=1, minsize=self.column_min_width)
        elif source_type == "file":
            self.log_type_combo.grid(row=0, column=4)
            for i in range(5):
                self.grid_columnconfigure(i, weight=1, minsize=self.column_min_width)

class   ImportFrame(tk.Frame):
    def __init__(self,master):
        super().__init__(master)

        ## define frames for screen sections
        self.sails = tk.Frame(self)
        self.files = tk.Frame(self)
        self.buttons = tk.Frame(self)
        ## define custom elements
        self.header_frame = Import_Frame_Header(self)
        self.port_main = Import_Frame_Source(self.sails, check_bool_pre=self.header_frame.port_main_check_bool, source_name="Port Main", source_type="sail")
        self.stb_main = Import_Frame_Source(self.sails, check_bool_pre=self.header_frame.stb_main_check_bool, source_name="Stb Main", source_type="sail")
        self.port_jib = Import_Frame_Source(self.sails, check_bool_pre=self.header_frame.port_jib_check_bool, source_name="Port JIB", source_type="sail")
        self.stb_jib = Import_Frame_Source(self.sails, check_bool_pre=self.header_frame.stb_jib_check_bool, source_name="Stb JIB", source_type="sail")
        self.log = Import_Frame_Source(self.files, check_bool_pre=self.header_frame.log_check_bool, source_name="Log", source_type="file")
        self.event = Import_Frame_Source(self.files, check_bool_pre=self.header_frame.event_check_bool, source_name="Event", source_type="file")

        ## define bools
        self.use_port_as_stb = tk.BooleanVar()
        self.use_port_as_stb.set(True)

        ## define stringVars
        self.log_path_final_stringVar = tk.StringVar()
        self.log_path_final_stringVar.set("Log File Not Selected")
        self.event_path_final_stringVar = tk.StringVar()
        self.event_path_final_stringVar.set("Event File Not Selected")


        ## define buttons
        self.import_sail_mp4_button = tk.Button(self.buttons, width=20, text="Import Sail .MP4", font='none 12 bold',command=self.On_Import_Sail)
        self.logs_process_button = tk.Button(self.buttons, width=20, text="Import Log Files", font='none 12 bold',command=self.On_Import_Logs)

        ## define checkbuttons
        self.use_port_as_stb_check = tk.Checkbutton(self.buttons, text="Use Port Jib for STB Jib", variable=self.use_port_as_stb, onvalue=True, offvalue=False, command=self.On_Use_Port_for_Stb)

        ## define labels
        self.sail_header_frame = self.Create_Labels(self.sails,["sail", "Import Path", "Select Directory", "Time Zone", "Time Step", "Time Origin", "Enter Manual File Name", "File Name Check"])
        self.data_header_frame = self.Create_Labels(self.files,["Data Source", "Import Path", "Select Directory", "Time Zone", "File Type"])

        ## grid elements
        self.Grid_Elements()

        ## bind events to update variables



        ## define functions
    def On_Use_Port_for_Stb(self):
        if self.use_port_as_stb.get():
            self.stb_jib.import_path.set(self.port_jib.import_path.get())
            self.stb_jib.timezone.set(self.port_jib.timezone.get())
            self.stb_jib.timestep.set(self.port_jib.timestep.get())
            self.stb_jib.origin.set(self.port_jib.origin.get())
            self.stb_jib.file_name_entry.set(self.port_jib.file_name_entry.get())


        ## define widget builders

    def Create_Labels(self,parent, text):
        frame = tk.Frame(parent)
        labels = []
        for i in range(len(text)):
            labels.append(tk.Label(frame, text=text[i], font='none 12 bold', width=15))

        for i in range(len(text)):
            labels[i].grid(row = 0, column=i)
            frame.columnconfigure(i, weight=1, minsize=self.header_frame.column_min_width)

        return frame

    def Grid_Elements(self):
        self.sail_header_frame.grid(column=0, row=0, columnspan=8)
        self.port_main.grid(column=0, row=1, columnspan=8)
        self.stb_main.grid(column=0, row=2, columnspan=8)
        self.port_jib.grid(column=0, row=3, columnspan=8)
        self.stb_jib.grid(column=0, row=4, columnspan=8)
        for i in range(8):
            self.sails.grid_columnconfigure(i, weight=1, minsize=self.port_main.column_min_width)

        self.data_header_frame.grid(column=0, row=0, columnspan=5)
        self.log.grid(column=0, row=1, columnspan=5)
        self.event.grid(column=0, row=2, columnspan=5)
        for i in range(5):
            self.files.grid_columnconfigure(i, weight=1, minsize=self.port_main.column_min_width)

        self.use_port_as_stb_check.grid(column=0, row=0, columnspan=2)
        self.import_sail_mp4_button.grid(column=0, row=1, columnspan=2)
        self.logs_process_button.grid(column=0, row=2, columnspan=2)
        for i in range(2):
            self.buttons.grid_columnconfigure(i, weight=1, minsize=self.port_main.column_min_width)

        self.header_frame.grid(column=0, row=0, columnspan=4, rowspan=2, padx=10, pady=10)
        self.sails.grid(column=0, row=2, columnspan=8, rowspan=5, padx=10, pady=10)
        self.files.grid(column=0, row=7, columnspan=5, rowspan=3, padx=10, pady=10)
        self.buttons.grid(column=0, row=10, columnspan=2, rowspan=3, padx=10, pady=10)
        for i in range(8):
            self.grid_columnconfigure(i, weight=1, minsize=self.port_main.column_min_width)

    def On_Import_Logs(self):
        if self.log.check_bool.get()==True:
            try:
                if self.log.log_type.get()=='csv':
                    newPath = os.path.join(self.header_frame.project_dir_stringVar.get(), "log", "log.csv")
                else:
                    newPath = os.path.join(self.header_frame.project_dir_stringVar.get(), "log", "exp.csv")
                shutil.copy(self.log.import_path.get(), newPath)
                self.log_path_final_stringVar.set(newPath)
            except Exception as e:
                logging.error(e)
                logging.error("Failed to import Log")
        if self.event.check_bool.get():
            try:
                newPath = os.path.join(self.header_frame.project_dir_stringVar.get(), "event", "event.xml")
                shutil.copy(self.event.import_path.get(), newPath)
                self.event_path_final_stringVar.set(newPath)
            except Exception as e:
                logging.error(e)
                logging.error("Failed to import Event File")

    def On_Import_Sail(self):
        selectedSails = [self.header_frame.port_main_check_bool, self.header_frame.stb_main_check_bool, self.header_frame.port_jib_check_bool,self.header_frame.stb_jib_check_bool]
        folderNames = ['portMain', 'stbMain', 'portJib', 'stbJib']
        for i in range(len(selectedSails)):
            if selectedSails[i].get() == True:
               self.Import_Sail(i)

    def Import_Sail(self,source):
        print('Import_Sail'+str(source))
        folderNames = ['portMain', 'stbMain', 'portJib', 'stbJib']
        sources = [[self.port_main.import_path.get(),self.port_main.timezone.get(), self.port_main.timestep.get(), self.port_main.origin.get(), self.port_main.file_name_entry.get()],
                   [self.stb_main.import_path.get(),self.stb_main.timezone.get(), self.stb_main.timestep.get(), self.stb_main.origin.get(), self.stb_main.file_name_entry.get()],
                   [self.port_jib.import_path.get(), self.port_jib.timezone.get(), self.port_jib.timestep.get(), self.port_jib.origin.get(), self.port_jib.file_name_entry.get()],
                   [self.stb_jib.import_path.get(), self.stb_jib.timezone.get(), self.stb_jib.timestep.get(), self.stb_jib.origin.get(), self.stb_jib.file_name_entry.get()]]
        try:
            if sources[source][3] == 'EXIF':
                existingFileName = sources[source][0].split('/')[-1]
                newPath = os.path.join(self.header_frame.project_dir_stringVar.get(),folderNames[source], existingFileName)
                shutil.copy(sources[source][0], newPath)
                try:
                    veeringVideo.Rename_GP_TimeLapse(newPath,sources[source][1],sources[source][2]).Rename()
                except Exception as e:
                    logging.error(e)
                    logging.error("Veering Rename Go Pro failed on"+str(sources[source][0]))
            else:
                try:
                    newPath = os.path.join(self.header_frame.project_dir_stringVar.get(), folderNames[source], sources[source][4]+"_"+str(sources[source][2])+".mp4")
                    shutil.copy(sources[source][0], newPath)
                except Exception as e:
                    logging.error(e)
                    logging.error("Copying File Failed "+str(sources[source][0]))
        except Exception as e:
            logging.error(e)
            logging.error('Failed to copy' + str(sources[source][0]))

class   Data_Cleaning_Top(tk.Frame):
    def __init__(self, master,width,height):
        super().__init__(master)
        self['borderwidth'] = 1
        self['relief'] = 'ridge'
        self.config(width=width, height=height)

        ## define buttons
        self.load_log_button = tk.Button(self, width=10, text="Load Log File", font='none 12 bold', command=self.On_Load_Log)
        self.export_log_button = tk.Button(self, width=10, text="Export Log File", font='none 12 bold', command=self.On_Export_Log)
        self.add_aggregation_button = tk.Button(self, width=10, text="Add Aggregation", font='none 12 bold', command=self.On_Add_Aggregation)

        ## define stringVars
        self.log_type_stringVar = tk.StringVar()
        self.log_type_stringVar.set("")
        self.log_path_stringVar = tk.StringVar()
        self.log_path_stringVar.set("Log File Note Selected")
        self.log_timezone_stringVar = tk.StringVar()
        self.var_to_agg = tk.StringVar()
        self.agg_type = tk.StringVar()
        self.hdg_var = tk.StringVar()
        self.twa_var = tk.StringVar()
        self.tws_var = tk.StringVar()
        self.raceTimer_var = tk.StringVar()

        ## define Labels
        self.log_type_label = tk.Label(self, textvariable=self.log_type_stringVar, font='none 12 bold')
        self.log_path_label = tk.Label(self, textvariable=self.log_path_stringVar, font='none 12 bold')
        self.log_presets_filter_label = tk.Label(self, text="Log Preset Filter Values", font='none 12 bold')
        self.hdg_var_label = tk.Label(self, text="Define HDG Variable", font='none 12 bold')
        self.twa_var_label = tk.Label(self, text="Define TWA Variable", font='none 12 bold')
        self.tws_var_label = tk.Label(self, text="Define TWS Variable", font='none 12 bold')
        self.raceTimer_var_label = tk.Label(self, text="Define Race Timer Variable", font='none 12 bold')
        self.logVars_heading_label = tk.Label(self, text="Log Variables", font='none 12 bold')
        self.refinedVars_heading_label = tk.Label(self, text="Refined Variables", font='none 12 bold')
        self.annotationVars_heading_label = tk.Label(self, text="Annotations", font='none 12 bold')
        self.varAgg_label = tk.Label(self, text="Variable for Aggregation", font='none 12 bold')

        self.log_path_label.configure(wraplength=150)

        ## define list boxes
        self.logVars_listbox = tk.Listbox(self, height=20, width=24, font='none 12', selectmode=tk.MULTIPLE, exportselection=False)
        self.refinedVars_listbox = tk.Listbox(self, height=20, width=24, font='none 12', selectmode=tk.MULTIPLE,exportselection=False)
        self.annotationVars_listbox = tk.Listbox(self, height=20, width=24, font='none 12', selectmode=tk.MULTIPLE, exportselection=False)

        ## define comboboxes
        self.var_to_agg_combobox = ttk.Combobox(self, textvariable=self.var_to_agg, width=20, font='none 12')
        self.agg_type_combobox = ttk.Combobox(self, textvariable=self.agg_type, width=20, font='none 12')
        self.hdg_var_combobox = ttk.Combobox(self, textvariable=self.hdg_var, width=15, font='none 12')
        self.twa_var_combobox = ttk.Combobox(self, textvariable=self.twa_var, width=15, font='none 12')
        self.tws_var_combobox = ttk.Combobox(self, textvariable=self.tws_var, width=15, font='none 12')
        self.raceTimer_var_combobox = ttk.Combobox(self, textvariable=self.raceTimer_var, width=15, font='none 12')

        ## grid
        self.Grid_Elements()

        self.logVars_listbox.bind('<<ListboxSelect>>', self.Update_List_Box_1)
        self.refinedVars_listbox.bind('<<ListboxSelect>>', self.Update_List_Box_2)

    def Grid_Elements(self):
        self.load_log_button.grid(row=0, column=0, padx=5, pady=5)
        self.log_path_label.grid(row=0, column=1, padx=5, pady=5)
        self.log_type_label.grid(row=0, column=2, padx=5, pady=5)
        self.export_log_button.grid(row=0, column=3, padx=5, pady=5)

        self.logVars_heading_label.grid(row=1, column=0, padx=5, pady=5)
        self.logVars_listbox.grid(row=2, column=0, padx=5, pady=5, rowspan=4)

        self.refinedVars_heading_label.grid(row=1, column=1, padx=5, pady=5)
        self.refinedVars_listbox.grid(row=2, column=1, padx=5, pady=5, rowspan=4)

        self.varAgg_label.grid(row=2, column=2, padx=5, pady=5)
        self.var_to_agg_combobox.grid(row=3, column=2, padx=5, pady=5)
        self.agg_type_combobox.grid(row=4, column=2, padx=5, pady=5)
        self.add_aggregation_button.grid(row=5, column=2, padx=5, pady=5)

        self.annotationVars_heading_label.grid(row=1, column=3, padx=5, pady=5)
        self.annotationVars_listbox.grid(row=2, column=3, padx=5, pady=5, rowspan=4)

        self.log_presets_filter_label.grid(row=1, column=4, padx=5, pady=5, columnspan=2)
        self.hdg_var_label.grid(row=2, column=4, padx=5, pady=5)
        self.twa_var_label.grid(row=3, column=4, padx=5, pady=5)
        self.tws_var_label.grid(row=4, column=4, padx=5, pady=5)
        self.raceTimer_var_label.grid(row=5, column=4, padx=5, pady=5)

        self.hdg_var_combobox.grid(row=2, column=5, padx=5, pady=5)
        self.twa_var_combobox.grid(row=3, column=5, padx=5, pady=5)
        self.tws_var_combobox.grid(row=4, column=5, padx=5, pady=5)
        self.raceTimer_var_combobox.grid(row=5, column=5, padx=5, pady=5)


    def Update_From_Import(self,*args):
        self.log_path_stringVar.set(app.mainframe.import_frame.log_path_final_stringVar.get())
        self.log_type_stringVar.set(app.mainframe.import_frame.log.log_type.get())
        self.log_timezone_stringVar.set(app.mainframe.import_frame.log.timezone.get())

    def Update_List_Box_1(self,*args):
        self.refinedVars_listbox.delete(0, tk.END)
        vars = []
        for i in self.logVars_listbox.curselection():
            self.refinedVars_listbox.insert(tk.END, self.logVars_listbox.get(i))
            vars.append(self.logVars_listbox.get(i))
        for combo in [self.var_to_agg_combobox, self.hdg_var_combobox, self.twa_var_combobox, self.tws_var_combobox, self.raceTimer_var_combobox]:
            combo['values'] = vars

    def Update_List_Box_2(self,*args):
        self.annotationVars_listbox.delete(0, tk.END)
        for i in self.refinedVars_listbox.curselection():
            self.annotationVars_listbox.insert(tk.END, self.refinedVars_listbox.get(i))


    ## define class functions
    def On_Load_Log(self):
        if self.log_type_stringVar.get() == "Expedition":
            try:
                exp_log = veeringLogs.VeeringLog(self.log_path_stringVar.get())
                exp_log.Expedition_To_DF()
                exp_log.Add_Time_Zone(int(self.log_timezone_stringVar.get()))
                exp_log.Add_Time_Stamp()
                self.exp_log = exp_log

                for header in exp_log.log_df.columns:
                    self.logVars_listbox.insert(tk.END, header)

            except Exception as e:
                logging.error(e)
                logging.error('Failed to load log')

    def On_Export_Log(self):
        filterVars = []
        try:
            for selection in self.logVars_listbox.curselection():
                filterVars.append(self.logVars_listbox.get(selection))
            self.exp_log.Select_Variables(filterVars)

        except Exception as e:
            logging.error(e)
            logging.error('Failed to select variables')

    def On_Add_Aggregation(self):
        print("Aggregation Added")

class   Data_Cleaning_Mid(tk.Frame):
    def __init__(self, master, width, height):
        super().__init__(master)
        self['borderwidth'] = 1
        self['relief'] = 'ridge'
        self.config(width=width, height=height)

        ## define buttons
        self.load_event_button = tk.Button(self, width=10, text="Load Event File", font='none 12 bold', command=self.On_Load_Event)
        self.export_event_button = tk.Button(self, width=10, text="Export Event File", font='none 12 bold', command=self.On_Export_Event)
        self.add_event_button = tk.Button(self, width=8, text="Add Event", font='none 12 bold', command=self.On_Add_Event)
        self.remove_event_button = tk.Button(self, width=8, text="Remove Event", font='none 12 bold', command=self.On_Remove_Event)
        self.commit_event_change_button = tk.Button(self, width=8, text="Commit Change", font='none 12 bold', command=self.On_Commit_Event_Change)
        self.add_attributes_button = tk.Button(self, width=8, text="Add attributes", font='none 12 bold', command=self.On_Add_Attributes)

        ## define stringVars
        self.event_path_stringVar = tk.StringVar()
        self.event_path_stringVar.set("Event File Not Selected")
        self.event_type_stringVar = tk.StringVar()
        self.event_timezone_stringVar = tk.StringVar()
        self.selected_type = tk.StringVar()
        self.selected_type.set("NA - Type")
        self.selected_time = tk.StringVar()
        self.selected_time.set("NA - Time")
        self.selected_attribute = tk.StringVar()
        self.selected_attribute.set("NA - Attribute")
        self.modified_time = tk.StringVar()
        self.modified_time.set("NA - Modified Time")
        self.new_attribute = tk.StringVar()
        self.new_attribute.set("NA - New Attribute")

        ## define bool
        self.preserve_phases_bool = tk.BooleanVar()

        ## define Label
        self.add_modify_delete_label = tk.Label(self, text="Add, Modify or Delete Events", font='none 12 bold')
        self.event_path_label = tk.Label(self, textvariable=self.event_path_stringVar, font='none 12 bold')
        self.event_file_type = tk.Label(self, textvariable=self.event_type_stringVar, font='none 12 bold')
        self.event_type_all_label = tk.Label(self, text="All Event Types", font='none 12 bold')
        self.event_type_filter_label = tk.Label(self, text="Filter Event Types", font='none 12 bold')
        self.event_list_label = tk.Label(self, text="Event List", font='none 12 bold')
        self.event_type_annotation_label = tk.Label(self, text="Event Type Annotation", font='none 12 bold')
        self.selected_type_label = tk.Label(self, textvariable=self.selected_type, font='none 12 bold')
        self.selected_time_label = tk.Label(self, textvariable=self.selected_time, font='none 12 bold')
        self.selected_attribute_label = tk.Label(self, textvariable=self.selected_attribute, font='none 12 bold')
        self.modified_time_label = tk.Label(self, textvariable=self.modified_time, font='none 12 bold')
        self.new_attribute_label = tk.Label(self, text="New Attribute", font='none 12 bold')
        self.new_type_label = tk.Label(self, text="New Type", font='none 12 bold')
        self.time_modify_label = tk.Label(self, text="Time Change", font='none 12 bold')

        self.event_path_label.configure(wraplength=150)

        ## define list boxes
        self.event_type_all_listbox = tk.Listbox(self, height=12, width=22,  font='none 12', selectmode=tk.MULTIPLE, exportselection=False)
        self.event_type_filter_listbox = tk.Listbox(self, height=12, width=22, font='none 12', selectmode=tk.MULTIPLE, exportselection=False)
        self.event_list_listbox = tk.Listbox(self, height=12, width=22, font='none 12', selectmode=tk.MULTIPLE, exportselection=False)
        self.event_type_annotation_listbox = tk.Listbox(self, height=12, width=22, font='none 12', selectmode=tk.MULTIPLE, exportselection=False)

        ## define combobox
        self.event_type_combobox = ttk.Combobox(self, width=12, font='none 12 bold')
        self.new_attribute_combobox = ttk.Combobox(self, width=12, font='none 12 bold')
        self.time_sign_combobox = ttk.Combobox(self, width=5, font='none 12 bold')
        self.time_hour_combobox = ttk.Combobox(self, width=5, font='none 12 bold')
        self.time_min_combobox = ttk.Combobox(self, width=5, font='none 12 bold')
        self.time_second_combobox = ttk.Combobox(self, width=5, font='none 12 bold')

        ## define checkbutton
        self.preserve_phases_checkbutton = tk.Checkbutton(self, text= "Preserve Phases for Filter", variable=self.preserve_phases_bool, onvalue=True, offvalue=False, command=self.On_Preserve_Phase)

        ## grid
        self.Grid_Elements()
        self.event_type_all_listbox.bind('<<ListboxSelect>>', self.Update_List_Box_1)
        self.event_type_filter_listbox.bind('<<ListboxSelect>>', self.Update_List_Box_2)

    def Grid_Elements(self):
        self.load_event_button.grid(row=0, column=0, padx=5, pady=5)
        self.event_path_label.grid(row=0, column=1, padx=5, pady=5)
        self.event_file_type.grid(row=0, column=2, padx=5, pady=5)
        self.preserve_phases_checkbutton.grid(row=0, column=3, padx=5, pady=5)
        self.export_event_button.grid(row=1, column=3, padx=5, pady=5)


        self.event_type_all_label.grid(row=1, column=0, padx=5, pady=5)
        self.event_type_all_listbox.grid(row=2, column=0, padx=5, pady=5, rowspan=5)

        self.event_type_filter_label.grid(row=1, column=1, padx=5, pady=5)
        self.event_type_filter_listbox.grid(row=2, column=1, padx=5, pady=5, rowspan=5)

        self.event_list_label.grid(row=1, column=2, padx=5, pady=5)
        self.event_list_listbox.grid(row=2, column=2, padx=5, pady=5, rowspan=5)

        self.add_modify_delete_label.grid(row=0, column=4, padx=5, pady=5, columnspan=4)
        self.selected_time_label.grid(row=2, column=3, padx=10, pady=10, columnspan=2)
        self.selected_type_label.grid(row=3, column=3, padx=10, pady=10, columnspan=2)
        self.selected_attribute_label.grid(row=4, column=3, padx=10, pady=10, columnspan=2)
        self.time_modify_label.grid(row=6, column=3, padx=10, pady=10, columnspan=4)
        self.time_sign_combobox.grid(row=7, column=3, padx=5, pady=5)
        self.time_hour_combobox.grid(row=7, column=4, padx=5, pady=5)
        self.time_min_combobox.grid(row=7, column=5, padx=5, pady=5)
        self.time_second_combobox.grid(row=7, column=6, padx=5, pady=5)

        self.modified_time_label.grid(row=1, column=5, columnspan=2)
        self.new_type_label.grid(row=2, column=5, columnspan=2)
        self.event_type_combobox.grid(row=3, column=5, padx=5, pady=5, columnspan=2)
        self.new_attribute_label.grid(row=4, column=5, columnspan=2)
        self.new_attribute_combobox.grid(row=5, column=5, columnspan=2)

        self.add_event_button.grid(row=2, column=7, padx=5, pady=5)
        self.remove_event_button.grid(row=3, column=7, padx=5, pady=5)
        self.commit_event_change_button.grid(row=4, column=7, padx=5, pady=5)
        self.add_attributes_button.grid(row=5, column=7, padx=5, pady=5)

        self.event_type_annotation_label.grid(row=1, column=8, padx=5, pady=5)
        self.event_type_annotation_listbox.grid(row=2, column=8, padx=5, pady=5, rowspan=5)

    ## define class functions

    def Update_From_Import(self,*args):
        self.event_path_stringVar.set(app.mainframe.import_frame.event_path_final_stringVar.get())
        self.event_type_stringVar.set(app.mainframe.import_frame.event.log_type.get())
        self.event_timezone_stringVar.set(app.mainframe.import_frame.event.timezone.get())

    def On_Preserve_Phase(self):
        print('On_Preserve_Phase')

    def On_Load_Event(self):
        if self.event_type_stringVar.get() == 'XML':
            try:
                self.eventFile = veeringLogs.VeeringEvent(self.event_path_stringVar.get())
                self.eventFile.Load_XML()
                self.eventFile.Add_Time_Zone(self.event_timezone_stringVar.get())
                self.eventFile.Build_Event_Dict()
                self.eventFile.Build_Phase_Dict()

                self.phase_dict = self.eventFile.phases
                self.event_dict = self.eventFile.events

                event_typ_unique = []
                for key in self.event_dict.keys():
                    if self.event_dict[key][1] not in event_typ_unique:
                        event_typ_unique.append(self.event_dict[key][1])

                for type in event_typ_unique:
                    self.event_type_all_listbox.insert(tk.END, type)

            except Exception as e:
                logging.error(e)
                logging.error('Failed to load event')

    def Update_List_Box_1(self,*args):
        self.event_type_filter_listbox.delete(0, tk.END)
        for i in self.event_type_all_listbox.curselection():
            self.event_type_filter_listbox.insert(tk.END, self.event_type_all_listbox.get(i))

    def Update_List_Box_2(self,*args):
        self.event_list_listbox.delete(0, tk.END)
        self.event_type_annotation_listbox.delete(0, tk.END)
        type = []
        for i in self.event_type_filter_listbox.curselection():
            self.event_type_annotation_listbox.insert(tk.END, self.event_type_filter_listbox.get(i))
            type.append(self.event_type_filter_listbox.get(i))
        print(type)
        for key in self.event_dict.keys():
            if self.event_dict[key][1] in type:
                self.event_list_listbox.insert(tk.END, str(self.event_dict[key][0])+" - "+str(self.event_dict[key][1])+" - "+str(self.event_dict[key][2]))

    def On_Export_Event(self):
        if self.preserve_phases_bool:
            try:
                self.eventFile.build_Phase_DF()

            except Exception as e:
                logging.error(e)
                logging.error('Failed to build phase DF')

    def On_Add_Event(self):
        print("Event File Added")

    def On_Remove_Event(self):
        print("Event File Removed")

    def On_Commit_Event_Change(self):
        print("Event File Commit Changed")

    def On_Add_Attributes(self):
        print("Event File Added")

class   Data_Cleaning_Side:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame['borderwidth'] = 1
        self.frame['relief'] = 'ridge'

        ## define Buttons
        self.add_event_times_button = self.add_event_button = tk.Button(self.frame, width=8, text="Add Events", font='none 12 bold', command=self.On_Add_Times)

        ## define labels
        self.race_timer_label = tk.Label(self.frame, text="Race Timer = 0", font='none 12 bold')

        ## define list box
        self.race_timer_listbox = tk.Listbox(self.frame, height=10, width=22, font='none 12 bold')

        ## grid
        self.race_timer_label.grid(row=0, column=0, padx=5, pady=5, columnspan=3)
        self.race_timer_listbox.grid(row=1, column=0, padx=5, pady=5, columnspan=3, rowspan=5)
        self.add_event_button.grid(row=7, column=0, padx=5, pady=5)

        ## define class functions
    def On_Add_Times(self):
        print('add_event_times')

class   Data_Cleaning_Frame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.Make_Data_Cleaning_Frame()

    def Make_Data_Cleaning_Frame(self):
        self.topFrame = Data_Cleaning_Top(self,1000,400)
        self.midFrame = Data_Cleaning_Mid(self,1000,400)
        self.sideFrame = Data_Cleaning_Side(self)

        self.sideFrame.frame.config(width=100, height=700)
        self.topFrame.grid(row=0, column=0, padx=10, pady=10, rowspan=10, columnspan=6)
        self.midFrame.grid(row=10, column=0, padx=10, pady=10, rowspan=10, columnspan=8)
        self.sideFrame.frame.grid(row=0, column=7, padx=10, pady=10, rowspan=10, columnspan=5)

class   Filter_Range_Selector(tk.Frame):
    def __init__(self, master, variable_name,df_var):
        super().__init__(master)
        self.df_var = df_var
        self.variable_name = variable_name
        ## define Bools
        self.use_filter_bool = tk.BooleanVar()
        self.use_filter_bool.set(False)

        ## define stingVars
        self.range_count_stringVar = tk.StringVar()
        self.range_count_stringVar.set('1')
        self.port_min_1_stringVar = tk.StringVar()
        self.port_max_1_stringVar = tk.StringVar()
        self.port_min_2_stringVar = tk.StringVar()
        self.port_max_2_stringVar = tk.StringVar()
        self.port_min_3_stringVar = tk.StringVar()
        self.port_max_3_stringVar = tk.StringVar()
        self.port_min_4_stringVar = tk.StringVar()
        self.port_max_4_stringVar = tk.StringVar()
        self.stb_min_1_stringVar = tk.StringVar()
        self.stb_max_1_stringVar = tk.StringVar()
        self.stb_min_2_stringVar = tk.StringVar()
        self.stb_max_2_stringVar = tk.StringVar()
        self.stb_min_3_stringVar = tk.StringVar()
        self.stb_max_3_stringVar = tk.StringVar()
        self.stb_min_4_stringVar = tk.StringVar()
        self.stb_max_4_stringVar = tk.StringVar()
        self.df_var_label = tk.StringVar()
        self.check_1 = tk.StringVar()
        self.check_2 = tk.StringVar()
        self.check_3 = tk.StringVar()
        self.check_4 = tk.StringVar()
        self.portMin = [self.port_min_1_stringVar, self.port_min_2_stringVar, self.port_min_3_stringVar, self.port_min_4_stringVar]
        self.portMax = [self.port_max_1_stringVar, self.port_max_2_stringVar, self.port_max_3_stringVar, self.port_max_4_stringVar]
        self.stbMin = [self.stb_min_1_stringVar, self.stb_min_2_stringVar, self.stb_min_3_stringVar, self.stb_min_4_stringVar]
        self.stbMax = [self.stb_max_1_stringVar, self.stb_max_2_stringVar, self.stb_max_3_stringVar, self.stb_max_4_stringVar]
        self.checks = [self.check_1, self.check_2, self.check_3, self.check_4]

        ## define check boxes
        self.use_filter_checkbox = tk.Checkbutton(self, text="Use "+str(self.variable_name)+" Filter", variable=self.use_filter_bool, onvalue=True, offvalue=False, command=self.Update_Filter)

        ## define combo boxes
        self.range_count_combo = ttk.Combobox(self, textvariable=self.range_count_stringVar, width=6)
        self.range_count_combo['values'] = ('1', '2', '3', '4')

        ## bind events
        self.range_count_combo.bind('<<ComboboxSelected>>', self.Update_Filter)

        ## define Labels
        self.port_label = tk.Label(self, text="Port", font='none 12 bold')
        self.stb_label = tk.Label(self, text="Starboard", font='none 12 bold')
        self.min_label_1 = tk.Label(self, text="Min", font='none 12 bold')
        self.max_label_1 = tk.Label(self, text="Max", font='none 12 bold')
        self.min_label_2 = tk.Label(self, text="Min", font='none 12 bold')
        self.max_label_2 = tk.Label(self, text="Max", font='none 12 bold')
        self.combo_label = tk.Label(self, text="# of Ranges", font='none 12 bold')
        self.check_1_label = tk.Label(self, textvariable=self.check_1, font='none 12 bold')
        self.check_2_label = tk.Label(self, textvariable=self.check_2, font='none 12 bold')
        self.check_3_label = tk.Label(self, textvariable=self.check_3, font='none 12 bold')
        self.check_4_label = tk.Label(self, textvariable=self.check_4, font='none 12 bold')
        self.checks_label = [self.check_1_label, self.check_2_label, self.check_3_label, self.check_4_label]

        self.use_filter_checkbox.grid(row=0, column=0, padx=5, pady=5, columnspan=3)
        self.range_count_combo.grid(row=1, column=0, padx=5, pady=5, columnspan=1)
        self.combo_label.grid(row=1, column=1, padx=5, pady=5, columnspan=2)
        self.port_label.grid(row=2, column=0, padx=5, pady=5, columnspan=2)
        self.stb_label.grid(row=2, column=3, padx=5, pady=5, columnspan=2)
        self.min_label_1.grid(row=3, column=0, padx=5, pady=5)
        self.max_label_1.grid(row=3, column=1, padx=5, pady=5)
        self.min_label_2.grid(row=3, column=3, padx=5, pady=5)
        self.max_label_2.grid(row=3, column=4, padx=5, pady=5)

        self.Box_or_label(df_var)
        self.Create_Grid_Boxes()

    def Box_or_label(self,df_var):
        try:
            if df_var == "Custom":
                self.df_var_combo = ttk.Combobox(self, textvariable=self.df_var_label, width=6)
                values = []
                for i in range(len(app.mainframe.data_cleaning.topFrame.logVars_listbox.curselection())):
                    values.append(app.mainframe.data_cleaning.topFrame.logVars_listbox.get(i))
                self.df_var_combo['values'] = values
                self.df_var_combo.grid(row=0, column=4, padx=5, pady=5, columnspan=3)

            else:
                if df_var == "hdg":
                    self.df_var_label.set(app.mainframe.data_cleaning.topFrame.hdg_var.get())
                if df_var == "twa":
                    self.df_var_label.set(app.mainframe.data_cleaning.topFrame.twa_var.get())
                if df_var == "tws":
                    self.df_var_label.set(app.mainframe.data_cleaning.topFrame.tws_var.get())
                if df_var == "time":
                    self.df_var_label.set(app.mainframe.data_cleaning.topFrame.raceTimer_var.get())
                self.df_var_label_label = tk.Label(self, textvariable=self.df_var_label, font='none 12 bold')
                self.df_var_label_label.grid(row=0, column=4, padx=5, pady=5, columnspan=3)
        except:
            print("Error")

    def Create_Grid_Boxes(self):
        self.entryBoxes = []
        for i in range(int(self.range_count_stringVar.get())):
            portMin = tk.Entry(self, textvariable=self.portMin[i], validate='focus', validatecommand=self.Check_Manual_Input, width=5)
            portMax = tk.Entry(self, textvariable=self.portMax[i], validate='focus', validatecommand=self.Check_Manual_Input, width=5)
            stbMin = tk.Entry(self, textvariable=self.stbMin[i], validate='focus', validatecommand=self.Check_Manual_Input, width=5)
            stbMax = tk.Entry(self, textvariable=self.stbMax[i], validate='focus', validatecommand=self.Check_Manual_Input, width=5)
            rangesBoxes = [portMin, portMax, stbMin, stbMax]
            self.entryBoxes.append(rangesBoxes)

        for i in range(int(self.range_count_combo.get())):
            self.entryBoxes[i][0].grid(row=i+4, column=0, padx=5, pady=5)
            self.entryBoxes[i][1].grid(row=i+4, column=1, padx=5, pady=5)
            self.entryBoxes[i][2].grid(row=i+4, column=3, padx=5, pady=5)
            self.entryBoxes[i][3].grid(row=i+4, column=4, padx=5, pady=5)
            self.checks_label[i].grid(row=i+4, column=5, padx=5, pady=5)

        for i in range(int(self.range_count_combo.get())):
            if self.use_filter_bool.get():
                self.entryBoxes[i][0].configure(state=tk.NORMAL)
                self.entryBoxes[i][1].configure(state=tk.NORMAL)
                self.entryBoxes[i][2].configure(state=tk.NORMAL)
                self.entryBoxes[i][3].configure(state=tk.NORMAL)
                self.entryBoxes[i][0].bind('<Key>', self.Check_Manual_Input)
                self.entryBoxes[i][0].bind('<FocusOut>', self.Check_Manual_Input)
                self.entryBoxes[i][1].bind('<Key>', self.Check_Manual_Input)
                self.entryBoxes[i][1].bind('<FocusOut>', self.Check_Manual_Input)
                self.entryBoxes[i][2].bind('<Key>', self.Check_Manual_Input)
                self.entryBoxes[i][2].bind('<FocusOut>', self.Check_Manual_Input)
                self.entryBoxes[i][3].bind('<Key>', self.Check_Manual_Input)
                self.entryBoxes[i][3].bind('<FocusOut>', self.Check_Manual_Input)
                self.checks[i].set("Fail")

            else:
                self.entryBoxes[i][0].configure(state=tk.DISABLED)
                self.entryBoxes[i][1].configure(state=tk.DISABLED)
                self.entryBoxes[i][2].configure(state=tk.DISABLED)
                self.entryBoxes[i][3].configure(state=tk.DISABLED)
                self.checks[i].set("")

    def Check_Manual_Input(self,*args):
        for i in range(int(self.range_count_combo.get())):
            if self.portMin[i].get().isdigit() and self.portMax[i].get().isdigit() and self.stbMin[i].get().isdigit() and self.stbMax[i].get().isdigit():
                self.checks[i].set("OK")
            else:
                self.checks[i].set("Fail")

    def Update_Filter(self,*args):
        self.Create_Grid_Boxes()
        self.Box_or_label(self.df_var)

class   Filter_Frame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        ## define Bools
        self.use_phases_bool = tk.BooleanVar()

        self.hdg_filter = Filter_Range_Selector(self, 'HDG filter', "hdg")
        self.hdg_filter.grid(row=0, column=0, padx=5, pady=5)

        self.twa_filter = Filter_Range_Selector(self, 'TWA filter', "twa")
        self.twa_filter.grid(row=0, column=1, padx=5, pady=5)

        self.tws_filter = Filter_Range_Selector(self, 'TWS filter', "tws")
        self.tws_filter.grid(row=0, column=2, padx=5, pady=5)

        self.timer_filter = Filter_Range_Selector(self, 'Timer filter', "time")
        self.timer_filter.grid(row=0, column=3, padx=5, pady=5)

        self.custom_1_filter = Filter_Range_Selector(self, 'Custom 1 filter', "Custom")
        self.custom_1_filter.grid(row=1, column=0, padx=5, pady=5)

        self.custom_2_filter = Filter_Range_Selector(self, 'Custom 2 filter', "Custom")
        self.custom_2_filter.grid(row=1, column=1, padx=5, pady=5)

        event_frame = self.Create_Event_Options()
        event_frame.grid(row=1, column=2, padx=5, pady=5)



    def Create_Event_Options(self):
        frame = tk.Frame(self)
        use_phases_check = tk.Checkbutton(frame, text="Use phases as filter", variable=self.use_phases_bool, onvalue=True, offvalue=False)
        use_phases_check.grid(row=0, column=0, padx=5, pady=5)
        return frame

    def Create_Filter_Agg(self):
        vars_used = []


        for var in [self.hdg_filter, self.twa_filter, self.tws_filter, self.timer_filter, self.custom_1_filter, self.custom_2_filter]:
            if var.use_filter_bool.get() == True:
                vars_used.append(var.df_var_label.get())

        print(vars_used)




    def Update_From_Import(self):
        print("update from import")
        self.Create_Filter_Agg()





class   Geometric_Transforms_Frame:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)

class   Autoscan_Frame:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)

class   Results_cleaning_Frame:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)

class   Reporting_Frame:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)

class Notebook(ttk.Notebook):
    def __init__(self, master):
        super().__init__(master)

        self.Make_Notebook()


        self.Generate_Gloabl_Variables(parent=self,
                                       port_main_default=True,
                                       stb_main_default=True,
                                       port_jib_default=True,
                                       stb_jib_default=True,
                                       log_default=True,
                                       event_default=True,
                                       project_default="No Directory Selected",
                                       root_default="No Directory Selected")

    def Make_Notebook(self):
        self.import_frame=ImportFrame(self)
        self.data_cleaning=Data_Cleaning_Frame(self)
        self.filter_frame=Filter_Frame(self)
        #self.frame4=Geometric_Transforms_Frame(self.notebook)
        #self.frame5=Autoscan_Frame(self.notebook)
        #self.frame6=Results_cleaning_Frame(self.notebook)
        #self.frame7=Reporting_Frame(self.notebook)

        self.add(self.import_frame, text='Import')
        self.add(self.data_cleaning,text='Data Cleaning')
        self.add(self.filter_frame,text='Filter' )
        #self.add(self.frame4,text='Geometric Transforms')
        #self.add(self.frame5,text='Autoscan')
        #self.notebook.add(self.frame6,text='Results Cleaning')
        #self.notebook.add(self.frame7,text='Results Cleaning')

        self.pack(fill='both', expand=True)
        self.bind('<<NotebookTabChanged>>', self.OnNotebookTabChanged)

    def OnNotebookTabChanged(self, *args):
        self.data_cleaning.topFrame.Update_From_Import()
        self.data_cleaning.topFrame.On_Load_Log()
        self.data_cleaning.midFrame.Update_From_Import()
        self.data_cleaning.midFrame.On_Load_Event()
        self.filter_frame.Update_From_Import()

    def Generate_Gloabl_Variables(self,parent, port_main_default, stb_main_default, port_jib_default, stb_jib_default, log_default, event_default, project_default, root_default):
        self.port_main_check_bool = tk.BooleanVar(parent)
        self.port_main_check_bool.set(port_main_default)
        self.stb_main_check_bool = tk.BooleanVar(parent)
        self.stb_main_check_bool.set(stb_main_default)
        self.port_jib_check_bool = tk.BooleanVar(parent)
        self.port_jib_check_bool.set(port_jib_default)
        self.stb_jib_check_bool = tk.BooleanVar(parent)
        self.stb_jib_check_bool.set(stb_jib_default)
        self.log_check_bool = tk.BooleanVar(parent)
        self.log_check_bool.set(log_default)
        self.event_check_bool = tk.BooleanVar(parent)
        self.event_check_bool.set(event_default)

        self.project_dir_stringVar = tk.StringVar(parent)
        self.project_dir_stringVar.set(project_default)
        self.root_dir_stringVar = tk.StringVar(parent)
        self.root_dir_stringVar.set(root_default)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Veering Stripe Field')
        self.geometry('1500x1100')
        self.mainframe = Notebook(self)

if __name__ == "__main__":
    app = App()
    app.mainloop()

