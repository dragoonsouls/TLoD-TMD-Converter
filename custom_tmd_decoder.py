"""

Custom TMD Decoder: This module decode the data from Vertex, Normal and Primitive
into integers for easy read/write for the Collada Writer.
This module has to be very flexible and easy to update

also it will be too experimental and almost written from scratch so bugs can happen

Copyright (C) 2023 DooMMetaL

"""

import numpy as np
from typing import Final

#########################
#### PRIMITIVE TYPES ####
#########################
# HERE I WILL WRITE THE PRIMITIVE PACKET TYPES FOUND IN THE RESEARCH
global prim_type_00
global prim_type_01
global prim_type_02
global prim_type_03
global prim_type_04
global prim_type_05
global prim_type_06
global prim_type_07
global prim_type_08
global prim_type_09
global prim_type_10
global prim_type_11
global prim_type_12
global prim_type_13

prim_type_00 = b'\x00\x0c\x30' # LSC_3V_GOURAUD_GRADATION_TEXTURED_TRANSLUCENT
prim_type_01 = b'\x00\x0c\x32' # LSC_3V_GOURAUD_GRADATION_SINGLE_FACED
prim_type_02 = b'\x00\x08\x34' # LSC_3V_GOURAUD_FLAT_TEXTURED_SINGLE_FACE
prim_type_03 = b'\x00\x09\x37' # NLSC_3V_FLAT_TEXTURED_SINGLE_FACED
prim_type_04 = b'\x00\x0c\x38' # LSC_4V_GOURAUD_GRADATION_SOLID_SINGLE_FACE_NO_TEXTURED
prim_type_05 = b'\x00\x0c\x3a' # LSC_4V_GOURAUD_GRADATION_SOLID_NO_TEXTURED_SINGLE_FACED
prim_type_06 = b'\x00\x08\x3c' # LSC_4V_GOURAUD_FLAT_TEXTURED_SINGLE_FACED
prim_type_07 = b'\x00\x09\x3d' # NLSC_4V_GOURAUD_FLAT_SOLID_SINGLE_FACED
prim_type_08 = b'\x00\x09\x3f' # NLSC_4V_GOURAUD_FLAT_TEXTURED_TRANSLUCENT_SINGLE_FACED
prim_type_09 = b'\x00\x08\x38' # LSC_4V_GOURAUD_SOLID_FLAT_NO_TEXTURED_SINGLE_FACED
prim_type_10 = b'\x00\x08\x30' # LSC_3V_GOURAUD_SOLID_NO_TEXTURED_SINGLE_FACED
prim_type_11 = b'\x00\x08\x3e' # LSC_4V_GOURAUD_TRANSLUCENT_SINGLE_FACE_TEXTURED
prim_type_12 = b'\x00\x08\x3a' # LSC_4V_GOURAUD_FLAT_SEMITRANSPARENT_NO_TEXTURED
prim_type_13 = b'\x00\x09\x35' # NLSC_3V_FLAT_TEXTURED_SINGLE_FACED recently found in Dart Flameshot |||| RESEARCH MORE ABOUT THIS ONE


################################
#### CUSTOM TMD INTERPRETER #### |||| THIS MODULE INTERPRET NORMAL/PRIMITIVE DATA TO WRITE READABLE PACKETS FOR THE COLLADA WRITER
################################

class CustomTmdNormal:
    def __init__(self, nobj_expected, normal_obj_int, normal_block_byte):
        self.self = CustomTmdNormal
        self.normal_decoder(nobj_expected=nobj_expected, normal_obj_int=normal_obj_int, normal_block_byte=normal_block_byte)

    def normal_decoder(self, nobj_expected=int, normal_obj_int=int, normal_block_byte=list):
        normal_decoded = []

        normal_to_decode = normal_block_byte # BLOCK BYTES OF VERTEX FOR EACH OBJECT
        normal_quantity = normal_obj_int # QUANTITY OF VERTEX IN EACH OBJECT
        number_of_objects = nobj_expected # TOTAL NUMBER OF OBJECTS IN THE CTMD

        for normal_actual in range(0, number_of_objects):
            # NORMALS SEEMS TO BE PROCESSED ONE IN A TIME
            split_blocks_n = normal_to_decode[normal_actual]

            split_block_count_n = normal_quantity[normal_actual]
            n_start_b = 0
            n_end_b = 4
            norm_split_4b = []
            while split_block_count_n > 0:
                split_it_n = split_blocks_n[n_start_b:n_end_b]
                norm_split_4b.append(split_it_n)
                split_block_count_n -= 1
                n_start_b += 4
                n_end_b += 4

            norm_in_obj = []
            for normal_dec in norm_split_4b:
                norm_x = np.short((normal_dec[0] << 20 ) >> 19 & 0xfffffff8)
                norm_y = np.short((normal_dec[1] << 10) >> 19 & 0xfffffff8)
                norm_z = np.short(normal_dec[0] >> 19 & 0xfffffff8)
                normal_values = [norm_x, norm_y, norm_z]
                norm_in_obj.append(normal_values)
            normal_decoded.append(norm_in_obj)
        
        return normal_decoded


#########################################
#### CUSTOM TMD DEPACKER/INTERPRETER ####
#########################################

