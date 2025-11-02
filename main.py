import os
import tkinter as tk
from doctest import master
from tkinter import filedialog, StringVar, messagebox
from tkinter import ttk
import logging
import datetime
import shutil
from tkinter.constants import ACTIVE
from wsgiref.validate import check_status
import threading
import queue

from PIL import Image
from PIL import ImageTk
import numpy as np
import h5py
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import veeringVideo
import veeringLogs
import veeringCV

logging.basicConfig(filename='stripeField.log', encoding='utf-8', level=logging.DEBUG)
logging.info('Veering Image Loader Opened')

class   Make_Project_Directory_Window(tk.Toplevel):
    def __init__(self,master):
        super().__init__(master)
        self.title("Make Project Directory")
        self.geometry("575x350")
        self.config(borderwidth=2)

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
        self.close_button = tk.Button(self, text="Close", width=10, command=self.Close_Window, default="normal")
        self.create_directory_button = tk.Button(self, text="Create Directory", width=15, command=self.Create_Directory, default="normal")
        self.select_root_dir_button = tk.Button(self, text="Select Root Directory", width=15, command=self.On_Select_Root_Dir, default="active")

        ## define labels
        self.root_dir_label = tk.Label(self, text="Root Directory", font='none 14 bold', width=10, anchor='w')
        self.root_dir_txt = tk.Label(self, textvariable=self.root_dir_stringVar, font='none 10', width=40, wraplength=160)
        self.Select_Folders = tk.Label(self, text="Select Folders to Generate", font='none 14 bold', width=20, anchor="center")
        self.Select_Date = tk.Label(self, text="Select Project Date", font='none 14 bold', width=20, anchor="center")
        self.Year_label = tk.Label(self, text="Year - ", font='none 12', width=8)
        self.Month_label = tk.Label(self, text="Month - ", font='none 12', width=8)
        self.Day_label = tk.Label(self, text="Day - ", font='none 12', width=8)
        self.success_label = tk.Label(self, textvariable=self.project_dir_success_stringVar, font='none 12 bold', width=20, wraplength=160, anchor="center")

        ## define combo box
        self.year_combobox = ttk.Combobox(self, textvariable=self.year_strVar, width=8, font='none 12')
        self.year_combobox['values'] = ('24', '25')
        self.year_combobox.state(["readonly"])
        self.year_combobox.current(1)

        self.month_combobox = ttk.Combobox(self, textvariable=self.month_strVar, width=8, font='none 12')
        self.month_combobox['values'] = ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12')
        self.month_combobox.state(["readonly"])
        self.month_combobox.current(int(self.month)-1)

        self.day_combobox = ttk.Combobox(self, textvariable=self.day_strVar, width=8, font='none 12')
        self.day_combobox['values'] = ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31')
        self.day_combobox.state(["readonly"])
        self.day_combobox.current(int(self.day)-1)

        ## define check buttons
        self.port_main_check = tk.Checkbutton(self, text="Port Main", variable=self.port_main_check_bool, onvalue=True, offvalue=False, width=10)
        self.port_main_check.select()
        self.stb_main_check = tk.Checkbutton(self, text="STB Main", variable=self.stb_main_check_bool, onvalue=True, offvalue=False, width=10)
        self.stb_main_check.select()
        self.port_jib_check = tk.Checkbutton(self, text="Port Jib", variable=self.port_jib_check_bool, onvalue=True, offvalue=False, width=10)
        self.port_jib_check.select()
        self.stb_jib_check = tk.Checkbutton(self, text="STB Jib", variable=self.stb_jib_check_bool, onvalue=True, offvalue=False, width=10)
        self.stb_jib_check.select()
        self.log_check = tk.Checkbutton(self, text="Log", variable=self.log_check_bool, onvalue=True, offvalue=False, width=10)
        self.log_check.select()
        self.event_check = tk.Checkbutton(self, text="Event", variable=self.event_check_bool, onvalue=True, offvalue=False, width=10)
        self.event_check.select()

        ## define seporators
        self.horz_sep_1 = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.horz_sep_2 = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.vert_sep_1 = ttk.Separator(self, orient=tk.VERTICAL)

        ## define bindings
        self.select_root_dir_button.bind("<Button-1>", self.Check_Button_Default)
        self.create_directory_button.bind("<Button-1>", self.Check_Button_Default)
        self.close_button.bind("<Button-1>", self.Check_Button_Default)

        ## grid all
        self.root_dir_label.grid(row=0, column=0, padx=2, pady=5, sticky=tk.W)
        self.root_dir_txt.grid(row=0, column=1, columnspan=3, pady=5, sticky=tk.W)
        self.select_root_dir_button.grid(row=0, column=4, pady=5, sticky=tk.E)
        self.horz_sep_1.grid(row=1, column=0, columnspan=5, pady=10, sticky=tk.EW)
        self.Select_Folders.grid(row=2, column=0, columnspan=2, pady=5, sticky=tk.NSEW)
        self.vert_sep_1.grid(row=2, column=2, rowspan=6, sticky=tk.NS)
        self.Select_Date.grid(row=2, column=3, columnspan=2, pady=10, sticky=tk.EW)
        self.port_main_check.grid(row=3, column=0, pady=5)
        self.log_check.grid(row=3, column=1, pady=5)
        self.Year_label.grid(row=3, column=3, pady=5, sticky=tk.E)
        self.year_combobox.grid(row=3, column=4, pady=5, sticky=tk.W)
        self.stb_main_check.grid(row=4, column=0, pady=5)
        self.event_check.grid(row=4, column=1, pady=5)
        self.Month_label.grid(row=4, column=3, pady=5, sticky=tk.E)
        self.month_combobox.grid(row=4, column=4, pady=5, sticky=tk.W)
        self.port_jib_check.grid(row=5, column=0, pady=5)
        self.Day_label.grid(row=5, column=3, pady=5, sticky=tk.E)
        self.day_combobox.grid(row=5, column=4, pady=5, sticky=tk.W)
        self.stb_jib_check.grid(row=6, column=0, pady=5)
        self.success_label.grid(row=6, column=3, rowspan=2, columnspan=2, pady=5)
        self.horz_sep_2.grid(row=8, column=0, columnspan=5, pady=5, sticky=tk.EW)
        self.close_button.grid(row=9, column=3, pady=5, sticky=tk.NE)
        self.create_directory_button.grid(row=9, column=4, pady=5, sticky=tk.NE)

    ## define functions
    def Close_Window(self):
        if self.close_button['default'] != "active":
            response = messagebox.askyesno(title="Are you sure?", message="No Project Directory has been created yet.")
            if response:
                self.destroy()
        else:
            app.mainframe.import_frame.header_frame.directory_selected_bool.set(True)
            self.destroy()

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

        self.Check_Button_Default()

    def On_Select_Root_Dir(self):
        try:
            self.root_dir = filedialog.askdirectory(initialdir='/Users/sean/mbp_storage')
            self.root_dir_stringVar.set(self.root_dir)
            self.root_dir_selected = True

        except Exception as e:
            logging.error(e)
            logging.error('Failed to set project root directory in make project directory')

        self.Check_Button_Default()

    def Check_Button_Default(self,*args):
        if self.root_dir_selected == False:
            self.close_button.config(default="normal")
            self.create_directory_button.config(default="normal")
            self.select_root_dir_button.config(default="active")

        elif self.project_dir_success_stringVar.get() == "":
            self.close_button.config(default="normal")
            self.create_directory_button.config(default="active")
            self.select_root_dir_button.config(default="normal")

        else:
            self.close_button.config(default="active")
            self.create_directory_button.config(default="normal")
            self.select_root_dir_button.config(default="normal")

class   Import_Frame_Header(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.column_min_width = 160

        ## define buttons
        self.select_project_button = tk.Button(self, width=15, text="Select Project Directory", font='none 12 bold', command=self.On_Select_Project_Dir)
        self.select_project_button['default'] = "active"
        self.make_project_dir_button = tk.Button(self, width=15, text="Make Project Directory", font='none 12 bold', command=self.Open_Make_Project_Dir)
        self.make_project_dir_button['default'] = "active"

        ## define seperators
        self.horiz_1 = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.horiz_2 = ttk.Separator(self, orient=tk.HORIZONTAL)

        ## define stringVars
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
        self.directory_selected_bool = tk.BooleanVar()
        self.directory_selected_bool.set(False)

        ## define Labels
        self.import_header_label = tk.Label(self, text="Define Project Directory", font='none 16 bold', width=60)
        self.project_dir_label = tk.Label(self, text="Project Directory", font='none 14 bold', width=20)
        self.project_dir_txt = tk.Label(self, textvariable=self.project_dir_stringVar, font='none 12', width=40)

        ## grid elements
        self.horiz_1.grid(row=0, column=0, columnspan=4, pady=5, sticky=tk.EW)
        self.import_header_label.grid(row=1, column=0, pady=5, columnspan=4)
        self.project_dir_label.grid(row=2, column=0)
        self.project_dir_txt.grid(row=2, column=1)
        self.select_project_button.grid(row=2, column=2)
        self.make_project_dir_button.grid(row=2, column=3)
        self.horiz_2.grid(row=3, column=0, columnspan=4, pady=5, sticky=tk.EW)

        for i in range(4):
            self.grid_columnconfigure(i, weight=1, minsize=self.column_min_width)

        ## bind events
        self.button_trace = self.directory_selected_bool.trace_add('write', self.Update_Button_Default)

    def Update_Button_Default(self, *args):
        if self.directory_selected_bool.get():
            self.select_project_button['default'] = "normal"
            self.make_project_dir_button['default'] = "normal"
            app.mainframe.import_frame.directory_defined_bool.set(True)

    def On_Select_Project_Dir(self):
        try:
            if self.project_dir_stringVar.get() == "No Directory Selected":
                self.project_dir = filedialog.askdirectory(initialdir='/Users/sean/mbp_storage')
                if self.project_dir:
                    self.project_dir_stringVar.set(self.project_dir)
                    self.directory_selected_bool.set(True)
            else:
                self.project_dir = filedialog.askdirectory(initialdir='/Users/sean/mbp_storage')
                if self.project_dir:
                    self.project_dir_stringVar.set(self.project_dir)
                    self.directory_selected_bool.set(True)
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
        self.Proj_Window

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
        self.timezone_combobox.state(["readonly"])

        ts_combo_list = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '15', '20', '30']
        self.timestep_combobox = self.Create_Combo(text_variable=self.timestep, combo_list=ts_combo_list, state_pre=["readonly"], current_value=5)
        self.timestep_combobox.state(["readonly"])

        origin_combo_list = ['EXIF', 'File Name']
        self.origin_combobox = self.Create_Combo(text_variable=self.origin, combo_list=origin_combo_list, state_pre=["readonly"], current_value=0)
        self.origin_combobox.state(["readonly"])

        log_type_combo_list = ['Expedition', 'CSV', 'XML']
        if source_name == 'Event':
            self.log_type_combo = self.Create_Combo(text_variable=self.log_type, combo_list=log_type_combo_list, state_pre=["readonly"], current_value=2)
            self.log_type_combo.state(["readonly"])
        else:
            self.log_type_combo = self.Create_Combo(text_variable=self.log_type, combo_list=log_type_combo_list, state_pre=["readonly"], current_value=0)
            self.log_type_combo.state(["readonly"])

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
        self.check.grid(row=0, column=0, pady=1)
        self.import_label.grid(row=0, column=1, pady=1)
        self.import_button.grid(row=0, column=2, pady=1)
        self.timezone_combobox.grid(row=0, column=3, pady=1)
        if source_type == "sail":
            self.timestep_combobox.grid(row=0, column=4, pady=1)
            self.origin_combobox.grid(row=0, column=5, pady=1)
            self.file_name_entry_box.grid(row=0, column=6, pady=1)
            self.file_name_check_label.grid(row=0, column=7, pady=1)
            for i in range(8):
                self.grid_columnconfigure(i, weight=1, minsize=self.column_min_width)
        elif source_type == "file":
            self.log_type_combo.grid(row=0, column=4, pady=1)
            for i in range(5):
                self.grid_columnconfigure(i, weight=1, minsize=self.column_min_width)

