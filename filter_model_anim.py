"""

FILE TYPE READER: here the tool will filter the file type
if a TMD or a CTMD, if none of those, tool will close

Copyright (C) 2023 DooMMetaL

"""
import os
from tkinter.filedialog import askopenfile, askdirectory
from tkinter import messagebox

# HERE I DECLARE THE 'MAGIC' OR HEADERS, THAT ARE "CONSTANTS"
# THIS IS PRETTY MUCH THE FOUND WE MADE UNTIL HERE

# TMD headers
TMD_HEADER_1 = b'A\x00\x00\x00\x00\x00\x00\x00'
TMD_HEADER_2 = b'A\x01\x00\x00\x00\x00\x00\x00'
TMD_HEADER_3 = b'A\x00\x01\x00\x00\x00\x00\x00'
TMD_HEADER_4 = b'A\x00\x00\x01\x00\x00\x00\x00'
TMD_HEADER_5 = b'A\x00\x03\x00\x00\x00\x00\x00'
TMD_HEADER_6 = b'A\x00\x02\x00\x00\x00\x00\x00'
# CTMD headers
CTMD_HEADER_1 = b'A\x00\x00\x00\x02\x00\x00\x00'
CTMD_HEADER_2 = b'A\x01\x00\x00\x02\x00\x00\x00'
CTMD_HEADER_3 = b'A\x00\x01\x00\x02\x00\x00\x00'
CTMD_HEADER_4 = b'A\x00\x00\x01\x02\x00\x00\x00'
CTMD_HEADER_5 = b'A\x00\x02\x00\x02\x00\x00\x00'
# Animation headers
CMB_HEADER = b'\x43\x4D\x42\x20'
LMB_HEADER = b'\x4C\x4D\x42\x00'
SAF_HEADER = b'\x0C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

""" NOTE 1: THE BYTES THAT ARE DIFFERENT IN THE TMD/CTMD MAGICS SEEMS TO BE OVERWRITING THE DATA OF TSB.
    NOTE 2: ACTUALLY SAF FILES DON'T HAVE AN SPECIFIC HEADER, just using the container (C_Container).""" 

