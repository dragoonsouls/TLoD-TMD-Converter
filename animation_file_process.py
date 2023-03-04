"""

Animation File Process: This module process files that believe to be animations,
be aware that is very buggy and experimental, the animation file has been called:
Scripted Animation File (SAF for short).

Note: This module is very buggy and experimental

Copyright (C) 2022 DooMMetaL

"""

import os
import standard_tmd
import struct
import custom_tmd

# SAF READER AND DECODER

class SafExtractor:
    def __init__(self, readersaf, comparedata, convertsaf):
        self.self = SafExtractor
        self.readersaf = readersaf
        self.comparedata = comparedata
        self.convertsaf = convertsaf
    
    def saf_reader_input(self):
        try:
            print("Please, write the full path to the Animation File: ")
            global animation_file
            input_ani_file = input()
            animation_file = (input_ani_file)
        
        except OSError:
            print("Is not a valid path, exiting")
            exit()
    
    def saf_reader_embedded(self, saf_block):

        animation_saf = saf_block

        global anm_objs
        global anm_frames
        avoid_header = animation_saf[12:] # HERE, AVOID THE 3 RELATIVE POINTERS IN ALL THE SAFs
        head_anmfile = avoid_header[0:4] # ANIMATION HEADER, WHICH INCLUDE NOBJ AND TOTAL FRAMES?
        anm_objs = int.from_bytes(head_anmfile[0:2], byteorder='little')
        anm_frames = int.from_bytes(head_anmfile[2:4], byteorder='little')
        header_str = f'This Animation file contains {anm_objs} Objects and {anm_frames} Frames'
        
        print(header_str) # Printing the Animation Properties

        anm_complete_block = avoid_header[4:] # Here the seek jump is done automatically
        length_each_block = anm_objs * 12 # 12 == 2 Bytes for (rx,ry,rz,tx,ty,tz)

        # File size - Getting the length of the complete block, for further calculations
        anm_stat = len(anm_complete_block)
        block_size = anm_stat

        # Correlativity Objects/NumberFrames/Blocks
        coincidence = (block_size / length_each_block)

        if int(coincidence * 2) == anm_frames:
            print("Exist correlativity between Animation Frames and Blocks")
        else:
            print("There are no correlativity between Animation Frames and Blocks, Report this as Frame/Block not equal")
            exit()
        
        keyframes_blocks_bytes = [] # HERE I GOT THE KEYFRAMES THAT REPRESENTS ALL THE BLOCKS SPLIT
        block_s = block_size
        s_block = 0
        e_block = length_each_block
        while block_s > 0:
            anm_split_data = anm_complete_block[s_block:e_block]
            keyframes_blocks_bytes.append(anm_split_data)
            s_block += length_each_block
            e_block += length_each_block
            block_s -= length_each_block
        
        global keyframe_obj_block
        keyframe_obj_block = [] # HERE I GOT THE KEYFRAMES BLOCK SPLIT
        for obj_unique in keyframes_blocks_bytes:
            obj_keyframe = []
            len_obj_u = len(obj_unique)
            s_obj = 0
            e_obj = 12
            while len_obj_u > 0:
                k_objunique = obj_unique[s_obj:e_obj]
                obj_keyframe.append(k_objunique)
                s_obj += 12
                e_obj += 12
                len_obj_u -=12
            keyframe_obj_block.append(obj_keyframe)

    def saf_reader(self):

        with open(animation_file, 'rb') as animation_saf:
            global anm_objs
            global anm_frames
            animation_saf.seek(12) # HERE, AVOID THE 3 RELATIVE POINTERS IN ALL THE SAFs
            head_anmfile = animation_saf.read(4) # ANIMATION HEADER, WHICH INCLUDE NOBJ AND TOTAL FRAMES?
            anm_objs = int.from_bytes(head_anmfile[0:2], byteorder='little')
            anm_frames = int.from_bytes(head_anmfile[2:4], byteorder='little')
            header_str = f'This Animation file contains {anm_objs} Objects and {anm_frames} Frames'
            
            print(header_str) # Printing the Animation Properties

            anm_complete_block = animation_saf.read() # Here the seek jump is done automatically
            length_each_block = anm_objs * 12 # 12 == 2 Bytes for (rx,ry,rz,tx,ty,tz)

            # File size - Getting the length of the complete block, for further calculations
            anm_stat = os.path.getsize(animation_file)
            block_size = anm_stat - 16

            # Correlativity Objects/NumberFrames/Blocks
            coincidence = (block_size / length_each_block)

            if int(coincidence * 2) == anm_frames:
                print("Exist correlativity between Animation Frames and Blocks")
            else:
                print("There are no correlativity between Animation Frames and Blocks, Report this as Frame/Block not equal")
                exit()
            
            keyframes_blocks_bytes = [] # HERE I GOT THE KEYFRAMES THAT REPRESENTS ALL THE BLOCKS SPLIT
            block_s = block_size
            s_block = 0
            e_block = length_each_block
            while block_s > 0:
                anm_split_data = anm_complete_block[s_block:e_block]
                keyframes_blocks_bytes.append(anm_split_data)
                s_block += length_each_block
                e_block += length_each_block
                block_s -= length_each_block
            
            global keyframe_obj_block
            keyframe_obj_block = [] # HERE I GOT THE KEYFRAMES BLOCK SPLIT
            for obj_unique in keyframes_blocks_bytes:
                obj_keyframe = []
                len_obj_u = len(obj_unique)
                s_obj = 0
                e_obj = 12
                while len_obj_u > 0:
                    k_objunique = obj_unique[s_obj:e_obj]
                    obj_keyframe.append(k_objunique)
                    s_obj += 12
                    e_obj += 12
                    len_obj_u -=12
                keyframe_obj_block.append(obj_keyframe)
        
    def compare_data(self): # HERE I COMPARE IF OBJ DATA IN TMD AND IN SAF FILE ARE EQUAL, IF NOT AN ERROR IS RAISED AND THE SOFTWARE TERMINATED
        try:
            if anm_objs == standard_tmd.tmd_nobj_expected:
                print("Objects from TMD file and Scripted Animation File are equal, so the processing will continue")
            else:
                print("TMD file and Scripted Animation file are different, exiting")
                exit()
        except OSError:
            print("No Data input")
    
    def convert_data(self):
        keyframes_converted = [] # HERE I GET THE KEYFRAMES CONVERTED FROM BYTES TO SIGNED INTS

        internal_keyframe_count = 0
        for keyf_byte in keyframe_obj_block:
            obj_number = 0
            single_obj_transformations = []
            for keyfb in keyf_byte: # Surely need to change the values to / 1000
                object_rot_trans = {"Rx": float(int(str(struct.unpack('<h', keyfb[0:2])).replace("(", "").replace(")", "").replace(",", "")) / round((4096/360), 12)),
                "Ry": float(int(str(struct.unpack('<h', keyfb[2:4])).replace("(", "").replace(")", "").replace(",", ""))/ round((4096/360), 12)),
                "Rz": float(int(str(struct.unpack('<h', keyfb[4:6])).replace("(", "").replace(")", "").replace(",", ""))/ round((4096/360), 12)), 
                "Tx": float(int(str(struct.unpack('<h', keyfb[6:8])).replace("(", "").replace(")", "").replace(",", "")) / 1000), 
                "Ty": float(int(str(struct.unpack('<h', keyfb[8:10])).replace("(", "").replace(")", "").replace(",", "")) / 1000), 
                "Tz": float(int(str(struct.unpack('<h', keyfb[10:12])).replace("(", "").replace(")", "").replace(",", "")) / 1000)}

                
                single_obj_transformations.append(object_rot_trans)

                obj_number += 1
            obj_transformations = list(enumerate(single_obj_transformations))
            keyframes_converted.append(obj_transformations)

            internal_keyframe_count += 1
        global keyframes_converted_enum 
        keyframes_converted_enum = list(enumerate(keyframes_converted)) # HERE I GET THE CORRECT NESTING USING THE KEYFRAME ENUMERATED
        print("Conversion of Keyframes successful")