class   Import_Frame_Files(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        ## define labels
        self.header_label = tk.Label(self, text="Import Files Destination", font='none 16 bold')
        self.header_label.grid(row=0, column=0, columnspan=3)

    def Print_File_Paths(self,*args):
        try:
            labels = ['Port Main', 'STB Main', "Port Jib", "STB Jib", "Log File", "Event File"]
            stringVars = [app.mainframe.import_frame.port_main_path_final_stringVar,
            app.mainframe.import_frame.stb_main_path_final_stringVar,
            app.mainframe.import_frame.port_jib_path_final_stringVar,
            app.mainframe.import_frame.stb_jib_path_final_stringVar,
            app.mainframe.import_frame.log_path_final_stringVar,
            app.mainframe.import_frame.event_path_final_stringVar]

            for i in range(len(labels)):
                label = tk.Label(self, text=labels[i], font='none 12 bold')
                label.grid(row=i+1, column=0)
                path = tk.Label(self, textvariable=stringVars[i], font='none 12')
                path.grid(row=i+1, column=1)

        except:
            print("Failed to make file path labels")

class   ImportFrame(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        ## define multithreading
        self.output_q = queue.Queue()
        self.after(100, self.Process_Queue)


        ## define default list
        self.defaults = [0,0,1,1,0,2]
        ## define frames for screen sections
        self.sails = tk.Frame(self)
        self.files = tk.Frame(self)
        self.buttons = tk.Frame(self)
        ## define custom elements
        self.header_frame = Import_Frame_Header(self)
        self.port_main = Import_Frame_Source(self.sails, check_bool_pre=self.header_frame.port_main_check_bool, source_name="Port Main", source_type="sail",)
        self.stb_main = Import_Frame_Source(self.sails, check_bool_pre=self.header_frame.stb_main_check_bool, source_name="Stb Main", source_type="sail")
        self.port_jib = Import_Frame_Source(self.sails, check_bool_pre=self.header_frame.port_jib_check_bool, source_name="Port JIB", source_type="sail")
        self.stb_jib = Import_Frame_Source(self.sails, check_bool_pre=self.header_frame.stb_jib_check_bool, source_name="Stb JIB", source_type="sail")
        self.log = Import_Frame_Source(self.files, check_bool_pre=self.header_frame.log_check_bool, source_name="Log", source_type="file")
        self.event = Import_Frame_Source(self.files, check_bool_pre=self.header_frame.event_check_bool, source_name="Event", source_type="file")
        self.final_file_paths = Import_Frame_Files(self)

        ## define bools
        self.use_port_as_stb = tk.BooleanVar()
        self.use_port_as_stb.set(True)
        self.directory_defined_bool = tk.BooleanVar()
        self.directory_defined_bool.set(False)

        ## define stringVars
        self.port_main_path_final_stringVar = tk.StringVar()
        self.port_main_path_final_stringVar.set("")
        self.stb_main_path_final_stringVar = tk.StringVar()
        self.stb_main_path_final_stringVar.set("")
        self.port_jib_path_final_stringVar = tk.StringVar()
        self.port_jib_path_final_stringVar.set("")
        self.stb_jib_path_final_stringVar = tk.StringVar()
        self.stb_jib_path_final_stringVar.set("")
        self.log_path_final_stringVar = tk.StringVar()
        self.log_path_final_stringVar.set("")
        self.event_path_final_stringVar = tk.StringVar()
        self.event_path_final_stringVar.set("")

        ## define buttons
        self.import_sail_mp4_button = tk.Button(self.buttons, width=15, text="Import Sail .MP4", font='none 12 bold',command=self.On_Import_Sail)
        self.logs_process_button = tk.Button(self.buttons, width=15, text="Import Log Files", font='none 12 bold',command=self.On_Import_Logs)
        self.find_files_button = tk.Button(self.buttons, width=15, text="Find Existing Files", font='none 12 bold',command=self.Find_Files)

        ## define checkbuttons
        self.use_port_as_stb_check = tk.Checkbutton(self.buttons, text="Use Port Jib for STB Jib", variable=self.use_port_as_stb, onvalue=True, offvalue=False, command=self.On_Use_Port_for_Stb)

        ## define labels
        self.sail_header_frame = self.Create_Labels(self.sails,["sail", "Import Path", "Select Directory", "Time Zone", "Time Step", "Time Origin", "Enter Manual File Name", "File Name Check"])
        self.data_header_frame = self.Create_Labels(self.files,["Data Source", "Import Path", "Select Directory", "Time Zone", "File Type"])

        ## define seporators
        self.horz_sep_1 = ttk.Separator(self.sails, orient=tk.HORIZONTAL)
        self.horz_sep_2 = ttk.Separator(self.sails, orient=tk.HORIZONTAL)
        self.horz_sep_3 = ttk.Separator(self.files, orient=tk.HORIZONTAL)
        self.horz_sep_4 = ttk.Separator(self.files, orient=tk.HORIZONTAL)
        self.horz_sep_5 = ttk.Separator(self.buttons, orient=tk.HORIZONTAL)

        ## grid elements
        self.Grid_Elements()

        ## bind events to update variables
        self.import_sail_mp4_button.bind("<Button-1>", self.Update_File_Paths)
        self.logs_process_button.bind("<Button-1>", self.Update_File_Paths)
        self.find_files_button.bind("<Button-1>", self.Update_File_Paths)
        self.directory_defined_bool.trace_add('write', self.Update_Defaults)
        traces = []
        for source in [self.port_main, self.stb_main, self.port_jib, self.stb_jib, self.log,self.event]:
            trace_1 = source.import_path.trace_add('write', self.Update_Defaults)
            trace_2 = source.check_bool.trace_add('write', self.Update_Defaults)
            traces.append(trace_1)
            traces.append(trace_2)

        for sources in [self.port_main_path_final_stringVar, self.stb_main_path_final_stringVar, self.port_jib_path_final_stringVar, self.stb_jib_path_final_stringVar, self.log_path_final_stringVar, self.event_path_final_stringVar]:
            trace_1 = sources.trace_add('write', self.Update_Defaults)
            traces.append(trace_1)

        for var in [self.port_jib.import_path, self.port_jib.timezone, self.port_jib.timestep, self.port_jib.origin, self.port_jib.file_name_entry]:
            traces.append(var.trace_add('write', self.On_Use_Port_for_Stb))

        ## define functions

    def Update_Defaults(self, *args):

        need_to_check_all = False
        sources = [self.port_main, self.stb_main, self.port_jib, self.stb_jib, self.log, self.event]
        final_paths = [self.port_main_path_final_stringVar, self.stb_jib_path_final_stringVar, self.port_jib_path_final_stringVar, self.stb_jib_path_final_stringVar, self.log_path_final_stringVar, self.event_path_final_stringVar]
        for i in range(len(sources)):
            check = sources[i].check_bool.get()
            button = sources[i].import_button
            path = sources[i].import_path.get()
            pathFinal = final_paths[i].get()

            if self.directory_defined_bool.get():
                if check:
                    if path == "No File Selected" and pathFinal == "":
                        button['default'] = "active"
                        need_to_check_all = True
                    else:
                        button['default'] = "normal"
                        need_to_check_all = True

                else:
                    button['default'] = "normal"
                    need_to_check_all = True

            elif not self.directory_defined_bool.get():
                button['default'] = "normal"
                need_to_check_all = False

        if need_to_check_all:
            test = []
            for i in range(4):
                if sources[i].check_bool.get():
                    if sources[i].import_path.get() != "No File Selected" or final_paths[i].get() != "":
                        test.append(True)
                    else:
                        test.append(False)
                else:
                    test.append(True)
            if all(test):
                bool_check = []
                for i in range(4):
                    sources[i].import_button['default'] = "normal"
                    if not sources[i].check_bool.get():
                        bool_check.append(1)
                if len(bool_check) < 4:
                    self.import_sail_mp4_button['default'] = "active"

                else:
                    self.import_sail_mp4_button['default'] = "normal"

            else:
                self.import_sail_mp4_button['default'] = "normal"


            test = []
            for i in range(4,6):
                if sources[i].check_bool.get():
                    if sources[i].import_path.get() != "No File Selected" or final_paths[i].get() != "":
                        test.append(True)

                    else:
                        test.append(False)

                else:
                    test.append(True)
                if all(test):
                    bool_check = []
                    for i in range(4,6):
                        sources[i].import_button['default'] = "normal"
                        if not sources[i].check_bool.get():
                            bool_check.append(1)
                    if len(bool_check) < 2:
                        self.logs_process_button['default'] = "active"

                    else:
                        self.logs_process_button['default'] = "normal"

                else:
                    self.logs_process_button['default'] = "normal"

        else:
            self.import_sail_mp4_button['default'] = "normal"
            self.logs_process_button['default'] = "normal"

        if self.import_sail_mp4_button['default'] == "active" and self.logs_process_button['default'] == "active":
            self.find_files_button['default'] = "normal"
        elif not self.directory_defined_bool.get():
            self.find_files_button['default'] = "normal"
        elif self.import_sail_mp4_button['default'] == "normal" and self.logs_process_button['default'] == "normal" and not self.directory_defined_bool.get():
            self.find_files_button['default'] = "normal"

        else:
            check = []
            for source in sources:
                if source.check_bool.get():
                    check.append(1)
            if len(check) == 0:
                self.find_files_button['default'] = "normal"
            else:
                self.find_files_button['default'] = "active"

    def Update_File_Paths(self,*args):
        self.final_file_paths.Print_File_Paths()

    def On_Use_Port_for_Stb(self,*args):
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
            labels.append(tk.Label(frame, text=text[i], font='none 12 bold', width=15, anchor="center"))

        for i in range(len(text)):
            labels[i].grid(row = 0, column=i)
            frame.columnconfigure(i, weight=1, minsize=self.header_frame.column_min_width)

        return frame

    def Grid_Elements(self):
        self.sail_header_frame.grid(column=0, row=0, columnspan=8, pady=5)
        self.horz_sep_1.grid(column=0, row=1, columnspan=8, pady=5, sticky=tk.EW)
        self.port_main.grid(column=0, row=2, columnspan=8, pady=2)
        self.stb_main.grid(column=0, row=3, columnspan=8, pady=2)
        self.port_jib.grid(column=0, row=4, columnspan=8, pady=2)
        self.stb_jib.grid(column=0, row=5, columnspan=8, pady=2)
        self.horz_sep_2.grid(column=0, row=6, columnspan=8, pady=2, sticky=tk.EW)
        for i in range(8):
            self.sails.grid_columnconfigure(i, weight=1, minsize=self.port_main.column_min_width)

        self.data_header_frame.grid(column=0, row=0, columnspan=5, pady=5)
        self.horz_sep_3.grid(column=0, row=1, columnspan=5, pady=2, sticky=tk.EW)
        self.log.grid(column=0, row=2, columnspan=5, pady=2)
        self.event.grid(column=0, row=3, columnspan=5, pady=2)
        self.horz_sep_4.grid(column=0, row=4, columnspan=5, pady=2, sticky=tk.EW)
        for i in range(5):
            self.files.grid_columnconfigure(i, weight=1, minsize=self.port_main.column_min_width)

        self.use_port_as_stb_check.grid(column=0, row=0,padx=2, pady=2)
        self.import_sail_mp4_button.grid(column=1, row=0,padx=2, pady=2)
        self.logs_process_button.grid(column=2, row=0,padx=2, pady=2)
        self.find_files_button.grid(column=3, row=0,padx=2, pady=2)
        self.horz_sep_5.grid(column=0, row=1, columnspan=4, pady=2, sticky=tk.EW)
        for i in range(2):
            self.buttons.grid_columnconfigure(i, weight=1, minsize=self.port_main.column_min_width)

        self.header_frame.grid(column=0, row=0, columnspan=4, rowspan=2, padx=10, pady=10)
        self.sails.grid(column=0, row=2, columnspan=8, rowspan=7, padx=10, pady=10)
        self.files.grid(column=0, row=9, columnspan=5, rowspan=5, padx=10, pady=10)
        self.buttons.grid(column=0, row=14, columnspan=4, rowspan=2, padx=10, pady=10)
        self.final_file_paths.grid(column=0, row=19, columnspan=3)
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

    def Update_Path_Final(self, output):
        path_stringVars = [self.port_main_path_final_stringVar, self.stb_main_path_final_stringVar,
                           self.port_jib_path_final_stringVar, self.stb_jib_path_final_stringVar]
        path_stringVars[output[0]].set(output[1])

    def Process_Queue(self):
        try:
            while True:
                output = self.output_q.get_nowait()
                self.Update_Path_Final(output)
        except queue.Empty:
            pass
        finally:
            self.after(100, self.Process_Queue)

    def On_Import_Sail(self):
        selectedSails = [self.header_frame.port_main_check_bool, self.header_frame.stb_main_check_bool, self.header_frame.port_jib_check_bool,self.header_frame.stb_jib_check_bool]
        threads = []
        for i in range(len(selectedSails)):
            if selectedSails[i].get() == True:
                t = threading.Thread(target=self.Import_Sail, args=(i,), daemon=True)
                threads.append(t)

        for t in threads:
            t.start()

    def Import_Sail(self,source):
        folderNames = ['portMain', 'stbMain', 'portJib', 'stbJib']
        sources = [[self.port_main.import_path.get(),self.port_main.timezone.get(), self.port_main.timestep.get(), self.port_main.origin.get(), self.port_main.file_name_entry.get()],
                   [self.stb_main.import_path.get(),self.stb_main.timezone.get(), self.stb_main.timestep.get(), self.stb_main.origin.get(), self.stb_main.file_name_entry.get()],
                   [self.port_jib.import_path.get(), self.port_jib.timezone.get(), self.port_jib.timestep.get(), self.port_jib.origin.get(), self.port_jib.file_name_entry.get()],
                   [self.stb_jib.import_path.get(), self.stb_jib.timezone.get(), self.stb_jib.timestep.get(), self.stb_jib.origin.get(), self.stb_jib.file_name_entry.get()]]

        try:
            if sources[source][3] == 'EXIF':
                existingFileName = sources[source][0].split('/')[-1]
                if existingFileName != "No File Selected":
                    newPath = os.path.join(self.header_frame.project_dir_stringVar.get(),folderNames[source], existingFileName)
                    shutil.copy(sources[source][0], newPath)
                    try:
                        veeringVideo.Rename_GP_TimeLapse(newPath,sources[source][1],sources[source][2]).Rename()

                    except Exception as e:
                        logging.error(e)
                        logging.error("Veering Rename Go Pro failed on"+str(sources[source][0]))
                        newPath = "Failed"
            else:
                try:
                    newPath = os.path.join(self.header_frame.project_dir_stringVar.get(), folderNames[source], sources[source][4]+"_"+str(sources[source][2])+".mp4")
                    shutil.copy(sources[source][0], newPath)

                except Exception as e:
                    logging.error(e)
                    logging.error("Copying File Failed "+str(sources[source][0]))
                    newPath = "Failed"

            self.output_q.put([source,newPath])

        except Exception as e:
            logging.error(e)
            logging.error('Failed to copy' + str(sources[source][0]))

    def Find_Files(self):

        for folder in ['portMain', 'stbMain', 'portJib', 'stbJib']:
            directory_path = os.path.join(self.header_frame.project_dir_stringVar.get(),folder)
            files = os.listdir(directory_path)
            for file in files:
                if file.endswith(".mp4"):
                    if folder == "portMain":
                        self.port_main_path_final_stringVar.set(os.path.join(directory_path, file))
                    elif folder == "stbMain":
                        self.stb_main_path_final_stringVar.set(os.path.join(directory_path, file))
                    elif folder == "portJib":
                        self.port_jib_path_final_stringVar.set(os.path.join(directory_path, file))
                    elif folder == "stbJib":
                        self.stb_jib_path_final_stringVar.set(os.path.join(directory_path, file))

        for folder in ['log', 'event']:
            directory_path = os.path.join(self.header_frame.project_dir_stringVar.get(),folder)
            files = os.listdir(directory_path)
            for file in files:
                if file.endswith(".csv"):
                    if folder == "log":
                        self.log_path_final_stringVar.set(os.path.join(directory_path, file))
                if file.endswith(".xml"):
                    if folder == "event":
                        self.event_path_final_stringVar.set(os.path.join(directory_path, file))

class   Data_Cleaning_Top(tk.Frame):
    def __init__(self, master,width,height):
        super().__init__(master)
        self['borderwidth'] = 1
        self['relief'] = 'ridge'
        self.config(width=width, height=height)

        self.first_load_log = True
        self.defaults = ['TWA', 'TWS', 'TWD', 'HDG', 'Heel', 'Trim', 'Rudder', 'Forestay', 'TmToGun', 'timeStamp']
        self.combo_defaults = [3,0,1,8]

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
        self.logVars_listbox = tk.Listbox(self, height=18, width=24, font='none 12', selectmode=tk.MULTIPLE, exportselection=False)
        self.refinedVars_listbox = tk.Listbox(self, height=18, width=24, font='none 12', selectmode=tk.MULTIPLE,exportselection=False)
        self.annotationVars_listbox = tk.Listbox(self, height=18, width=24, font='none 12', selectmode=tk.MULTIPLE, exportselection=False)

        ## define comboboxes
        self.var_to_agg_combobox = ttk.Combobox(self, textvariable=self.var_to_agg, width=20, font='none 12')
        self.agg_type_combobox = ttk.Combobox(self, textvariable=self.agg_type, width=20, font='none 12')
        self.hdg_var_combobox = ttk.Combobox(self, textvariable=self.hdg_var, width=15, font='none 12')
        self.twa_var_combobox = ttk.Combobox(self, textvariable=self.twa_var, width=15, font='none 12')
        self.tws_var_combobox = ttk.Combobox(self, textvariable=self.tws_var, width=15, font='none 12')
        self.raceTimer_var_combobox = ttk.Combobox(self, textvariable=self.raceTimer_var, width=15, font='none 12', )
        self.raceTimer_var_combobox.set(self.combo_defaults[3])

        ## define Sep
        self.vert_1 = ttk.Separator(self, orient=tk.VERTICAL)
        self.vert_2 = ttk.Separator(self, orient=tk.VERTICAL)

        ## grid
        self.Grid_Elements()
        self.logVars_listbox.bind('<<ListboxSelect>>', self.Update_List_Box_1)
        self.refinedVars_listbox.bind('<<ListboxSelect>>', self.Update_List_Box_2)

    def Grid_Elements(self):
        self.load_log_button.grid(row=0, column=0, padx=5, pady=5)
        self.log_path_label.grid(row=0, column=1, padx=5, pady=5)
        self.log_type_label.grid(row=0, column=3, padx=5, pady=5)
        self.export_log_button.grid(row=0, column=4, padx=5, pady=5)

        self.logVars_heading_label.grid(row=1, column=0, padx=5, pady=5)
        self.logVars_listbox.grid(row=2, column=0, padx=2, pady=5, rowspan=4)

        self.refinedVars_heading_label.grid(row=1, column=1, padx=5, pady=5)
        self.refinedVars_listbox.grid(row=2, column=1, padx=2, pady=5, rowspan=4)

        self.vert_1.grid(row=1, column=2,rowspan=5, padx=2, sticky=tk.NS)
        self.varAgg_label.grid(row=2, column=3, padx=5, pady=5)
        self.var_to_agg_combobox.grid(row=3, column=3, padx=5, pady=5)
        self.agg_type_combobox.grid(row=4, column=3, padx=5, pady=5)
        self.add_aggregation_button.grid(row=5, column=3, padx=5, pady=5)

        self.annotationVars_heading_label.grid(row=1, column=3,columnspan=2, padx=5, pady=5)
        self.annotationVars_listbox.grid(row=2, column=4, padx=2, pady=5, rowspan=4)
        self.vert_2.grid(row=1, column=5,rowspan=5, padx=2, sticky=tk.NS)

        self.log_presets_filter_label.grid(row=1, column=6, padx=5, pady=5, columnspan=2)
        self.hdg_var_label.grid(row=2, column=6, padx=5, pady=5)
        self.twa_var_label.grid(row=3, column=6, padx=5, pady=5)
        self.tws_var_label.grid(row=4, column=6, padx=5, pady=5)
        self.raceTimer_var_label.grid(row=5, column=6, padx=5, pady=5)

        self.hdg_var_combobox.grid(row=2, column=7, padx=5, pady=5)
        self.twa_var_combobox.grid(row=3, column=7, padx=5, pady=5)
        self.tws_var_combobox.grid(row=4, column=7, padx=5, pady=5)
        self.raceTimer_var_combobox.grid(row=5, column=7, padx=5, pady=5)

    def Update_From_Import(self,*args):
        self.log_path_stringVar.set(app.mainframe.import_frame.log_path_final_stringVar.get())
        self.log_type_stringVar.set(app.mainframe.import_frame.log.log_type.get())
        self.log_timezone_stringVar.set(app.mainframe.import_frame.log.timezone.get())
        if (len(app.mainframe.import_frame.log_path_final_stringVar.get()) > 0 and self.first_load_log == True):
            print("Update Load log button")
            self.load_log_button['default'] = "active"

        else:
            self.load_log_button['default'] = "normal"

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

    def Load_Log_Exp(self, presets):
        counter = 0
        preset_ind = []
        exp_log = veeringLogs.VeeringLog(self.log_path_stringVar.get())
        exp_log.Expedition_To_DF()
        exp_log.Add_Time_Zone(int(self.log_timezone_stringVar.get()))
        exp_log.Add_Time_Stamp()
        self.exp_log = exp_log

        self.logVars_listbox.delete(0, tk.END)
        for header in exp_log.log_df.columns:
            self.logVars_listbox.insert(tk.END, header)
            if header in presets:
                preset_ind.append(counter)
            counter += 1

        for ind in preset_ind:
            self.logVars_listbox.select_set(ind)
        self.Update_List_Box_1()
        preset_list = [self.hdg_var_combobox, self.twa_var_combobox, self.tws_var_combobox,
                       self.raceTimer_var_combobox]

        for i in range(len(preset_list)):
            preset_list[i].current(self.combo_defaults[i])

    def On_Load_Log(self):
        if self.log_type_stringVar.get() == "Expedition":
            try:
                if self.first_load_log:
                    self.Load_Log_Exp(self.defaults)
                    self.first_load_log = False

                else:
                    current_selection = []
                    for i in self.logVars_listbox.curselection():
                        current_selection.append(self.logVars_listbox.get(i))
                    self.Load_Log_Exp(current_selection)

                self.load_log_button['default'] = "normal"
                self.export_log_button['default'] = "active"

            except Exception as e:
                logging.error(e)
                logging.error('Failed to load log')

        try:
            gun_zero = self.exp_log.log_df.loc[(self.exp_log.log_df['TmToGun']*60*60*24 > 0) & (self.exp_log.log_df['TmToGun']*60*60*24<1),['timeStamp']]
            self.gun_zero = list(gun_zero['timeStamp'])
            if len(self.gun_zero) > 0:
                app.mainframe.data_cleaning.sideFrame.Update_List()

        except Exception as e:
            logging.error(e)
            logging.error('Failed to find zero gun time')

    def On_Export_Log(self):
        filterVars = []
        try:
            for selection in self.logVars_listbox.curselection():
                filterVars.append(self.logVars_listbox.get(selection))
            self.exp_log.Select_Variables(filterVars)
            app.mainframe.filter_frame.logs_exported_bool.set(True)
            self.export_log_button['default'] = "normal"
            app.mainframe.data_cleaning.sideFrame.Update_Button_State()

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

        self.first_load_event = True
        self.defaults = []

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
        self.preserve_phases_bool.set(True)

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
        self.preserve_phases_checkbutton = tk.Checkbutton(self, text= "Preserve Phases for Filter", variable=self.preserve_phases_bool, onvalue=True, offvalue=False)

        ## grid
        self.Grid_Elements()
        self.event_type_all_listbox.bind('<<ListboxSelect>>', self.Update_List_Box_1)
        self.event_type_filter_listbox.bind('<<ListboxSelect>>', self.Update_List_Box_2)

    ## define class functions
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

    def Update_From_Import(self,*args):
        self.event_path_stringVar.set(app.mainframe.import_frame.event_path_final_stringVar.get())
        self.event_type_stringVar.set(app.mainframe.import_frame.event.log_type.get())
        self.event_timezone_stringVar.set(app.mainframe.import_frame.event.timezone.get())
        if (len(app.mainframe.import_frame.event_path_final_stringVar.get()) > 0 and self.first_load_event == True):
            print("Update Load log button")
            self.load_event_button['default'] = "active"

        else:
            self.load_event_button['default'] = "normal"

    def Load_Event_XML(self, presets):
        counter = 0
        preset_ind = []
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
                if self.event_dict[key][1] in presets:
                    preset_ind.append(counter)
            counter += 1
        self.event_type_all_listbox.delete(0, tk.END)
        for type in event_typ_unique:
            self.event_type_all_listbox.insert(tk.END, type)

        for ind in preset_ind:
            self.event_type_all_listbox.select_set(ind)

    def On_Load_Event(self):
        if self.event_type_stringVar.get() == 'XML':
            try:
                if self.first_load_event:
                    self.Load_Event_XML(self.defaults)
                    self.first_load_event = False

                else:
                    current_selection = []
                    for i in self.event_type_all_listbox.curselection():
                        current_selection.append(self.event_type_all_listbox.get(i))
                    self.Load_Event_XML(current_selection)

                self.load_event_button['default'] = "normal"
                self.export_event_button['default'] = "active"

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
        for key in self.event_dict.keys():
            if self.event_dict[key][1] in type:
                self.event_list_listbox.insert(tk.END, str(self.event_dict[key][0])+" - "+str(self.event_dict[key][1])+" - "+str(self.event_dict[key][2]))

    def On_Export_Event(self):
        try:
            if self.preserve_phases_bool.get():
                self.eventFile.Build_Phase_DF()
                app.mainframe.filter_frame.phases_exported_bool.set(True)

        except Exception as e:
            logging.error(e)
            logging.error('Failed to build phase DF')
        try:
            self.eventFile.Build_Event_DF()
            app.mainframe.filter_frame.events_exported_bool.set(True)
            self.export_event_button['default'] = "normal"
            app.mainframe.data_cleaning.sideFrame.Update_Button_State()
        except Exception as e:
            logging.error(e)
            logging.error('Failed to build event DF')

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
        self.export_csv_button = tk.Button(self.frame, width=10, text="Export Logs as CSV", font='none 12 bold', command=self.On_Export_Logs_CSV)

        ## define labels
        self.race_timer_label = tk.Label(self.frame, text="Race Timer = 0", font='none 12 bold')

        ## define list box
        self.race_timer_listbox = tk.Listbox(self.frame, height=10, width=22, font='none 12 bold')

        ## grid
        self.export_csv_button.grid(row=0, column=0, padx=10, pady=10, columnspan=3, rowspan=2)
        self.race_timer_label.grid(row=2, column=0, padx=5, pady=5, columnspan=3)
        self.race_timer_listbox.grid(row=3, column=0, padx=5, pady=5, columnspan=3, rowspan=5)
        self.add_event_button.grid(row=8, column=0, padx=5, pady=5)

        ## define class functions
    def Update_List(self):
        self.race_timer_listbox.delete(0, tk.END)
        for time in app.mainframe.data_cleaning.topFrame.gun_zero:
            self.race_timer_listbox.insert(tk.END, time.replace(microsecond=0))

    def On_Add_Times(self):
        print('add_event_times')

    def Update_Button_State(self):
        if app.mainframe.filter_frame.logs_exported_bool.get() and app.mainframe.filter_frame.events_exported_bool.get():
            self.export_csv_button['default'] = "active"
        else:
            self.export_csv_button['default'] = "normal"

    def On_Export_Logs_CSV(self):
        print('On_Export_Logs_CSV')
        if app.mainframe.filter_frame.logs_exported_bool.get():
            path, file = os.path.split(app.mainframe.data_cleaning.topFrame.log_path_stringVar.get())
            exp_path = os.path.join(path,"log_clean.csv")
            app.mainframe.data_cleaning.topFrame.exp_log.log_df.to_csv(exp_path, index=False, encoding='utf-8', sep=',')

        if app.mainframe.filter_frame.events_exported_bool.get():
            path, file = os.path.split(app.mainframe.data_cleaning.midFrame.event_path_stringVar.get())
            exp_path = os.path.join(path, "event_clean.csv")
            app.mainframe.data_cleaning.midFrame.eventFile.events_df.to_csv(exp_path, index=False, encoding='utf-8', sep=',')

class   Data_Cleaning_Frame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.Make_Data_Cleaning_Frame()

    def Make_Data_Cleaning_Frame(self):
        self.topFrame = Data_Cleaning_Top(self,900,400)
        self.midFrame = Data_Cleaning_Mid(self,1000,400)
        self.sideFrame = Data_Cleaning_Side(self)

        self.sideFrame.frame.config(width=100, height=700)
        self.topFrame.grid(row=0, column=0, sticky=tk.NSEW)
        self.midFrame.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)
        self.sideFrame.frame.grid(row=0, column=1, sticky=tk.NSEW)

class   Filter_Range_Selector(tk.Frame):
    def __init__(self, master, variable_name,df_var,default_active,default_values):
        super().__init__(master)
        self['borderwidth'] = 1
        self['relief'] = 'ridge'
        self.df_var = df_var ## log df label
        self.variable_name = variable_name ## human readable variable name for label
        ## define Bools
        self.use_filter_bool = tk.BooleanVar()
        self.use_filter_bool.set(default_active)


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

        if self.use_filter_bool.get():
            self.port_min_1_stringVar.set(default_values[0])
            self.port_max_1_stringVar.set(default_values[1])
            self.stb_min_1_stringVar.set(default_values[2])
            self.stb_max_1_stringVar.set(default_values[3])

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
        self.Update_Filter()

    def Box_or_label(self,df_var):
        try:
            if df_var == "Custom":
                self.df_var_combo = ttk.Combobox(self, textvariable=self.df_var_label, width=6)
                values = []
                for i in range(len(app.mainframe.data_cleaning.topFrame.logVars_listbox.curselection())):
                    values.append(app.mainframe.data_cleaning.topFrame.logVars_listbox.get(i))
                self.df_var_combo['values'] = values
                self.df_var_combo.state(["readonly"])
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
            self.entryBoxes[i][3].forget()

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
        self.output_q = queue.Queue()
        self.after(100, self.Process_Queue)
        self.JPG_Sumary('INITAL','hi','hi')

        ## define Bools
        self.use_phases_bool = tk.BooleanVar()
        self.use_phases_bool.set(True)
        self.logs_exported_bool = tk.BooleanVar()
        self.logs_exported_bool.set(False)
        self.phases_exported_bool = tk.BooleanVar()
        self.phases_exported_bool.set(False)
        self.events_exported_bool = tk.BooleanVar()
        self.events_exported_bool.set(False)
        self.log_filter_sum_run_bool = tk.BooleanVar()
        self.log_filter_sum_run_bool.set(False)
        self.filter_agg_bool = tk.BooleanVar()
        self.filter_agg_bool.set(False)

        ## define lists
        self.log_vars = []
        self.upwind_port_ts = []
        self.upwind_stb_ts = []

        self.hdg_filter = Filter_Range_Selector(self, 'HDG filter', "hdg",False, [0,0,0,0])
        self.hdg_filter.grid(row=0, column=0, padx=5, pady=5)

        self.twa_filter = Filter_Range_Selector(self, 'TWA filter', "twa", True, [-50,-30,30,50])
        self.twa_filter.grid(row=0, column=1, padx=5, pady=5)

        self.tws_filter = Filter_Range_Selector(self, 'TWS filter', "tws", False, [0,20,0,20])
        self.tws_filter.grid(row=0, column=2, padx=5, pady=5)

        self.timer_filter = Filter_Range_Selector(self, 'Timer filter', "time", False, [0,0,0,0])
        self.timer_filter.grid(row=0, column=3, padx=5, pady=5)

        self.custom_1_filter = Filter_Range_Selector(self, 'Custom 1 filter', "Custom", False, [0,0,0,0])
        self.custom_1_filter.grid(row=1, column=0, padx=5, pady=5)

        self.custom_2_filter = Filter_Range_Selector(self, 'Custom 2 filter', "Custom", False, [0,0,0,0])
        self.custom_2_filter.grid(row=1, column=1, padx=5, pady=5)

        self.event_frame = self.Create_Event_Options()
        self.event_frame.grid(row=1, column=2, padx=5, pady=5, sticky=tk.NSEW)

        self.entire_set_summary = self.Create_Import_Summary_Labels()
        self.entire_set_summary.grid(row=1, column=3, padx=5, pady=5, sticky=tk.NSEW)

        self.button_frame = self.Create_Buttons()
        self.button_frame.grid(row=2, column=0, padx=5, pady=5, sticky=tk.NSEW)

    def Process_Queue(self):
        try:
            while True:
                output = self.output_q.get_nowait()
                self.JPG_Sumary(output[0],output[1],output[2])
        except queue.Empty:
            pass
        finally:
            self.after(100, self.Process_Queue)

    def Togle_Filter_Update(self,*args):
        self.hdg_filter.Update_Filter()
        self.twa_filter.Update_Filter()
        self.tws_filter.Update_Filter()
        self.timer_filter.Update_Filter()
        self.custom_1_filter.Update_Filter()
        self.custom_2_filter.Update_Filter()

    def Generate_Filter_Summary(self):
        frame = tk.Frame(self)
        header_label = tk.Label(frame, text="Filter TS Count", font='none 12 bold')
        port_Label = tk.Label(frame, text="Port Count", font='none 12 bold')
        stb_Label = tk.Label(frame, text="Stb Count", font='none 12 bold')
        header_label.grid(row=0, column=0, padx=5, pady=5, columnspan=3)
        port_Label.grid(row=1, column=1, padx=5, pady=5)
        stb_Label.grid(row=1, column=2, padx=5, pady=5)

        stringVars_list = []
        labels_list = []
        if self.log_filter_sum_run_bool.get():
            for i in range(len(self.aggregation_combo_list)):
                var = self.aggregation_combo_list[i].get()
                index = self.log_vars_to_filter.index(var)
                port_count = len(self.log_vars_filters[index][0])
                stb_count = len(self.log_vars_filters[index][1])
                stringVar_var = tk.StringVar()
                stringVar_var.set(var)
                stringVar_pt = tk.StringVar()
                stringVar_pt.set(str(port_count))
                stringVar_stb = tk.StringVar()
                stringVar_stb.set(str(stb_count))
                stringVars_list.append([stringVar_var, stringVar_pt, stringVar_stb])
                label_var = tk.Label(frame, textvariable=stringVar_var)
                label_pt = tk.Label(frame, textvariable=stringVar_pt, font='none 12')
                label_stb = tk.Label(frame, textvariable=stringVar_stb, font='none 12')
                labels_list.append([label_var, label_pt, label_stb])
        if self.filter_agg_bool.get():
            port_count = len(self.filter_port_ts_agg)
            stringVar_var = tk.StringVar()
            stb_count = len(self.filter_stb_ts_agg)
            stringVar_var.set("Aggregated Counts")
            stringVar_pt = tk.StringVar()
            stringVar_pt.set(str(port_count))
            stringVar_stb = tk.StringVar()
            stringVar_stb.set(str(stb_count))
            stringVars_list.append([stringVar_var, stringVar_pt, stringVar_stb])
            label_var = tk.Label(frame, textvariable=stringVar_var)
            label_pt = tk.Label(frame, textvariable=stringVar_pt, font='none 12')
            label_stb = tk.Label(frame, textvariable=stringVar_stb, font='none 12')
            labels_list.append([label_var, label_pt, label_stb])

        for i in range(len(labels_list)):
            labels_list[i][0].grid(row=i+2, column=0, padx=5, pady=5)
            labels_list[i][1].grid(row=i+2, column=1, padx=5, pady=5)
            labels_list[i][2].grid(row=i+2, column=2, padx=5, pady=5)

        self.log_filter_sum_run_bool.set(True)


        self.filter_summary = frame
        self.filter_summary.grid(row=2, column=2, padx=5, pady=5)

    def Create_Event_Options(self):
        frame = tk.Frame(self)
        frame['borderwidth'] = 1
        frame['relief'] = 'ridge'
        use_phases_check = tk.Checkbutton(frame, text="Use phases as filter", variable=self.use_phases_bool, onvalue=True, offvalue=False)
        use_phases_check.grid(row=0, column=0, padx=5, pady=5)
        return frame

    def Create_Buttons(self):
        frame = tk.Frame(self)
        frame['borderwidth'] = 1
        frame['relief'] = 'ridge'
        self.generate_log_filters_button = tk.Button(frame, width=20, text="Generate Filter Aggregation", font='none 12 bold', command=self.Generate_Filters)
        self.aggregate_filters_button = tk.Button(frame, width=20, text="Aggregate Filters", font='none 12 bold', command=self.Aggregate_Filters)
        self.create_jpg_button = tk.Button(frame, width=20, text="Create JPG's", font='none 12 bold', command=self.On_Generate_JPG)

        self.generate_log_filters_button.grid(row=0, column=0, padx=5, pady=5)
        self.aggregate_filters_button.grid(row=1, column=0, padx=5, pady=5)
        self.create_jpg_button.grid(row=2, column=0, padx=5, pady=5)

        return frame

    def Create_Import_Summary_Labels(self):
        frame = tk.Frame(self)
        frame['borderwidth'] = 1
        frame['relief'] = 'ridge'
        self.log_rows_stringVar = tk.StringVar()
        self.log_rows_stringVar.set("Nil Rows")
        self.log_columns_stringVar = tk.StringVar()
        self.log_columns_stringVar.set("Nil Columns")

        self.log_header_label = tk.Label(frame, text="Log File Imported with", font='none 12 bold')
        self.log_rows_label = tk.Label(frame, textvariable=self.log_rows_stringVar, font='none 12')
        self.log_columns_label = tk.Label(frame, textvariable=self.log_columns_stringVar, font='none 12')

        self.phases_rows_stringVar = tk.StringVar()
        self.phases_rows_stringVar.set("Nil Rows")
        self.event_rows_stringVar = tk.StringVar()
        self.event_rows_stringVar.set("Nil Rows")
        self.event_columns_stringVar = tk.StringVar()
        self.event_columns_stringVar.set("Nil Columns")

        self.phase_header_label = tk.Label(frame, text="Phase File Imported with", font='none 12 bold')
        self.phases_rows_label = tk.Label(frame, textvariable=self.phases_rows_stringVar, font='none 12')
        self.event_header_label = tk.Label(frame, text="EventFile Imported with", font='none 12 bold')
        self.event_rows_label = tk.Label(frame, textvariable=self.event_rows_stringVar, font='none 12')
        self.event_columns_label = tk.Label(frame, textvariable=self.event_columns_stringVar, font='none 12')

        self.log_header_label.grid(row=0, column=0, padx=5, pady=5, columnspan=2)
        self.log_rows_label.grid(row=1, column=0, padx=5, pady=5)
        self.log_columns_label.grid(row=1, column=1, padx=5, pady=5)
        self.phase_header_label.grid(row=2, column=0, padx=5, pady=5, columnspan=2)
        self.phases_rows_label.grid(row=3, column=0, padx=5, pady=5)
        self.event_header_label.grid(row=4, column=0, padx=5, pady=5, columnspan=2)
        self.event_rows_label.grid(row=5, column=0, padx=5, pady=5)
        self.event_columns_label.grid(row=5, column=1, padx=5, pady=5)

        return frame

    def Generate_Phase_Filters(self):
        self.phases_filter = [app.mainframe.data_cleaning.midFrame.eventFile.phase_df['timeStamp'],
                              app.mainframe.data_cleaning.midFrame.eventFile.phase_df['timeStamp']]

    def Generate_Log_Filters(self):
        self.log_vars_to_filter = []
        self.log_vars_filters = []
        for  logVar in [self.hdg_filter, self.twa_filter, self.tws_filter, self.timer_filter, self.custom_1_filter, self.custom_2_filter]:
            if logVar.use_filter_bool.get():
                self.log_vars_to_filter.append(logVar.df_var_label.get())
                portMin = []
                portMax = []
                stbMin = []
                stbMax = []
                for i in range(int(logVar.range_count_stringVar.get())):
                    portMin.append(int(logVar.portMin[i].get()))
                    portMax.append(int(logVar.portMax[i].get()))
                    stbMin.append(int(logVar.stbMin[i].get()))
                    stbMax.append(int(logVar.stbMax[i].get()))

                port_ts, stb_ts = app.mainframe.data_cleaning.topFrame.exp_log.Get_Filter_TS(portMin, portMax, stbMin, stbMax,logVar.df_var_label.get())
                self.log_vars_filters.append([port_ts, stb_ts])

    def Create_Filter_Agg(self):
        frame = tk.Frame(self)
        self.aggregation_combo_list = []
        self.aggregation_combo_stringVars = []
        self.and_or_stringVar_list = []
        self.and_or_radio_list = []
        if self.use_phases_bool.get() == True:
            self.log_vars_to_filter.append('Phases')
            self.log_vars_filters.append(self.phases_filter)

        for i in range(len(self.log_vars_to_filter)):
            self.aggregation_combo_stringVars.append(tk.StringVar())
            combo = ttk.Combobox(frame, width=10, textvariable=self.aggregation_combo_stringVars[i])
            combo['values'] = self.log_vars_to_filter
            combo.set(self.log_vars_to_filter[i])
            self.aggregation_combo_list.append(combo)
            self.and_or_stringVar_list.append(tk.StringVar())
            self.aggregation_combo_list[i].grid(row=i, column=0, padx=5, pady=5)
            if i < len(self.log_vars_to_filter)-1:
                radio = [ttk.Radiobutton(frame, width=10, text="AND", variable=self.and_or_stringVar_list[i], value='and'),
                     ttk.Radiobutton(frame, width=10, text="OR", variable=self.and_or_stringVar_list[i], value='or')]
                self.and_or_stringVar_list[i].set('and')
                self.and_or_radio_list.append(radio)
                self.and_or_radio_list[i][0].grid(row=i, column=1, padx=5, pady=5)
                self.and_or_radio_list[i][1].grid(row=i, column=2, padx=5, pady=5)

        return frame

    def Generate_Filters(self):
        if self.use_phases_bool.get():
            self.Generate_Phase_Filters()
        self.Generate_Log_Filters()
        self.agg_frame = self.Create_Filter_Agg()
        self.agg_frame.grid(row=2, column=1, padx=5, pady=5)
        self.log_filter_sum_run_bool.set(True)
        self.Generate_Filter_Summary()
        self.Update_Button_State()

    def Update_From_Import(self):
        if self.logs_exported_bool.get():
            rows = app.mainframe.data_cleaning.topFrame.exp_log.log_df.shape[0]
            cols = app.mainframe.data_cleaning.topFrame.exp_log.log_df.shape[1]
            self.log_rows_stringVar.set("with "+str(rows)+" rows")
            self.log_columns_stringVar.set("with "+str(cols)+" columns")



        if self.phases_exported_bool.get():
            rows = app.mainframe.data_cleaning.midFrame.eventFile.phase_df.shape[0]
            self.phases_rows_stringVar.set("with "+str(rows)+" rows")

        if self.logs_exported_bool.get():
            rows = app.mainframe.data_cleaning.midFrame.eventFile.events_df.shape[0]
            cols = app.mainframe.data_cleaning.midFrame.eventFile.events_df.shape[1]
            self.event_rows_stringVar.set("with "+str(rows)+" rows")
            self.event_columns_stringVar.set("with "+str(cols)+" columns")

        self.Update_Button_State()

    def Aggregate_Filters(self,*args):
        var = self.aggregation_combo_list[0].get()
        index = self.log_vars_to_filter.index(var)
        filter_port_ts_agg = self.log_vars_filters[index][0]
        filter_stb_ts_agg = self.log_vars_filters[index][1]

        for i in range(1,len(self.aggregation_combo_list)):
            var_next = self.aggregation_combo_list[i].get()
            index_next = self.log_vars_to_filter.index(var_next)
            combine_type = self.and_or_stringVar_list[i-1].get()

            if combine_type == 'and':
                filter_port_ts_agg = list(set(filter_port_ts_agg) & set(self.log_vars_filters[index_next][0]))
                filter_stb_ts_agg = list(set(filter_stb_ts_agg) & set(self.log_vars_filters[index_next][1]))

            elif combine_type == 'or':
                filter_port_ts_agg = list(set(filter_port_ts_agg) | set(self.log_vars_filters[index_next][0]))
                filter_stb_ts_agg = list(set(filter_stb_ts_agg) | set(self.log_vars_filters[index_next][1]))

        self.filter_port_ts_agg = filter_port_ts_agg
        self.filter_stb_ts_agg = filter_stb_ts_agg
        self.filter_agg_bool.set(True)
        self.Generate_Filter_Summary()
        self.Update_Button_State()

    def JPG_Sumary(self, type, sail, msg):
        self.sumary_frame = tk.Frame(self)

        print("JPG Sumary")
        if type == 'INITAL':
            self.port_main_stringVar = tk.StringVar()
            self.port_main_stringVar.set("Port Main not in use")
            self.stb_main_stringVar = tk.StringVar()
            self.stb_main_stringVar.set("Stb Main not in use")
            self.port_jib_stringVar = tk.StringVar()
            self.port_jib_stringVar.set("Port jib not in use")
            self.stb_jib_stringVar = tk.StringVar()
            self.stb_jib_stringVar.set("Stb Jib not in use")
            self.port_main_label = tk.Label(self.sumary_frame, textvariable=self.port_main_stringVar)
            self.stb_main_label = tk.Label(self.sumary_frame, textvariable=self.stb_main_stringVar)
            self.port_jib_label = tk.Label(self.sumary_frame, textvariable=self.port_jib_stringVar)
            self.stb_jib_label = tk.Label(self.sumary_frame, textvariable=self.stb_jib_stringVar)

        elif type == 'status':
            if sail == 'portMain':
                self.port_main_stringVar.set(sail+" "+msg)
            elif sail == 'stbMain':
                self.stb_main_stringVar.set(sail+" "+msg)
            elif sail == 'portJib':
                self.port_jib_stringVar.set(sail+" "+msg)
            elif sail == 'stbJib':
                self.stb_jib_stringVar.set(sail+" "+msg)

        self.port_main_label.grid(row=0, column=0, padx=5, pady=5)
        self.stb_main_label.grid(row=1, column=0, padx=5, pady=5)
        self.port_jib_label.grid(row=2, column=0, padx=5, pady=5)
        self.stb_jib_label.grid(row=3, column=0, padx=5, pady=5)

        self.sumary_frame.grid(row=3, column=0, padx=5, pady=5)

    def On_Generate_JPG(self,*args):
        filePaths = [app.mainframe.import_frame.port_main_path_final_stringVar.get(),
                     app.mainframe.import_frame.stb_main_path_final_stringVar.get(),
                     app.mainframe.import_frame.port_jib_path_final_stringVar.get(),
                     app.mainframe.import_frame.stb_jib_path_final_stringVar.get()]

        sails = ['portMain', 'stbMain', 'portJib', 'stbJib']

        threads = []

        for i in range (len(filePaths)):
            thread = threading.Thread(target=self.Generate_JPG, args=(filePaths[i],sails[i]))
            threads.append(thread)
            print("add thread")
        for t in threads:
            t.start()

    def Generate_JPG(self,filePath,sail):
        try:
            print(sail)
            self.output_q.put(['status', sail, 'Converting to JPG'])
            veeringVideo.SailTimeLapse(filePath,sail).TimeLapse_To_JPG()

            if sail == 'stbMain' or sail == 'stbJib':
                self.output_q.put(['status', sail, 'Filtering JPG'])
                veeringVideo.Filter_JPG(os.path.join(app.mainframe.import_frame.header_frame.project_dir_stringVar.get(),str(sail),'jpg'), self.filter_stb_ts_agg).Remove_Files()


            elif sail == 'portMain' or sail == 'portJib':
                self.output_q.put(['status', sail, 'Filtering JPG'])
                veeringVideo.Filter_JPG(os.path.join(app.mainframe.import_frame.header_frame.project_dir_stringVar.get(),str(sail),'jpg'), self.filter_port_ts_agg).Remove_Files()

            message = "DONE with "+str(len(os.listdir(os.path.join(app.mainframe.import_frame.header_frame.project_dir_stringVar.get(),str(sail),'jpg'))))+" files"
            self.output_q.put(['status', sail, message])
            print(sail+" Done")
        except Exception as e:
            logging.error(e)
            logging.error('Failed to create JPG for '+str(sail))
            self.output_q.put(['status', sail, 'ERROR'])

        self.Update_Button_State()

    def Update_Button_State(self):
        if not self.logs_exported_bool.get() and not self.log_filter_sum_run_bool.get() and not self.filter_agg_bool.get():
            self.generate_log_filters_button['default'] = "normal"
            self.aggregate_filters_button['default'] = "normal"
            self.create_jpg_button['default'] = "normal"

        elif self.logs_exported_bool.get() and not self.log_filter_sum_run_bool.get() and not self.filter_agg_bool.get():
            self.generate_log_filters_button['default'] = "active"
            self.aggregate_filters_button['default'] = "normal"
            self.create_jpg_button['default'] = "normal"

        elif self.logs_exported_bool.get() and self.log_filter_sum_run_bool.get() and not self.filter_agg_bool.get():
            self.generate_log_filters_button['default'] = "normal"
            self.aggregate_filters_button['default'] = "active"
            self.create_jpg_button['default'] = "normal"

        elif self.logs_exported_bool.get() and self.log_filter_sum_run_bool.get() and self.filter_agg_bool.get():
            self.generate_log_filters_button['default'] = "normal"
            self.aggregate_filters_button['default'] = "normal"
            self.create_jpg_button['default'] = "active"

        else:
            self.generate_log_filters_button['default'] = "normal"
            self.aggregate_filters_button['default'] = "normal"
            self.create_jpg_button['default'] = "normal"

class   Visual_Picker(tk.Toplevel):
    def __init__(self, master, file_path,orig_height,orig_width, flip_vertical, flip_horizontal, rotate_90, rotate_270, start_values):
        super().__init__(master)
        self.title("Visual Picker")

        self.crop_top_stringVar = tk.StringVar()
        self.crop_bottom_stringVar = tk.StringVar()
        self.crop_lhs_stringVar = tk.StringVar()
        self.crop_rhs_stringVar = tk.StringVar()

        self.file_path = file_path
        self.flip_vertical = flip_vertical
        self.flip_horizontal = flip_horizontal
        self.rotate_90 = rotate_90
        self.rotate_270 = rotate_270
        self.canvas_width = 666
        self.canvas_height = orig_height * (self.canvas_width / orig_width)
        self.scale = self.canvas_height / orig_height

        self.main_canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg='#C8C8C8')
        self.top_scale = tk.Scale(self, orient='horizontal', length=self.canvas_width, from_=0,
                              to=self.canvas_width, command=self.On_Crop_Slider)
        self.top_scale.set(int(start_values[0]*self.scale))
        self.bottom_scale = tk.Scale(self, orient='horizontal', length=self.canvas_width, from_=0,
                                 to=self.canvas_width, command=self.On_Crop_Slider)
        self.bottom_scale.set(int(start_values[3]*self.scale))
        self.left_scale = tk.Scale(self, orient='vertical', length=self.canvas_height, from_=0,
                               to=self.canvas_height, command=self.On_Crop_Slider)
        self.left_scale.set(int(start_values[1]*self.scale))
        self.right_scale = tk.Scale(self, orient='vertical', length=self.canvas_height, from_=0,
                                to=self.canvas_height, command=self.On_Crop_Slider)
        self.right_scale.set(int(start_values[2]*self.scale))
        image = Image.open(self.file_path)

        image = image.resize((int(self.canvas_width), int(self.canvas_height)), Image.Resampling.LANCZOS)
        if self.flip_vertical:
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
        if self.flip_horizontal:
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
        if self.rotate_90:
            image = image.transpose(Image.ROTATE_90)
        if self.rotate_270:
            image = image.transpose(Image.ROTATE_270)
        self.image = ImageTk.PhotoImage(image)
        self.thumbnail_canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg='#C8C8C8')
        self.thumbnail_canvas.create_image(self.canvas_width/2, self.canvas_height/2, image=self.image)
        self.thumbnail_canvas.grid(row=1, column=1, rowspan=3)

    ## Create Buttons


    ## Grid Canvas and scales
        self.main_canvas.grid(column=1, row=1)
        self.top_scale.grid(column=1, row=0)
        self.bottom_scale.grid(column=1, row=2)
        self.left_scale.grid(column=0, row=1)
        self.right_scale.grid(column=2, row=1)


    def Display_Image(self):
        image = Image.open(self.file_path)
        image = image.resize((int(self.canvas_width), int(self.canvas_height)), Image.Resampling.LANCZOS)
        if self.flip_vertical:
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
        if self.flip_horizontal:
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
        if self.rotate_90:
            image = image.transpose(Image.ROTATE_90)
        if self.rotate_270:
            image = image.transpose(Image.ROTATE_270)
        image = image.crop((int(self.top_scale.get()), int(self.left_scale.get()), int(self.bottom_scale.get()), int(self.right_scale.get())))
        self.image = ImageTk.PhotoImage(image)
        horizontal_centre = int(((int(self.bottom_scale.get()) - int(self.top_scale.get())) / 2) + int(self.top_scale.get()))
        vertical_centre = int(((int(self.right_scale.get()) - int(self.left_scale.get())) / 2) + int(self.left_scale.get()))
        self.thumbnail_canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg='#C8C8C8')
        self.thumbnail_canvas.create_image(horizontal_centre, vertical_centre, image=self.image)
        self.thumbnail_canvas.grid(row=1, column=1, rowspan=3)

    def On_Crop_Slider(self,*args):
        self.Display_Image()
        self.crop_top_stringVar.set(str(int(self.left_scale.get()/self.scale)))
        self.crop_bottom_stringVar.set(str(int(self.right_scale.get()/self.scale)))
        self.crop_lhs_stringVar.set(str(int(self.top_scale.get()/self.scale)))
        self.crop_rhs_stringVar.set(str(int(self.bottom_scale.get()/self.scale)))

