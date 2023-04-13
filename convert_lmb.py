"""

Convert CMB: This module process LMB files
LMB Files this Animation File support scalling in real time
(animated scale), this files are complex and in here
we will maintain the three Types

LMB_Type_0, LMB_Type_1, LMB_Type_2

as a side note, currently the Type 0 is "fully supported"

Copyright (C) 2023 DooMMetaL

"""

from tkinter import messagebox

class LmbConverter:
    def __init__(self):
        self.self = LmbConverter
    
    def lmb_type0_convert(self, lmb_anim_data=bytes, lmb_transform_info=list):
        lmb_objs_num = lmb_transform_info[0]
        lmb_table_calc = (lmb_objs_num * 12) # Here i get the total table length
        lmb_table = lmb_anim_data[0:lmb_table_calc] # Here i get the table
        lmb_data = lmb_anim_data[lmb_table_calc:]

        lmb_blocks = self.lmb_split_blocks(lmb_obj_count=lmb_objs_num, lmb_table_data=lmb_table, lmb_data_after=lmb_data)
        lmb_decoded_animation = self.lmb_decode(lmb_data_transformation=lmb_blocks)
        return lmb_decoded_animation
    
    @staticmethod
    def lmb_split_blocks(lmb_obj_count=int, lmb_table_data=list, lmb_data_after=list):
        lmb_table = lmb_table_data
        lmb_data = lmb_data_after

        count_objs = lmb_obj_count
        s_pos = 0
        e_pos = 12
        transform_count = []
        while count_objs > 0:
            current_table = lmb_table[s_pos:e_pos]
            current_table_count = current_table[4:8]
            count_int = int.from_bytes(current_table_count, 'little', signed=False)
            transform_count.append(count_int)
            s_pos += 12
            e_pos += 12
            count_objs -= 1

        transform_count_check = set(transform_count)

        if len(transform_count_check) == 1:
            number_transform_fix = transform_count[0]
            lmb_joined_data_trans = [] # HERE I JOIN THE DATA FOR EACH TRANSFORM BY OBJECT
            next_value = 0
            for current_transform in range(0, number_transform_fix):
                obj_count = lmb_obj_count
                jump_value_start = next_value
                jump_value_end = next_value + 20
                lmb_object_sub = []
                while obj_count > 0:
                    lmb_subtrans_block = lmb_data[jump_value_start:jump_value_end]
                    lmb_object_sub.append(lmb_subtrans_block)
                    new_jump = (number_transform_fix) * 20
                    jump_value_start += new_jump
                    jump_value_end += new_jump
                    obj_count -= 1
                lmb_joined_data_trans.append(lmb_object_sub)
                next_value += 20
            return lmb_joined_data_trans
        else:
            different_transforms = f'different number in the transformations: {transform_count_check}'
            different_transforms_window = messagebox.showerror(title=f'FATAL CRASH!!!...', message=different_transforms)
            exit()

    @staticmethod
    def lmb_decode(lmb_data_transformation=list):
        lmb_joined_data_trans = lmb_data_transformation
        if len(lmb_joined_data_trans) != 0:
            lmb_anm_frames = len(lmb_joined_data_trans) # This is important stuff! be aware!!
            enumerating_keyframe_final = []
            for lmb_transform in lmb_joined_data_trans:
                lmb_object_inside = []
                for object_lmb in lmb_transform:
                    lmb_in_obj = {"Sx": object_lmb[0:2], "Sy": object_lmb[2:4], "Sz": object_lmb[4:6],
                    "Tx": float(int.from_bytes(object_lmb[6:8], 'little', signed=True) / 1000), 
                    "Ty": float(int.from_bytes(object_lmb[8:10], 'little', signed=True) / 1000), 
                    "Tz": float(int.from_bytes(object_lmb[10:12], 'little', signed=True) / 1000),
                    "Rx": float(int.from_bytes(object_lmb[12:14], 'little', signed=True) / round((4096/360), 12)),
                    "Ry": float(int.from_bytes(object_lmb[14:16], 'little', signed=True) / round((4096/360), 12)),
                    "Rz": float(int.from_bytes(object_lmb[16:18], 'little', signed=True) / round((4096/360), 12)), "PadLmb": object_lmb[18:20]}
                    lmb_object_inside.append(lmb_in_obj)
                lmb_obj_enum = list(enumerate(lmb_object_inside))
                enumerating_keyframe_final.append(lmb_obj_enum)
            lmb_keyframes_converted_enum = list(enumerate(enumerating_keyframe_final)) # HERE I GET THE CORRECT NESTING USING THE KEYFRAME ENUMERATED
            global lmb_conversion_finished
            lmb_conversion_finished = f'Conversion of Keyframes successful'
            return lmb_keyframes_converted_enum, lmb_anm_frames
        else:
            no_lmb_data = f'No LMB data found'
            different_transforms_window = messagebox.showerror(title=f'FATAL CRASH!!!...', message=no_lmb_data)
            exit()