class FilterFile:
    """First we need to filter the type of file from the input"""
    def __init__(self, model_file):
        self.self = FilterFile
        self.model_file = model_file
        self.filter_model_file(model_file=model_file)
    
    def filter_model_file(self, model_file):
        check_this_header = model_file

        with open(check_this_header, 'rb') as check_header:
            read_file = check_header.read()
            file_checked = self.search_type(file_search=read_file)
            global file_type
            """File Type == the supported model files TMD/CTMD"""
            file_type = file_checked[0] # special model types will be TMD_DEFF and CTMD
            file_start = file_checked[1] # Index in which the file data starts

            global model_data
            """Model Data == Array of Bytes of model"""
            global model_data_objects
            """Model Data Objects == Number of Objects in model"""
            global animation_data
            global animation_data_info
            """File Filter Text to be printed"""
            global file_filter_text
            file_filter_text = f''
            
            model_data = b''
            model_data_objects = 0
            animation_data = b''
            animation_data_info = []

            # FIRST I FILTER THE FILES BY TYPE
            if (file_type == f'TMD') or (file_type == f'TMD_CCONTAINER') or (file_type == f'TMD_DEFF'):
                start_slice_model = read_file[file_start:]
                header_type = start_slice_model[0:4]
                data_grab = self.getting_header_data(start_slice_model)
                data_grab_model = data_grab[0]
                model_data_objects = data_grab[1]
                model_data = data_grab_model
                file_filter_text = f'\nThis is a Standard TMD {header_type}, Number of Objects: {model_data_objects}'
            elif (file_type == f'CTMD'):
                start_slice_model = read_file[file_start:]
                header_type = start_slice_model[0:4]
                data_grab = self.getting_header_data(start_slice_model)
                data_grab_model = data_grab[0]
                model_data_objects = data_grab[1]
                model_data = data_grab_model
                file_filter_text = f'\nThis is a Standard CTMD {header_type}, Number of Objects: {model_data_objects}'
            else:
                file_filter_text = f'\nfile {check_header} is not a 3D model file'
                exit()
            
            # NOW I FILTER IF THEY HAVE EMBEDDED ANIMATION DATA
            if (file_type == f'TMD_DEFF') or (file_type == f'CTMD'):
                animation_find = self.search_anim_type(anim_search_file=model_data)
                animation_data = animation_find[0]
                animation_data_info = animation_find[1]
                self.animation_obj_compare(compare_tmd=model_data_objects, compare_anim=animation_data_info)
                
            else:
                new_message = messagebox.showinfo(title=f'Warning!', message=f'No embedded Animation file found, load animations or cancel to continue the processing')
                if new_message == f'ok':
                    select_processing = messagebox.askyesnocancel(title=f'Select an Option to continue...', message=f'[Yes] = Load Single SAF\n[No] = Merge SAF\n[Cancel] = Don\'t load animation')
                
                if select_processing == None:
                    animation_data_info = [0, 0, f'NONE']
                
                elif select_processing == False:
                    merge_1 = f'Working of Merge SAF Animation Mode'
                    merge_2 = f'\nFor sake of simplicity be sure of have the animations isolated in a folder'
                    merge_3 = f'\nInput the Folder complete path...'
                    merge_message = merge_1 + merge_2 + merge_3
                    new_message_merge = messagebox.showinfo(title=f'IMPORTANT!!...', message=merge_message)
                    path_folder_anim = askdirectory(title='Select a SAF Animation Folder')
                    
                    folder_search = path_folder_anim
                    list_files = self.look_anims_in_folder(folder_path=folder_search)

                    multi_animation_data = []
                    multi_animation_info = []
                    for animation_file_path in list_files:
                        with open(animation_file_path, 'rb') as single_animation:
                            anim_file_read = single_animation.read()
                            anim_external = self.search_anim_type(anim_search_file=anim_file_read)
                            animation_data_single = anim_external[0]
                            animation_data_info_single = anim_external[1]
                            self.animation_obj_compare(compare_tmd=model_data_objects, compare_anim=animation_data_info_single)
                            multi_animation_data.append(animation_data_single)
                            multi_animation_info.append(animation_data_info_single)
                    animation_merged = self.merge_saf_data(animation_data_to_merge=multi_animation_data, animation_info_to_merge=multi_animation_info)
                    animation_data = animation_merged[0]
                    animation_data_info = animation_merged[1]
                
                else:
                    path_anim = askopenfile(title=f'Select a SAF file...')
                    path_animation = path_anim.name
                    with open(path_animation, 'rb') as animation_file:
                        animation_file_read = animation_file.read()
                        animation_external = self.search_anim_type(anim_search_file=animation_file_read)
                        animation_data = animation_external[0]
                        animation_data_info = animation_external[1]
                        self.animation_obj_compare(compare_tmd=model_data_objects, compare_anim=animation_data_info)

    @staticmethod
    def search_type(file_search=bytes):
        # HERE I RETURN THE FILE TYPE AND THE START INDEX OF THE FILE
        checking_file = file_search
        # FIND TMD
        file_find_tmd_1 = checking_file.find(TMD_HEADER_1)
        file_find_tmd_2 = checking_file.find(TMD_HEADER_2)
        file_find_tmd_3 = checking_file.find(TMD_HEADER_3)
        file_find_tmd_4 = checking_file.find(TMD_HEADER_4)
        file_find_tmd_5 = checking_file.find(TMD_HEADER_5)
        file_find_tmd_6 = checking_file.find(TMD_HEADER_6)
        # FIND CTMD
        file_find_ctmd_1 = checking_file.find(CTMD_HEADER_1)
        file_find_ctmd_2 = checking_file.find(CTMD_HEADER_2)
        file_find_ctmd_3 = checking_file.find(CTMD_HEADER_3)
        file_find_ctmd_4 = checking_file.find(CTMD_HEADER_4)
        file_find_ctmd_5 = checking_file.find(CTMD_HEADER_5)

        model_type = f''
        model_start = []
        # Classic TMD Header CHECK
        if ((file_find_tmd_1 != -1) and (file_find_tmd_1 == 0)) or ((file_find_tmd_2 != -1) and (file_find_tmd_2 == 0)) or ((file_find_tmd_3 != -1) and (file_find_tmd_3 == 0)):
            model_type = f'TMD'
            model_start = [file_find_tmd_1, file_find_tmd_2, file_find_tmd_3, file_find_tmd_4, file_find_tmd_5, file_find_tmd_6]
        elif ((file_find_tmd_4 != -1) and (file_find_tmd_4 == 0)) or ((file_find_tmd_5 != -1) and (file_find_tmd_5 == 0)) or ((file_find_tmd_6 != -1) and (file_find_tmd_6 == 0)):
            model_type = f'TMD'
            model_start = [file_find_tmd_1, file_find_tmd_2, file_find_tmd_3, file_find_tmd_4, file_find_tmd_5, file_find_tmd_6]
        # CContainer TMD Header CHECK
        elif ((file_find_tmd_1 != -1) and (file_find_tmd_1 == 12)) or ((file_find_tmd_2 != -1) and (file_find_tmd_2 == 12)) or ((file_find_tmd_3 != -1) and (file_find_tmd_3 == 12)):
            model_type = f'TMD_CCONTAINER'
            model_start = [file_find_tmd_1, file_find_tmd_2, file_find_tmd_3, file_find_tmd_4, file_find_tmd_5, file_find_tmd_6]
        elif ((file_find_tmd_4 != -1) and (file_find_tmd_4 == 12)) or ((file_find_tmd_5 != -1) and (file_find_tmd_5 == 12)) or ((file_find_tmd_6 != -1) and (file_find_tmd_6 == 12)):
            model_type = f'TMD_CCONTAINER'
            model_start = [file_find_tmd_1, file_find_tmd_2, file_find_tmd_3, file_find_tmd_4, file_find_tmd_5, file_find_tmd_6]
        # DEFF TMD Header CHECK
        elif ((file_find_tmd_1 != -1) and (file_find_tmd_1 > 24)) or ((file_find_tmd_2 != -1) and (file_find_tmd_2 > 24)) or ((file_find_tmd_3 != -1) and (file_find_tmd_3 > 24)):
            model_type = f'TMD_DEFF'
            model_start = [file_find_tmd_1, file_find_tmd_2, file_find_tmd_3, file_find_tmd_4, file_find_tmd_5, file_find_tmd_6]
        elif ((file_find_tmd_4 != -1) and (file_find_tmd_4 > 24)) or ((file_find_tmd_5 != -1) and (file_find_tmd_5 > 24)) or ((file_find_tmd_6 != -1) and (file_find_tmd_6 > 24)):
            model_type = f'TMD_DEFF'
            model_start = [file_find_tmd_1, file_find_tmd_2, file_find_tmd_3, file_find_tmd_4, file_find_tmd_5, file_find_tmd_6]
        
        elif (file_find_ctmd_1 != -1) or (file_find_ctmd_2 != -1) or (file_find_ctmd_3 != -1) or (file_find_ctmd_4 != -1) or (file_find_ctmd_5 != -1):
            model_type = f'CTMD'
            model_start = [file_find_ctmd_1, file_find_ctmd_2, file_find_ctmd_3, file_find_ctmd_4, file_find_ctmd_5]
        
        model_final_start = f'' # Filtering the 
        for model_start_index in model_start:
            if (model_start_index != -1) and (model_start_index < 500): # BIG EYE ON THIS
                model_final_start = model_start_index
        
        return model_type, model_final_start
    
    @staticmethod
    def search_anim_type(anim_search_file=bytes):
        # FIND ANIMATIONS EMBEDDED
        file_find_cmb = anim_search_file.find(CMB_HEADER)
        file_find_lmb = anim_search_file.find(LMB_HEADER)
        # FOR SAF I MUST DO A DOUBLE CHECK, SINCE C_CONTAINERS are set also in the tmd/ctmd headers
        file_find_saf = anim_search_file.rfind(SAF_HEADER) # THIS WILL TRY TO FIND AT THE END OF THE FILE, BUT I HAVE TO MATCH WITH THE NUMBER OF OBJECTS

        anim_data = b''
        anim_info = []
        if file_find_cmb != -1:
            start_cmb = anim_search_file[file_find_cmb:]
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
            start_lmb = anim_search_file[file_find_lmb:]
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
            
        elif file_find_saf != -1:
            start_saf_data = file_find_saf + 12
            start_saf = anim_search_file[start_saf_data:]
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

        else:
            message_no_animation = f'No embedded Animation found in file, would load an animation?\n-force, this command is not available at the moment\nSelect [NO]'
            new_ctmd_no_anim = messagebox.showwarning(title=f'WARNING!!...', message=message_no_animation)
            user_force_select = messagebox.askyesno(title=f'Select Option...', message=f'Select [Yes] = Force animation loading[NOT AVAILABLE]\nSelect [No] = Continue without Animation')
            if user_force_select == False:
                anim_data = b''
                anim_info = [0, 0, f'NONE']
            else:
                force_crash = f'i tell ya!, this option is not available at the moment!!.. exiting...' # here i must write a proper animation force algorithm
                show_error_merge = messagebox.showerror(title=f'FATAL CRASH!!!', message=force_crash)
                exit()
        return anim_data, anim_info

    @staticmethod
    def getting_header_data(model_file=bytes):
        read_header_data = model_file[0:12]
        header_type = read_header_data[0:4] # IGNORING THE HEADER, READ ONCE BEFORE
        fixp_type = read_header_data[4:8] # IGNORING FIXP ||| AT LEAST NOT NEED TO READ MODEL FILES IN TLOD
        number_objects = read_header_data[8:12]
        number_objects_int = int.from_bytes(number_objects, 'little', signed=False)
        model_data_end = model_file[12:]
        return model_data_end, number_objects_int
    
    @staticmethod
    def animation_obj_compare(compare_tmd=int, compare_anim=list):
        model_data_objects = compare_tmd
        animation_data_info = compare_anim
        anim_obj_info = animation_data_info[0]
        anim_transform_info = animation_data_info[1]
        anim_type = animation_data_info[2] # WOULD EXIST DIFFERENT ANIM TYPES: SAF, CMB, LMB_TYPE_0, LMB_TYPE_1, LMB_TYPE_2 AND NONE
        if anim_obj_info == model_data_objects:
            global animation_check_info
            animation_check_info = f'\nThis {anim_type}, have: {anim_transform_info} Transforms for {anim_obj_info} Objects'
        elif anim_obj_info == 0:
            pass
        else:
            message_merge_error = f'FATAL DISCREPANCY!! - Number of Objects in Model: {model_data_objects} - {anim_type} Expected: {anim_obj_info}, processing will stop...'
            show_error_merge = messagebox.showerror(title=f'FATAL CRASH!!!', message=message_merge_error)
            exit()
    
    @staticmethod
    def look_anims_in_folder(folder_path=str):
        anim_files_in_folder = os.listdir(folder_path)
        anim_file_list = []
        for anim_files in anim_files_in_folder:
            complete_file_path = folder_path + f'\\' + anim_files
            anim_file_list.append(complete_file_path)
        return anim_file_list
    
    @staticmethod
    def merge_saf_data(animation_data_to_merge=list, animation_info_to_merge=list):
        tmd_objects = []
        saf_transformation = []

        for info in animation_info_to_merge:
            if info[2] == f'SAF':
                num_objs = info[0]
                transformations = info[1]
                tmd_objects.append(num_objs)
                saf_transformation.append(transformations)
            else:
                message_merge_error_2 = f'FATAL - MERGING IMPOSSIBLE DUE TO A NON SAF FILE, EXITING...'
                show_error_merge_2 = messagebox.showerror(title=f'FATAL CRASH!!!', message=message_merge_error_2)
                exit()
        
        objects_in_animations = list(set(tmd_objects))
        total_transformations = sum(saf_transformation)

        if len(objects_in_animations) != 1:
            message_merge_error_3 = f'FATAL - Number of objects in animation merging is different, exiting...'
            show_error_merge_3 = messagebox.showerror(title=f'FATAL CRASH!!!', message=message_merge_error_3)
            exit()

        total_animation_data = b''.join(animation_data_to_merge)
        anim_info_total = [objects_in_animations[0], total_transformations, f'SAF']
        return total_animation_data, anim_info_total