class   Sail_Geometric_Properties(tk.Frame):
    def __init__(self, master,imgDir,sail,defaults, flip_rot):
        super().__init__(master)

        ## definevars
        self.img_index = 0
        self.directory = imgDir
        self.defaults = defaults
        self.flip_rot = flip_rot

        ## define bools
        self.flip_horizontal_bool = tk.BooleanVar()
        self.flip_vertical_bool  = tk.BooleanVar()
        self.rotate_90_bool  = tk.BooleanVar()
        self.rotate_270_bool  = tk.BooleanVar()
        self.load_bool = tk.BooleanVar()
        self.load_bool.set(True)

        ## define stringvars
        self.crop_lhs_stringVar = tk.StringVar()
        self.crop_rhs_stringVar = tk.StringVar()
        self.crop_top_stringVar = tk.StringVar()
        self.crop_bottom_stringVar = tk.StringVar()
        self.mask_lhs_stringVar = tk.StringVar()
        self.mask_rhs_stringVar = tk.StringVar()
        self.mask_top_stringVar = tk.StringVar()
        self.mask_bottom_stringVar = tk.StringVar()
        self.sail_header_stringVar = tk.StringVar()
        self.sail_header_stringVar.set(sail)
        self.change_preview_ind_intVar = tk.IntVar()
        self.image_count_stringVar = tk.StringVar()
        self.image_width_stringVar = tk.StringVar()
        self.image_height_stringVar = tk.StringVar()


        ## create checkboxes
        self.flip_horizontal_check = tk.Checkbutton(self, text="Flip Horizontal", variable=self.flip_horizontal_bool, onvalue=True, offvalue=False)
        self.flip_vertical_check = tk.Checkbutton(self, text="Flip Vertical", variable=self.flip_vertical_bool, onvalue=True, offvalue=False)
        self.rotate_90_check = tk.Checkbutton(self, text="Rotate 90", variable=self.rotate_90_bool, onvalue=True, offvalue=False)
        self.rotate_270_check = tk.Checkbutton(self, text="Rotate 270", variable=self.rotate_270_bool, onvalue=True, offvalue=False)
        self.load_check = tk.Checkbutton(self, text="Load into .H5 format", variable=self.load_bool, onvalue=True, offvalue=False)

        ## create entryboxes
        self.crop_lhs_entry = tk.Entry(self, textvariable=self.crop_lhs_stringVar, width=5)
        self.crop_rhs_entry = tk.Entry(self, textvariable=self.crop_rhs_stringVar, width=5)
        self.crop_top_entry = tk.Entry(self, textvariable=self.crop_top_stringVar, width=5)
        self.crop_bottom_entry = tk.Entry(self, textvariable=self.crop_bottom_stringVar, width=5)
        self.mask_lhs_entry = tk.Entry(self, textvariable=self.mask_lhs_stringVar, width=5)
        self.mask_rhs_entry = tk.Entry(self, textvariable=self.mask_rhs_stringVar, width=5)
        self.mask_top_entry = tk.Entry(self, textvariable=self.mask_top_stringVar, width=5)
        self.mask_bottom_entry = tk.Entry(self, textvariable=self.mask_bottom_stringVar, width=5)

        ## create Buttons
        self.graph_chooser_button = tk.Button(self, text="Launch Graphical Chooser", command=self.Launch_Graphical_Chooser)
        self.load_preview_button = tk.Button(self, text="Load Preview", command=self.Load_Preview)
        self.update_preview_button = tk.Button(self, text="Update Preview", command=self.Update_Preview)

        ## create labels
        self.sail_header_label = tk.Label(self, textvariable=self.sail_header_stringVar, font='none 12 bold')
        self.preview_label = tk.Label(self, text="Original Image", font='none 12')
        self.crop_label = tk.Label(self, text="Crop Values", font='none 12')
        self.mask_label = tk.Label(self, text="Mask Values", font='none 12')
        self.small_labels = []
        for text in ['Crop LHS','Crop Top', 'Crop Bottom', 'Crop RHS', 'Mask Top','Mask  Bottom', 'Mask  LHS', 'Mask  RHS']:
            self.small_labels.append(tk.Label(self, text=text, font='none 10'))
        self.image_count_label = tk.Label(self, textvariable=self.image_count_stringVar, font='none 12')
        self.image_width_label = tk.Label(self, textvariable=self.image_width_stringVar, font='none 12')
        self.image_height_label = tk.Label(self, textvariable=self.image_height_stringVar, font='none 12')

        ## create combobox
        self.change_preview_ind_combo = ttk.Combobox(self, textvariable=self.change_preview_ind_intVar, width=5)
        self.change_preview_ind_combo['values'] = [-100, -10, -1, 0, 1, 10, 100]
        self.change_preview_ind_combo.state(["readonly"])

        ## create seperators
        self.horiz_1 = ttk.Separator(self, orient=tk.HORIZONTAL)

        ## Grid
        self.sail_header_label.grid(column=0, row=0, padx=5, pady=5)
        self.preview_label.grid(column=1, row=0, padx=5, pady=5)
        self.crop_label.grid(column=2, row=0, padx=5, pady=5, columnspan=2)
        self.mask_label.grid(column=4, row=0, padx=5, pady=5, columnspan=2)

        self.load_preview_button.grid(row=1, column=0)
        self.graph_chooser_button.grid(row=2, column=0)
        self.update_preview_button.grid(row=3, column=0)
        self.change_preview_ind_combo.grid(row=4, column=0)

        self.small_labels[0].grid(row=1,column=2)
        self.crop_lhs_entry.grid(row=2, column=2)
        self.small_labels[1].grid(row=1,column=3)
        self.crop_top_entry.grid(row=2, column=3)
        self.small_labels[2].grid(row=3,column=2)
        self.crop_bottom_entry.grid(row=4, column=2)
        self.small_labels[3].grid(row=3,column=3)
        self.crop_rhs_entry.grid(row=4, column=3)

        self.small_labels[4].grid(row=1,column=4)
        self.mask_lhs_entry.grid(row=2,column=4)
        self.small_labels[5].grid(row=1,column=5)
        self.mask_top_entry.grid(row=2,column=5)
        self.small_labels[6].grid(row=3,column=4)
        self.mask_bottom_entry.grid(row=4,column=4)
        self.small_labels[7].grid(row=3,column=5)
        self.mask_rhs_entry.grid(row=4,column=5)

        self.flip_vertical_check.grid(row=1, column=6)
        self.flip_horizontal_check.grid(row=2, column=6)
        self.rotate_90_check.grid(row=3, column=6)
        self.rotate_270_check.grid(row=4, column=6)

        self.load_check.grid(row=1, column=16, padx=5, pady=2)
        self.image_count_label.grid(row=2, column=16, padx=5)
        self.image_height_label.grid(row=3, column=16, padx=5)
        self.image_width_label.grid(row=4, column=16, padx=5)

        self.horiz_1.grid(row=5, column=0, columnspan=16, pady=2, sticky=tk.EW)

        ## bind events
        trace = self.change_preview_ind_intVar.trace_add('write',self.Update_From_Index)

    def Bind_Events(self,*args):
        self.graphical_chooser.crop_top_stringVar.trace('w',self.Update_From_Chooser)
        self.graphical_chooser.crop_lhs_stringVar.trace('w', self.Update_From_Chooser)
        self.graphical_chooser.crop_bottom_stringVar.trace('w', self.Update_From_Chooser)
        self.graphical_chooser.crop_rhs_stringVar.trace('w', self.Update_From_Chooser)

    def Launch_Graphical_Chooser(self):
        self.graphical_chooser = Visual_Picker(self,self.img_path,self.orig_height, self.orig_width,self.flip_vertical_bool.get(),self.flip_horizontal_bool.get(), self.rotate_90_bool.get(), self.rotate_270_bool.get(),
                                               [int(self.crop_lhs_stringVar.get()),
                                                int(self.crop_top_stringVar.get()),
                                                int(self.crop_bottom_stringVar.get()),
                                                int(self.crop_rhs_stringVar.get()),])
        self.Bind_Events()

    def Update_From_Chooser(self,*args):
        self.crop_top_stringVar.set(str(self.graphical_chooser.crop_top_stringVar.get()))
        self.crop_lhs_stringVar.set(str(self.graphical_chooser.crop_lhs_stringVar.get()))
        self.crop_bottom_stringVar.set(str(self.graphical_chooser.crop_bottom_stringVar.get()))
        self.crop_rhs_stringVar.set(str(self.graphical_chooser.crop_rhs_stringVar.get()))
        self.Update_Width_Height()

    def Update_From_Index(self,*args):
        self.Load_Preview()
        self.Update_Preview()

    def Update_Width_Height(self,*args):
        self.image_height_stringVar.set("The Image Height is - "+str(int(self.crop_bottom_stringVar.get()) - int(self.crop_top_stringVar.get())))
        self.image_width_stringVar.set("The Image Width is - "+str(int(self.crop_rhs_stringVar.get()) - int(self.crop_lhs_stringVar.get())))

    def Load_Preview(self):
        thumbnail_width = 200
        self.img_index = self.img_index+self.change_preview_ind_intVar.get()
        self.img_path = os.path.join(self.directory,os.listdir(self.directory)[self.img_index])
        image = Image.open(self.img_path)
        self.orig_width, self.orig_height = image.size
        thumbnail_height = int(self.orig_height * (thumbnail_width / self.orig_width))
        image = image.resize((int(thumbnail_width), int(thumbnail_height)), Image.Resampling.LANCZOS)
        self.image = ImageTk.PhotoImage(image)
        self.thumbnail_canvas = tk.Canvas(self, width=thumbnail_width, height=thumbnail_height, bg='#C8C8C8')
        self.thumbnail_canvas.create_image(thumbnail_width/2, thumbnail_height/2, image=self.image)
        self.thumbnail_canvas.grid(row=1, column=1, rowspan=3)
        if len(self.defaults) == 4:
            self.crop_lhs_stringVar.set(str(self.defaults[0]))
            self.crop_top_stringVar.set(str(self.defaults[1]))
            self.crop_bottom_stringVar.set(str(self.defaults[2]))
            self.crop_rhs_stringVar.set(str(self.defaults[3]))
        else:
            self.crop_lhs_stringVar.set(str(0))
            self.crop_top_stringVar.set(str(0))
            self.crop_bottom_stringVar.set(str(self.orig_height))
            self.crop_rhs_stringVar.set(str(self.orig_width))

        if len(self.flip_rot) == 4:
            self.flip_vertical_bool.set(self.flip_rot[0])
            self.flip_horizontal_bool.set(self.flip_rot[1])
            self.rotate_90_bool.set(self.flip_rot[2])
            self.rotate_270_bool.set(self.flip_rot[3])

    def Update_Preview(self):
        thumbnail_width = 300
        image = Image.open(self.img_path)
        if self.flip_vertical_bool.get():
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
        if self.flip_horizontal_bool.get():
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
        if self.rotate_90_bool.get():
            image = image.transpose(Image.ROTATE_90)
        if self.rotate_270_bool.get():
            image = image.transpose(Image.ROTATE_270)
        thumbnail_height = int((int(self.crop_bottom_stringVar.get())-int(self.crop_top_stringVar.get())) * (thumbnail_width / (int(self.crop_rhs_stringVar.get())-int(self.crop_lhs_stringVar.get()))))
        image = image.crop((int(self.crop_lhs_stringVar.get()),int(self.crop_top_stringVar.get()), int(self.crop_rhs_stringVar.get()), int(self.crop_bottom_stringVar.get())))
        image = image.resize((int(thumbnail_width), int(thumbnail_height)), Image.Resampling.LANCZOS)

        self.image_final = ImageTk.PhotoImage(image)
        self.thumbnail_canvas_final = tk.Canvas(self, width=thumbnail_width, height=thumbnail_height, bg='#C8C8C8')
        self.thumbnail_canvas_final.create_image(thumbnail_width/2, thumbnail_height/2, image=self.image_final)
        self.thumbnail_canvas_final.grid(row=1, column=7, rowspan=8)
        self.image_count_stringVar.set("The image count is - "+str(len(os.listdir(self.directory))))
        self.Update_Width_Height()