class CmbFileReader:
    def __init__(self, cmb_bool=bool, cmb_anim=bytes, tmd_file_b=bool, ctmd_file_b=bool):
        self.self = CmbFileReader
        self.cmb_bool = cmb_bool
        self.cmb_anim = cmb_anim
        self.tmd_file_b = tmd_file_b
        self.ctmd_file_b = ctmd_file_b

    def cmb_decoder(self, cmb_bool, cmb_anim, tmd_file_b, ctmd_file_b):
        if cmb_bool == True:
            print(f'PROCESSING CMB FILE')
            global ctmd_anm_objs
            global ctmd_anm_frames
            read_header = cmb_anim[0:16]
            head_anmfile = read_header[12:] # ANIMATION HEADER, WHICH INCLUDE NOBJ AND TOTAL FRAMES?
            ctmd_anm_objs = int.from_bytes(head_anmfile[0:2], byteorder='little', signed=False)
            ctmd_anm_frames = int.from_bytes(head_anmfile[2:4], byteorder='little', signed=False)
            header_str = f'This Animation file contains {ctmd_anm_objs} Objects and {ctmd_anm_frames} Frames'
            print(header_str)
            cmb_data = cmb_anim[16:]

            # This is only done if the quantity of Objects from the tool is different to the Expected number of objects
            if ctmd_file_b == True:
                try:
                    if (ctmd_anm_objs == custom_tmd.ctmd_nobj_expected):
                        print("Objects from CTMD file and CMB Animation File are equal, so the processing will continue")
                    else:
                        print("TMD file and Scripted Animation file are different, exiting")
                        exit()
                except OSError:
                    print("No Data input")
            elif tmd_file_b == True:
                try:
                    if (ctmd_anm_objs == standard_tmd.tmd_nobj_expected):
                        print("Objects from CTMD file and CMB Animation File are equal, so the processing will continue")
                    else:
                        print("TMD file and Scripted Animation file are different, exiting")
                        exit()
                except OSError:
                    print("No Data input")
            else:
                print(f'Invalid 3D file!, exiting...')
                exit()
            
            # Another check to make sure that the data block is equal to the described in the CMB header
            total_len = len(cmb_anim)
            block_head = int.from_bytes(read_header[8:11], 'little', signed=False)
            if total_len != block_head:
                print(f'FATAL ERROR, Total Length:{total_len} and Block Header: {block_head} are different!!, Exiting')
                exit()
            
            first_animation_block = []
            static_block_len = ctmd_anm_objs * 12
            static_block = cmb_data[0:static_block_len]
            
            static_value = static_block_len
            s_static = 0
            e_static = 12
            while static_value > 0:
                static_extract = static_block[s_static:e_static]
                first_animation_block.append(static_extract)
                s_static += 12
                e_static += 12
                static_value -= 12
            
            static_rot_trans_cmb = [] # HERE I GET THE KEYFRAMES CONVERTED FROM BYTES TO SIGNED INTS

            object_number_cmb = 0
            for cmb_static in first_animation_block:
                rottrans_static_dict = {"Rx": float(int.from_bytes(cmb_static[0:2], 'little', signed=True) / round((4096/360), 12)),
                        "Ry": float(int.from_bytes(cmb_static[2:4], 'little', signed=True) / round((4096/360), 12)),
                        "Rz": float(int.from_bytes(cmb_static[4:6], 'little', signed=True) / round((4096/360), 12)), 
                        "Tx": float(int.from_bytes(cmb_static[6:8], 'little', signed=True) / 1000), 
                        "Ty": float(int.from_bytes(cmb_static[8:10], 'little', signed=True) / 1000), 
                        "Tz": float(int.from_bytes(cmb_static[10:12], 'little', signed=True) / 1000)}
                rot_trans_static = object_number_cmb, rottrans_static_dict
                static_rot_trans_cmb.append(rot_trans_static)
                object_number_cmb += 1

            subtransform_block = cmb_data[static_block_len:]
            each_block_size = ctmd_anm_objs * 8
            subtransform_animation = []
            s_subanm = 0
            e_subanm = each_block_size
            length_sub_anm = len(subtransform_block)
            while length_sub_anm > 0:
                sub_extract = subtransform_block[s_subanm:e_subanm]
                subtransform_animation.append(sub_extract)
                s_subanm += each_block_size
                e_subanm += each_block_size
                length_sub_anm -= each_block_size
            
            cmb_anm_block = []
            for unique_subtransform_obj in subtransform_animation:
                obj_sub_keyframe = []
                len_obj_uni = len(unique_subtransform_obj)
                s_unkey = 0
                e_unkey = 8
                while len_obj_uni > 0:
                    u_key_get = unique_subtransform_obj[s_unkey:e_unkey]
                    obj_sub_keyframe.append(u_key_get)
                    s_unkey += 8
                    e_unkey += 8
                    len_obj_uni -= 8
                cmb_anm_block.append(obj_sub_keyframe)

            cmb_keyframes_converted = []
            internal_keyframe_count = 0
            length_init = len(cmb_anm_block) + 1
            for current_frame in range(0, length_init):
                number_obj = 0
                if internal_keyframe_count == 0:
                    ctmd_first_anm = []
                    for static_anm_1st in static_rot_trans_cmb:
                        change_a_little = static_anm_1st[1]
                        ctmd_first_anm.append(change_a_little)
                    cmb_keyframes_converted.append(ctmd_first_anm)
                else:
                    ctmd_obj_transformations = []
                    next_sum = []
                    for keyfb_cmb in cmb_anm_block[current_frame - 1]:
                        # GETTING STATIC VALUES
                        sum_static_val = static_rot_trans_cmb[number_obj]
                        non_enum_static_value = sum_static_val[1]
                        
                        static_value_rotx = non_enum_static_value.get("Rx")
                        static_value_roty = non_enum_static_value.get("Ry")
                        static_value_rotz = non_enum_static_value.get("Rz")
                        static_value_transx = non_enum_static_value.get("Tx")
                        static_value_transy = non_enum_static_value.get("Ty")
                        static_value_transz = non_enum_static_value.get("Tz")

                        # GETTING THE ACTIVE VALUES
                        rot_scalar_uint = int.from_bytes(keyfb_cmb[0:1], 'little', signed=True)
                        trans_scalar_uint = int.from_bytes(keyfb_cmb[4:5], 'little', signed=True)

                        rot_x_int = int.from_bytes(keyfb_cmb[1:2], 'little', signed=True)
                        rot_y_int = int.from_bytes(keyfb_cmb[2:3], 'little', signed=True)
                        rot_z_int = int.from_bytes(keyfb_cmb[3:4], 'little', signed=True)
                        trans_x_int = int.from_bytes(keyfb_cmb[5:6], 'little', signed=True)
                        trans_y_int = int.from_bytes(keyfb_cmb[6:7], 'little', signed=True)
                        trans_z_int = int.from_bytes(keyfb_cmb[7:8], 'little', signed=True)

                        rot_x_calc = rot_x_int << rot_scalar_uint
                        rot_y_calc = rot_y_int << rot_scalar_uint
                        rot_z_calc = rot_z_int << rot_scalar_uint
                        trans_x_calc = trans_x_int << trans_scalar_uint
                        trans_y_calc = trans_y_int << trans_scalar_uint
                        trans_z_calc = trans_z_int << trans_scalar_uint

                        end_calc_rotx = static_value_rotx + float(rot_x_calc / round((4096/360), 12))
                        end_calc_roty = static_value_roty + float(rot_y_calc / round((4096/360), 12))
                        end_calc_rotz = static_value_rotz + float(rot_z_calc / round((4096/360), 12))
                        end_calc_locx = static_value_transx + float(trans_x_calc / 1000)
                        end_calc_locy = static_value_transy + float(trans_y_calc / 1000)
                        end_calc_locz = static_value_transz + float(trans_z_calc / 1000)

                        #New Static Value
                        non_enum_static_value.update({"Rx": end_calc_rotx})
                        non_enum_static_value.update({"Ry": end_calc_roty})
                        non_enum_static_value.update({"Rz": end_calc_rotz})
                        non_enum_static_value.update({"Tx": end_calc_locx})
                        non_enum_static_value.update({"Ty": end_calc_locy})
                        non_enum_static_value.update({"Tz": end_calc_locz})

                        ctmd_rot_trans = {"Rx": float(end_calc_rotx), "Ry": float(end_calc_roty), "Rz": float(end_calc_rotz), "Tx": float(end_calc_locx), "Ty": float(end_calc_locy), "Tz": float(end_calc_locz)}
                        ctmd_obj_transformations.append(ctmd_rot_trans)
                        next_sum.append(ctmd_rot_trans)
                        number_obj += 1
                    cmb_keyframes_converted.append(ctmd_obj_transformations)
                internal_keyframe_count += 1
            
            enumerating_keyframe_final = []
            for enumerating in cmb_keyframes_converted:
                enumerating_keyframe_obj = []
                for enum in enumerating:
                    enum_inside = enum
                    enumerating_keyframe_obj.append(enum_inside)
                getting_enum = list(enumerate(enumerating_keyframe_obj))
                enumerating_keyframe_final.append(getting_enum)
            global ctmd_keyframes_converted_enum 
            ctmd_keyframes_converted_enum = list(enumerate(enumerating_keyframe_final)) # HERE I GET THE CORRECT NESTING USING THE KEYFRAME ENUMERATED
            print("Conversion of Keyframes successful")
        else:
            print(f'FATAL ERROR, CMB DECODER BOOL ERROR, EXITING')
            exit()

    def check_cmb_file(self):
        print(f'Please Enter the full path for the CMB file...')
        cmb_input = input()
        with open(cmb_input, 'rb') as cmb_file:
            cmb_read_file = cmb_file.read()
            cmb_search_header = cmb_read_file.find(custom_tmd.CMB_HEADER)
            if cmb_search_header > -1:
                cmb_file.seek(cmb_search_header)
                cmb_anim_binary = cmb_file.read()
                custom_tmd.ctmd_nobj_expected = standard_tmd.tmd_nobj_expected
                print(cmb_anim_binary[0:16], custom_tmd.ctmd_nobj_expected)
                cmb_decode_this = CmbFileReader.cmb_decoder(CmbFileReader.cmb_decoder, cmb_bool=True, cmb_anim=cmb_anim_binary)

