"""

SubMap Database Reader:
I wrote this algorithm, since the way that is handle it's different
than in DRGN0, i will try to keep it as simple as possible

Copyright (C) 2024 DooMMetaL

"""
import os
from tkinter import messagebox

class SubmapDatabase:
    def __init__(self, database_path):
        self.self = SubmapDatabase
        self.database_path = database_path
        self.process_drgn2x_database(database_path=database_path)
    
    def process_drgn2x_database(self, database_path):
        database_dict_base = {} # Here will contain DRGN2x
        database_path_drgn21 = database_path + f'\\DRGN21\\'
        database_path_drgn22 = database_path + f'\\DRGN22\\'
        database_path_drgn23 = database_path + f'\\DRGN23\\'
        database_path_drgn24 = database_path + f'\\DRGN24\\'
        
        database_files_drgn21 = self.get_database_files(database_files_path=database_path_drgn21)
        database_drgn21 = self.database_generator(files_path=database_files_drgn21)

        database_files_drgn22 = self.get_database_files(database_files_path=database_path_drgn22)
        database_drgn22 = self.database_generator(files_path=database_files_drgn22)

        database_files_drgn23 = self.get_database_files(database_files_path=database_path_drgn23)
        database_drgn23 = self.database_generator(files_path=database_files_drgn23)

        database_files_drgn24 = self.get_database_files(database_files_path=database_path_drgn24)
        database_drgn24 = self.database_generator(files_path=database_files_drgn24)

        database_dict_base = {'DRGN21': database_drgn21, 'DRGN22': database_drgn22, 'DRGN23': database_drgn23, 'DRGN24': database_drgn24}
        
        return database_dict_base
    
    def database_generator(self, files_path=list) -> dict:
        new_database = {}
        for file in files_path:
            file_name_end = file.rfind(f'\\')
            file_name = file[file_name_end + 1:].replace(f'.txt', '')
            with open(file, 'r') as read_database:
                text_database = read_database.readlines()
                separator_indices = self.get_separator(text_string=text_database)
                split_this_blocks = self.calculate_segments(text_segments=separator_indices)
                split_in_segments = self.split_segments(split_this_text=text_database, segments_to_split=split_this_blocks)
                generate_subdatabase_dict = self.generate_subdatabase(segments_to_convert=split_in_segments) # TODO an eye on this, need the database name
                new_database.update({f'{file_name}': generate_subdatabase_dict})
        return new_database

    def generate_subdatabase(self, segments_to_convert=list) -> dict:
        this_submap_dict = {}
        for joined_text in segments_to_convert:
            split_lines = joined_text.splitlines()
            environment_line = split_lines[0]
            environment_model = split_lines[1]
            objects_line = split_lines[2]
            objects_models = split_lines[3:]
            
            get_submap_cut_name = self.get_submap_name(name_string=environment_line)
            get_env_folder = self.get_folder(folder_string=environment_line)
            get_obj_folder = self.get_folder(folder_string=objects_line)
            get_env_model_anim = self.get_model_anim(model_string=environment_model)

            if ("[/Base -" in environment_line) and ("[/Base -" in environment_line): # ===> Special handling for Files which are in the root of DRGN2x Files
                this_submap_dict.update({f'{get_submap_cut_name}': {'Environment': ['', get_env_model_anim], 'Objects': ['None', 'None']}})
            
            else:
                get_objs_model_anim = {}
                for model_anim_names in objects_models:
                    name_3d_object, model_anims = self.get_model_anim(model_string=model_anim_names)
                    get_objs_model_anim.update({f'{name_3d_object}': model_anims})
                
                this_submap_dict.update({f'{get_submap_cut_name}': {'Environment': [get_env_folder, get_env_model_anim], 'Objects': [get_obj_folder, get_objs_model_anim]}})

        return this_submap_dict

    def split_segments(self, split_this_text=list, segments_to_split=list) -> list:
        split_text = []
        for segment in range(0, len(segments_to_split)):
            current_segment = segments_to_split[segment]
            start_of_segment = current_segment[0]
            end_of_segment = current_segment[1]
            text_splitting = split_this_text[start_of_segment:end_of_segment]
            new_text = ''.join(text_splitting)
            split_text.append(new_text)
        
        return split_text
    
    def calculate_segments(self, text_segments=str) -> list:
        segments_list = []
        slice_segment = 0
        for segment_text in range(0, (len(text_segments) // 2)):
            start_segment = segment_text + slice_segment
            end_segment = segment_text + slice_segment + 2
            block_segment = text_segments[start_segment:end_segment]
            segments_list.append(block_segment)
            slice_segment += 1
        
        return segments_list
    
    def get_separator(self, text_string=str) -> list:
        separators_indices = []
        index_num = 0
        for separator in text_string:
            if f'==========' in separator:
                separators_indices.append(index_num)
                if len(text_string) != (index_num + 1):
                    separators_indices.append(index_num + 1)
            if index_num == 0:
                separators_indices.append(index_num)
            index_num += 1
        
        return separators_indices

    def get_folder(self, folder_string=str) -> str: # Generic Get Folder function
        string_search = folder_string.find('-> FOLDER:')
        folder_number = folder_string[string_search + 10:].strip()
        
        return folder_number

    def get_model_anim(self, model_string=str) -> tuple:
        start_position_model = model_string.find(f': ')
        name_3d_object = model_string[:start_position_model]
        model_anims = model_string[start_position_model + 2:]
        
        return name_3d_object, model_anims

    def get_submap_name(self, name_string=str) -> str:
        name_submap = f''
        find_end_string = name_string.find(f' - Environment')
        find_start_string = name_string.find(f' - ')
        name_submap = name_string[find_start_string + 2: find_end_string].strip()
        
        return name_submap

    def get_database_files(self, database_files_path=str):
        database_files = []
        if os.path.isdir(database_files_path):
            total_files = os.walk(database_files_path)
            for root, dirs, files in total_files:
                for single_file in files:
                    new_path = os.path.join(root, single_file)
                    database_files.append(new_path)
        else:
            error_string = f'{database_files_path} is not a correct path, exiting...'
            messagebox.showerror(title='FATAL ERROR!', message=error_string)
            exit()
        
        return database_files