class   Geometric_Transforms_Frame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.load_and_process_button = tk.Button(self, text="Load to .H5", command=self.On_Load_Button)
        self.load_and_process_button.config(default="active")
        self.geometric_properties_list = ["Disabled", "Disabled", "Disabled", "Disabled"]

    def Make_Geometry_Transforms(self):

        self.bools = [app.mainframe.import_frame.port_main.check_bool.get(),
                 app.mainframe.import_frame.stb_main.check_bool.get(),
                 app.mainframe.import_frame.port_jib.check_bool.get(),
                 app.mainframe.import_frame.stb_jib.check_bool.get()]

        self.paths = [app.mainframe.import_frame.port_main_path_final_stringVar.get(),
                 app.mainframe.import_frame.stb_main_path_final_stringVar.get(),
                 app.mainframe.import_frame.port_jib_path_final_stringVar.get(),
                 app.mainframe.import_frame.stb_jib_path_final_stringVar.get()]

        self.sails = ['Port Main', 'Stb Main', 'Port Jib', 'Stb Jib']

        defaults_crop = [[790,1200,2345,4290],[790,1200,2345,4290],[675,990,1660,2715],[675,990,1660,2715]]
        defaults_flip_rot = [[False,False,False,False],[False,False,False,False],[False,False,False,False],[True,False,False,False]]

        for i in range(len(self.geometric_properties_list)):
            if self.geometric_properties_list[i] == 'Disabled' and self.bools[i] == True:
                sail = Sail_Geometric_Properties(self, os.path.join(os.path.dirname(self.paths[i]), 'jpg'),
                                                 self.sails[i], defaults_crop[i], defaults_flip_rot[i])
                sail.grid(row=i, column=0)
                if len(self.paths[i]) > 0:
                    sail.Load_Preview()
                    sail.Update_Preview()
                self.geometric_properties_list[i] = sail

            elif (self.geometric_properties_list[i] != 'Disabled' and self.bools[i] == False):
                sail = self.geometric_properties_list[i]
                sail.destroy()
                self.geometric_properties_list[i] = "Disabled"

            elif self.geometric_properties_list[i] != 'Disabled' and self.bools[i] == True:
                sail = self.geometric_properties_list[i]
                sail.destroy()
                sail = Sail_Geometric_Properties(self, os.path.join(os.path.dirname(self.paths[i]), 'jpg'),
                                                 self.sails[i], defaults_crop[i], defaults_flip_rot[i])
                sail.grid(row=i, column=0)
                if len(self.paths[i]) > 0:
                    sail.Load_Preview()
                    sail.Update_Preview()
                self.geometric_properties_list[i] = sail


        self.load_and_process_button.grid(row=i+1, column=5, padx=10, pady=10)

    def Load_to_Array(self,file_path,crops):
        time_stamps = []
        file_names = os.listdir(file_path)
        file_names = [file for file in file_names if '.jpg' in file]

        for i in range(len(file_names)):
            file_name = file_names[i]
            img_path = os.path.join(file_path, file_name)

            try:
                image = Image.open(img_path)
                print("processing " + str(i) + " of " + str(len(file_names)))

                ts = image.getexif()[306]
                time_stamps.append(ts)
                image = image.crop(crops)

                if i == 0:
                    w, h = image.size
                    img_array = np.zeros((h, w, 3, len(file_names)), dtype='float32')

                img_array[:, :, :, i] = np.array(image)

            except Exception as e:
                logging.error(e)
                logging.error('failed to load image in for loop - ' + str(img_path))

        self.image_array = img_array
        self.time_stamps = time_stamps

    def Load_and_Process(self, exp_dir,sail):
        try:
            exp_path = os.path.join(exp_dir, str(sail)+".h5")
            hf = h5py.File(exp_path, 'w')
            hf.create_dataset('IMG_ARRAY', data=self.image_array)
            hf.create_dataset('TIME_STAMPS', data=self.time_stamps)
            hf.close()
        except Exception as e:
            logging.error(e)
            logging.error("Failed to load and process")

    def On_Load_Button(self):
        for i in range(len(self.bools)):
            if self.bools[i] and app.mainframe.geometric_transfor_frame.geometric_properties_list[i].load_bool.get():

                head, tail = os.path.split(self.paths[i])
                file_path = os.path.join(head,"jpg")

                crops = [int(app.mainframe.geometric_transfor_frame.geometric_properties_list[i].crop_lhs_stringVar.get()),
                            int(app.mainframe.geometric_transfor_frame.geometric_properties_list[i].crop_top_stringVar.get()),
                            int(app.mainframe.geometric_transfor_frame.geometric_properties_list[i].crop_rhs_stringVar.get()),
                            int(app.mainframe.geometric_transfor_frame.geometric_properties_list[i].crop_bottom_stringVar.get())]

                self.Load_to_Array(file_path, crops)
                file_path = head
                self.Load_and_Process(file_path,self.sails[i])