class LmbFileReader:
    def __init__(self, lmb_bool=bool, lmb_anim=bytes):
        self.self = LmbFileReader
        self.lmb_bool = lmb_bool
        self.lmb_anim = lmb_anim
            
    def read_lmb_external(self):
        print(f'Write the complete path to the LMB file')
        lmb_input = input()
        print(f'reading an external LMB Header')
        with open(lmb_input, 'rb') as lmb_file:
            lmb_all_file = lmb_file.read()
            lmb_type = lmb_all_file[4:8]
            lmb_type_int = int.from_bytes(lmb_type, 'little', signed=False)
            lmb_header_find = lmb_all_file.find(custom_tmd.LMB_HEADER_0)
            print(lmb_header_find, lmb_type)

            if (lmb_type_int == 0) and (lmb_header_find != -1):
                print(f'LMB Type {lmb_type_int}')
            elif (lmb_type_int == 1) and (lmb_header_find != -1):
                print(f'LMB Type {lmb_type_int}')
            elif (lmb_type_int == 2) and (lmb_header_find != -1):
                print(f'LMB Type {lmb_type_int}')
                lmb_anim_data = lmb_all_file[lmb_header_find:]
                LmbFileReader.lmb_type_2_decoder(lmb_data=lmb_anim_data)
            else:
                print(f'Not an LMB file, exiting the tool...')
                exit()



    def lmb_type_0(self, lmb0_bool, lmb_anim):
        if lmb0_bool == True:
            print("PROCESSING LMB FILE TYPE 0")
            global ctmd_anm_objs
            read_header = lmb_anim[4:8]
            ctmd_anm_objs = int.from_bytes(read_header, byteorder='little', signed=False)
            ctmd_lmb_table_calc = (ctmd_anm_objs * 12) + 8 # Here i get the total table length
            lmb_table = lmb_anim[8:ctmd_lmb_table_calc] # Here i get the table
            lmb_table_len = len(lmb_table)
            ctmd_anm_frames_sub = int(lmb_table_len / 12)
            header_str = f'This Animation file contains {ctmd_anm_objs} Objects and {ctmd_anm_frames_sub} Frames'
            print(header_str)
            lmb_data = lmb_anim[ctmd_lmb_table_calc:]
            
            count_objs = int.from_bytes(read_header, byteorder='little', signed=False)
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

                global lmb_joined_data_trans
                lmb_joined_data_trans = [] # HERE I JOIN THE DATA FOR EACH TRANSFORM BY OBJECT
                next_value = 0
                for current_transform in range(0, number_transform_fix):
                    obj_count = ctmd_anm_objs
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
                print(next_value)
            else:
                print(f'different number in the transformations: {transform_count_check}')
                exit()
            
            if len(lmb_joined_data_trans) != 0:
                global ctmd_anm_frames
                ctmd_anm_frames = len(lmb_joined_data_trans)

                enumerating_keyframe_final = []
                for lmb_transform in lmb_joined_data_trans:
                    lmb_object_inside = []
                    object_numer = 0
                    for object_lmb in lmb_transform:
                        lmb_in_obj = {"Sx": object_lmb[0:2], "Sy": object_lmb[2:4], "Sz": object_lmb[4:6],
                        "Tx": float(int.from_bytes(object_lmb[6:8], 'little', signed=True) / 1000), 
                        "Ty": float(int.from_bytes(object_lmb[8:10], 'little', signed=True) / 1000), 
                        "Tz": float(int.from_bytes(object_lmb[10:12], 'little', signed=True) / 1000),
                        "Rx": float(int.from_bytes(object_lmb[12:14], 'little', signed=True) / round((4096/360), 12)),
                        "Ry": float(int.from_bytes(object_lmb[14:16], 'little', signed=True) / round((4096/360), 12)),
                        "Rz": float(int.from_bytes(object_lmb[16:18], 'little', signed=True) / round((4096/360), 12)), "PadLmb": object_lmb[18:20]}
                        lmb_object_inside.append(lmb_in_obj)
                        object_numer += 1
                    lmb_obj_enum = list(enumerate(lmb_object_inside))
                    enumerating_keyframe_final.append(lmb_obj_enum)
                global ctmd_keyframes_converted_enum 
                ctmd_keyframes_converted_enum = list(enumerate(enumerating_keyframe_final)) # HERE I GET THE CORRECT NESTING USING THE KEYFRAME ENUMERATED
                print("Conversion of Keyframes successful")
            
            else:
                print("Fatal Error - No LMB data found")