class CustomTmdPrimitive:
    def __init__(self, nobj_model, primitive_number, primitive_block, tmd_attribute):
        self.self = CustomTmdPrimitive
        self.cprimitive_types_depacker(object_num=nobj_model, prim_num=primitive_number, prim_block_byte=primitive_block, tmd_attribute=tmd_attribute)
        
    def cprimitive_types_depacker(self, object_num=int, prim_num=int, prim_block_byte=list, tmd_attribute=int): # THIS IS A SECTION FOR CALCULATE THE QUANTITY OF PRIMITIVES PACKETS IN EACH PRIMITIVE BLOCK

        block_obj_primitives = prim_block_byte # Complete block of Primtives
        num_of_prim_in_obj = prim_num # Number of Primitives in each object
        num_obj_ctmd = object_num # Total number of Objects in the CTMD
        total_original_primitives = sum(num_of_prim_in_obj)

        processed_prim_block = [] # CTMD CONVERTED BUT IN HEX

        for p_block_num in range(0, num_obj_ctmd): # HERE I LOOP IN THE NUMBER OF OBJECT AND PRIMITIVE BLOCK
            if tmd_attribute == 1:
                attribute_hex = 0x1400_0040
            elif tmd_attribute == 2:
                attribute_hex = 0x1400_0000
            elif tmd_attribute == 3:
                attribute_hex = 0x5400_0000
            elif tmd_attribute == 4:
                attribute_hex = 0x5000_0000
            elif tmd_attribute == 5:
                attribute_hex = 0x6400_0040
            else:
                attribute_hex = 0x1400_0040
            
            if (attribute_hex & 0x4000_0000) == 0:
                mode_prim_single = 0x00
            else:
                mode_prim_single = 0x12

            #### STRUCT50 or Depack Struct ###
            global parameters_for_depack
            global depacked_elements
            parameters_for_depack = {"_00": 0, "_04": 0, "_08": 0, "_0c": 0} # CURRENT PARAMETERS FOR DEPACK IN THE PRIMTIVE == a3._00//_0c
            depacked_elements = {} # CURRENT ELEMENTS (DATA) IN THE PRIMITIVE == a3._10 |||| in this 32 slots Dict i hold all the data from depacking in the current primitive
            total_length_depack = 32
            for i in range(0, total_length_depack): # Filling with 0 the dictionary
                depacked_elements[f'{i}'] = 0
            ### END of STRUCT50 ###

            num_packet_prim = block_obj_primitives[p_block_num] # CURRENT BLOCK OF PRIMITIVES IN THE OBJECT
            num_prims = num_of_prim_in_obj[p_block_num]
            obj_prim_processed = []
            total_prims_in_obj = num_of_prim_in_obj[p_block_num]
            parameters_for_depack.update({"_00": 0})

            # This will iter into the numbers of primitives, if the number is not reach it will continue in the next iter
            global current_prim_slice
            current_prim_slice = 0
            while num_prims != 0:
                print(f'////////========PRIMITIVE PROCESSING========\\\\\\\\')
                print(f'============|||Object Number: {p_block_num}|||============')
                print(f'NUMBER OF PRIMITIVES LEFT: {num_prims}')
                print(f'Length of Primitive Block {len(num_packet_prim)}, Current Slice: {current_prim_slice}')

                parameters_for_depack.update({"_0c": 0})
                parameters_for_depack.update({"_08": 0})
                value_04_update = parameters_for_depack.get("_00")
                parameters_for_depack.update({"_04": value_04_update})
                
                type_len = int.from_bytes(num_packet_prim[current_prim_slice: (current_prim_slice + 2)], 'little', signed=False)
                type_command = int.from_bytes(num_packet_prim[current_prim_slice: (current_prim_slice + 4)], 'little', signed=False)

                new_prim_command_single = np.right_shift(type_command, 24) & 0x3e | mode_prim_single
                index_render_single = np.right_shift(type_command, 14) & 0x20 | np.right_shift(type_command, 24) & 0xf | np.right_shift(type_command, 18) & 0x1 | mode_prim_single
                print(f'New Primitive Command: {new_prim_command_single}, Index of Renderer: {index_render_single},\nTotal Primitives in Block: {total_prims_in_obj}, Current Primitives Processed: {type_len}')
                print(num_packet_prim[current_prim_slice: (current_prim_slice + 4)])
                
                not_possible_render = [16, 17, 20, 21, 24, 25, 28, 29, 48, 49, 52, 53, 56, 57, 60, 61]
                classic_renders = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 18, 19, 22, 23, 26, 27, 30, 31]
                new_slice = 0

                if index_render_single in not_possible_render:
                    print(f'Index Render Number: {index_render_single} is not a possible value')
                    exit()
                elif index_render_single in classic_renders:
                    print(f'THIS CTMD USE CLASSIC PRIMITIVES RENDERS????!!!: {index_render_single}') # THIS IS WEIRD, SINCE I NEVER FOUND ONE
                    break
                
                # From this point to onwards all had unpackers
                elif (index_render_single == 32) or (index_render_single == 34) or (index_render_single == 50):
                    print(f'Renderer 13 Single Block, need to be unpacked')
                    num_packet_prim_new = num_packet_prim[current_prim_slice + 4:]
                    for number_prim in range(0, type_len):
                        primitive_last = num_packet_prim_new[new_slice:]
                        primitive_13, sliced = PrimitiveDepacker.custom_primitives_depacker(unpacked_length=16, custom_primitive_packet=primitive_last)
                        prim_header_13_single = f'render_13'
                        render_13_single = prim_header_13_single, primitive_13
                        obj_prim_processed.append(render_13_single)
                        new_slice += sliced
                    print("Depacking Succesfully")
                    
                elif (index_render_single == 33) or (index_render_single == 35) or (index_render_single == 51):
                    print(f'Renderer 14 Single Block, need to be unpacked')
                    num_packet_prim_new = num_packet_prim[current_prim_slice + 4:]
                    for number_prim in range(0, type_len):
                        primitive_last = num_packet_prim_new[new_slice:]
                        primitive_14, sliced = PrimitiveDepacker.custom_primitives_depacker(unpacked_length=24, custom_primitive_packet=primitive_last)
                        prim_header_14_single = f'render_14'
                        render_14_single = prim_header_14_single, primitive_14
                        obj_prim_processed.append(render_14_single)
                        new_slice += sliced
                    print("Depacking Succesfully")

                elif (index_render_single == 36) or (index_render_single == 38):
                    print(f'Renderer 15 Single Block, need to be unpacked')
                    num_packet_prim_new = num_packet_prim[current_prim_slice + 4:]
                    for number_prim in range(0, type_len):
                        primitive_last = num_packet_prim_new[new_slice:]
                        primitive_15, sliced = PrimitiveDepacker.custom_primitives_depacker(unpacked_length=24, custom_primitive_packet=primitive_last)
                        prim_header_15_single = f'render_15'
                        render_15_single = prim_header_15_single, primitive_15
                        obj_prim_processed.append(render_15_single)
                        new_slice += sliced
                    print("Depacking Succesfully")

                elif (index_render_single == 37) or (index_render_single == 39):
                    print(f'Renderer 16 Single Block, need to be unpacked')
                    num_packet_prim_new = num_packet_prim[current_prim_slice + 4:]
                    for number_prim in range(0, type_len):
                        primitive_last = num_packet_prim_new[new_slice:]
                        primitive_16, sliced = PrimitiveDepacker.custom_primitives_depacker(unpacked_length=32, custom_primitive_packet=primitive_last)
                        prim_header_16_single = f'render_16'
                        render_16_single = prim_header_16_single, primitive_16
                        obj_prim_processed.append(render_16_single)
                        new_slice += sliced
                    print("Depacking Succesfully")

                elif (index_render_single == 40) or (index_render_single == 42) or (index_render_single == 58):
                    print(f'Renderer 17 Single Block, need to be unpacked')
                    num_packet_prim_new = num_packet_prim[current_prim_slice + 4:]
                    for number_prim in range(0, type_len):
                        primitive_last = num_packet_prim_new[new_slice:]
                        primitive_17, sliced = PrimitiveDepacker.custom_primitives_depacker(unpacked_length=20, custom_primitive_packet=primitive_last)
                        prim_header_17_single = f'render_17'
                        render_17_single = prim_header_17_single, primitive_17
                        obj_prim_processed.append(render_17_single)
                        new_slice += sliced
                    print("Depacking Succesfully")

                elif (index_render_single == 41) or (index_render_single == 43) or (index_render_single == 59):
                    print(f'Renderer 18 Single Block, need to be unpacked')
                    num_packet_prim_new = num_packet_prim[current_prim_slice + 4:]
                    for number_prim in range(0, type_len):
                        primitive_last = num_packet_prim_new[new_slice:]
                        primitive_18, sliced = PrimitiveDepacker.custom_primitives_depacker(unpacked_length=32, custom_primitive_packet=primitive_last)
                        prim_header_18_single = f'render_18'
                        render_18_single = prim_header_18_single, primitive_18
                        obj_prim_processed.append(render_18_single)
                        new_slice += sliced
                    print("Depacking Succesfully")

                elif (index_render_single == 44) or (index_render_single == 46):
                    print(f'Renderer 19 Single Block, need to be unpacked')
                    num_packet_prim_new = num_packet_prim[current_prim_slice + 4:]
                    for number_prim in range(0, type_len):
                        primitive_last = num_packet_prim_new[new_slice:]
                        primitive_19, sliced = PrimitiveDepacker.custom_primitives_depacker(unpacked_length=32, custom_primitive_packet=primitive_last)
                        prim_header_19_single = f'render_19'
                        render_19_single = prim_header_19_single, primitive_19
                        obj_prim_processed.append(render_19_single)
                        new_slice += sliced
                    print("Depacking Succesfully")

                elif (index_render_single == 45) or (index_render_single == 47):
                    print(f'Renderer 20 Single Block, need to be unpacked')
                    num_packet_prim_new = num_packet_prim[current_prim_slice + 4:]
                    for number_prim in range(0, type_len):
                        primitive_last = num_packet_prim_new[new_slice:]
                        primitive_20, sliced = PrimitiveDepacker.custom_primitives_depacker(unpacked_length=40, custom_primitive_packet=primitive_last)
                        prim_header_20_single = f'render_20'
                        render_20_single = prim_header_20_single, primitive_20
                        obj_prim_processed.append(render_20_single)
                        new_slice += sliced
                    print("Depacking Succesfully")

                elif (index_render_single == 54):
                    print(f'Renderer 21 Single Block, need to be unpacked')
                    num_packet_prim_new = num_packet_prim[current_prim_slice + 4:]
                    for number_prim in range(0, type_len):
                        primitive_last = num_packet_prim_new[new_slice:]
                        primitive_21, sliced = PrimitiveDepacker.custom_primitives_depacker(unpacked_length=24, custom_primitive_packet=primitive_last)
                        prim_header_21_single = f'render_21'
                        render_21_single = prim_header_21_single, primitive_21
                        obj_prim_processed.append(render_21_single)
                        new_slice += sliced
                    print("Depacking Succesfully")

                elif (index_render_single == 55):
                    print(f'Renderer 22 Single Block, need to be unpacked')
                    num_packet_prim_new = num_packet_prim[current_prim_slice + 4:]
                    for number_prim in range(0, type_len):
                        primitive_last = num_packet_prim_new[new_slice:]
                        primitive_22, sliced = PrimitiveDepacker.custom_primitives_depacker(unpacked_length=32, custom_primitive_packet=primitive_last)
                        prim_header_22_single = f'render_22'
                        render_22_single = prim_header_22_single, primitive_22
                        obj_prim_processed.append(render_22_single)
                        new_slice += sliced
                    print("Depacking Succesfully")

                elif (index_render_single == 62):
                    print(f'Renderer 23 Single Block, need to be unpacked')
                    num_packet_prim_new = num_packet_prim[current_prim_slice + 4:]
                    for number_prim in range(0, type_len):
                        primitive_last = num_packet_prim_new[new_slice:]
                        primitive_23, sliced = PrimitiveDepacker.custom_primitives_depacker(unpacked_length=32, custom_primitive_packet=primitive_last)
                        prim_header_23_single = f'render_23'
                        render_23_single = prim_header_23_single, primitive_23
                        obj_prim_processed.append(render_23_single)
                        new_slice += sliced
                    print("Depacking Succesfully")

                elif (index_render_single == 63):
                    print(f'Renderer 24 Single Block, need to be unpacked')
                    num_packet_prim_new = num_packet_prim[current_prim_slice + 4:]
                    for number_prim in range(0, type_len):
                        primitive_last = num_packet_prim_new[new_slice:]
                        primitive_24, sliced = PrimitiveDepacker.custom_primitives_depacker(unpacked_length=40, custom_primitive_packet=primitive_last)
                        prim_header_24_single = f'render_24'
                        render_24_single = prim_header_24_single, primitive_24
                        obj_prim_processed.append(render_24_single)
                        new_slice += sliced
                    print("Depacking Succesfully")

                else:
                    print(f'Index Render Number: {index_render_single} do not exist!!, exiting the Tool...')
                    exit()

                adjusted_slice_00 = new_slice + 0x3
                adjusted_slice_01 = adjusted_slice_00 & 0xffff_fffc
                adjusted_slice_last = adjusted_slice_01 + 4
                num_prims -= type_len
                current_prim_slice += adjusted_slice_last
            
            processed_prim_block.append(obj_prim_processed)
            parameters_for_depack.update({"_00": 0})
            parameters_for_depack.update({"_04": 0})
            parameters_for_depack.update({"_08": 0})
            parameters_for_depack.update({"_0c": 0})
            depacked_elements = {} # CURRENT ELEMENTS (DATA) IN THE PRIMITIVE == a3._10 |||| in this 32 slots Dict i hold all the data from depacking in the current primitive
            total_length_depack = 32
            for i in range(0, total_length_depack): # Filling with 0 the dictionary
                depacked_elements[f'{i}'] = 0

        print(f'ALL PRIMITIVES WERE UNPACKED\n')

        global primitive_block_dict
        primitive_block_dict = [] # CTMD CONVERTED INTO READABLE FORM

        prim_dec_block_num = 0
        for prim_dec_block in processed_prim_block:
            prim_block_inner_obj = []
            for prim_d_b in prim_dec_block:
                if (prim_d_b[0] == 0) or (len(prim_d_b[1]) == 0):
                    print(f'None Primitive Unpacked {prim_d_b}, Primitive Number: {prim_dec_block_num}')
                    print(f'Exiting...')
                    exit()
                
                elif prim_d_b[0] == f'render_13':
                    byte_array = b''.join(prim_d_b[1])
                    lsc3vntgs = {"lsc3vntgs":b'\x06\x04\x00\x30', 
                            "r0":int.from_bytes(byte_array[0:1], byteorder='little', signed=False), "g0":int.from_bytes(byte_array[1:2], byteorder='little', signed=False), "b0":int.from_bytes(byte_array[2:3], byteorder='little', signed=False), "pad0":int.from_bytes(byte_array[3:4], byteorder='little', signed=False), 
                            "normal0":int.from_bytes(byte_array[4:6], byteorder='little', signed=False), "vertex0":int.from_bytes(byte_array[6:8], byteorder='little', signed=False), 
                            "normal1":int.from_bytes(byte_array[8:10], byteorder='little', signed=False), "vertex1":int.from_bytes(byte_array[10:12], byteorder='little', signed=False), 
                            "normal2":int.from_bytes(byte_array[12:14], byteorder='little', signed=False), "vertex2":int.from_bytes(byte_array[14:16], byteorder='little', signed=False)}
                    prim_block_inner_obj.append(lsc3vntgs)

                elif prim_d_b[0] == f'render_14':
                    byte_array = b''.join(prim_d_b[1])
                    lsc3vntgg = {"lsc3vntgg":b'\x06\x06\x04\x30', 
                            "r0":int.from_bytes(byte_array[0:1], byteorder='little', signed=False), "g0":int.from_bytes(byte_array[1:2], byteorder='little', signed=False), "b0":int.from_bytes(byte_array[2:3], byteorder='little', signed=False), "pad0":byte_array[3:4], 
                            "r1":int.from_bytes(byte_array[4:5], byteorder='little', signed=False), "g1":int.from_bytes(byte_array[5:6], byteorder='little', signed=False), "b1":int.from_bytes(byte_array[6:7], byteorder='little', signed=False), "pad1":byte_array[7:8], 
                            "r2":int.from_bytes(byte_array[8:9], byteorder='little', signed=False), "g2":int.from_bytes(byte_array[9:10], byteorder='little', signed=False), "b2":int.from_bytes(byte_array[10:11], byteorder='little', signed=False), "pad2":byte_array[11:12], 
                            "normal0":int.from_bytes(byte_array[12:14], byteorder='little', signed=False), "vertex0":int.from_bytes(byte_array[14:16], byteorder='little', signed=False), 
                            "normal1":int.from_bytes(byte_array[16:18], byteorder='little', signed=False), "vertex1":int.from_bytes(byte_array[18:20], byteorder='little', signed=False), 
                            "normal2":int.from_bytes(byte_array[20:22], byteorder='little', signed=False), "vertex2":int.from_bytes(byte_array[22:24], byteorder='little', signed=False)}
                    prim_block_inner_obj.append(lsc3vntgg)

                elif prim_d_b[0] == f'render_15':
                    byte_array = b''.join(prim_d_b[1])
                    lsc3vgt = {"lsc3vgt":b'\x09\x06\x00\x34', 
                            "u0":(int.from_bytes(byte_array[0:1], byteorder='little', signed=False) / 256), "v0":(int.from_bytes(byte_array[1:2], byteorder='little', signed=False) / 256), "cba":byte_array[2:4], 
                            "u1":(int.from_bytes(byte_array[4:5], byteorder='little', signed=False) / 256), "v1":(int.from_bytes(byte_array[5:6], byteorder='little', signed=False) / 256), "tsb":byte_array[6:8], 
                            "u2":(int.from_bytes(byte_array[8:9], byteorder='little', signed=False) / 256), "v2":(int.from_bytes(byte_array[9:10], byteorder='little', signed=False) / 256), "pad0":byte_array[10:12], 
                            "normal0":int.from_bytes(byte_array[12:14], byteorder='little', signed=False), "vertex0":int.from_bytes(byte_array[14:16], byteorder='little', signed=False), 
                            "normal1":int.from_bytes(byte_array[16:18], byteorder='little', signed=False), "vertex1":int.from_bytes(byte_array[18:20], byteorder='little', signed=False), 
                            "normal2":int.from_bytes(byte_array[20:22], byteorder='little', signed=False), "vertex2":int.from_bytes(byte_array[22:24], byteorder='little', signed=False)}
                    prim_block_inner_obj.append(lsc3vgt)

                elif prim_d_b[0] == f'render_16':
                    byte_array = b''.join(prim_d_b[1])
                    nlsc3vgt = {"nlsc3vgt": b'\x09\x08\x01\x35', 
                        "u0":(int.from_bytes(byte_array[0:1], byteorder='little', signed=False) / 256), "v0":(int.from_bytes(byte_array[1:2], byteorder='little', signed=False) / 256), "cba":byte_array[2:4], 
                        "u1":(int.from_bytes(byte_array[4:5], byteorder='little', signed=False) / 256), "v1":(int.from_bytes(byte_array[5:6], byteorder='little', signed=False) / 256), "tsb":byte_array[6:8], 
                        "u2":(int.from_bytes(byte_array[8:9], byteorder='little', signed=False) / 256), "v2":(int.from_bytes(byte_array[9:10], byteorder='little', signed=False) / 256), "pad0":byte_array[10:12], 
                        "r0":int.from_bytes(byte_array[12:13], byteorder='little', signed=False), "g0":int.from_bytes(byte_array[13:14], byteorder='little', signed=False), "b0":int.from_bytes(byte_array[14:15], byteorder='little', signed=False), "pad1":byte_array[15:16], 
                        "r1":int.from_bytes(byte_array[16:17], byteorder='little', signed=False), "g1":int.from_bytes(byte_array[17:18], byteorder='little', signed=False), "b1":int.from_bytes(byte_array[18:19], byteorder='little', signed=False), "pad2":byte_array[19:20], 
                        "r2":int.from_bytes(byte_array[20:21], byteorder='little', signed=False), "g2":int.from_bytes(byte_array[21:22], byteorder='little', signed=False), "b2":int.from_bytes(byte_array[22:23], byteorder='little', signed=False), "pad3":byte_array[23:24], 
                        "vertex0":int.from_bytes(byte_array[24:26], byteorder='little', signed=False), "vertex1":int.from_bytes(byte_array[26:28], byteorder='little', signed=False), 
                        "vertex2":int.from_bytes(byte_array[28:30], byteorder='little', signed=False), "pad4":byte_array[30:32]}
                    prim_block_inner_obj.append(nlsc3vgt)

                elif prim_d_b[0] == f'render_17':
                    byte_array = b''.join(prim_d_b[1])
                    lsc4vntgs = {"lsc4vntgs": b'\x08\x05\x00\x38', 
                            "r0":int.from_bytes(byte_array[0:1], byteorder='little', signed=False), "g0":int.from_bytes(byte_array[1:2], byteorder='little', signed=False), "b0":int.from_bytes(byte_array[2:3], byteorder='little', signed=False), "pad0":int.from_bytes(byte_array[3:4], byteorder='little', signed=False), 
                            "normal0":int.from_bytes(byte_array[4:6], byteorder='little', signed=False), "vertex0":int.from_bytes(byte_array[6:8], byteorder='little', signed=False), 
                            "normal1":int.from_bytes(byte_array[8:10], byteorder='little', signed=False), "vertex1":int.from_bytes(byte_array[10:12], byteorder='little', signed=False), 
                            "normal2":int.from_bytes(byte_array[12:14], byteorder='little', signed=False), "vertex2":int.from_bytes(byte_array[14:16], byteorder='little', signed=False), 
                            "normal3":int.from_bytes(byte_array[16:18], byteorder='little', signed=False), "vertex3":int.from_bytes(byte_array[18:20], byteorder='little', signed=False)}
                    prim_block_inner_obj.append(lsc4vntgs)

                elif prim_d_b[0] == f'render_18':
                    byte_array = b''.join(prim_d_b[1])
                    lsc4vntgg = {"lsc4vntgg": b'\x08\x08\x04\x38', 
                            "r0":int.from_bytes(byte_array[0:1], byteorder='little', signed=False), "g0":int.from_bytes(byte_array[1:2], byteorder='little', signed=False), "b0":int.from_bytes(byte_array[2:3], byteorder='little', signed=False), "pad0":byte_array[3:4], 
                            "r1":int.from_bytes(byte_array[4:5], byteorder='little', signed=False), "g1":int.from_bytes(byte_array[5:6], byteorder='little', signed=False), "b1":int.from_bytes(byte_array[6:7], byteorder='little', signed=False), "pad1":byte_array[7:8], 
                            "r2":int.from_bytes(byte_array[8:9], byteorder='little', signed=False), "g2":int.from_bytes(byte_array[9:10], byteorder='little', signed=False), "b2":int.from_bytes(byte_array[10:11], byteorder='little', signed=False), "pad2":byte_array[11:12], 
                            "r3":int.from_bytes(byte_array[12:13], byteorder='little', signed=False), "g3":int.from_bytes(byte_array[13:14], byteorder='little', signed=False), "b3":int.from_bytes(byte_array[14:15], byteorder='little', signed=False), "pad3":byte_array[15:16], 
                            "normal0":int.from_bytes(byte_array[16:18], byteorder='little', signed=False), "vertex0":int.from_bytes(byte_array[18:20], byteorder='little', signed=False), 
                            "normal1":int.from_bytes(byte_array[20:22], byteorder='little', signed=False), "vertex1":int.from_bytes(byte_array[22:24], byteorder='little', signed=False), 
                            "normal2":int.from_bytes(byte_array[24:26], byteorder='little', signed=False), "vertex2":int.from_bytes(byte_array[26:28], byteorder='little', signed=False), 
                            "normal3":int.from_bytes(byte_array[28:30], byteorder='little', signed=False), "vertex3":int.from_bytes(byte_array[30:32], byteorder='little', signed=False)}
                    prim_block_inner_obj.append(lsc4vntgg)

                elif prim_d_b[0] == f'render_19':
                    byte_array = b''.join(prim_d_b[1])
                    lsc4vgt = {"lsc4vgt": b'\x0c\x08\x00\x3c', 
                            "u0":(int.from_bytes(byte_array[0:1], byteorder='little', signed=False) / 256), "v0":(int.from_bytes(byte_array[1:2], byteorder='little', signed=False) / 256), "cba":byte_array[2:4], 
                            "u1":(int.from_bytes(byte_array[4:5], byteorder='little', signed=False) / 256), "v1":(int.from_bytes(byte_array[5:6], byteorder='little', signed=False) / 256), "tsb":byte_array[6:8], 
                            "u2":(int.from_bytes(byte_array[8:9], byteorder='little', signed=False) / 256), "v2":(int.from_bytes(byte_array[9:10], byteorder='little', signed=False) / 256), "pad0":byte_array[10:12], 
                            "u3":(int.from_bytes(byte_array[12:13], byteorder='little', signed=False) / 256), "v3":(int.from_bytes(byte_array[13:14], byteorder='little', signed=False) / 256), "pad1":byte_array[14:16], 
                            "normal0":int.from_bytes(byte_array[16:18], byteorder='little', signed=False), "vertex0":int.from_bytes(byte_array[18:20], byteorder='little', signed=False), 
                            "normal1":int.from_bytes(byte_array[20:22], byteorder='little', signed=False), "vertex1":int.from_bytes(byte_array[22:24], byteorder='little', signed=False), 
                            "normal2":int.from_bytes(byte_array[24:26], byteorder='little', signed=False), "vertex2":int.from_bytes(byte_array[26:28], byteorder='little', signed=False), 
                            "normal3":int.from_bytes(byte_array[28:30], byteorder='little', signed=False), "vertex3":int.from_bytes(byte_array[30:32], byteorder='little', signed=False)}
                    prim_block_inner_obj.append(lsc4vgt)
                    
                elif prim_d_b[0] == f'render_20':
                    byte_array = b''.join(prim_d_b[1])
                    nlsc4vgt = {"nlsc4vgt": b'\x0c\x0a\x01\x3d', 
                    "u0":(int.from_bytes(byte_array[0:1], byteorder='little', signed=False) / 256), "v0":(int.from_bytes(byte_array[1:2], byteorder='little', signed=False) / 256), "cba":byte_array[2:4], 
                    "u1":(int.from_bytes(byte_array[4:5], byteorder='little', signed=False) / 256), "v1":(int.from_bytes(byte_array[5:6], byteorder='little', signed=False) / 256), "tsb":byte_array[6:8], 
                    "u2":(int.from_bytes(byte_array[8:9], byteorder='little', signed=False) / 256), "v2":(int.from_bytes(byte_array[9:10], byteorder='little', signed=False) / 256), "pad0":byte_array[10:12], 
                    "u3":(int.from_bytes(byte_array[12:13], byteorder='little', signed=False) / 256), "v3":(int.from_bytes(byte_array[13:14], byteorder='little', signed=False) / 256), "pad1":byte_array[14:16], 
                    "r0":int.from_bytes(byte_array[16:17], byteorder='little', signed=False), "g0":int.from_bytes(byte_array[17:18], byteorder='little', signed=False), "b0":int.from_bytes(byte_array[18:19], byteorder='little', signed=False), "pad2":byte_array[19:20], 
                    "r1":int.from_bytes(byte_array[20:21], byteorder='little', signed=False), "g1":int.from_bytes(byte_array[21:22], byteorder='little', signed=False), "b1":int.from_bytes(byte_array[22:23], byteorder='little', signed=False), "pad3":byte_array[23:24], 
                    "r2":int.from_bytes(byte_array[24:25], byteorder='little', signed=False), "g2":int.from_bytes(byte_array[25:26], byteorder='little', signed=False), "b2":int.from_bytes(byte_array[26:27], byteorder='little', signed=False), "pad4":byte_array[27:28], 
                    "r3":int.from_bytes(byte_array[28:29], byteorder='little', signed=False), "g3":int.from_bytes(byte_array[29:30], byteorder='little', signed=False), "b3":int.from_bytes(byte_array[30:31], byteorder='little', signed=False), "pad5":byte_array[31:32], 
                    "vertex0":int.from_bytes(byte_array[32:34], byteorder='little', signed=False), "vertex1":int.from_bytes(byte_array[34:36], byteorder='little', signed=False), 
                    "vertex2":int.from_bytes(byte_array[36:38], byteorder='little', signed=False), "vertex3":int.from_bytes(byte_array[38:40], byteorder='little', signed=False)}
                    prim_block_inner_obj.append(nlsc4vgt)

                elif prim_d_b[0] == f'render_21':
                    byte_array = b''.join(prim_d_b[1])
                    # THE ONLY DIFFERENCE WITH CLASSIC LSC3VGT IS, IN CTMD RENDERS IS CHECKING FOR SPECIFIC TRANSLUCENCY
                    lsc3vgt_trans = {"lsc3vgt":b'\x09\x06\x00\x34', 
                        "u0":(int.from_bytes(byte_array[0:1], byteorder='little', signed=False) / 256), "v0":(int.from_bytes(byte_array[1:2], byteorder='little', signed=False) / 256), "cba":byte_array[2:4], 
                        "u1":(int.from_bytes(byte_array[4:5], byteorder='little', signed=False) / 256), "v1":(int.from_bytes(byte_array[5:6], byteorder='little', signed=False) / 256), "tsb":byte_array[6:8], 
                        "u2":(int.from_bytes(byte_array[8:9], byteorder='little', signed=False) / 256), "v2":(int.from_bytes(byte_array[9:10], byteorder='little', signed=False) / 256), "pad0":byte_array[10:12], 
                        "normal0":int.from_bytes(byte_array[12:14], byteorder='little', signed=False), "vertex0":int.from_bytes(byte_array[14:16], byteorder='little', signed=False), 
                        "normal1":int.from_bytes(byte_array[16:18], byteorder='little', signed=False), "vertex1":int.from_bytes(byte_array[18:20], byteorder='little', signed=False), 
                        "normal2":int.from_bytes(byte_array[20:22], byteorder='little', signed=False), "vertex2":int.from_bytes(byte_array[22:24], byteorder='little', signed=False)}
                    prim_block_inner_obj.append(lsc3vgt_trans)

                elif prim_d_b[0] == f'render_22':
                    byte_array = b''.join(prim_d_b[1])
                    # THE ONLY DIFFERENCE WITH CLASSIC NLSC3VGT IS, IN CTMD RENDERS IS CHECKING FOR SPECIFIC TRANSLUCENCY
                    nlsc3vgt_trans = {"nlsc3vgt": b'\x09\x08\x01\x35', 
                    "u0":(int.from_bytes(byte_array[0:1], byteorder='little', signed=False) / 256), "v0":(int.from_bytes(byte_array[1:2], byteorder='little', signed=False) / 256), "cba":byte_array[2:4], 
                    "u1":(int.from_bytes(byte_array[4:5], byteorder='little', signed=False) / 256), "v1":(int.from_bytes(byte_array[5:6], byteorder='little', signed=False) / 256), "tsb":byte_array[6:8], 
                    "u2":(int.from_bytes(byte_array[8:9], byteorder='little', signed=False) / 256), "v2":(int.from_bytes(byte_array[9:10], byteorder='little', signed=False) / 256), "pad0":byte_array[10:12], 
                    "r0":int.from_bytes(byte_array[12:13], byteorder='little', signed=False), "g0":int.from_bytes(byte_array[13:14], byteorder='little', signed=False), "b0":int.from_bytes(byte_array[14:15], byteorder='little', signed=False), "pad1":byte_array[15:16], 
                    "r1":int.from_bytes(byte_array[16:17], byteorder='little', signed=False), "g1":int.from_bytes(byte_array[17:18], byteorder='little', signed=False), "b1":int.from_bytes(byte_array[18:19], byteorder='little', signed=False), "pad2":byte_array[19:20], 
                    "r2":int.from_bytes(byte_array[20:21], byteorder='little', signed=False), "g2":int.from_bytes(byte_array[21:22], byteorder='little', signed=False), "b2":int.from_bytes(byte_array[22:23], byteorder='little', signed=False), "pad3":byte_array[23:24], 
                    "vertex0":int.from_bytes(byte_array[24:26], byteorder='little', signed=False), "vertex1":int.from_bytes(byte_array[26:28], byteorder='little', signed=False), 
                    "vertex2":int.from_bytes(byte_array[28:30], byteorder='little', signed=False), "pad4":byte_array[30:32]}
                    prim_block_inner_obj.append(nlsc3vgt_trans)

                elif prim_d_b[0] == f'render_23':
                    byte_array = b''.join(prim_d_b[1])
                    # THE ONLY DIFFERENCE WITH CLASSIC LSC4VGT IS, IN CTMD RENDERS IS CHECKING FOR SPECIFIC TRANSLUCENCY
                    lsc4vgt_trans = {"lsc4vgt": b'\x0c\x08\x00\x3c', 
                        "u0":(int.from_bytes(byte_array[0:1], byteorder='little', signed=False) / 256), "v0":(int.from_bytes(byte_array[1:2], byteorder='little', signed=False) / 256), "cba":byte_array[2:4], 
                        "u1":(int.from_bytes(byte_array[4:5], byteorder='little', signed=False) / 256), "v1":(int.from_bytes(byte_array[5:6], byteorder='little', signed=False) / 256), "tsb":byte_array[6:8], 
                        "u2":(int.from_bytes(byte_array[8:9], byteorder='little', signed=False) / 256), "v2":(int.from_bytes(byte_array[9:10], byteorder='little', signed=False) / 256), "pad0":byte_array[10:12], 
                        "u3":(int.from_bytes(byte_array[12:13], byteorder='little', signed=False) / 256), "v3":(int.from_bytes(byte_array[13:14], byteorder='little', signed=False) / 256), "pad1":byte_array[14:16], 
                        "normal0":int.from_bytes(byte_array[16:18], byteorder='little', signed=False), "vertex0":int.from_bytes(byte_array[18:20], byteorder='little', signed=False), 
                        "normal1":int.from_bytes(byte_array[20:22], byteorder='little', signed=False), "vertex1":int.from_bytes(byte_array[22:24], byteorder='little', signed=False), 
                        "normal2":int.from_bytes(byte_array[24:26], byteorder='little', signed=False), "vertex2":int.from_bytes(byte_array[26:28], byteorder='little', signed=False), 
                        "normal3":int.from_bytes(byte_array[28:30], byteorder='little', signed=False), "vertex3":int.from_bytes(byte_array[30:32], byteorder='little', signed=False)}
                    prim_block_inner_obj.append(lsc4vgt_trans)

                elif prim_d_b[0] == f'render_24':
                    byte_array = b''.join(prim_d_b[1])
                    # THE ONLY DIFFERENCE WITH CLASSIC NLSC4VGT IS, IN CTMD RENDERS IS CHECKING FOR SPECIFIC TRANSLUCENCY
                    nlsc4vgt_trans = {"nlsc4vgt": b'\x0c\x0a\x01\x3d', 
                    "u0":(int.from_bytes(byte_array[0:1], byteorder='little', signed=False) / 256), "v0":(int.from_bytes(byte_array[1:2], byteorder='little', signed=False) / 256), "cba":byte_array[2:4], 
                    "u1":(int.from_bytes(byte_array[4:5], byteorder='little', signed=False) / 256), "v1":(int.from_bytes(byte_array[5:6], byteorder='little', signed=False) / 256), "tsb":byte_array[6:8], 
                    "u2":(int.from_bytes(byte_array[8:9], byteorder='little', signed=False) / 256), "v2":(int.from_bytes(byte_array[9:10], byteorder='little', signed=False) / 256), "pad0":byte_array[10:12], 
                    "u3":(int.from_bytes(byte_array[12:13], byteorder='little', signed=False) / 256), "v3":(int.from_bytes(byte_array[13:14], byteorder='little', signed=False) / 256), "pad1":byte_array[14:16], 
                    "r0":int.from_bytes(byte_array[16:17], byteorder='little', signed=False), "g0":int.from_bytes(byte_array[17:18], byteorder='little', signed=False), "b0":int.from_bytes(byte_array[18:19], byteorder='little', signed=False), "pad2":byte_array[19:20], 
                    "r1":int.from_bytes(byte_array[20:21], byteorder='little', signed=False), "g1":int.from_bytes(byte_array[21:22], byteorder='little', signed=False), "b1":int.from_bytes(byte_array[22:23], byteorder='little', signed=False), "pad3":byte_array[23:24], 
                    "r2":int.from_bytes(byte_array[24:25], byteorder='little', signed=False), "g2":int.from_bytes(byte_array[25:26], byteorder='little', signed=False), "b2":int.from_bytes(byte_array[26:27], byteorder='little', signed=False), "pad4":byte_array[27:28], 
                    "r3":int.from_bytes(byte_array[28:29], byteorder='little', signed=False), "g3":int.from_bytes(byte_array[29:30], byteorder='little', signed=False), "b3":int.from_bytes(byte_array[30:31], byteorder='little', signed=False), "pad5":byte_array[31:32], 
                    "vertex0":int.from_bytes(byte_array[32:34], byteorder='little', signed=False), "vertex1":int.from_bytes(byte_array[34:36], byteorder='little', signed=False), 
                    "vertex2":int.from_bytes(byte_array[36:38], byteorder='little', signed=False), "vertex3":int.from_bytes(byte_array[38:40], byteorder='little', signed=False)}
                    prim_block_inner_obj.append(nlsc4vgt_trans)
                             
            prim_dec_block_num += 1
            primitive_block_dict.append(prim_block_inner_obj)

        # CHECKING IF THE DEPACKED PRIMITIVES ARE EQUAL AS THE TOTAL NUMBER OF PRIMITIVES SAID BY THE FILE
        # IF NOT AN ERROR IS RAISED AND THE TOOL WILL EXIT
        total_objects_last = len(primitive_block_dict)
        total_prims_depacked = []
        for test_total in primitive_block_dict:
            total_prims_depacked.append(len(test_total))
        sum_prims_depacked = sum(total_prims_depacked)
        print(f'Number of Depacked Primitives: {sum_prims_depacked}, Number of Total Primitives: {total_original_primitives}, Total Objects: {total_objects_last}')
        if sum_prims_depacked != total_original_primitives:
            print(f'ERROR - Number of Primitives is not equal, report this bug')
            exit()
        
        primitives_decoded = primitive_block_dict
        return primitives_decoded