class   Graph_Popup(tk.Toplevel):
    def __init__(self, master, title, fig,type, source):
        super().__init__(master)
        self.title = title
        self.type = type
        self.source = int(source)
        self.close_button = tk.Button(self, text="Close", command=self.destroy)
        self.close_button.grid(row=0, column=2, padx=10, pady=10)
        if self.type == "search":
            stringVars_main = [app.mainframe.autoscan_parent.pages[self.source].threshold_search_min_stringVar,
                          app.mainframe.autoscan_parent.pages[self.source].threshold_search_max_stringVar,
                          app.mainframe.autoscan_parent.pages[self.source].threshold_search_increment_stringVar]

            self.stringVars = []
            trace = []

            lebel_text = ["Threshold Search min value", "Threshold Search max value", "Threshold Search increment value"]
            label_widgets = []
            entry_widgets = []
            for i in range(3):
                stringVar = tk.StringVar()
                stringVar.set(stringVars_main[i].get())

                trace = stringVar.trace_add("write", app.mainframe.autoscan_parent.pages[self.source].Update_From_Popup)
                self.stringVars.append(stringVar)
                label = tk.Label(self, text=lebel_text[i])
                label.grid(row=1, column=i, padx=2, pady=2)
                label_widgets.append(label)
                entry = tk.Entry(self, textvariable=self.stringVars[i], width=5)
                entry.grid(row=2, column=i)
                entry_widgets.append(entry)

        canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.grid(row=3, column=0, columnspan=5, sticky='nsew')

