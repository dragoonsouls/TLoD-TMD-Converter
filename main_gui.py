"""

MAIN GUI: main Python code to create the GUI for TLoD TMD Converter

Copyright (C) 2023 DooMMetaL
"""

from tkinter import INSERT, CENTER, END, Canvas, Tk, Button, Frame, Text, LabelFrame, Label, messagebox, Scrollbar, Toplevel, Listbox, Checkbutton, IntVar, ttk, Entry
from tkinter.filedialog import askopenfile, askdirectory
from PIL import ImageTk, Image
import webbrowser
import database_to_listbox as dtl
import tlod_tmd_converter
import force_animation_loading
import convert_queue_files
import os

class Options:
    def __init__(self):
        self.self = Options
        self.read_write_options()
    
    def read_write_options(self):
        self.option_file = f'Resources/converter_config.config'
        global size_x
        global size_y
        global sc_folder_def
        global dump_folder
        global first_run
        size_x = None
        size_y = None
        sc_folder_def = None
        dump_folder = None
        first_run = True

        little_root = Tk()
        little_root.iconbitmap(default='Resources/DD_Eye.ico')
        little_root.wm_withdraw()
        with open(self.option_file, 'r') as read_config: # Reading the Config file to
            read_all_config = read_config.readlines()
            for r_all_config in read_all_config:
                if f'FIRST_RUN' in r_all_config:
                    start_read_fr = r_all_config.find(f'=')
                    read_fr = r_all_config[start_read_fr + 1:].strip()
                    if read_fr == f'True':
                        message_box_first_time = messagebox.showinfo(title='First Time Configuration', message='Now we will do a Startup Configuration...')
                        first_run = False
                    else:
                        first_run = False

                elif f'DEFAULT_RES_X' in r_all_config:
                    start_x = r_all_config.find(f'=')
                    r_a_config_x = r_all_config[start_x + 1:].strip()
                    size_x = int(r_a_config_x)
                
                elif f'DEFAULT_RES_Y' in r_all_config:
                    start_y = r_all_config.find(f'=')
                    r_a_config_y = r_all_config[start_y + 1:].strip()
                    size_y = int(r_a_config_y)
                
                elif f'SC_FOLDER' in r_all_config:
                    start_read_sc = r_all_config.find(f'=')
                    read_sc = r_all_config[start_read_sc + 1:].strip()
                    if read_sc != f'None':
                        sc_folder_def = read_sc
                    else:
                        message_box_sc = messagebox.showinfo(title=f'SELECT SC FOLDER', message='Please select the folder called \"files\" in SC root folder')
                        root_files_sc = askdirectory(title='Select files folder from SC')
                        getting_all_folders = os.walk(root_files_sc)

                        if root_files_sc == f'':
                            messagebox.showerror(title=f'Incorrect SC FOLDER', message='FATAL CRASH!: Folder not selected')
                            exit()

                        for root, dirs, files in getting_all_folders:
                            if f'files' in root:
                                sc_folder_def = root_files_sc
                                break
                            else:
                                messagebox.showerror(title=f'Incorrect SC FOLDER', message=f'Something went wrong, this is not the SC root folder')
                                exit()
                
                elif f'DUMP_FOLDER' in r_all_config:
                    start_read_dump = r_all_config.find(f'=')
                    read_dump = r_all_config[start_read_dump + 1:].strip()
                    if read_dump == f'None':
                        messagebox.showinfo(title='SELECT A FOLDER TO DUMP', message='Please, select a folder to dump converted files.\nRecommendation: Do not create inside SC FOLDER')
                        new_dump_folder = askdirectory(title='SELECT A FOLDER TO DUMP FILES')
                        dump_folder = new_dump_folder
                    else:
                        dump_folder = read_dump
        
        self.write_options(self, path_cnf_file=self.option_file, first_run=False, size_x=size_x, size_y=size_y, sc_folder_def=sc_folder_def, dump_folder=dump_folder)
        little_root.destroy()
        return size_x, size_y

    def write_options(self, path_cnf_file=str, first_run=bool, size_x=int, size_y=int, sc_folder_def=str, dump_folder=str):
        
        if ((size_x == None) or (size_y == None) or (sc_folder_def == None) or (dump_folder == None)) and (first_run == True):
            return messagebox.showerror(title='FATAL CRASH!!', message='Unexpected condition of First Run, please report this error immediately')
        else:
            path_to_config_file = path_cnf_file
            with open(path_to_config_file, 'w') as writing_options:
                header = f'[CONFIG]\n'
                fr_flag = f'FIRST_RUN = {first_run}\n'
                def_res_x = f'DEFAULT_RES_X = {size_x}\n'
                def_res_y = f'DEFAULT_RES_Y = {size_y}\n'
                def_sc_folder = f'SC_FOLDER = {sc_folder_def}\n'
                dump_f = f'DUMP_FOLDER = {dump_folder}'
                grabbing_every_str = header + fr_flag + def_res_x + def_res_y + def_sc_folder + dump_f
                writing_options.write(grabbing_every_str)