class PrimitiveDepacker:
    def __init__(self, unpacked_length, custom_primitive_packet):
        self.self = PrimitiveDepacker
        self.custom_primitives_depacker()        
        self.unpacked_length = unpacked_length
        self.custom_primitive_packet = custom_primitive_packet

    @classmethod
    def custom_primitives_depacker(cls, unpacked_length=int, custom_primitive_packet=bytes): # PRIMITIVE DEPACKER FUNCTION

        packed_data_slice_internal = 0
        custom_primitive_depacked = [] # PROCESSED PRIMITIVES in the Object
        packed_data = custom_primitive_packet # current object primitive packet data
        
        UNPACKED_COUNT: Final = unpacked_length // 2 # type: ignore # little math to get a counter used below
        ###############################
        ##### START OF WHILE LOOP ##### |||| THIS LOOP DECODE THE DATA PACKET
        while parameters_for_depack.get("_0c") < UNPACKED_COUNT:
            if (parameters_for_depack.get("_08") & 0x100) == 0:
                parameter_3_new_value = int.from_bytes(packed_data[packed_data_slice_internal: packed_data_slice_internal + 1], 'little', signed=False) | 0xff00
                parameters_for_depack.update({"_08": parameter_3_new_value})
                packed_data_slice_internal += 1
                #print(parameters_for_depack)

            if (parameters_for_depack.get("_08") & 0x1) != 0:
                index_pack_it = parameters_for_depack.get("_00")
                val_byte_00 = int.from_bytes(packed_data[packed_data_slice_internal: packed_data_slice_internal + 1], 'little', signed=False)
                val_byte_01 = int.from_bytes(packed_data[packed_data_slice_internal + 1: packed_data_slice_internal + 2], 'little', signed=False) << 8
                val_ushort = val_byte_01 | val_byte_00 # Building a U_SHORT
                depacked_elements.update({f'{index_pack_it}': val_ushort}) # Setting the previous SHORT in the Depacked Elements using the _00 as place parameter
                first_value_changed = parameters_for_depack.get("_00") + 1
                parameters_for_depack.update({"_00": first_value_changed})
                and_to_param_00 = parameters_for_depack.get("_00") & 0x1f
                parameters_for_depack.update({"_00": and_to_param_00})
                fourth_value_changed = parameters_for_depack.get("_0c") + 1
                parameters_for_depack.update({"_0c": fourth_value_changed})
                packed_data_slice_internal += 2
                #print(parameters_for_depack)
            
            else:
                long_value_01 = int.from_bytes(packed_data[packed_data_slice_internal: packed_data_slice_internal + 1], 'little', signed=False)
                long_val_02_prev = long_value_01 >> 5
                LENGTH: Final =  long_val_02_prev + 1

                for i_val in range(0, LENGTH):
                    long_value_01 = long_value_01 & 0x1f
                    get_00_for_pack = parameters_for_depack.get("_00")
                    new_value_01 = depacked_elements.get(f'{long_value_01}')
                    depacked_elements.update({f'{get_00_for_pack}': new_value_01})
                    first_value_change = parameters_for_depack.get("_00") + 1
                    parameters_for_depack.update({"_00": first_value_change})
                    and_to_first_val = parameters_for_depack.get("_00") & 0x1f
                    parameters_for_depack.update({"_00": and_to_first_val})
                    long_value_01 += 1

                fourth_value_change = parameters_for_depack.get("_0c") + LENGTH
                parameters_for_depack.update({"_0c": fourth_value_change})
                packed_data_slice_internal += 1
            third_value_change = parameters_for_depack.get("_08") >> 1
            parameters_for_depack.update({"_08": third_value_change})

        for nn_number in range(0, UNPACKED_COUNT):
            value_set_00 = parameters_for_depack.get("_04")
            value_set_01 = depacked_elements.get(f'{value_set_00}')
            # Converting the uint into Hex
            value_set_2_hex = int.to_bytes(value_set_01, length=2, byteorder='little', signed=False)
            custom_primitive_depacked.append(value_set_2_hex) # Setting all the U_SHORTs into a List to hold the actual Primitive Depacked Data
            second_value_change = parameters_for_depack.get("_04") + 1
            parameters_for_depack.update({"_04": second_value_change})
            and_to_second_value_change = parameters_for_depack.get("_04") & 0x1f
            parameters_for_depack.update({"_04": and_to_second_value_change})
            fourth_value_change_lastloop = parameters_for_depack.get("_0c") - 1
            parameters_for_depack.update({"_0c": fourth_value_change_lastloop})

        return custom_primitive_depacked, packed_data_slice_internal


