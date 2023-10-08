"""

Filter File: Model and Animation files, to work in batch mode

Copyright (C) 2023 DooMMetaL

"""

from tkinter import messagebox
import decompress_bpe

# HERE I DECLARE THE 'MAGIC' OR HEADERS, THAT ARE "CONSTANTS"
# THIS IS PRETTY MUCH THE FOUND WE MADE UNTIL HERE

# TMD headers
TMD_HEADER_1 = b'A\x00\x00\x00\x00\x00\x00\x00'
TMD_HEADER_2 = b'A\x01\x00\x00\x00\x00\x00\x00'
TMD_HEADER_3 = b'A\x00\x01\x00\x00\x00\x00\x00'
TMD_HEADER_4 = b'A\x00\x00\x01\x00\x00\x00\x00'
TMD_HEADER_5 = b'A\x00\x03\x00\x00\x00\x00\x00'
TMD_HEADER_6 = b'A\x00\x02\x00\x00\x00\x00\x00'
# Animation headers
SAF_HEADER = b'\x0C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

""" NOTE 1: THE BYTES THAT ARE DIFFERENT IN THE TMD/CTMD MAGICS SEEMS TO BE OVERWRITING THE DATA OF TSB.
    NOTE 2: ACTUALLY SAF FILES DON'T HAVE AN SPECIFIC HEADER, just using the container (C_Container).""" 

class ModelFilterFile:
    """First we need to filter the type of file from the input"""
    def __init__(self, model_file, animation_file, animation_type):
        self.self = ModelFilterFile
        self.model_file = model_file
        self.animation_file = animation_file
        self.filter_model_file(model_file=model_file, animation_file=animation_file, animation_type=animation_type)
    
    def filter_model_file(self, model_file=str, animation_file=str, animation_type=str):
        check_this_model = model_file
        check_this_animtype = animation_type
        check_this_animation = animation_file
        
        global file_type
        """File Type == the supported model files TMD/CTMD"""
        global model_data
        """Model Data == Array of Bytes of model"""
        global model_data_objects
        """Model Data Objects == Number of Objects in model"""
        global animation_data
        global animation_data_info
        """File Filter Text to be printed"""
        global file_filter_text
        file_filter_text = f''
        
        file_type = f''
        model_data = b''
        model_data_objects = 0
        animation_data = b''
        animation_data_info = []

        with open(check_this_model, 'rb') as check_header:
            read_file = check_header.read()
            file_checked = self.search_type(file_search=read_file)
            file_type = file_checked[0] # special model types will be TMD_DEFF and CTMD
            file_start = file_checked[1] # Index in which the file data starts
            # FIRST I FILTER THE FILES BY TYPE
            if (file_type == f'TMD') or (file_type == f'TMD_CCONTAINER') or (file_type == f'TMD_DEFF'):
                start_slice_model = read_file[file_start:]
                header_type = start_slice_model[0:4]
                data_grab = self.getting_header_data(start_slice_model)
                data_grab_model = data_grab[0]
                model_data_objects = data_grab[1]
                model_data = data_grab_model
                file_filter_text = f'\nThis is a Standard TMD {header_type}, Number of Objects: {model_data_objects}'
            else:
                file_filter_text = f'\nfile {check_header} is not a 3D model file'
                exit()

        if animation_type != f'No Animation':
            if check_this_animtype == f'Additions':
                convert_from_bpe = decompress_bpe.decompress_bpe(animation_file)
                animation_find = self.search_anim_type(anim_search_file=convert_from_bpe[0])
                animation_data = animation_find[0]
                animation_data_info = animation_find[1]
                self.animation_obj_compare(compare_tmd=model_data_objects, compare_anim=animation_data_info)
            else:
                with open(check_this_animation, 'rb') as anim_data:
                    animation_file_read = anim_data.read()
                    animation_find = self.search_anim_type(anim_search_file=animation_file_read)
                    animation_data = animation_find[0]
                    animation_data_info = animation_find[1]
                    self.animation_obj_compare(compare_tmd=model_data_objects, compare_anim=animation_data_info)
        else:
            animation_data_info = [0, 0, f'NONE']

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
        
        model_final_start = f'' # Filtering the 
        for model_start_index in model_start:
            if (model_start_index != -1) and (model_start_index < 500): # BIG EYE ON THIS
                model_final_start = model_start_index
        
        return model_type, model_final_start
    
    @staticmethod
    def search_anim_type(anim_search_file=bytes):
        # TODO need a better way to do this FOR SAF I MUST DO A DOUBLE CHECK, SINCE C_CONTAINERS are set also in the tmd/ctmd headers
        file_find_saf = anim_search_file.find(SAF_HEADER) # THIS WILL TRY TO FIND AT THE END OF THE FILE, BUT I HAVE TO MATCH WITH THE NUMBER OF OBJECTS

        anim_data = b''
        anim_info = []
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