class   Autoscan_Frame(tk.Frame):
    def __init__(self, master, path, index):
        super().__init__(master)

        self.index_stringVar = tk.StringVar()
        self.index_stringVar.set(index)
        self.path_to_h5_stringVar = tk.StringVar()
        self.path_to_h5_stringVar.set(path)
        self.stripe_count_stringVar = tk.StringVar()
        self.stripe_count_stringVar.set("")
        self.threshold_offset_stringVar = tk.StringVar()
        self.threshold_offset_stringVar.set("")
        self.red_orig_stringVar = tk.StringVar()
        self.red_orig_stringVar.set("256")
        self.green_orig_stringVar = tk.StringVar()
        self.green_orig_stringVar.set("165")
        self.blue_orig_stringVar = tk.StringVar()
        self.blue_orig_stringVar.set("130")
        self.count_filter_lower_stringVar = tk.StringVar()
        self.count_filter_lower_stringVar.set("0.1")
        self.count_filter_upper_stringVar = tk.StringVar()
        self.count_filter_upper_stringVar.set("0.9")
        self.set_eps_mult_stringVar = tk.StringVar()
        self.set_eps_mult_stringVar.set("0.005")
        self.set_min_mult_stringVar = tk.StringVar()
        self.set_min_mult_stringVar.set("0.001")
        self.pic_eps_mult_stringVar = tk.StringVar()
        self.pic_eps_mult_stringVar.set("0.005")
        self.pic_min_mult_stringVar = tk.StringVar()
        self.pic_min_mult_stringVar.set("0.001")
        self.cluster_offset_stringVar = tk.StringVar()
        self.cluster_offset_stringVar.set("")
        self.pic_db_samples_stringVar = tk.StringVar()
        self.pic_db_samples_stringVar.set("10")
        self.threshold_search_min_stringVar = tk.StringVar()
        self.threshold_search_min_stringVar.set("175")
        self.threshold_search_max_stringVar = tk.StringVar()
        self.threshold_search_max_stringVar.set("200")
        self.threshold_search_increment_stringVar = tk.StringVar()
        self.threshold_search_increment_stringVar.set("5")

        self.norm_1_bool = tk.BooleanVar()
        self.norm_1_bool.set(True)
        self.norm_2_bool = tk.BooleanVar()
        self.norm_2_bool.set(False)
        self.norm_3_bool = tk.BooleanVar()
        self.norm_3_bool.set(True)
        self.pdf_bool = tk.BooleanVar()
        self.pdf_bool.set(False)
        self.jpg_bool = tk.BooleanVar()
        self.jpg_bool.set(True)
        self.sql_bool = tk.BooleanVar()
        self.sql_bool.set(True)
        self.generate_pixcels_run_bool = tk.BooleanVar()
        self.generate_pixcels_run_bool.set(False)

        self.path_to_h5_label = tk.Label(self, textvariable=self.path_to_h5_stringVar, font='none 10')
        self.path_to_h5_label.configure(wraplength=150)
        self.red_orig_label = tk.Label(self, text="Target Colour Red - ", font='none 12')
        self.green_orig_label = tk.Label(self, text="Target Colour Green - ", font='none 12')
        self.blue_orig_label = tk.Label(self, text="Target Colour Blue - ", font='none 12')
        self.header_label = tk.Label(self, text="AutoScan Hyperparameters", font='Bold 14')
        self.stripe_count_label = tk.Label(self, text="Stripe Count - ", font='none 12')
        self.threshold_offset_label = tk.Label(self, text="Threshold Offset - ", font='none 12')
        self.lower_count_label = tk.Label(self, text="Lower Count Filter - ", font='none 12')
        self.upper_count_label = tk.Label(self, text="Upper Count - ", font='none 12')
        self.set_eps_mult_label = tk.Label(self, text="Set Eps Multiplier - ", font='none 12')
        self.set_min_mult_label = tk.Label(self, text="Set Min Multiplier - ", font='none 12')
        self.cluster_offset_label = tk.Label(self, text="Cluster Offset - ", font='none 12')
        self.pic_eps_mult_label = tk.Label(self, text="Pic Eps Multiplier - ", font='none 12')
        self.pic_min_mult_label = tk.Label(self, text="Pic Min Multiplier - ", font='none 12')
        self.pic_db_samples_label = tk.Label(self, text="# Samples for pic DB Scan - ", font='none 12')
        self.file_info_label = tk.Label(self, text="File Info ", font='bold 12')
        self.colour_label = tk.Label(self, text="Colour and Normalisation ", font='bold 12')
        self.threshold_label = tk.Label(self, text="Thresholding ", font='bold 12')
        self.dbScan_label = tk.Label(self, text="DB Scan and PCA", font='bold 12')

        self.h5_chooser_button = tk.Button(self, text="Select .H5 File", command=self.Open_H5_File)
        self.load_h5_button = tk.Button(self, text="Load .H5 File", command=self.Load_H5_File)
        self.run_all_button = tk.Button(self, text="Run All", command=self.Run_All)
        self.threshold_graph_button = tk.Button(self, text="Threshold Graph", command=self.Threshold_Graph)
        self.offset_sweep_button = tk.Button(self, text="Offset Sweep", command=self.Open_Offset_Sweep)
        self.count_cleaning_graphs_button = tk.Button(self, text="Count Cleaning Graphs", command=self.Count_Cleaning_Graphs)
        self.generate_pixcels_button = tk.Button(self, text="Generate Pixcels", command=self.Generate_pixcels)
        self.check_set_dbScan_button = tk.Button(self, text="Check Set DB Scan", command=self.Check_Set_DBScan)
        self.set_dbScan_button = tk.Button(self, text="Run DB Scan on Set", command=self.SetDBScan)
        self.check_pic_dbScan_button = tk.Button(self, text="Check PIC DB Scan", command=self.Check_Pic_DBScan)
        self.pic_dbScan_button = tk.Button(self, text="Run DB Scan on Pics", command=self.Run_Pic_DBScan)
        self.fit_splines_calc_button = tk.Button(self, text="Fit Splines and Calculate Properties", command=self.Fit_Splines_Calc_Properties)
        self.export_button = tk.Button(self, text="Export Results", command=self.Export_Results)
        self.sql_button = tk.Button(self, text="Enter SQL Credentials", command=self.Enter_SQL_Credentials)

        self.stripe_count_combo = ttk.Combobox(self, textvariable=self.stripe_count_stringVar, width=5)
        self.stripe_count_combo['values'] = [2, 3, 4, 5]
        self.stripe_count_combo.state(["readonly"])
        self.stripe_count_combo.current(2)


        self.threshold_offset_combo = ttk.Combobox(self, textvariable=self.threshold_offset_stringVar, width=5)
        self.threshold_offset_combo['values'] = [-6, -5, -4, -3, -2, -1, 0, 1, 2, 3]
        self.threshold_offset_combo.state(["readonly"])
        self.threshold_offset_combo.current(6)

        self.cluster_offset_combo = ttk.Combobox(self, textvariable=self.cluster_offset_stringVar, width=5)
        self.cluster_offset_combo['values'] = [-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6]
        self.cluster_offset_combo.state(["readonly"])
        self.cluster_offset_combo.current(6)

        self.norm_1_check = tk.Checkbutton(self, text="Length Normalisation", variable=self.norm_1_bool, onvalue=True, offvalue=False)
        self.norm_2_check = tk.Checkbutton(self, text="Colour Normalisation", variable=self.norm_2_bool, onvalue=True, offvalue=False)
        self.norm_3_check = tk.Checkbutton(self, text="RGB Chrom Normalisation", variable=self.norm_3_bool, onvalue=True, offvalue=False)
        self.pdf_check= tk.Checkbutton(self, text="PDF", variable=self.pdf_bool, onvalue=True, offvalue=False)
        self.jpg_check = tk.Checkbutton(self, text="JPG", variable=self.jpg_bool, onvalue=True, offvalue=False)
        self.sql_check = tk.Checkbutton(self, text="SQL", variable=self.sql_bool, onvalue=True, offvalue=False)

        self.red_orig_entry = tk.Entry(self, textvariable=self.red_orig_stringVar, width=5)
        self.green_orig_entry = tk.Entry(self, textvariable=self.green_orig_stringVar, width=5)
        self.blue_orig_entry = tk.Entry(self, textvariable=self.blue_orig_stringVar, width=5)
        self.count_filter_lower_entry = tk.Entry(self, textvariable=self.count_filter_lower_stringVar, width=5)
        self.count_filter_upper_entry = tk.Entry(self, textvariable=self.count_filter_upper_stringVar, width=5)
        self.set_eps_mult_entry = tk.Entry(self, textvariable=self.set_eps_mult_stringVar, width=5)
        self.set_min_mult_entry = tk.Entry(self, textvariable=self.set_min_mult_stringVar, width=5)
        self.pic_eps_mult_entry = tk.Entry(self, textvariable=self.pic_eps_mult_stringVar, width=5)
        self.pic_min_mult_entry = tk.Entry(self, textvariable=self.pic_min_mult_stringVar, width=5)
        self.pic_db_samples_entry = tk.Entry(self, textvariable=self.pic_db_samples_stringVar, width=5)

        self.path_to_h5_label.grid(row=2, column=0)
        self.h5_chooser_button.grid(row=2, column=1, padx=5)
        self.load_h5_button.grid(row=2, column=2, padx=5, sticky=tk.W)
        self.stripe_count_label.grid(row=2, column=2, sticky=tk.E)
        self.stripe_count_combo.grid(row=2, column=3, sticky=tk.W)
        self.run_all_button.grid(row=2, column=4)
        self.colour_label.grid(row=3, column=0, columnspan=4, padx=10, pady=5)
        self.red_orig_label.grid(row=4, column=0, sticky=tk.E)
        self.red_orig_entry.grid(row=4, column=1, sticky=tk.W)
        self.norm_1_check.grid(row=4, column=2)
        self.green_orig_label.grid(row=5, column=0, sticky=tk.E)
        self.green_orig_entry.grid(row=5, column=1, sticky=tk.W)
        self.norm_2_check.grid(row=5, column=2)
        self.blue_orig_label.grid(row=6, column=0, sticky=tk.E)
        self.blue_orig_entry.grid(row=6, column=1, sticky=tk.W)
        self.norm_3_check.grid(row=6, column=2)
        self.threshold_label.grid(row=7, column=0, columnspan=4, padx=10, pady=5)
        self.threshold_offset_label.grid(row=8, column=0, sticky=tk.E)
        self.threshold_offset_combo.grid(row=8, column=1, sticky=tk.W)
        self.threshold_graph_button.grid(row=8, column=2)
        self.lower_count_label.grid(row=9, column=0, sticky=tk.E)
        self.count_filter_lower_entry.grid(row=9, column=1, sticky=tk.W)
        self.offset_sweep_button.grid(row=9, column=2, rowspan=2)
        self.upper_count_label.grid(row=10, column=0, sticky=tk.E)
        self.count_filter_upper_entry.grid(row=10, column=1, sticky=tk.W)
        self.count_cleaning_graphs_button.grid(row=10, column=2, rowspan=2)
        self.generate_pixcels_button.grid(row=11, column=1, padx=15, pady=10)
        self.dbScan_label.grid(row=12, column=0, columnspan=4, padx=10, pady=5)
        self.set_eps_mult_label.grid(row=13, column=0, sticky=tk.E)
        self.set_eps_mult_entry.grid(row=13, column=1, sticky=tk.W)
        self.set_min_mult_label.grid(row=14, column=0, sticky=tk.E)
        self.set_min_mult_entry.grid(row=14, column=1, sticky=tk.W)
        self.cluster_offset_label.grid(row=15, column=0, sticky=tk.E)
        self.cluster_offset_combo.grid(row=15, column=1, sticky=tk.W)
        self.check_set_dbScan_button.grid(row=15, column=2)
        self.set_dbScan_button.grid(row=16, column=1, padx=15, pady=10)
        self.pic_eps_mult_label.grid(row=17, column=0, sticky=tk.E)
        self.pic_eps_mult_entry.grid(row=17, column=1, sticky=tk.W)
        self.pic_db_samples_label.grid(row=17, column=2, sticky=tk.E)
        self.pic_db_samples_entry.grid(row=17, column=3, sticky=tk.W)
        self.pic_min_mult_label.grid(row=18, column=0, sticky=tk.E)
        self.pic_min_mult_entry.grid(row=18, column=1, sticky=tk.W)
        self.check_pic_dbScan_button.grid(row=18, column=2)
        self.pic_dbScan_button.grid(row=19, column=1, padx=15, pady=10)
        self.fit_splines_calc_button.grid(row=20, column=1, padx=15, pady=10)
        self.pdf_check.grid(row=21, column=0)
        self.jpg_check.grid(row=21, column=1)
        self.sql_check.grid(row=21, column=2)
        self.sql_button.grid(row=21, column=3)
        self.export_button.grid(row=22, column=1, padx=15, pady=10)

    def Update_From_Popup(self,*args):
        print('Update_From_Popup')
        self.threshold_search_min_stringVar.set(self.thresh_graph.stringVars[0].get())
        self.threshold_search_max_stringVar.set(self.thresh_graph.stringVars[1].get())
        self.threshold_search_increment_stringVar.set(self.thresh_graph.stringVars[2].get())
        print(self.threshold_search_min_stringVar.get())
        self.generate_pixcels_run_bool.set(False)

    def Make_Plot(self,fig,gridPos, gridSpan):
        canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.grid(row=gridPos[0], column=gridPos[1], rowspan=gridSpan[0], columnspan=gridSpan[1],  sticky='nsew')

    def Open_H5_File(self):
        self.path_to_h5_stringVar.set(tk.filedialog.askopenfilename(initialdir=self.path_to_h5_stringVar.get()))

    def Load_H5_File(self):
        normalisations = []
        if self.norm_1_bool.get():
            normalisations.append(1)
        if self.norm_2_bool.get():
            normalisations.append(2)
        if self.norm_3_bool.get():
            normalisations.append(3)
        self.features = veeringCV.VeeringNormalisation(self.path_to_h5_stringVar.get())
        self.features.RunNormalisation(normalisations)
        print("H5 files loaded and normalised")

    def Run_All(self):
        print("Running All")
        self.Load_H5_File()
        self.Generate_pixcels()

    def Threshold_Graph(self):
        if self.generate_pixcels_run_bool.get() == False:
            self.Generate_pixcels()
        self.thresholds.Threshold_Graphs()
        print(self.thresholds.searchRange)
        Graph_Popup(self,"Threshold Selection", self.thresholds.thesholdFigure, "search", self.index_stringVar.get())

    def Open_Offset_Sweep(self):
        targetColour = [int(self.red_orig_stringVar.get()), int(self.green_orig_stringVar.get()),
                        int(self.blue_orig_stringVar.get())]
        self.threshold_for_sweep = veeringCV.Thresholding(self.features.pixcels,targetColour,[int(self.threshold_search_min_stringVar.get()),int(self.threshold_search_max_stringVar.get()),int(self.threshold_search_increment_stringVar.get())])
        self.threshold_for_sweep.Run_Thresholding()
        self.threshold_for_sweep.Threshold_Sweep_Graphs([-6,-4,-2,0], self.features.origShape, self.features.pixcels)
        Graph_Popup(self,"Threshold Sweep", self.threshold_for_sweep.thresh_offsetPlot, "sweep", self.index_stringVar.get())

    def Count_Cleaning_Graphs(self):
        self.thresholds.Cnt_Filter_Plot()
        Graph_Popup(self,"Count Cleaning", self.thresholds.cnt_filterFig, "count", self.index_stringVar.get())

    def Generate_pixcels(self):
        targetColour = [int(self.red_orig_stringVar.get()), int(self.green_orig_stringVar.get()), int(self.blue_orig_stringVar.get())]
        self.thresholds = veeringCV.Thresholding(self.features.pixcels,targetColour,[int(self.threshold_search_min_stringVar.get()),int(self.threshold_search_max_stringVar.get()),int(self.threshold_search_increment_stringVar.get())])
        self.thresholds.Run_Thresholding()
        self.thresholds.Generate_Stripe_Pixcels(int(self.threshold_offset_combo.get()),self.features.pixcels,self.features.origShape)
        self.thresholds.Count_Filter(float(self.count_filter_lower_entry.get()),float(self.count_filter_upper_entry.get()))
        self.thresholds.Stripes_Plot_Clean()
        self.generate_pixcels_run_bool.set(True)
        self.Make_Plot(self.thresholds.CNT_cleanPlot,[3,4],[4,4])
        print(self.thresholds.threshold)

    def SetDBScan(self):
        multipliers = [float(self.set_eps_mult_stringVar.get()), float(self.set_min_mult_stringVar.get())]
        self.set_db = veeringCV.Set_DB(self.thresholds.stripes, multipliers, self.thresholds.countFilter_ind, int(self.cluster_offset_stringVar.get()))
        self.set_db.Set_PCA_DB()
        self.set_db.Make_DB_Scan_Set()

    def Check_Set_DBScan(self):
        multipliers = [float(self.set_eps_mult_stringVar.get()), float(self.set_min_mult_stringVar.get())]
        self.set_db = veeringCV.Set_DB(self.thresholds.stripes, multipliers, self.thresholds.countFilter_ind,
                                       int(self.cluster_offset_stringVar.get()))
        self.set_db.Set_PCA_DB()
        self.set_db.Cluster_Filter_FIG()
        self.set_db.Cluster_Plot_FIG()
        self.plot_comb, axes = plt.subplots(2,1)
        Graph_Popup(self, "Set DB Scan", self.set_db.cluster_Plot, "inspection", self.index_stringVar.get())

    def Check_Pic_DBScan(self):
        print("Checking Pic DB Scan")

    def Run_Pic_DBScan(self):
        print("Running Pic DB Scan")

    def Fit_Splines_Calc_Properties(self):
        print("Fitting Splines Calc Properties")

    def Export_Results(self):
        print("Exporting Results")

    def Enter_SQL_Credentials(self):
        print("Entering SQL Credentials")

