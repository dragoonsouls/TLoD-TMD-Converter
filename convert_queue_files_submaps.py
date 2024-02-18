"""

Module used for the conversion of the Queued files
from the previous steps

Copyright (C) 2024 DooMMetaL

"""
from tkinter import messagebox, Label
from tkinter import ttk
import os
import convert_batch
import convert_queue_files

# Folder creation
"""for this i will need <<self.this_super_parent>> which will be the root folder to create, then the current SubMap Name, that would be next nesting in folder,
then will came the Cut Name that would be the next nesting and finally if Environment or Objects or both will be the last nesting step, example:
FOLDERS: DRGN21 => Bale => Cut_1 => Environment
                                 => Objects"""
# File conversion
"""for this i will need <<self.final_list_files_to_convert>>, first i will need to get the data from each list data, also animation array must be read and change
from string into a list so i can get each model an animation, also i need the files/ folder location and check if need to add more stuff to the string"""

class ConvertSubMapFiles:
    def __init__(self, disk_parent, list_to_convert, masterbar):
        """Convert SubMap Queued Files: This code will convert the files from the SubMap Queue"""
        self.self = ConvertSubMapFiles
        self.disk_parent = disk_parent
        self.list_to_convert = list_to_convert
        self.master = masterbar
        self.convert_submap_files()
    
    def convert_submap_files(self):
        sc_dump_path = convert_queue_files.ConvertGuiFiles.get_dump_path(self=self)
        sc_files_path = convert_queue_files.ConvertGuiFiles.get_sc_folder(self=self)
        """Structure for knowing the way to handle files and folders:
        [If ENV/OBJ, SubMap Name, SubMap Cut, ENV DATA PATH, OBJ DATA PATH]"""
        self.folders_to_create = []
        files_list_processed = []
        self.real_total_files = 0 # For each coincidence for ENV or OBJ models i will sum +1 for convert models, this way i save one or three functions

        for current_item_to_convert in self.list_to_convert:
            env_obj_flag = current_item_to_convert[0]
            submap_name = current_item_to_convert[1]
            submap_cut = current_item_to_convert[2]
            generic_final_dump_folder = f'{sc_dump_path}SubMap/{self.disk_parent}/{submap_name.replace(" ", "_")}/{submap_cut.replace(" ", "_")}'

            """ENV DATA PATH: [Folder, (Name, File)]
            OBJ DATA PATH: Folder, {Dictionary of Objects; 'NameObj': NameFile - [Animations] this last is a string}"""
            if env_obj_flag == 'ENV and OBJ':
                environment_string = current_item_to_convert[3]
                objects_string = current_item_to_convert[4]
                environment_file = self.get_3d_model_ready_path(model_string=environment_string, sc_pathf=sc_files_path, final_dump_folder=generic_final_dump_folder, type_file='ENV')
                objects_file = self.get_3d_model_ready_path(model_string=objects_string, sc_pathf=sc_files_path, final_dump_folder=generic_final_dump_folder, type_file='OBJ')
                files_list_processed.append(environment_file)
                files_list_processed.append(objects_file)
            
            elif env_obj_flag == 'OBJ Only':
                obj_only_to_convert = current_item_to_convert[3]
                object_file_only = self.get_3d_model_ready_path(model_string=obj_only_to_convert, sc_pathf=sc_files_path, final_dump_folder=generic_final_dump_folder, type_file='OBJ')
                files_list_processed.append(object_file_only)
            
            elif env_obj_flag == 'ENV Only':
                env_only_to_convert = current_item_to_convert[3]
                environment_file_only = self.get_3d_model_ready_path(model_string=env_only_to_convert, sc_pathf=sc_files_path, final_dump_folder=generic_final_dump_folder, type_file='ENV')
                files_list_processed.append(environment_file_only)

        set_folders = list(set(self.folders_to_create)) # Need to avoid duplicates!!!
        self.create_folders(folders=set_folders)

        length_bar = 100 / self.real_total_files
        self.new_bar = ttk.Progressbar(master=self.master, length=100, maximum=100, mode='determinate', orient='horizontal')
        self.new_bar.place(relx=0.01, rely=0.2, relwidth= 0.98, relheight= 0.2)
        percent = float(length_bar)
        percent_string = "%.2f" % percent
        self.percentage_label = Label(master=self.master, text=f'{percent_string}%')
        self.percentage_label.place(relx=0.45, rely=0.5, relwidth= 0.1, relheight= 0.1)

        this_file_processed = 0
        for folder_convert in files_list_processed:
            folder_denest = folder_convert[0]
            folder_flag = folder_denest[0]

            if folder_flag == 'ENV':
                folder_to_convert_denest = folder_denest[1]
                env_folder_to_convert = folder_to_convert_denest[0]
                env_model_file = env_folder_to_convert[0]
                env_animation_file = env_folder_to_convert[1]
                env_animation_type = env_folder_to_convert[2]
                env_new_folder = env_folder_to_convert[3]
                convert_batch.main(model_file=env_model_file, animation_file=env_animation_file, animation_type=env_animation_type, new_folder=env_new_folder)
                this_file_processed += 1
                self.update_percent_label(number_add=percent)
                self.update_bar_progression(model_processed=percent)
                percent += length_bar
            
            elif folder_flag == 'OBJ':
                folder_denest_stage_1 = folder_denest[1]
                for folder_denest_stage_2 in folder_denest_stage_1:
                    for obj_folder_to_convert in folder_denest_stage_2:
                        obj_model_file = obj_folder_to_convert[0]
                        obj_animation_file = obj_folder_to_convert[1]
                        obj_animation_type = obj_folder_to_convert[2]
                        obj_new_folder = obj_folder_to_convert[3]
                        convert_batch.main(model_file=obj_model_file, animation_file=obj_animation_file, animation_type=obj_animation_type, new_folder=obj_new_folder)
                        this_file_processed += 1
                        self.update_percent_label(number_add=percent)
                        self.update_bar_progression(model_processed=percent)
                        percent += length_bar

            else:
                messagebox.showerror(title='FATAL CRASH', message='Processing of Files Failed!!...')
        print("CONVERSION FINISHED")
    
    def create_folders(self, folders=list):
        for folder in folders:
            try:
                os.makedirs(folder, exist_ok=True)
            except OSError:
                error_folder = f'Can\'t create the folder, permission denied'
                messagebox.showerror(title='System Error...', message=error_folder)
                exit()
    
    def get_3d_model_ready_path(self, model_string=str, sc_pathf=str, final_dump_folder=str, type_file=str) -> list:
        """Batch Converter expects this way of Data:
        Model_File, Animation_File, Animation_Type, New_folder"""
        ready_to_convert = []

        if type_file == 'ENV':
            model_folder = model_string[0] # This is in which folder the Model is
            model_name_file = model_string[1] # This is a tuple containing "fantasy name" and Model name
            model_name = model_name_file[0] # "Fantasy Name" or AKA
            model_file = model_name_file[1] # Model File Name

            complete_path_to_file = f'{sc_pathf}SECT/{self.disk_parent}.BIN/{model_folder}/{model_file}'
            animation_path_to_file = 'None'
            animation_type = f'No Animation'
            new_folder = f'{final_dump_folder}/Environment/{model_name.replace(" ", "_")}-Map_Model'
            create_this_folder = f'{final_dump_folder}/Environment/'
            self.folders_to_create.append(create_this_folder)

            string_ready = 'ENV', [(complete_path_to_file, animation_path_to_file, animation_type, new_folder)]
            ready_to_convert.append(string_ready)
            self.real_total_files += 1
        
        elif type_file == 'OBJ':
            modelanmim_folder = model_string[0] # Where are the Models and Animations located
            objects_files = model_string[1]
            current_list_files_to_convert = []
            for current_object in objects_files:
                current_object_name = current_object # I get it in a new variable to keep the track on it
                current_object_model = objects_files.get(f'{current_object_name}')
                if 'None' not in current_object_model:
                    current_files_in_object = self.convert_str_from_dict(value_fm_dict=current_object_model, model_folder=modelanmim_folder, sc_pathf=sc_pathf, disk_parent=self.disk_parent, model_name=current_object_name, dump_folder=final_dump_folder)
                    current_list_files_to_convert.append(current_files_in_object)
                else:
                    print("Ignoring Retail Bugged files") # Retail Bugged files would be ignored in this version
            current_files_objects = 'OBJ', current_list_files_to_convert
            ready_to_convert.append(current_files_objects)
                    
        return ready_to_convert
    
    def convert_str_from_dict(self, value_fm_dict=str, model_folder=str, sc_pathf=str, disk_parent=str, model_name=str, dump_folder=str) -> list:
        new_list = []
        search_dash = value_fm_dict.find(f'-')
        file_name_end = value_fm_dict[0:search_dash].strip()
        isolated_anim_files = value_fm_dict[search_dash + 1:].strip()

        # Now that i get the Model file and the Animations isolated i need to split the animations into a list
        search_bracket_left = isolated_anim_files.find(f'[')
        search_bracket_right = isolated_anim_files.find(f']')
        anim_files_string_joined = isolated_anim_files[search_bracket_left + 1:search_bracket_right]
        split_anim_files = anim_files_string_joined.split(f', ')
        
        for current_anim in split_anim_files:
            adjust_end_name = model_name.replace(" ", "_").replace('"',"").replace("?","").replace("/","-")
            string_model = f'{sc_pathf}SECT/{disk_parent}.BIN/{model_folder}/{file_name_end}'
            string_anim = f'{sc_pathf}SECT/{disk_parent}.BIN/{model_folder}/{current_anim}'
            animation_type = f'SAF'
            new_folder = f'{dump_folder}/Objects/{adjust_end_name}/{adjust_end_name}-Anim_{current_anim}'
            create_this_folder = f'{dump_folder}/Objects/{adjust_end_name}/'
            self.folders_to_create.append(create_this_folder)
            ready_to_convert = string_model, string_anim, animation_type, new_folder
            new_list.append(ready_to_convert)
            self.real_total_files += 1
        return new_list
    
    def update_percent_label(self, number_add=float):
        self.percentage_label.update_idletasks()
        percent_string = "%.2f" % number_add
        print(percent_string)
        self.percentage_label.config(text=f'{percent_string}%')

    def update_bar_progression(self, model_processed=float):
        self.new_bar.update_idletasks()
        model_processed_round = round(model_processed)
        self.new_bar['value'] = model_processed_round
        print(self.new_bar['value'])