########################################
#### VERTEX DECODER AND INDEX FIXER #### # HERE I WILL CALCULATE THE NEW VERTEX INDEX, UPDATE IT AND ALSO THE REAL VERTEX TO BE USED IN THE MODELS
########################################
class CustomTmdVertex:
    def __init__(self, vertex_number, vertex_block):
        self.self = CustomTmdVertex
        self.vertex_decoder(vertex_number=vertex_number, vertex_block=vertex_block)

    def vertex_decoder(self, vertex_number=int, vertex_block=list):
        primitive_index = primitive_block_dict
        vertex_original = vertex_block # This is the original Block byte of Vertex
        vertex_num_original = vertex_number # This is the total number of Vertices in the model
        vertex_num_sum = sum(vertex_num_original)
        print(f'Total Number of Vertices in the CTMD: {vertex_num_original} == {vertex_num_sum}')

        vertex_full_split = []
        for vertex_split in vertex_original:
            length_vertex = len(vertex_split)
            start_vertex = 0
            end_vertex = 4
            vertex_split_4 = []
            while length_vertex >= 0:
                vertex_new_array = vertex_split[start_vertex:end_vertex]
                vertex_split_4.append(vertex_new_array)
                start_vertex += 4
                end_vertex += 4
                length_vertex -= 4
            vertex_full_split.append(vertex_split_4)

        # HERE I'M LOOPING INSIDE THE PRIMITIVES BLOCKS UNPACKED
        # ALSO LOOPING INTO EACH PRIMITIVE TO GET THE INDEX VALUES AND GETTING THE REAL VERTEX TO BE USED
        decoded_vertex_in_object = []
        obj_number = 0
        for prims_inside_obj in primitive_index:
            vertex_current_block = vertex_full_split[obj_number]
            decoded_vertex_inside_prim = [0, 0, 0] * len((vertex_current_block)) #TODO WRITE A FIX FOR PRIMITIVES INDICES
            long_2_init = [0, 0, 0]
            decoded_vertex_inside_prim[0] = long_2_init
            for prims_inside in prims_inside_obj:
                # NEED TO SUBTRACT -1 TO THE INDEX VALUE PRESENT TO MATCH WITH THE INDEX IN THE LIST/BYTEARRAY
                # THE VERTEX IS COMPOSED BY TWO VALUES A HIGH AND A LOW WITH A LITTLE CALC WE CAN GET THEM
                # ALSO I HAVE TO MAKE AN ALGORITHM TO CALCULATE THE VERTICES JUST ONCE
                if prims_inside.get('vertex3') != None:
                    index_0_4 = prims_inside.get('vertex0')
                    vertex_0_4 = VertexDecoder.vertex_decoding(v_index=index_0_4, v_byte_block=vertex_current_block)
                    index_1_4 = prims_inside.get('vertex1')
                    vertex_1_4 = VertexDecoder.vertex_decoding(v_index=index_1_4, v_byte_block=vertex_current_block)
                    index_2_4 = prims_inside.get('vertex2')
                    vertex_2_4 = VertexDecoder.vertex_decoding(v_index=index_2_4, v_byte_block=vertex_current_block)
                    index_3_4 = prims_inside.get('vertex3')
                    vertex_3_4 = VertexDecoder.vertex_decoding(v_index=index_3_4, v_byte_block=vertex_current_block)

                    decoded_vertex_inside_prim[index_0_4] = vertex_0_4
                    decoded_vertex_inside_prim[index_1_4] = vertex_1_4
                    decoded_vertex_inside_prim[index_2_4] = vertex_2_4
                    decoded_vertex_inside_prim[index_3_4] = vertex_3_4

                elif (prims_inside.get('vertex3') == None) and (prims_inside.get('vertex2') != None):
                    index_0 = prims_inside.get('vertex0')
                    vertex_0 = VertexDecoder.vertex_decoding(v_index=index_0, v_byte_block=vertex_current_block)
                    index_1 = prims_inside.get('vertex1')
                    vertex_1 = VertexDecoder.vertex_decoding(v_index=index_1, v_byte_block=vertex_current_block)
                    index_2 = prims_inside.get('vertex2')
                    vertex_2 = VertexDecoder.vertex_decoding(v_index=index_2, v_byte_block=vertex_current_block)

                    decoded_vertex_inside_prim[index_0] = vertex_0
                    decoded_vertex_inside_prim[index_1] = vertex_1
                    decoded_vertex_inside_prim[index_2] = vertex_2
                
                else:
                    print(f'NO VERTEX CTMD ERROR!!')
            decoded_vertex_in_object.append(decoded_vertex_inside_prim)
            obj_number += 1
            
        print(f'Total Blocks of Vertices: {len(decoded_vertex_in_object)}\n\n')

        vertex_decoded = decoded_vertex_in_object
        return vertex_decoded

