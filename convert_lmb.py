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
    
    def lmb_type1_convert(self, lmb_anim_data=bytes, lmb_transform_info=list):
        lmb_objs_num = lmb_transform_info[0]
        lmb_data_process = lmb_anim_data
        # NEED TO ADJUST THE INDEX SO A LITTLE MATH WHICH NOT REPRESENT THE ACTUAL TABLE VALUE
        data_08 = int.from_bytes(lmb_anim_data[0:2], 'little', signed=False) 
        data_0a = int.from_bytes(lmb_anim_data[2:4], 'little', signed=False)
        data_0c_table = int.from_bytes(lmb_anim_data[4:8], 'little', signed=False) - 8
        data_10 = int.from_bytes(lmb_anim_data[8:10], 'little', signed=False) - 8
        data_14_subblock = int.from_bytes(lmb_anim_data[12:14], 'little', signed=False) - 8

        split_blocks = self.lmb_type1_split_blocks(lmb_data=lmb_data_process, lmb_objs_count=lmb_objs_num, d_08=data_08, d_0a=data_0a, d_0c=data_0c_table, d_10=data_10, d_14=data_14_subblock)
        flag_table = split_blocks[0]
        base_transform = split_blocks[1]
        sub_transform = split_blocks[2]
        decoded_animation = self.lmb_type1_decode(flag_t=flag_table, b_trans=base_transform, sub_trans=sub_transform, d_08_value=data_08, obj_count=lmb_objs_num, count_0a=data_0a)
        return decoded_animation
    
    def lmb_type2_convert(self, lmb_anim_data=bytes, lmb_transform_info=list):
        lmb_objs_num = lmb_transform_info[0]
        lmb_data_process = lmb_anim_data
        # NEED TO ADJUST THE INDEX SO A LITTLE OF MATH WHICH NOT REPRESENT THE ACTUAL TABLE VALUE
        data_08 = int.from_bytes(lmb_anim_data[0:2], 'little', signed=False) 
        data_0a = int.from_bytes(lmb_anim_data[2:4], 'little', signed=False)
        data_0c_table = int.from_bytes(lmb_anim_data[4:8], 'little', signed=False) - 8
        data_10 = int.from_bytes(lmb_anim_data[8:10], 'little', signed=False) - 8
        data_14_subblock = int.from_bytes(lmb_anim_data[12:14], 'little', signed=False) - 8

        split_blocks = self.lmb_type2_split_blocks(lmb_data=lmb_data_process, lmb_objs_count=lmb_objs_num, d_08=data_08, d_0a=data_0a, d_0c=data_0c_table, d_10=data_10, d_14=data_14_subblock)
        flag_table = split_blocks[0]
        base_transform = split_blocks[1]
        sub_transform = split_blocks[2]
        decoded_animation = self.lmb_type2_decode(flag_t=flag_table, b_trans=base_transform, sub_trans=sub_transform, d_08_value=data_08, obj_count=lmb_objs_num, count_0a=data_0a)
        return decoded_animation
    
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
    
    @staticmethod
    def lmb_type1_split_blocks(lmb_data=bytes, lmb_objs_count=int, d_08=bytes, d_0a=bytes, d_0c=bytes, d_10=bytes, d_14=bytes):
        
        # FLAG TABLE EXTRACTION
        flag_table = [] # ---> the FLAG data is related with the object count for some reason
        start_table_flag = d_0c
        end_table_flag = d_0c + 4
        for moving_in_flags in range(0, lmb_objs_count):
            flag_extracted = lmb_data[start_table_flag:end_table_flag]
            flag_table.append(flag_extracted)
            start_table_flag += 4
            end_table_flag += 4
        
        # Base - Transform Block
        base_transform = [] # ---> base transforms are related directly to the objects
        start_base_trans = d_10
        end_base_trans = d_10 + 20
        for moving_base_trans in range(0, lmb_objs_count):
            base_trans_extracted = lmb_data[start_base_trans:end_base_trans]
            base_transform.append(base_trans_extracted)
            start_base_trans += 20
            end_base_trans += 20

        # Sub - Transform Block
        sub_transform = [] # ---> the Low part to complete into the base transform
        start_position_sublock = d_14
        end_position_sublock = d_14 + 2
        block_length = d_08 * (d_0a - 1) // 2 # ---> Number of Bytes, //2 to get (an int instead of Float) the correct Array length range
        for moving_subtrans in range(0, block_length):
            sub_transform_extracted = lmb_data[start_position_sublock:end_position_sublock]
            sub_transform.append(sub_transform_extracted)
            start_position_sublock += 2
            end_position_sublock += 2
        
        return flag_table, base_transform, sub_transform
    
    @staticmethod
    def lmb_type1_decode(flag_t=list, b_trans=list, sub_trans=list, d_08_value=int, obj_count=int, count_0a=int):
        # Structure ROT/TRANS/SCALE
        count_transformations = int(count_0a)
        # FIRST i will split the FLAGs because i will need them in the end of the code
        flag_split = []
        for f_split in flag_t:
            flag_head = int.from_bytes(f_split[0:2], 'little', signed=False)
            flag_tail = int.from_bytes(f_split[3:4], 'little', signed=False)
            flag_new = [flag_head, flag_tail]
            flag_split.append(flag_new)
        
        base_transform = []
        b_trans_length = len(b_trans)
        for number_object in range(0, b_trans_length):
            b_transform_data = b_trans[number_object]
            # Using Nesting right now to match the animation spec
            lmb_in_obj = {"Sx": int.from_bytes(b_transform_data[0:2], 'little', signed=False), "Sy": int.from_bytes(b_transform_data[2:4], 'little', signed=False), "Sz": int.from_bytes(b_transform_data[4:6], 'little', signed=False),
                    "Tx": float(int.from_bytes(b_transform_data[6:8], 'little', signed=True) / 1000), 
                    "Ty": float(int.from_bytes(b_transform_data[8:10], 'little', signed=True) / 1000), 
                    "Tz": float(int.from_bytes(b_transform_data[10:12], 'little', signed=True) / 1000),
                    "Rx": float(int.from_bytes(b_transform_data[12:14], 'little', signed=True) / round((4096/360), 12)),
                    "Ry": float(int.from_bytes(b_transform_data[14:16], 'little', signed=True) / round((4096/360), 12)),
                    "Rz": float(int.from_bytes(b_transform_data[16:18], 'little', signed=True) / round((4096/360), 12)), "PadLmb": b_transform_data[18:20]}
            base_transform.append(lmb_in_obj)
        enumerate_objects_base = list(enumerate(base_transform))
        
        final_sub_transforms = []
        start_count_super = 0
        start_count_super_2 = 0
        for looping_lmb in range(0, count_transformations):
            if looping_lmb == 0:
                final_sub_transforms.append(enumerate_objects_base)
            else:
                sub_transforms_total_obj = []
                sub_transforms_total_obj_processed = []
                start_count = 0 + start_count_super
                slice_to_values = (start_count - 1) * d_08_value // 2
                for number_obj in range(0, int(obj_count)):
                    sub_transforms_current_obj = [0] * 9
                    flag_complete = flag_split[number_obj]
                    flag_check = flag_complete[0]
                    # Scale Check
                    if (flag_check & 0x8000) == 0:
                        new_x_scale = sub_trans[slice_to_values]
                        sub_transforms_current_obj[0] = int.from_bytes(new_x_scale, 'little', signed=False)
                        slice_to_values += 1
                    if (flag_check & 0x4000) == 0:
                        new_y_scale = sub_trans[slice_to_values]
                        sub_transforms_current_obj[1] = int.from_bytes(new_y_scale, 'little', signed=False)
                        slice_to_values += 1
                    if (flag_check & 0x2000) == 0:
                        new_z_scale = sub_trans[slice_to_values]
                        sub_transforms_current_obj[2] = int.from_bytes(new_z_scale, 'little', signed=False)
                        slice_to_values += 1
                    # Translation Check
                    if (flag_check & 0x1000) == 0:
                        new_x_trans = sub_trans[slice_to_values]
                        sub_transforms_current_obj[3] = int.from_bytes(new_x_trans, 'little', signed=True)
                        slice_to_values += 1
                    if (flag_check & 0x800) == 0:
                        new_y_trans = sub_trans[slice_to_values]
                        sub_transforms_current_obj[4] = int.from_bytes(new_y_trans, 'little', signed=True)
                        slice_to_values += 1
                    if (flag_check & 0x400) == 0:
                        new_z_trans = sub_trans[slice_to_values]
                        sub_transforms_current_obj[5] = int.from_bytes(new_z_trans, 'little', signed=True)
                        slice_to_values += 1
                    # Rotation Check
                    if (flag_check & 0x200) == 0:
                        new_x_rot = sub_trans[slice_to_values]
                        sub_transforms_current_obj[6] = int.from_bytes(new_x_rot, 'little', signed=True)
                        slice_to_values += 1
                    if (flag_check & 0x100) == 0:
                        new_y_rot = sub_trans[slice_to_values]
                        sub_transforms_current_obj[7] = int.from_bytes(new_y_rot, 'little', signed=True)
                        slice_to_values += 1
                    if (flag_check & 0x80) == 0:
                        new_z_rot = sub_trans[slice_to_values]
                        sub_transforms_current_obj[8] = int.from_bytes(new_z_rot, 'little', signed=True)
                        slice_to_values += 1
                    
                    sub_transforms_total_obj.append(sub_transforms_current_obj)

                start_count_2 = 1 + start_count_super_2
                slice_to_values_2 = (start_count_2 - 1) * d_08_value // 2
                for number_obj_2 in range(0, int(obj_count)):
                    new_flag_complete = flag_split[number_obj_2]
                    new_flag_check = new_flag_complete[0]
                    sub_transforms = sub_transforms_total_obj[number_obj_2]

                    # Scale Check
                    if (new_flag_check & 0x8000) == 0:
                        order_new_x_scale = sub_transforms[0]
                        calc_new_x_scale = (order_new_x_scale * 4096 + int.from_bytes(sub_trans[slice_to_values_2], 'little', signed=False) * 4096) // 0x2000
                        sub_transforms[0] = calc_new_x_scale
                        slice_to_values_2 += 1

                    if (new_flag_check & 0x4000) == 0:
                        order_new_y_scale = sub_transforms[1]
                        calc_new_y_scale = (order_new_y_scale * 4096 + int.from_bytes(sub_trans[slice_to_values_2], 'little', signed=False) * 4096) // 0x2000
                        sub_transforms[1] = calc_new_y_scale
                        slice_to_values_2 += 1

                    if (new_flag_check & 0x2000) == 0:
                        order_new_z_scale = sub_transforms[2]
                        calc_new_z_scale = (order_new_z_scale * 4096 + int.from_bytes(sub_trans[slice_to_values_2], 'little', signed=False) * 4096) // 0x2000
                        sub_transforms[2] = calc_new_z_scale
                        slice_to_values_2 += 1

                    # Translation Check
                    if (new_flag_check & 0x1000) == 0:
                        order_new_x_trans = sub_transforms[3]
                        calc_new_x_trans = (order_new_x_trans * 4096 + int.from_bytes(sub_trans[slice_to_values_2], 'little', signed=True) * 4096) // 0x2000
                        sub_transforms[3] = calc_new_x_trans
                        slice_to_values_2 += 1

                    if (new_flag_check & 0x800) == 0:
                        order_new_y_trans = sub_transforms[4]
                        calc_new_y_trans = (order_new_y_trans * 4096 + int.from_bytes(sub_trans[slice_to_values_2], 'little', signed=True) * 4096) // 0x2000
                        sub_transforms[4] = calc_new_y_trans
                        slice_to_values_2 += 1
                        
                    if (new_flag_check & 0x400) == 0:
                        order_new_z_trans = sub_transforms[5]
                        calc_new_z_trans = (order_new_z_trans * 4096 + int.from_bytes(sub_trans[slice_to_values_2], 'little', signed=True) * 4096) // 0x2000
                        sub_transforms[5] = calc_new_z_trans
                        slice_to_values_2 += 1
                        
                    # Rotation Check
                    if (new_flag_check & 0x200) == 0:
                        slice_to_values_2 += 1
                    if (new_flag_check & 0x100) == 0:
                        slice_to_values_2 += 1
                    if (new_flag_check & 0x80) == 0:
                        slice_to_values_2 += 1
                    sub_transforms_total_obj_processed.append(sub_transforms)
                
                converted_sub_transformations = []
                for conversion_sub_trans in sub_transforms_total_obj_processed:
                    converted_block = {"Sx": conversion_sub_trans[0], "Sy": conversion_sub_trans[1], "Sz": conversion_sub_trans[2],
                            "Tx": conversion_sub_trans[3] / 1000, 
                            "Ty": conversion_sub_trans[4] / 1000, 
                            "Tz": conversion_sub_trans[5] / 1000,
                            "Rx": conversion_sub_trans[6] / round((4096/360), 12),
                            "Ry": conversion_sub_trans[7] / round((4096/360), 12),
                            "Rz": conversion_sub_trans[8] / round((4096/360), 12), "PadLmb": 0}
                    converted_sub_transformations.append(converted_block)
                enumerate_objects = list(enumerate(converted_sub_transformations))
                final_sub_transforms.append(enumerate_objects)
                start_count_super += 1
        lmb_keyframes_converted_enum = list(enumerate(final_sub_transforms)) # HERE I GET THE CORRECT NESTING USING THE KEYFRAME ENUMERATED
        lmb_anm_frames = count_transformations
        global lmb_conversion_finished
        lmb_conversion_finished = f'Conversion of Keyframes successful'
        return lmb_keyframes_converted_enum, lmb_anm_frames
    
    @staticmethod
    def lmb_type2_split_blocks(lmb_data=bytes, lmb_objs_count=int, d_08=bytes, d_0a=bytes, d_0c=bytes, d_10=bytes, d_14=bytes):
        
        # FLAG TABLE EXTRACTION
        flag_table = [] # ---> the FLAG data is related with the object count for some reason
        start_table_flag = d_0c
        end_table_flag = d_0c + 4
        for moving_in_flags in range(0, lmb_objs_count):
            flag_extracted = lmb_data[start_table_flag:end_table_flag]
            flag_table.append(flag_extracted)
            start_table_flag += 4
            end_table_flag += 4
        
        # Base - Transform Block
        base_transform = [] # ---> base transforms are related directly to the objects
        start_base_trans = d_10
        end_base_trans = d_10 + 20
        for moving_base_trans in range(0, lmb_objs_count):
            base_trans_extracted = lmb_data[start_base_trans:end_base_trans]
            base_transform.append(base_trans_extracted)
            start_base_trans += 20
            end_base_trans += 20

        # Sub - Transform Block
        sub_transform = [] # ---> the Low part to complete into the base transform
        start_position_sublock = d_14
        end_position_sublock = d_14 + 1
        block_length = d_08 * (d_0a - 1) # ---> Array Length
        for moving_subtrans in range(0, block_length):
            sub_transform_extracted = lmb_data[start_position_sublock:end_position_sublock]
            sub_transform.append(sub_transform_extracted)
            start_position_sublock += 1
            end_position_sublock += 1
        
        return flag_table, base_transform, sub_transform
    
    @staticmethod
    def lmb_type2_decode(flag_t=list, b_trans=list, sub_trans=list, d_08_value=int, obj_count=int, count_0a=int):
        # FIRST FRAME SEEMS TO BE THE BASE TRANSFORM (Frame 1)
        # THEN WILL PROCESS THE HIGH Bytes to be ready for the next processing (Frame 2)
        # Finally will start process the High values and the previous iters for calculate the new transforms
        # FLAGS ARE READ as a single number, not like LMB Type 1
        base_transform = []
        for number_object in range(0, obj_count): # Base Transformation Model Object Level
            b_transform_data = b_trans[number_object]
            # Using Nesting right now to match the animation spec
            lmb_in_obj = {"Sx": int.from_bytes(b_transform_data[0:2], 'little', signed=True), "Sy": int.from_bytes(b_transform_data[2:4], 'little', signed=True), "Sz": int.from_bytes(b_transform_data[4:6], 'little', signed=True),
                        "Tx": int.from_bytes(b_transform_data[6:8], 'little', signed=True),
                        "Ty": int.from_bytes(b_transform_data[8:10], 'little', signed=True),
                        "Tz": int.from_bytes(b_transform_data[10:12], 'little', signed=True),
                        "Rx": int.from_bytes(b_transform_data[12:14], 'little', signed=True),
                        "Ry": int.from_bytes(b_transform_data[14:16], 'little', signed=True),
                        "Rz": int.from_bytes(b_transform_data[16:18], 'little', signed=True),
                        "PadLmb": int.from_bytes(b_transform_data[18:20], 'little', signed=True)}
            base_transform.append(lmb_in_obj)

        shifting_hibytes = [] # ---> High Bytes Shifted for transforms
        """THIS IS Count_0a - 1 because the count_0a represent all the transforms including the first, since the first transform is ignored the block
        of sub-transforms naturally would be all the transforms subtracting one"""
        for sub_trans_number in range(0, (count_0a - 1) ):
            block_nest = []
            nest_high_slice = sub_trans_number * d_08_value
            total_length_subtrans = d_08_value * 2 # THIS * 2 because the same byte it's used twice
            for length_subtrans in range(0, total_length_subtrans, 2):
                byte_1_int = int.from_bytes(sub_trans[nest_high_slice], 'little', signed=True) >> 4
                byte_2_int = int.from_bytes(sub_trans[nest_high_slice], 'little', signed=True) << 28 >> 28
                block_nest.append(byte_1_int)
                block_nest.append(byte_2_int)
                nest_high_slice += 1
            shifting_hibytes.append(block_nest)
        
        transforms_base = [] # FILLING ALL THE KEYFRAMES WITH BASE TRANSFORM // This is Keyframe Level
        for all_key_frames_fill in range(0, count_0a):
            transforms_base.append(base_transform)
        
        #################################################################################################
        #|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
        #################################################################################################
        # TRANSFORMATIONS CALCS

        keyframes_calculated = [] # FINAL CALCULATION OF KEYFRAMES
        """Keyframe 0 is ignored and just contains the base transform, the subsequent transformations are done this way:
        1st a pre-process involving the BVecs from shifting_hibytes and adding them to the base transform this will result 
        in a Low Transform block.
        2nd main process in which the Low Transform data is additionally calculated in a sum of the shift values, resulting
        in a High Transform, in the SC Code there are some additional conditions that i'm ignoring, not sure if this the correct way
        but i believe that much of those calculations are done to keep all the things synchroniced"""
        for keyframe in range(0, count_0a):
            if keyframe == 0:
                keyframe_0 = transforms_base[keyframe]
                keyframes_calculated.append(keyframe_0)
            else:
                if keyframe == 1:
                    sub_transforms_low = []
                    previous_keyframe_transform = keyframes_calculated[keyframe - 1] # This always will be the previous keyframe in the current loop
                    subtransform_shift_block = shifting_hibytes[keyframe - 1] # This is the current aligned block of bytes to be used during the conversion
                    slicing_shift_values_2 = 0
                    for current_object_2 in range(0, obj_count):
                        object_previous_keyframe_transform_2 = previous_keyframe_transform[current_object_2] # This is the Current Object Transform Base Table
                        flags_current_object_2 = int.from_bytes(flag_t[current_object_2], 'little', signed=False)
                        new_sub_transform_2 = {"Sx": object_previous_keyframe_transform_2.get("Sx"), "Sy": object_previous_keyframe_transform_2.get("Sy"), "Sz": object_previous_keyframe_transform_2.get("Sz"), 
                                            "Tx": object_previous_keyframe_transform_2.get("Tx"), "Ty": object_previous_keyframe_transform_2.get("Ty"), "Tz": object_previous_keyframe_transform_2.get("Tz"), 
                                            "Rx": object_previous_keyframe_transform_2.get("Rx"), "Ry": object_previous_keyframe_transform_2.get("Ry"), "Rz": object_previous_keyframe_transform_2.get("Rz"), 
                                            "PadLmb": 0}
                        multiplier_value = 8192
                        # SCALE
                        if (flags_current_object_2 & 0xe000) != 0xe000:
                            shift_value = subtransform_shift_block[slicing_shift_values_2] & 0xf
                            slicing_shift_values_2 += 1

                            if (flags_current_object_2 & 0x8000) == 0:
                                shift_sx = (subtransform_shift_block[slicing_shift_values_2] << shift_value) * multiplier_value / 0x2000
                                new_sx = new_sub_transform_2.get("Sx") + shift_sx
                                new_sub_transform_2.update({"Sx": new_sx})
                                slicing_shift_values_2 += 1

                            if (flags_current_object_2 & 0x4000) == 0:
                                shift_sy = (subtransform_shift_block[slicing_shift_values_2] << shift_value) * multiplier_value / 0x2000
                                new_sy = new_sub_transform_2.get("Sy") + shift_sy
                                new_sub_transform_2.update({"Sy": new_sy})
                                slicing_shift_values_2 += 1

                            if (flags_current_object_2 & 0x2000) == 0:
                                shift_sz = (subtransform_shift_block[slicing_shift_values_2] << shift_value) * multiplier_value / 0x2000
                                new_sz = new_sub_transform_2.get("Sz") + shift_sz
                                new_sub_transform_2.update({"Sz": new_sz})
                                slicing_shift_values_2 += 1

                        # TRANSLATION
                        if (flags_current_object_2 & 0x1c00) != 0x1c00:
                            shift_value = subtransform_shift_block[slicing_shift_values_2] & 0xf
                            slicing_shift_values_2 += 1

                            if (flags_current_object_2 & 0x1000) == 0:
                                shift_tx = (subtransform_shift_block[slicing_shift_values_2] << shift_value) * multiplier_value / 0x2000
                                new_tx = new_sub_transform_2.get("Tx") + shift_tx
                                new_sub_transform_2.update({"Tx": new_tx})
                                slicing_shift_values_2 += 1

                            if (flags_current_object_2 & 0x800) == 0:
                                shift_ty = (subtransform_shift_block[slicing_shift_values_2] << shift_value) * multiplier_value / 0x2000
                                new_ty = new_sub_transform_2.get("Ty") + shift_ty
                                new_sub_transform_2.update({"Ty": new_ty})
                                slicing_shift_values_2 += 1

                            if (flags_current_object_2 & 0x400) == 0:
                                shift_tz = (subtransform_shift_block[slicing_shift_values_2] << shift_value) * multiplier_value / 0x2000
                                new_tz = new_sub_transform_2.get("Tz") + shift_tz
                                new_sub_transform_2.update({"Tz": new_tz})
                                slicing_shift_values_2 += 1

                        # ROTATION
                        if (flags_current_object_2 & 0x380) != 0x380:
                            slicing_shift_values_2 += 1

                            if (flags_current_object_2 & 0x200) == 0:
                                slicing_shift_values_2 += 1

                            if (flags_current_object_2 & 0x100) == 0:
                                slicing_shift_values_2 += 1

                            if (flags_current_object_2 & 0x80) == 0:
                                slicing_shift_values_2 += 1

                        sub_transforms_low.append(new_sub_transform_2)
                    keyframes_calculated.append(sub_transforms_low)

                else:
                    sub_transforms_high = []
                    slicing_shift_values = 0
                    sub_transforms_low_after = keyframes_calculated[keyframe - 1]
                    for current_object in range(0, obj_count):
                        object_previous_keyframe_transform = sub_transforms_low_after[current_object] # This is the Current Object Transform Base Table
                        flags_current_object = int.from_bytes(flag_t[current_object], 'little', signed=False)
                        new_sub_transform = {"Sx": object_previous_keyframe_transform.get("Sx"), "Sy": object_previous_keyframe_transform.get("Sy"), "Sz": object_previous_keyframe_transform.get("Sz"), 
                                            "Tx": object_previous_keyframe_transform.get("Tx"), "Ty": object_previous_keyframe_transform.get("Ty"), "Tz": object_previous_keyframe_transform.get("Tz"), 
                                            "Rx": object_previous_keyframe_transform.get("Rx"), "Ry": object_previous_keyframe_transform.get("Ry"), "Rz": object_previous_keyframe_transform.get("Rz"), 
                                            "PadLmb": 0}
                        # SCALE
                        if (flags_current_object & 0xe000) != 0xe000:
                            shift_value = subtransform_shift_block[slicing_shift_values] & 0xf
                            slicing_shift_values += 1

                            if (flags_current_object & 0x8000) == 0:
                                shift_sx = subtransform_shift_block[slicing_shift_values] << shift_value
                                new_sx = new_sub_transform.get("Sx") + shift_sx
                                new_sub_transform.update({"Sx": new_sx})
                                slicing_shift_values += 1

                            if (flags_current_object & 0x4000) == 0:
                                shift_sy = subtransform_shift_block[slicing_shift_values] << shift_value
                                new_sy = new_sub_transform.get("Sy") + shift_sy
                                new_sub_transform.update({"Sy": new_sy})
                                slicing_shift_values += 1

                            if (flags_current_object & 0x2000) == 0:
                                shift_sz = subtransform_shift_block[slicing_shift_values] << shift_value
                                new_sz = new_sub_transform.get("Sz") + shift_sz
                                new_sub_transform.update({"Sz": new_sz})
                                slicing_shift_values += 1

                        # TRANSLATION
                        if (flags_current_object & 0x1c00) != 0x1c00:
                            shift_value = subtransform_shift_block[slicing_shift_values] & 0xf
                            slicing_shift_values += 1

                            if (flags_current_object & 0x1000) == 0:
                                shift_tx = (subtransform_shift_block[slicing_shift_values] << shift_value)
                                new_tx = new_sub_transform.get("Tx") + shift_tx
                                new_sub_transform.update({"Tx": new_tx})
                                slicing_shift_values += 1

                            if (flags_current_object & 0x800) == 0:
                                shift_ty = (subtransform_shift_block[slicing_shift_values] << shift_value)
                                new_ty = new_sub_transform.get("Ty") + shift_ty
                                new_sub_transform.update({"Ty": new_ty})
                                slicing_shift_values += 1

                            if (flags_current_object & 0x400) == 0:
                                shift_tz = (subtransform_shift_block[slicing_shift_values] << shift_value)
                                new_tz = new_sub_transform.get("Tz") + shift_tz
                                new_sub_transform.update({"Tz": new_tz})
                                slicing_shift_values += 1

                        # ROTATION
                        if (flags_current_object & 0x380) != 0x380:
                            shift_value = subtransform_shift_block[slicing_shift_values] & 0xf
                            slicing_shift_values += 1

                            if (flags_current_object & 0x200) == 0:
                                shift_rx = (subtransform_shift_block[slicing_shift_values] << shift_value)
                                new_rx = new_sub_transform.get("Rx") + shift_rx
                                new_sub_transform.update({"Rx": new_rx})
                                slicing_shift_values += 1

                            if (flags_current_object & 0x100) == 0:
                                shift_ry = (subtransform_shift_block[slicing_shift_values] << shift_value)
                                new_ry = new_sub_transform.get("Ry") + shift_ry
                                new_sub_transform.update({"Ry": new_ry})
                                slicing_shift_values += 1

                            if (flags_current_object & 0x80) == 0:
                                shift_rz = (subtransform_shift_block[slicing_shift_values] << shift_value)
                                new_rz = new_sub_transform.get("Rz") + shift_rz
                                new_sub_transform.update({"Rz": new_rz})
                                slicing_shift_values += 1
                            
                        sub_transforms_high.append(new_sub_transform)
                    keyframes_calculated.append(sub_transforms_high)
        
        # END OF TRANSFORMS CALCULATIONS
        #################################################################################################
        #|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
        #################################################################################################

        final_transform_object_enumerate = []
        for final_trans in keyframes_calculated:
            doing_object_enumeration = []
            for final_t in final_trans:
                final_t_sx = final_t.get("Sx")
                final_t_sy = final_t.get("Sy")
                final_t_sz = final_t.get("Sz")
                final_t_tx = final_t.get("Tx")
                final_t_ty = final_t.get("Ty")
                final_t_tz = final_t.get("Tz")
                final_t_rx = final_t.get("Rx")
                final_t_ry = final_t.get("Ry")
                final_t_rz = final_t.get("Rz")
                final_t_pad = final_t.get("PadLmb")
                calculated_lmb = {"Sx": final_t_sx, "Sy": final_t_sy, "Sz": final_t_sz,
                        "Tx": float(final_t_tx / 1000),
                        "Ty": float(final_t_ty /1000),
                        "Tz": float(final_t_tz /1000),
                        "Rx": float(final_t_rx / round((4096/360), 12)),
                        "Ry": float(final_t_ry / round((4096/360), 12)),
                        "Rz": float(final_t_rz / round((4096/360), 12)),
                        "PadLmb": final_t_pad}
                doing_object_enumeration.append(calculated_lmb)
            object_enumeration = list(enumerate(doing_object_enumeration))
            final_transform_object_enumerate.append(object_enumeration)
        
        lmb_anm_frames = len(final_transform_object_enumerate)
        lmb_keyframes_converted_enum = list(enumerate(final_transform_object_enumerate)) # HERE I GET THE CORRECT NESTING USING THE KEYFRAME ENUMERATED
        global lmb_conversion_finished
        lmb_conversion_finished = f'Conversion of Keyframes successful'
        return lmb_keyframes_converted_enum, lmb_anm_frames