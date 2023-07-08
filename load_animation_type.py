"""

Load Animation Type: for analise it, when we know which type is will
continue the processing

Copyright (C) 2023 DooMMetaL

"""
import os
from tkinter import messagebox

# Animation headers
CMB_HEADER = b'\x43\x4D\x42\x20'
LMB_HEADER = b'\x4C\x4D\x42\x00'
SAF_HEADER = b'\x0C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

class LoadAnimation:
    """Loading Animation File Algorithm"""
    def __init__(self, animation_file_path):
        self.self = LoadAnimation
        self.animation_file = animation_file_path
        self.load_animation(animation_file=animation_file_path)
        self.create_folder(animation_file=animation_file_path)
    
    def load_animation(self, animation_file=str):
        check_this_anim = animation_file
        with open(check_this_anim, 'rb') as animation_f:
            read_anim = animation_f.read()
            anim_data_extracted = self.check_animation_types(animation_file=read_anim)
            global animation_data
            global animation_type
            animation_data = anim_data_extracted[0]
            animation_type = anim_data_extracted[1]
    
    def create_folder(self, animation_file):
        global new_folder
        global file_name
        path_folder = os.path.dirname(animation_file)
        file_path_complete = (animation_file).strip()
        file_name_complete = os.path.basename(file_path_complete)
        file_name = os.path.splitext(file_name_complete)[0]
        check_dot_model_path = animation_file.find('.')
        if check_dot_model_path == -1:
            file_name = file_name + f'_converted'
        new_folder = os.path.join(path_folder, file_name)

        try:
            os.makedirs(new_folder, exist_ok=True)
        except OSError:
            error_folder = f'Can\'t create the folder, permission denied'
            error_folder_window = messagebox.showerror(title='System Error...', message=error_folder)
            exit()

    @staticmethod
    def check_animation_types(animation_file=bytes):

        # FIND ANIMATIONS EMBEDDED
        file_find_cmb = animation_file.find(CMB_HEADER)
        file_find_lmb = animation_file.find(LMB_HEADER)
        # FOR SAF I MUST DO A DOUBLE CHECK, SINCE C_CONTAINERS are set also in the tmd/ctmd headers
        file_find_saf = animation_file.rfind(SAF_HEADER) # THIS WILL TRY TO FIND AT THE END OF THE FILE, BUT I HAVE TO MATCH WITH THE NUMBER OF OBJECTS

        anim_data = b''
        anim_info = []
        if file_find_cmb != -1:
            start_cmb = animation_file[file_find_cmb:]
            header_cmb = start_cmb[0:16]
            total_length = header_cmb[8:12]
            number_obj_cmb = header_cmb[12:14]
            number_sub_transforms = header_cmb[14:16]
            total_length_int = int.from_bytes(total_length, 'little', signed=False)
            number_obj_cmb_int = int.from_bytes(number_obj_cmb, 'little', signed=False)
            number_sub_transforms_int = int.from_bytes(number_sub_transforms, 'little', signed=False)
            final_data_cmb = start_cmb[16:]

            if len(start_cmb) != total_length_int:
                cmb_error = f'FATAL ERROR - CMB FILE SIZE DON\'T MATCH!, processing can\'t continue, closing tool...'
                show_error_cmb = messagebox.showerror(title=f'FATAL CRASH!!!', message=cmb_error)
                exit()
            
            anim_data = final_data_cmb
            anim_type_str = f'CMB'
            anim_info.append(number_obj_cmb_int)
            anim_info.append(number_sub_transforms_int)
            anim_info.append(anim_type_str)

        elif file_find_lmb != -1:
            if file_find_lmb == 0: 
                start_lmb = animation_file[file_find_lmb:]
                header_lmb = start_lmb[0:16]
                number_obj_lmb = header_lmb[4:8]
                number_obj_lmb_int = int.from_bytes(number_obj_lmb, 'little', signed=False)
                subtransforms_table_lmb = (number_obj_lmb_int * 12) // 4
                final_data_lmb = start_lmb[8:]

                anim_data = final_data_lmb
                anim_type_str = f'LMB_Type_0'
                anim_info.append(number_obj_lmb_int)
                anim_info.append(subtransforms_table_lmb)
                anim_info.append(anim_type_str)
            else:
                find_type = int.from_bytes(animation_file[4:8], 'little', signed=False)
                start_lmb = animation_file[file_find_lmb:]
                header_lmb = start_lmb[0:20]
                number_obj_lmb = int.from_bytes(header_lmb[4:8], 'little', signed=False)
                subtransforms_table_lmb = (number_obj_lmb * 12) // 4
                final_data_lmb = start_lmb[8:]
                anim_data = final_data_lmb
                if find_type == 0:
                    anim_type_str = f'LMB_Type_0'
                    anim_info.append(number_obj_lmb)
                    anim_info.append(subtransforms_table_lmb)
                    anim_info.append(anim_type_str)
                elif find_type == 1:
                    anim_type_str = f'LMB_Type_1'
                    anim_info.append(number_obj_lmb)
                    anim_info.append(subtransforms_table_lmb)
                    anim_info.append(anim_type_str)
                elif find_type == 2:
                    anim_type_str = f'LMB_Type_2'
                    anim_info.append(number_obj_lmb)
                    anim_info.append(subtransforms_table_lmb)
                    anim_info.append(anim_type_str)
            
        elif file_find_saf != -1:
            start_saf_data = file_find_saf + 12
            start_saf = animation_file[start_saf_data:]
            header_saf = start_saf[0:4]
            number_obj_saf = header_saf[0:2]
            number_transforms_saf = header_saf[2:4]
            number_obj_saf_int = int.from_bytes(number_obj_saf, 'little', signed=False)
            number_transforms_saf_int = int.from_bytes(number_transforms_saf, 'little', signed=False) // 2 # Divided by 2 because count ROT/LOC
            final_data_saf = start_saf[4:]

            anim_data = final_data_saf
            anim_type_str = f'SAF'
            anim_info.append(number_obj_saf_int)
            anim_info.append(number_transforms_saf_int)
            anim_info.append(anim_type_str)
        
        elif (file_find_cmb == -1) and (file_find_lmb == -1) and (file_find_saf == -1):
            check_failure = f'This file is not an recognised animation file'
            check_failure_message = messagebox.showerror(title=f'FATAL CRASH!!!', message=check_failure)
            exit()
        return anim_data, anim_info