class VertexDecoder:
    def __init__(self, v_index, v_byte_block):
        self.self = VertexDecoder
        self.vertex_decoding()
        self.v_index = v_index
        self.v_byte_block = v_byte_block
    
    @classmethod
    def vertex_decoding(self, v_index=int, v_byte_block=bytes):
        # Calculating the vertex index #
        low_v = v_byte_block[v_index]
        get_w = low_v[3]
        high_v = v_byte_block[get_w]

        low_v_x = np.int8(low_v[0])
        low_v_y = np.int8(low_v[1])
        low_v_z = np.int8(low_v[2])

        unpack_high_x = np.uint8(high_v[0])
        unpack_high_y = np.uint8(high_v[1])
        unpack_high_z = np.uint8(high_v[2])

        high_and_x = unpack_high_x & 0xff
        high_and_y = unpack_high_y & 0xff
        high_and_z = unpack_high_z & 0xff
        high_ls_x = high_and_x << 8
        high_ls_y = high_and_y << 8
        high_ls_z = high_and_z << 8

        hi_plus_lo_x = np.int16(low_v_x + high_ls_x)
        hi_plus_lo_y = np.int16(low_v_y + high_ls_y)
        hi_plus_lo_z = np.int16(low_v_z + high_ls_z)

        py_int_x = hi_plus_lo_x.item()
        py_int_y = hi_plus_lo_y.item()
        py_int_z = hi_plus_lo_z.item()

        build_short_x = int.to_bytes(py_int_x, 2, 'little', signed=True)
        build_short_y = int.to_bytes(py_int_y, 2, 'little', signed=True)
        build_short_z = int.to_bytes(py_int_z, 2, 'little', signed=True)

        short_2_int_x = int.from_bytes(build_short_x, 'little', signed=True)
        short_2_int_y = int.from_bytes(build_short_y, 'little', signed=True)
        short_2_int_z = int.from_bytes(build_short_z, 'little', signed=True)

        build_total = [short_2_int_x, short_2_int_y, short_2_int_z]
        return build_total