class TCWindow(Frame):
    # Constructor

    def __init__(self, master=None, width=int, height=int):
        super().__init__(master, width=width, height=height)
        self.master = master
        self.pack()
        self.create_widget(width_mainframe=width, height_mainframe=height)
    
    def create_widget(self, width_mainframe=int, height_mainframe=int):
        #### Creation of widgets ####
        # Buttons - Labels - Frame - Text [Text Box Output]
        ## Image
        self.image_filename = "Resources/Ruff_GUI.png"
        self.model_database = "Model_Database/"
        self.create_list_files = dtl.DatabaseDict.process_database(self=dtl.DatabaseDict(database_path=self.model_database), database_path_str=self.model_database)
        self.open_image = Image.open(self.image_filename)
        self.x_y_values = self.resize_window(width_mainframe_change=width_mainframe, height_mainframe_change=height_mainframe)
        self.resize_image = self.open_image.resize(self.x_y_values, Image.Resampling.LANCZOS)
        self.image_background = ImageTk.PhotoImage(image=self.resize_image)
        ## Canvas (Background image)
        self.background_canvas = Canvas(self, width=self.x_y_values[0], height=self.x_y_values[1])

        ## Buttons - Main Frame
        self.tmd_button = Button(self, text='Model Conversion', command=self.convert_model, cursor='hand2')
        self.advanced_button = Button(self, text='Advanced Conversion', command=self.advanced_conversion, cursor='hand2')
        ## LabelFrame - Info and Conversion Result
        self.label_info = LabelFrame(self, text='Info... Ruff')
        self.label_dump = LabelFrame(self, text='Conversion Result')
        ## Label - Parent Info LabelFrame
        self.tmd_label = Label(self.label_info, text= f'Model Conversion: Convert a Model into DAE file format,\nif no animation data embedded or loaded,\nobjects will be placed at the retail Origin Point.', justify=CENTER)
        ## Text - Parent Conversion Result LabelFrame
        self.conversion_text = Text(self.label_dump)
        initial_text = f'||||---> TLoD TMD CONVERTER <---||||\nIMPORTANT NOTE: For TMD and CTMD Files from DEFF packages, \ntool will try to find embedded CMB/LMB/SAF animations'
        self.conversion_text.insert(INSERT, initial_text)
        self.conversion_text.config(state='disabled')
        ## ScrollBar for Text Dump
        self.scrollbar_text = Scrollbar(self.conversion_text, command=self.conversion_text.yview, cursor='arrow')
        ## About Button
        self.about_button = Button(self, text="About", command=self.execute_about, cursor='hand2')
        ## Configuration Button
        self.config_button = Button(self, text='CONFIG', cursor="hand2", command=self.configure_tool)
        ## Github Hyperlink
        self.github_page = Label(self, text='https://github.com/Legend-of-Dragoon-Modding/TLoD-TMD-Converter', font=('Calibri', 11), fg='#0000EE', cursor='hand2')

        #### Placing Methods ####
        self.background_canvas.place(relwidth=1, relheight=1, relx=-0.28, rely= -0.25)
        self.background_canvas.create_image(self.x_y_values[0], self.x_y_values[1], image=self.image_background)
        self.tmd_button.place(relwidth=0.2, relheight=0.1, relx=0.30, rely=0.01)
        self.advanced_button.place(relwidth=0.2, relheight=0.1, relx=0.55, rely=0.01)
        self.label_info.place(relx=0.26, rely=0.15, relwidth= 0.55, relheight= 0.23)
        self.label_dump.place(relx=0.26, rely=0.40, relwidth= 0.70, relheight= 0.53)
        self.tmd_label.place(relx=0.01, rely=0.01, relwidth= 0.9, relheight= 0.9)
        self.tmd_label.config(font=('Arial Black', 12), fg='#4578b0')
        self.conversion_text.place(relx=0.001, rely=0.01, relwidth= 0.99, relheight= 0.98)
        self.conversion_text.config(yscrollcommand=self.scrollbar_text.set)
        self.scrollbar_text.place(relx=0.975, rely=0, relwidth= 0.03, relheight= 1)
        self.about_button.place(relx=0.05, rely=0.69, relwidth= 0.15, relheight= 0.1)
        self.config_button.place(relx=0.05, rely=0.79, relwidth= 0.15, relheight= 0.1)
        self.github_page.place(relx=0.35, rely=0.93, relwidth= 0.4, relheight= 0.07)
        self.github_page.bind("<Button-1>", lambda e: self.callback_link('https://github.com/Legend-of-Dragoon-Modding/TLoD-TMD-Converter'))
    
    # Main Window Callbacks

    def resize_window(self, width_mainframe_change=int, height_mainframe_change=int):
        self.image_width_changed = round((60 * width_mainframe_change) / 100)
        self.image_height_changed = round((60 * height_mainframe_change) / 100)
        self.tuple_xy_changed = self.image_width_changed, self.image_height_changed
        return self.tuple_xy_changed

    def execute_about(self): # About Button show
        message_about = f'TLoD TMD Converter BETA v0.3 \nCoded By DooMMetal (AKA DragoonSouls) 2023 ©\nThis Tool was made from fans to fans!, keep it as it is!\nVisit my Github for updates'
        self.message_box_win = messagebox.showinfo('About TLoD TMD Converter', message_about)
    
    def callback_link(self, url=str):
        webbrowser.open_new_tab(url)

    # Convert Models Windows

    def convert_model(self):
        # Create new Widget for the Select Box
        self.new_window_box = Toplevel(master=self)
        self.new_window_box.grab_set()
        self.new_window_box.focus_set()
        x_main = self.x_y_values[0]
        y_main = self.x_y_values[1]
        self.new_window_box.title(string=f'Select the Files you want to Convert')
        self.new_window_box.geometry(f'+%d+%d' %(x_main // 2, y_main // 2))
        self.new_window_box.geometry(f'{x_main + (x_main - 200)}x{y_main + (y_main - 125)}')
        
        # Create Convert All and Merge Check Boxes - BUT FIRST I NEED A FRAME
        self.labelf_container_checkboxes = LabelFrame(master=self.new_window_box, text='Options')
        self.check_all_convert_variable = IntVar()
        self.merge_animations_variable = IntVar()
        self.convert_all_check = Checkbutton(master=self.labelf_container_checkboxes, text=f'Convert All', variable=self.check_all_convert_variable)
        self.merge_animations_check = Checkbutton(master=self.labelf_container_checkboxes, text=f'Merge Animations', variable=self.merge_animations_variable)
        self.merge_animations_check.configure(state='disabled')

        # Create the Parent List Box
        self.list_box_conversion_parent_table = Listbox(self.new_window_box, cursor="hand2", selectmode='single')
        # Create Sub List Box
        self.list_box_conversion_sublist = Listbox(self.new_window_box, cursor="hand2", selectmode='multiple')
        self.scroll_listbox_2 = Scrollbar(self.list_box_conversion_sublist, command=self.list_box_conversion_sublist.yview, orient='vertical', cursor='arrow')
        self.list_box_conversion_sublist.config(yscrollcommand=self.scroll_listbox_2.set)
        self.list_box_conversion_sublist.configure(state='disabled')
        # Conversion Queue List Box
        self.conversion_queue_listbox = Listbox(self.new_window_box)
        self.scroll_queue_listbox = Scrollbar(self.conversion_queue_listbox, command=self.conversion_queue_listbox.yview, orient='vertical', cursor='arrow')
        self.conversion_queue_listbox.config(yscrollcommand=self.scroll_queue_listbox.set)
        self.conversion_queue_listbox.configure(state='disabled')

        # Options Check Buttons Callbacks
        self.convert_all_check.configure(command=lambda: self.convert_all_models())
                
        # Populating Parent List Box (the only really necessary)
        self.populate_listbox(table_to_populate=self.list_box_conversion_parent_table, list_objects=self.create_list_files)
        # Parent List - Sub List Box Callbacks
        self.list_box_conversion_parent_table.bind("<<ListboxSelect>>", lambda e: self.handling_parentlist_callback())
        self.list_box_conversion_sublist.bind("<<ListboxSelect>>", lambda e: self.handling_sublist_callback())

        # Buttons for Add/Remove From Parent List Box to Sub-List Box
        self.move_to_sub_listbox_button = Button(self.new_window_box, text='Add', cursor='arrow')
        self.move_to_sub_listbox_button.configure(state='disabled')
        # Buttons for Add/Remove From Sub-List Box to Queue List Box
        self.move_to_queue = Button(self.new_window_box, text='Add', cursor='arrow')
        self.move_to_queue.configure(state='disabled')
        self.select_all_sublist_button = Button(self.new_window_box, text='Select All', cursor='arrow')
        self.select_all_sublist_button.configure(state='disabled')
        self.clear_sublist_button = Button(self.new_window_box, text='Clear List', cursor='arrow')
        self.clear_sublist_button.configure(state='disabled')

        # Placing the Check Buttons and the Frame
        self.labelf_container_checkboxes.place(relx=0.01, rely=0.01, relwidth=0.97, relheight=0.12)
        self.convert_all_check.place(relx=0.1, rely=0.01, relwidth=0.3, relheight=0.9)
        self.merge_animations_check.place(relx=0.5, rely=0.01, relwidth=0.3, relheight=0.9)

        # Placing List Boxes
        self.list_box_conversion_parent_table.place(relx=0.01, rely=0.15, relwidth= 0.12, relheight= 0.30)
        self.list_box_conversion_sublist.place(relx=0.23, rely=0.15, relwidth= 0.3, relheight= 0.30)
        self.scroll_listbox_2.place(relx=0.95, rely=0, relwidth= 0.05, relheight= 1) # This is parented to the previous ListBox
        # Placing Queue List Box
        self.conversion_queue_listbox.place(relx=0.01, rely=0.47, relwidth= 0.97, relheight= 0.4)
        self.scroll_queue_listbox.place(relx=0.975, rely=0, relwidth= 0.025, relheight= 1) # This is parented to the previous ListBox

        # Placing Related List Box Buttons
        self.move_to_sub_listbox_button.place(relx=0.13, rely=0.225, relwidth= 0.10, relheight= 0.1)
        self.move_to_queue.place(relx=0.53, rely=0.15, relwidth= 0.1, relheight= 0.1)
        self.select_all_sublist_button.place(relx=0.53, rely=0.25, relwidth= 0.1, relheight= 0.1)
        self.clear_sublist_button.place(relx=0.53, rely=0.35, relwidth= 0.1, relheight= 0.1)

        # Buttons
        self.button_convert_models = Button(master=self.new_window_box, cursor="arrow", text=f'Convert Models')
        self.button_convert_models.configure(state='disabled', command=lambda: self.convert_models_process())
        # Placing Buttons
        self.button_convert_models.place(relx=0.35, rely=0.88, relwidth= 0.3, relheight= 0.1)

        # Total Models in Queue Label
        self.count_models_queue()

    def advanced_conversion(self):
        ## Setting the new created window
        global advanced_conversion_window
        advanced_conversion_window = Toplevel(self)
        advanced_conversion_window.grab_set()
        advanced_conversion_window.focus_set()
        x_main = main_window.winfo_x()
        y_main = main_window.winfo_y()
        advanced_conversion_window.title(string=f'Advanced Conversion Options')
        advanced_conversion_window.geometry(f'+%d+%d' %(x_main + 300, y_main + 150))
        advanced_conversion_window.geometry(f'{x_main + 100}x{y_main + 50}')
        advanced_conversion_window.attributes('-topmost', True)
        advanced_conversion_window.resizable(False, False)

        ## Buttons - Advance Conversion Options
        model_conversion_button = Button(master=advanced_conversion_window, text=f'Manual Conversion', command=self.convert_model_advanced, cursor='hand2')
        animation_conversion_button = Button(master=advanced_conversion_window, text=f'Force Animation', command=self.force_animation, cursor='hand2')

        ## Placing Stuff
        model_conversion_button.place(relwidth=0.8, relheight=0.4, relx=0.1, rely=0.05)
        animation_conversion_button.place(relwidth=0.8, relheight=0.4, relx=0.1, rely=0.5)
    
    def convert_model_advanced(self):
        advanced_conversion_window.attributes('-topmost', False)
        self.conversion_text.config(state='normal')
        model_to_convert = askopenfile(title=f'Select a Model file...')
        self.conversion_text.delete(1.0, END)
        if model_to_convert != None:
            model_path = model_to_convert.name
            try:
                tlod_tmd_converter.main(model_path)
                self.conversion_text.insert(INSERT, tlod_tmd_converter.fma.file_filter_text)
                if tlod_tmd_converter.fma.file_type == f'CTMD':
                    for each_prim_unpack in tlod_tmd_converter.md.ctd.primitive_conversion_info:
                        self.conversion_text.insert(INSERT, each_prim_unpack)
                    self.conversion_text.insert(INSERT, tlod_tmd_converter.md.ctd.primitives_unpacked_info)
                    self.conversion_text.insert(INSERT, tlod_tmd_converter.md.ctd.total_block_vertices_info)
                    self.conversion_text.insert(INSERT, tlod_tmd_converter.md.ctd.vertices_converted_info)
                if tlod_tmd_converter.fma.animation_data_info[2] != f'NONE':
                    self.conversion_text.insert(INSERT, tlod_tmd_converter.fma.animation_check_info)
                    self.conversion_text.insert(INSERT, tlod_tmd_converter.afp.processing_anim)
                    if tlod_tmd_converter.afp.animation_type_check == f'SAF':
                        self.conversion_text.insert(INSERT, tlod_tmd_converter.afp.csaf.conversion_saf_ok)
                        self.conversion_text.insert(INSERT, tlod_tmd_converter.afp.csaf.finished_convert_saf)
                    elif tlod_tmd_converter.afp.animation_type_check == f'CMB':
                        self.conversion_text.insert(INSERT, tlod_tmd_converter.afp.ccmb.cmb_conversion_finished)
                    elif tlod_tmd_converter.afp.animation_type_check == f'LMB_Type_0':
                        self.conversion_text.insert(INSERT, tlod_tmd_converter.afp.clmb.lmb_conversion_finished)
                for check_dup in tlod_tmd_converter.colcomp.check_duplicate_state:
                    self.conversion_text.insert(INSERT, check_dup)
                if tlod_tmd_converter.colcomp.check_bool == True:
                    self.conversion_text.insert(INSERT, tlod_tmd_converter.colcomp.winding_diff_info)
                self.conversion_text.insert(INSERT, tlod_tmd_converter.pr.total_number_vnp)
                self.conversion_text.insert(INSERT, tlod_tmd_converter.cw.collada_success)
            except OSError:
                messagebox.showwarning(title=f'Warning!!...', message=f'Is not a Model file, selct another file...')
                self.conversion_text.delete(1.0, END)
        else:
            error_text = f'\nYou must load a file...'
            self.conversion_text.insert(INSERT, error_text)
        self.conversion_text.config(state='disabled')
    
    def force_animation(self):
        advanced_conversion_window.attributes('-topmost', False)
        self.conversion_text.config(state='normal')
        animation_to_force = askopenfile(title=f'Select an Animation file...')
        self.conversion_text.delete(1.0, END)
        if animation_to_force != None:
            animation_path = animation_to_force.name
            try:
                force_animation_loading.force_animation_loading(input_file=animation_path)
                self.conversion_text.insert(INSERT, force_animation_loading.afp.processing_anim)
                self.conversion_text.insert(INSERT, f'\n')
                self.conversion_text.insert(INSERT, force_animation_loading.df.warning_load)
                self.conversion_text.insert(INSERT, f'\n')
                self.conversion_text.insert(INSERT, force_animation_loading.cw.collada_success)
            except OSError:
                messagebox.showwarning(title=f'Warning!!...', message=f'Is not an Animation file, selct another file...')
                self.conversion_text.delete(1.0, END)
        else:
            error_text = f'\nYou must load a file...'
            self.conversion_text.insert(INSERT, error_text)
        self.conversion_text.config(state='disabled')

    def convert_all_models(self):
        check_done = self.check_all_convert_variable.get()
        if check_done == 1:
            self.list_box_conversion_parent_table.configure(state='disabled')
            self.list_box_conversion_sublist.configure(state='disabled')
            self.move_to_sub_listbox_button.configure(cursor="arrow", state='disabled')
            self.move_to_queue.configure(cursor="arrow", state='disabled')
            self.select_all_sublist_button.configure(cursor="arrow", state='disabled')
            self.button_convert_models.configure(cursor='hand2', state='active')
            self.conversion_queue_listbox.configure(state='normal')
            self.merge_animations_check.configure(state='active')
            
            populate_total = []
            for parents in self.create_list_files:
                sub_dict = self.create_list_files[f'{parents}']
                for sb in sub_dict:
                    string_child = f''
                    if f', ' in sb:
                        find_comma = sb.find(f', ')
                        string_sb = sb[find_comma + 1:]
                        final_sb = string_sb.strip()
                        string_child = final_sb
                    else:
                        final_string = sb.strip()
                        string_child = final_string
                    total_string = f'{parents}==>{string_child}'
                    populate_total.append(total_string)
            self.populate_listbox(table_to_populate=self.conversion_queue_listbox, list_objects=populate_total)

        else:
            self.conversion_queue_listbox.delete(0, END)
            self.list_box_conversion_parent_table.configure(state='normal')
            self.list_box_conversion_sublist.configure(state='normal')
            self.move_to_sub_listbox_button.config(state='active')
            self.list_box_conversion_sublist.delete(0, END)
            self.merge_animations_check.configure(state='disabled')
            if len(self.conversion_queue_listbox.get(0, END)) > 0:
                self.button_convert_models.configure(cursor="hand2", state='active')
                self.conversion_queue_listbox.configure(state='normal')
            else:
                self.button_convert_models.configure(cursor="arrow", state='disabled')

    def populate_listbox(self, table_to_populate, list_objects):
        index_to_place = 0
        for name_key_main in list_objects:
            if f', ' in name_key_main:
                string_start = name_key_main.find(f', ')
                final_string = name_key_main[(string_start + 2):]
                table_to_populate.insert(index_to_place, final_string)
                index_to_place += 1
            else:
                table_to_populate.insert(index_to_place, name_key_main)
                index_to_place += 1

    def handling_parentlist_callback(self):
        selected_item_parent = self.list_box_conversion_parent_table.curselection()
        if len(selected_item_parent) >= 1:
            single_selection = selected_item_parent[0]
            self.selected_parent = self.list_box_conversion_parent_table.get(single_selection)
            self.move_to_sub_listbox_button.configure(cursor= 'hand2',state='active', command=lambda:self.add_button_sublist(add_this_parent=self.selected_parent))
    
    def add_button_sublist(self, add_this_parent=str):
        self.select_all_sublist_button.configure(cursor='hand2', state='active', command=lambda:self.select_all_sublist())
        self.clear_sublist_button.configure(cursor='hand2', state='active', command=lambda:self.clear_sublist())
        self.list_box_conversion_parent_table.configure(state='disabled')
        self.list_box_conversion_sublist.configure(state='normal')
        self.move_to_sub_listbox_button.configure(state='disabled')
        # Populate the Sub List Box after hitting ADD
        sub_list_get = self.create_list_files.get(add_this_parent)
        self.populate_listbox(table_to_populate=self.list_box_conversion_sublist, list_objects=sub_list_get)

    def handling_sublist_callback(self):
        select_item_sublist = self.list_box_conversion_sublist.curselection()
        self.selections_made = []
        for selection_done in select_item_sublist:
            if len(select_item_sublist) >= 1:
                single_sub_selection_index = selection_done
                string_sublist_selected = self.list_box_conversion_sublist.get(single_sub_selection_index)
                self.selections_made.append(string_sublist_selected)
        self.move_to_queue.configure(cursor='hand2', state='active', command= lambda:self.add_to_queue_callback(add_this_parent=self.selected_parent, add_this_objects=self.selections_made))
        self.select_all_sublist_button.configure(cursor='hand2', state='active', command= lambda:self.select_all_sublist())
        self.clear_sublist_button.configure(cursor='hand2', state='active', command=lambda:self.clear_sublist())

    def select_all_sublist(self):
        self.list_box_conversion_sublist.selection_set(0, END)
        select_item_sublist = self.list_box_conversion_sublist.curselection()
        self.selections_made = []
        for selection_done in select_item_sublist:
            if len(select_item_sublist) >= 1:
                single_sub_selection_index = selection_done
                string_sublist_selected = self.list_box_conversion_sublist.get(single_sub_selection_index)
                self.selections_made.append(string_sublist_selected)
        self.move_to_queue.configure(cursor='hand2', state='active', command= lambda:self.add_to_queue_callback(add_this_parent=self.selected_parent, add_this_objects=self.selections_made))
        self.select_all_sublist_button.configure(cursor='arrow', state='disabled')
        self.clear_sublist_button.configure(cursor='hand2', state='active', command=lambda:self.clear_sublist())

    def add_to_queue_callback(self, add_this_parent=str, add_this_objects=list):
        self.conversion_queue_listbox.configure(state='normal')
        self.move_to_queue.configure(cursor='arrow', state='disabled')
        for add_this_obj in add_this_objects:
            string_for_queue_listbox = f'{add_this_parent}==>{add_this_obj}'
            self.populate_listbox(table_to_populate=self.conversion_queue_listbox, list_objects=[string_for_queue_listbox])
            all_object_in_current = self.list_box_conversion_sublist.get(0, END)
            if f'Characters' in add_this_parent:
                self.merge_animations_check.configure(state='active')
            for delete_this_obj in all_object_in_current:
                if add_this_obj == delete_this_obj:
                    index_for_delete = all_object_in_current.index(add_this_obj)
                    self.list_box_conversion_sublist.delete(index_for_delete)
        self.list_box_conversion_parent_table.configure(state='normal')
        self.button_convert_models.configure(cursor="hand2", state='active')
        if len(self.list_box_conversion_sublist.get(0, END)) <= 0:
            self.list_box_conversion_sublist.configure(state='disabled')
            #self.conversion_queue_listbox.configure(state='disabled')
            self.move_to_queue.configure(state='disabled')
            self.select_all_sublist_button.configure(state='disabled')
            self.list_box_conversion_parent_table.configure(state='normal')
            self.move_to_sub_listbox_button.configure(state='active')
            self.clear_sublist_button.configure(cursor='arrow', state='disabled')

    def clear_sublist(self):
        self.list_box_conversion_sublist.delete(0, END)
        self.select_all_sublist_button.configure(cursor='arrow', state='disabled')
        self.move_to_queue.configure(cursor='arrow', state='disabled')
        self.list_box_conversion_sublist.configure(state='disabled')
        self.list_box_conversion_parent_table.configure(state='normal')
        self.move_to_sub_listbox_button.configure(state='active')
        self.clear_sublist_button.configure(cursor='arrow', state='disabled')

    # Final Conversion Steps

    def convert_models_process(self):
        final_list = self.conversion_queue_listbox.get(0, END)
        final_list_to_set = []
        for list_sorted in final_list:
            final_list_to_set.append(list_sorted)
        final_list_to_set.sort()
        final_list_set = set(final_list_to_set)

        final_list_set_sorted = []
        for f_list_set in final_list_set:
            final_list_set_sorted.append(f_list_set)
        final_list_set_sorted.sort()
        self.start_conversion(total_list_files=final_list_set_sorted)

    def count_models_queue(self):
        # Total Models Queue Label
        self.total_models_in_queue_start = len(self.conversion_queue_listbox.get(0, END))
        self.total_models_label = Label(self.new_window_box, text=f'Total Number of Models in Queue: {self.total_models_in_queue_start}')
        # Placing Total Models in Queue
        self.total_models_label.place(relx=0.65, rely=0.41, relwidth= 0.2, relheight= 0.05)
        self.new_window_box.after(50, self.count_models_queue)
        self.total_models_label.update()
        self.total_models_in_queue = len(self.conversion_queue_listbox.get(0, END))
        self.total_models_label.configure(text=f'Total Number of Models in Queue: {self.total_models_in_queue}')
        
    def start_conversion(self, total_list_files=list):
        try:
            self.conversion_new_window = Toplevel(master=self.new_window_box)
            self.conversion_new_window.grab_set()
            self.conversion_new_window.focus_set()
            x_main = self.x_y_values[0]
            y_main = self.x_y_values[1]
            self.conversion_new_window.title(string=f'Conversion in Progress...')
            self.conversion_new_window.geometry(f'+%d+%d' %(x_main, y_main))
            self.conversion_new_window.geometry(f'{x_main + (500 - x_main)}x{(y_main + (300 - y_main)) // 2}')
            self.conversion_new_window.wm_protocol(name="WM_DELETE_WINDOW", func=self.no_close)
            self.conversion_new_window.overrideredirect(True)
            self.conversion_new_window.configure(bd=4, relief='ridge')

            # Start Conversion Button
            self.start_button = Button(master=self.conversion_new_window, cursor='hand2', text='START', command=lambda: self.final_conversion(files_convert=total_list_files))
            self.start_button.place(relx=0.1, rely=0.7, relwidth= 0.3, relheight= 0.3)

            # Cancel Button
            self.cancel_conversion_button = Button(master=self.conversion_new_window, cursor='hand2', text='CANCEL', command=lambda: self.stop_conversion())
            self.cancel_conversion_button.place(relx=0.65, rely=0.7, relwidth= 0.3, relheight= 0.3)
        
        except RuntimeError:
            messagebox.showerror(title='FATAL CRASH', message='Something Fail during Conversion...')
            exit()
    
    def stop_conversion(self):
        cancel_conversion = messagebox.askyesno(title='IMPORTANT', message='Are you sure that want to stop the conversion?')
        if cancel_conversion:
            self.conversion_new_window.destroy()
            self.new_window_box.grab_set()
            self.new_window_box.focus_set()
            self.conversion_queue_listbox.delete(0, END)
            check_done_cancel = self.check_all_convert_variable.get()
            if check_done_cancel == 1:
                self.check_all_convert_variable.set(0)
            self.list_box_conversion_parent_table.configure(state='normal')
    
    def final_conversion(self, files_convert=list):
        self.start_button.configure(cursor='arrow',state='disabled')
        self.cancel_conversion_button.configure(cursor='arrow', state='disabled')
        self.new_working_label = Label(master=self.conversion_new_window, text=f'Converting Models, please wait...', relief='groove')
        self.new_working_label.place(relx=0.01, rely=0.6, relwidth= 0.98, relheight= 0.4)

        self.get_var_merge = self.merge_animations_variable.get()
        convert_queue_files.ConvertGuiFiles(files_to_convert=files_convert, all_files_list=self.create_list_files, merge_flag=self.get_var_merge, masterbar=self.conversion_new_window)
        new_message = messagebox.showinfo(title='Conversion Finished', message=f'Total Files Converted: {len(files_convert)}')
        if new_message == f'ok':
            self.conversion_new_window.destroy()
            self.new_window_box.grab_set()
            self.new_window_box.focus_set()

    def no_close(self): # THIS FUNCTION is to bypass the [X] Windows icon for closing the window
        pass

    # Configuration Window

    def configure_tool(self):
        self.size_x = size_x
        self.size_y = size_y
        self.sc_folder_def = sc_folder_def
        self.dump_folder = dump_folder
        self.configure_window = Toplevel(master=self)
        self.configure_window.grab_set()
        self.configure_window.focus_set()
        x_main = self.x_y_values[0] // 2
        y_main = self.x_y_values[1] // 2
        self.configure_window.title(string=f'Tool Configuration')
        self.configure_window.geometry(f'+%d+%d' %(x_main, y_main))
        self.configure_window.geometry(f'{x_main + (x_main - 100)}x{y_main + (y_main - 75)}')

        # RESOLUTION FRAME
        self.resolution_frame = LabelFrame(master=self.configure_window, text=f'Tool Window size')
        self.resolution_list = [f'{self.size_x}x{self.size_y}',f'7680x4320', f'3840x2160', f'2560x1440', f'1920x1080', f'1280x720', f'854x480', f'640x360', f'426x240']
        self.combobox_resolution = ttk.Combobox(master=self.resolution_frame, values=self.resolution_list)
        self.combobox_resolution.current(0)
        self.combobox_resolution.bind('<<ComboboxSelected>>', lambda e: self.combo_box_selected_callback())
        self.ckb_variable_resolution = IntVar()
        self.check_box_custom_res = Checkbutton(master=self.resolution_frame, text=f'Use custom size', variable=self.ckb_variable_resolution)
        self.label_w_entry = Label(master=self.resolution_frame, text='WIDTH')
        self.label_h_entry = Label(master=self.resolution_frame, text='HEIGHT')
        self.width_res_change = Entry(master=self.resolution_frame, justify='center', validate='key', )
        self.height_res_change = Entry(master=self.resolution_frame, justify='center')
        self.set_resolution_button = Button(master=self.resolution_frame, text='SET')
        self.width_res_change.insert(0, size_x)
        self.height_res_change.insert(0, size_y)
        self.width_res_change.configure(state='disabled')
        self.height_res_change.configure(state='disabled')
        self.set_resolution_button.configure(state='disabled')
        self.check_box_custom_res.configure(command=lambda: self.checkbox_change_resolution())
        self.set_resolution_button.configure(command=lambda: self.get_xy_values_entries())
        self.validate_cmd = self.register(self.validate_digit)
        self.width_res_change.configure(validatecommand=(self.validate_cmd, '%P'))
        self.height_res_change.configure(validatecommand=(self.validate_cmd, '%P'))

        # SC FRAME
        self.sc_frame = LabelFrame(master=self.configure_window, text='SC Default Folder')
        self.sc_folder_path_text = Text(master=self.sc_frame, background='#edece3', font='Arial 12')
        self.sc_folder_path_text.insert(END, f'{sc_folder_def}')
        self.sc_folder_path_text.tag_configure("new_configure", justify='center')
        self.sc_folder_path_text.tag_add("new_configure", "1.0", END)
        self.sc_change_folder_path = Button(master=self.sc_frame, cursor='hand2', text=f'Change SC Folder', command=lambda: self.change_sc_folder())

        # DUMP FRAME
        self.dump_frame = LabelFrame(master=self.configure_window, text='Dump Folder')
        self.dump_folder_path_text = Text(master=self.dump_frame, background='#edece3', font='Arial 12')
        self.dump_folder_path_text.insert(END, f'{dump_folder}')
        self.dump_folder_path_text.tag_configure("new_configure", justify='center')
        self.dump_folder_path_text.tag_add("new_configure", "1.0", END)
        self.dump_change_folder_path = Button(master=self.dump_frame, cursor='hand2', text=f'Change DUMP Folder', command=lambda: self.change_dump_folder())

        # SAVE BUTTON
        self.save_configuration_button = Button(master=self.configure_window, cursor='hand2', text=f'SAVE CONFIG', command=lambda: self.save_config(res_x=self.size_x, res_y=self.size_y, sc_path=self.sc_folder_def, dump_path=self.dump_folder))
        # CANCEL BUTTON
        self.cancel_configuration_button = Button(master=self.configure_window, cursor='hand2', text=f'CANCEL', command=lambda: self.cancel_config())

        # PLACING STUFF
        # Resolution Frame
        self.resolution_frame.place(relx=0.05, rely=0.02, relwidth= 0.9, relheight= 0.25)
        self.combobox_resolution.place(relx=0.01, rely=0.4, relwidth= 0.3, relheight= 0.50)
        self.check_box_custom_res.place(relx=0.31, rely=0.4, relwidth= 0.2, relheight= 0.50)
        self.width_res_change.place(relx=0.51, rely=0.4, relwidth= 0.15, relheight= 0.50)
        self.height_res_change.place(relx=0.70, rely=0.4, relwidth= 0.15, relheight= 0.50)
        self.label_w_entry.place(relx=0.51, rely=0.05, relwidth= 0.15, relheight= 0.30)
        self.label_h_entry.place(relx=0.70, rely=0.05, relwidth= 0.15, relheight= 0.20)
        self.set_resolution_button.place(relx=0.87, rely=0.4, relwidth= 0.10, relheight= 0.50)
        # SC Frame
        self.sc_frame.place(relx=0.05, rely=0.27, relwidth= 0.9, relheight= 0.25)
        self.sc_folder_path_text.place(relx=0.05, rely=0.10, relwidth= 0.9, relheight= 0.35)
        self.sc_change_folder_path.place(relx=0.30, rely=0.50, relwidth= 0.4, relheight= 0.45)
        # Dump Frame
        self.dump_frame.place(relx=0.05, rely=0.52, relwidth= 0.9, relheight= 0.25)
        self.dump_folder_path_text.place(relx=0.05, rely=0.10, relwidth= 0.9, relheight= 0.35)
        self.dump_change_folder_path.place(relx=0.30, rely=0.50, relwidth= 0.4, relheight= 0.45)
        # Save Config
        self.save_configuration_button.place(relx=0.2, rely=0.78, relwidth= 0.3, relheight= 0.18)
        # Cancel Config
        self.cancel_configuration_button.place(relx=0.5, rely=0.78, relwidth= 0.3, relheight= 0.18)
    
    def checkbox_change_resolution(self):
        check_state_resolution = self.ckb_variable_resolution.get()
        if check_state_resolution == 1:
            self.combobox_resolution.configure(state='disabled')
            self.width_res_change.configure(state='normal')
            self.height_res_change.configure(state='normal')
            self.set_resolution_button.configure(state='active')
        else:
            self.combobox_resolution.configure(state='normal')
            self.width_res_change.configure(state='disabled')
            self.height_res_change.configure(state='disabled')
            self.set_resolution_button.configure(state='disabled')

    def combo_box_selected_callback(self):
        selected_res = self.combobox_resolution.get()
        find_x = selected_res.find("x")
        self.size_x = selected_res[0:find_x]
        self.size_y = selected_res[find_x + 1:]

    def get_xy_values_entries(self):
        value_x = self.width_res_change.get()
        value_y = self.height_res_change.get()

        value_x_int = int(value_x)
        value_y_int = int(value_y)

        if value_x_int < 100 or value_y_int < 100:
            messagebox.showwarning(title=f'INCORRECT VALUE', message=f'{value_x}, {value_y} is not a possible resolution\nPlease select values above 100')
        else:
            self.size_x = value_x_int
            self.size_y = value_y_int
            messagebox.showinfo(title='Values set', message=f'{self.size_x} and {self.size_y} are set as new resolution values')

    def validate_digit(self, text_entered):
        if (str.isdigit(text_entered)) or (text_entered == f''):
            return True
        else:
            return False

    def change_sc_folder(self):
        new_folder_sc = askdirectory(title='Select new SC Folder')
        if new_folder_sc == f'':
            messagebox.showinfo(title=f'Incorrect SC FOLDER', message='Please Try Again...')
            self.change_sc_folder()
        
        self.sc_folder_path_text.delete("1.0", END)
        self.sc_folder_path_text.insert(END, new_folder_sc)
        self.sc_folder_path_text.tag_configure("new_configure", justify='center')
        self.sc_folder_path_text.tag_add("new_configure", "1.0", END)
        self.sc_folder_def = new_folder_sc

    def change_dump_folder(self):
        new_folder_dump = askdirectory(title='Select new SC Folder')
        if new_folder_dump == f'':
            messagebox.showinfo(title=f'Incorrect DUMP FOLDER', message='Please Try Again...')
            self.change_dump_folder()
        
        self.dump_folder_path_text.delete("1.0", END)
        self.dump_folder_path_text.insert(END, new_folder_dump)
        self.dump_folder_path_text.tag_configure("new_configure", justify='center')
        self.dump_folder_path_text.tag_add("new_configure", "1.0", END)
        self.dump_folder = new_folder_dump

    def save_config(self, res_x=int, res_y=int, sc_path=str, dump_path=str):
        path_file = f'Resources/converter_config.config'
        Options.write_options(Options, path_cnf_file=path_file, first_run=False, size_x=res_x, size_y=res_y, sc_folder_def=sc_path, dump_folder=dump_path)
        messagebox.showinfo(master=self.configure_window, title='CONFIG SAVED', message='Your configuration has been saved...')
        self.configure_window.destroy()

    def cancel_config(self):
        messagebox.showinfo(master=self.configure_window, title='IMPORTANT', message='Your configuration won\'t be saved')
        self.configure_window.destroy()


if __name__ == "__main__":
    main_window = Tk()
    config_window = Options.read_write_options(Options)
    main_window.iconbitmap(default='Resources/DD_Eye.ico')
    main_window.wm_title("TLoD TMD Converter BETA v0.3")
    width_native_windows = main_window.winfo_screenwidth()
    height_native_windows = main_window.winfo_screenheight()
    middle_place_width = (width_native_windows // 2) - (width_native_windows // 3)
    middle_place_height = (height_native_windows // 2) - (height_native_windows // 3)
    main_window.geometry(f'+{middle_place_width}+{middle_place_height}')

    tlod_tmd_converter_gui = TCWindow(main_window, width=config_window[0], height=config_window[1])
    tlod_tmd_converter_gui.mainloop()