class   Autoscan_Parent(ttk.Notebook):
    def __init__(self, master):
        super().__init__(master)
        self.pages_made = []
        self.pages = []
    def Make_Autoscan_NB(self):

        self.bools = [app.mainframe.import_frame.port_main.check_bool.get(),
                 app.mainframe.import_frame.stb_main.check_bool.get(),
                 app.mainframe.import_frame.port_jib.check_bool.get(),
                 app.mainframe.import_frame.stb_jib.check_bool.get()]

        self.paths = [app.mainframe.import_frame.port_main_path_final_stringVar.get(),
                 app.mainframe.import_frame.stb_main_path_final_stringVar.get(),
                 app.mainframe.import_frame.port_jib_path_final_stringVar.get(),
                 app.mainframe.import_frame.stb_jib_path_final_stringVar.get()]

        self.sails = ['Port Main', 'Stb Main', 'Port Jib', 'Stb Jib']


        for i in range(len(self.bools)):
            if self.bools[i]:
                if self.sails[i] not in self.pages_made:
                    page = Autoscan_Frame(self, self.paths[i], i)
                    self.add(page, text=self.sails[i])
                    self.pages.append(page)
                    self.pages_made.append(self.sails[i])

                else:
                    self.pages[i].path_to_h5_stringVar.set(self.paths[i])

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
        self.geometric_transfor_frame=Geometric_Transforms_Frame(self)
        self.autoscan_parent=Autoscan_Parent(self)
        #self.frame6=Results_cleaning_Frame(self.notebook)
        #self.frame7=Reporting_Frame(self.notebook)

        self.add(self.import_frame, text='Import')
        self.add(self.data_cleaning,text='Data Cleaning')
        self.add(self.filter_frame,text='Filter' )
        self.add(self.geometric_transfor_frame,text='Geometric Transforms')
        self.add(self.autoscan_parent,text='Autoscan')
        #self.notebook.add(self.frame6,text='Results Cleaning')
        #self.notebook.add(self.frame7,text='Results Cleaning')

        self.pack(fill='both', expand=True)
        self.bind('<<NotebookTabChanged>>', self.OnNotebookTabChanged)

    def OnNotebookTabChanged(self, *args):
        self.data_cleaning.topFrame.Update_From_Import()
        #self.data_cleaning.topFrame.On_Load_Log()
        self.data_cleaning.midFrame.Update_From_Import()
        #self.data_cleaning.midFrame.On_Load_Event()
        self.filter_frame.Update_From_Import()
        self.filter_frame.Togle_Filter_Update()
        self.geometric_transfor_frame.Make_Geometry_Transforms()
        self.autoscan_parent.Make_Autoscan_NB()


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

