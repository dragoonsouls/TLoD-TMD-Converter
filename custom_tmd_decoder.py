"""

Custom TMD Decoder: This module decode the data from Vertex, Normal and Primitive
into integers for easy read/write for the Custom TMD Writer.
This module has to be very flexible and easy to update

also it will be too experimental and almost written from scratch so bugs can happen

Copyright (C) 2021 DooMMetaL

"""
import os
import custom_tmd_structure
import custom_tmd
import struct
import numpy as np
from itertools import zip_longest

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

#############################
#### CUSTOM TMD DEPACKER ####
#############################

class PrimitiveDepacker:
    def __init__(self, unpacked_length, custom_primitive_count, custom_primitive_packet):
        self.self = PrimitiveDepacker
        self.custom_primitives_depacker()        
        self.unpacked_length = unpacked_length
        self.custom_primitives_depacked = custom_primitive_depacked
        self.custom_primitive_count = custom_primitive_count
        self.custom_primitive_packet = custom_primitive_packet

    @classmethod
    def custom_primitives_depacker(cls, unpacked_length=int, custom_primitive_count=int, custom_primitive_packet=bytes): # PRIMITIVE DEPACKER FUNCTION

        global custom_primitive_depacked
        custom_primitive_depacked = [] # PROCESSED PRIMITIVES in the Object
        print(f'Custom Primitive COUNT: {custom_primitive_count}')
        primitive_internal_count = custom_primitive_count # current object primitive count value
        packed_data = custom_primitive_packet # current object primitive packet data
        depacked_elements_final = [] # in this list i hold all the dicts from depacking in the current object or block of primitives
        parameters_for_depack = {"_00": np.uint(0), "_04": np.uint(0), "_08": np.uint(0), "_0c": np.uint(0)} # CURRENT PARAMETERS FOR DEPACK IN THE PRIMTIVE == a3._00//_0c
        depacked_elements = {} # CURRENT ELEMENTS (DATA) IN THE PRIMITIVE == a3._10 |||| in this 64 slots Dict i hold all the data from depacking in the current primitive
        total_length_depack = 32
        for i in range(0, total_length_depack): # Filling with 0 the dictionary
            depacked_elements[f'{i}'] = np.uint(0)

        ###################################
        ##### START OF DEPACKING LOOP ##### |||| THIS LOOP IS PROCESSING THE PACKED DATA AND CONVERT INTO READABLE PACKETS
        packed_data_slice = 0
        for primitive_number in range(0, primitive_internal_count): # THIS LOOP ITER IN THE QUANTITY OF PRIMITIVES IN THE ACTUAL OBJECT
            custom_prim_depacked_internal = [] # DEPACKED PRIMITIVES INTERNAL DICT 
            unpacked_count = int(unpacked_length / 2) # little math to get a counter used below

            ###############################
            ##### START OF WHILE LOOP ##### |||| THIS LOOP DECODE THE DATA PACKET
            while np.uint(parameters_for_depack.get("_0c")) < unpacked_count : # while(a3._0c.get() < unpackedCount) DONE |||| TAKE THE FOURTH VALUE IN THE PARAMETERS AND WILL CONTINUE UNTIL GET EXHAUSTED
                if (np.uint(parameters_for_depack.get("_08")) & 0x100) == 0: # if((a3._08.get() & 0x100L) == 0) DONE |||| CHECK IF THE THIRD VALUE IS EQUAL TO 0, IF TRUE EXECUTE THIS CONDITION
                    parameter_3_new_value = np.uint(packed_data[packed_data_slice] | 0xff00) #unsigned_int_00 = 0 # a3._08.set(MEMORY.ref(1, packedData).get() | 0xff00L); DONE |||| bitwise op to the previous value
                    parameters_for_depack.update({"_08": parameter_3_new_value}) #["_08"] = parameter_3_new_value # Simplfied code for inserting (maybe will change to parameters_for_depack[2] = np.uint(transformed_byte_int | 0xff00))
                    packed_data_slice += 1 # packedData++; sum + 1 to the data slice

                if np.uint(parameters_for_depack.get("_08") & 0x1) != 0:# if((a3._08.get() & 0x1L) != 0) DONE |||| TAKE THE THIRD PARAMETER AND BITWISE IT, IF DIFFERENT THAN 0 WILL EXECUTE THIS CONDITION

                    #unsigned_short_00 =  a3._10.get((int)a3._00.get()).set((int)(MEMORY.ref(1, packedData).offset(0x1L).get() << 8 | MEMORY.ref(1, packedData).offset(0x0L).get())); _10 array, _00 index, combined data is (|) DONE
                    val_byte_01 = np.uint(packed_data[packed_data_slice]) # MEMORY.ref(1, packedData).offset(0x0L).get() |||| the current packed byte
                    val_byte_00 = np.uint((packed_data[packed_data_slice + 1]) << 8) # MEMORY.ref(1, packedData).offset(0x1L).get() << 8 |||| bitwise the next packed byte << 8
                    val_dep_00 = np.ushort(val_byte_00 | val_byte_01) # bitwise OR op to the two values and converting into a U_SHORT
                    index_pack_it = parameters_for_depack.get("_00") # a3._00.get() |||| getting the value from the 1st depack parameter
                    depacked_elements.update({f'{index_pack_it}': val_dep_00}) # Simplfied code for inserting

                    #unsigned_int_01 = 0 # a3._00.incr().and(0x1fL); DONE |||| sum + 1 to the 1st value plus bitwise op OR to 0x1f; result will be inserted in the 1st parameter for depack
                    first_value_changed = np.uint((parameters_for_depack.get("_00") + 1) & 0x1f)
                    parameters_for_depack.update({"_00": first_value_changed})

                    #unsigned_int_02 = 0 # a3._0c.incr(); DONE |||| sum + 1 to the 4th value; result will be inserted in the 4th parameter
                    fourth_value_changed = np.uint(parameters_for_depack.get("_0c") + 1)
                    parameters_for_depack.update({"_0c": fourth_value_changed})
                    packed_data_slice += 2 # packedData += 2; DONE |||| sum + 2 to the data slice
                
                else: # IF THE PREVIOUS LOOP IS FALSE, THIS LOOP WILL BE EXECUTED

                    long_value_01 = np.uint(packed_data[packed_data_slice]) # long a1 = MEMORY.ref(1, packedData).get(); DONE |||| take the current data packet and change it into a long
                    long_value_02 = np.uint(np.right_shift(long_value_01, 5) + 1) # final long t2 = (a1 >>> 5) + 1; DONE |||| bitwise unsigned right shift to the previous long and sum + 1 to the result

                    n1_number = 0
                    for number_iter in range(0, long_value_02): # for(i = 0; i < t2; i++) DONE |||| this block iters in the range of previous long value (0 to long_value_2 result)

                        #new_value_00 = long_value_01 & 0x1f # a1 &= 0x1fL; DONE |||| take the first long and bitwise a1 = a1 & 0x1fL
                        new_long_value = np.uint(long_value_01 & 0x1f)

                        #unsigned_short_01 = 0 # a3._10.get((int)a3._00.get()).set(a3._10.get((int)a1).get()); DONE |||| replacing some values from depacked elements in the specified index
                        new_value_01 = np.ushort(depacked_elements.get(f'{new_long_value}')) # a3._10.get((int)a1).get()) |||| getting the element to change from the depacked elements using the first long as index
                        get_00_for_pack = parameters_for_depack.get("_00") # a3._00.get()) getting the index using the 1st element from the parameter for depack
                        depacked_elements.update({f'{get_00_for_pack}': new_value_01}) # Simplified code insertion ---- # setting the new value into the depacked elements using index specified by the same parameters for depack

                        #unsigned_int_03 = 0 # a3._00.incr().and(0x1fL); DONE ||||  sum + 1 to the 1st value plus bitwise op AND to 0x1f; result will be inserted in the 1st parameter for depack
                        first_value_change = np.uint((parameters_for_depack.get("_00") + 1) & 0x1f)
                        parameters_for_depack.update({"_00": first_value_change}) # Simplified code for insertion
                        print(type(number_iter))
                        long_value_01 += 1 # a1++; sum + 1 to the long value to continue the iter
                        n1_number += 1

                    #unsigned_int_04 = 0 # a3._0c.add(i); DONE |||| sum the last value obtained from the for loop to the 4th parameter for depack and insert it into the 3rd parameter
                    fourth_value_change = np.uint(parameters_for_depack.get("_0c") + n1_number)
                    parameters_for_depack.update({"_0c": fourth_value_change}) # setting the new 4th value
                    packed_data_slice += 1 # packedData++; DONE |||| sum + 1 to the data slice
                #unsigned_int_05 = 0 # a3._08.set(a3._08.get() >> 1); |||| set a new value for the 3rd value using bitshift >> 1
                third_value_change = np.uint(parameters_for_depack.get("_08") >> 1)
                parameters_for_depack.update({"_08": third_value_change}) # setting the new 3rd value
                #print(parameters_for_depack)
                #DEBUG Printing
            ##### END OF WHILE LOOP #####
            #############################
            #///////////////////////////#
            #############################
            ##### START OF FOR LOOP ##### |||| THIS LOOP WILL PACK THE PREVIOUSLY PROCESSED ELEMENTS INTO READABLE PACKET DATA
            for nn_number in range(0, unpacked_count): # for(int i = 0; i < unpackedCount; i++) |||| iters in range of 0 to the unpacked count
                
                #"this is marked just a value ????" # MEMORY.ref(2, unpackedData).offset(i * 0x2L).setu(a3._10.get((int)a3._04.get()).get()); |||| TAKE THE DATA FROM DEPACKED ELEMENTS USING INDEX SPECIFIED INDEX IN THE 2ND VALUE AND CREATE U_SHORT PACKETS
                value_set_00 = np.uint(parameters_for_depack.get("_04")) # a3._04.get()).get()) |||| getting the parameter value
                value_set_01 = np.uint(depacked_elements.get(f'{value_set_00}')) # setu(a3._10.get(....) |||| setting the unsigned depacked element

                # Converting the uint into Hex
                value_set_to_python = value_set_01.item()
                value_set_2_hex = int.to_bytes(value_set_to_python, length=2, byteorder='little', signed=False)
                if value_set_to_python == 12298:
                            print(value_set_01, value_set_00, primitive_number)

                custom_prim_depacked_internal.append(value_set_2_hex) # MEMORY.ref(2, unpackedData) |||| appending the U_SHORT into the internal list ||| Originally value_set_01
                # Note: the offset setting is ignored because i don't need it in the list sorting

                #unsigned_int_06 = 0 # a3._04.incr().and(0x1fL); DONE |||| SUM + 1 and apply bitwise op to the 2nd paramenter, inserting the result at the end
                second_value_change = np.uint(np.uint(parameters_for_depack.get("_04") + 1) & 0x1f)
                #print(f'SECOND VALUE CHANGE!!!!: {second_value_change}')
                parameters_for_depack.update({"_04": second_value_change}) # setting the new 2nd parameter

                #unsigned_int_07 = 0 # a3._0c.decr(); |||| SUBTRACT - 1 TO THE 4TH VALUE, inserting the result at the end
                fourth_value_change_lastloop = np.uint(parameters_for_depack.get("_0c") - 1)
                parameters_for_depack.update({"_0c": fourth_value_change_lastloop}) # setting the new 4th parameter
                #DEBUG Printing
                #### END OF FOR LOOP ####
                #########################
            ##### END OF DEPACKING LOOP ##### |||| THIS LOOP IS ENDING THE PROCESS OF THE PACKED DATA AND CONVERT INTO READABLE PACKETS
            #################################
            #Apending
            custom_primitive_depacked.append(custom_prim_depacked_internal) # appending the internal list depacked to the current object primitive packet
            depacked_elements_final.append(depacked_elements)
            #DEBUG Printing
            ##### END OF DEPACKING LOOP #####
            #################################
        #### END OF OBJECT LOOP #####
        #############################
        #///////////////////////////#
        #############################
        #print(len(custom_primitive_depacked), unpacked_length, primitive_internal_count)
        return custom_primitive_depacked

##################################
#### MULTI-PRIMITIVES CHECKER #### |||| this class is in charge not only to check the primitive types in the same block, but also to create the arrays/packets for each type
##################################

class MultiPrimitivesChecker:
    def __init__(self, check_multi_prim, number_of_prims):
        self.self = MultiPrimitivesChecker
        self.check_multi_prim = check_multi_prim
        self.number_of_prims = number_of_prims
    
    @classmethod
    def multi_prim_checker(cls, check_multi_prim=list, number_of_prims=int):
        global split_multiprim_blocks
        split_multiprim_blocks = []
        primitives_position_block = []
        global type_found
        type_found = []
        possible_values_finish = []
        if check_multi_prim[0] != number_of_prims:
            print(f'Total primitive number in the object:', number_of_prims)
            
            length_byte_array = len(check_multi_prim)
            get_prim_next_s = 0
            get_prim_next_e = 4
            split_finish = []
            while length_byte_array > 0:
                split_4_bytes = check_multi_prim[get_prim_next_s:get_prim_next_e]
                split_finish.append(split_4_bytes)
                length_byte_array -= 4
                get_prim_next_s += 4
                get_prim_next_e += 4

            possible_values = []
            possible_values_int = []
            for split_f in split_finish:
                if (prim_type_00 in split_f) and (split_f[0] != 0):
                    #print("prim_type_00, found")
                    possible_values.append(split_f)
                    possible_values_int.append(split_f[0])
                    type_found.append("prim_type_00")
                elif (prim_type_01 in split_f) and (split_f[0] != 0):
                    #print("prim_type_01, found")
                    possible_values.append(split_f)
                    possible_values_int.append(split_f[0])
                    type_found.append("prim_type_01")
                elif (prim_type_02 in split_f) and (split_f[0] != 0):
                    #print("prim_type_02, found")
                    possible_values.append(split_f)
                    possible_values_int.append(split_f[0])
                    type_found.append("prim_type_02")
                elif (prim_type_03 in split_f) and (split_f[0] != 0):
                    #print("prim_type_03, found")
                    possible_values.append(split_f)
                    possible_values_int.append(split_f[0])
                    type_found.append("prim_type_03")
                elif (prim_type_04 in split_f) and (split_f[0] != 0):
                    #print("prim_type_04, found")
                    possible_values.append(split_f)
                    possible_values_int.append(split_f[0])
                    type_found.append("prim_type_04")
                elif (prim_type_05 in split_f) and (split_f[0] != 0):
                    #print("prim_type_05, found")
                    possible_values.append(split_f)
                    possible_values_int.append(split_f[0])
                    type_found.append("prim_type_05")
                elif (prim_type_06 in split_f) and (split_f[0] != 0):
                    #print("prim_type_06, found")
                    possible_values.append(split_f)
                    possible_values_int.append(split_f[0])
                    type_found.append("prim_type_06")
                elif (prim_type_07 in split_f) and (split_f[0] != 0):
                    #print("prim_type_07, found")
                    possible_values.append(split_f)
                    possible_values_int.append(split_f[0])
                    type_found.append("prim_type_07")
                elif (prim_type_08 in split_f) and (split_f[0] != 0):
                    #print("prim_type_08, found")
                    possible_values.append(split_f)
                    possible_values_int.append(split_f[0])
                    type_found.append("prim_type_08")
                elif (prim_type_09 in split_f) and (split_f[0] != 0):
                    #print("prim_type_09, found")
                    possible_values.append(split_f)
                    possible_values_int.append(split_f[0])
                    type_found.append("prim_type_09")
                elif (prim_type_10 in split_f) and (split_f[0] != 0):
                    #print("prim_type_10, found")
                    possible_values.append(split_f)
                    possible_values_int.append(split_f[0])
                    type_found.append("prim_type_10")
                elif (prim_type_11 in split_f) and (split_f[0] != 0):
                    #print("prim_type_11, found")
                    possible_values.append(split_f)
                    possible_values_int.append(split_f[0])
                    type_found.append("prim_type_11")
                elif (prim_type_12 in split_f) and (split_f[0] != 0):
                    #print("prim_type_12, found")
                    possible_values.append(split_f)
                    possible_values_int.append(split_f[0])
                    type_found.append("prim_type_12")
                elif (prim_type_13 in split_f) and (split_f[0] != 0):
                    #print("prim_type_13, found")
                    possible_values.append(split_f)
                    possible_values_int.append(split_f[0])
                    type_found.append("prim_type_13")
                else:
                    pass
            #print(possible_values, possible_values_int)
            #possible_values_finish.append(possible_values_int)
            if sum(possible_values_int) == number_of_prims:
                print(f'Total Values calculated: {sum(possible_values_int)}', f'Summed Values: {possible_values_int}'  )
                for possible_vals in possible_values:
                    position_primitive = check_multi_prim.find(possible_vals)
                    primitives_position_block.append(position_primitive)
                    possible_values_finish.append(possible_vals[0])
                finishing_value = len(check_multi_prim)
                primitives_position_block.append(finishing_value)
            else:
                print("FAIL to get the correct number of Primitives in the Block Byte!!!")
                exit()
        
        total_index_list = len(primitives_position_block)
        slice_the_slice_s = 0
        slice_the_slice_e = 1
        sum_posblock = sum(primitives_position_block)
        len_block_ori = len(check_multi_prim)
        print(f'Original len: {len_block_ori}, found {primitives_position_block}, sum = {sum_posblock - len_block_ori}, {total_index_list}')
        while total_index_list > 1:
            pos_start = primitives_position_block[slice_the_slice_s]
            pos_end = primitives_position_block[slice_the_slice_e]
            new_block_prim = check_multi_prim[pos_start:pos_end]
            split_multiprim_blocks.append(new_block_prim)
            total_index_list -= 1
            slice_the_slice_s += 1
            slice_the_slice_e += 1

################################
#### CUSTOM TMD INTERPRETER #### |||| THIS MODULE INTERPRET NORMAL/PRIMITIVE DATA TO WRITE READABLE PACKETS FOR THE COLLADA WRITER
################################

class CustomTmdInterpreter:
    def __init__(self):
        self.self = CustomTmdInterpreter
    
    """def vertex_decoder(self):
        global vertex_decoded
        vertex_decoded = [] # VERTEX ALREADY DECODED
        vertex_to_decode = custom_tmd_structure.cvertex_block_byte # BLOCK BYTES OF VERTEX FOR EACH OBJECT
        vertex_quantity = custom_tmd_structure.cvertex_number_int # QUANTITY OF VERTEX IN EACH OBJECT
        number_of_objects = custom_tmd.ctmd_nobj_expected

        for vertex_actual in range(0, number_of_objects):
            ###############################
            #### SPLIT BLOCK IN A HALF ####
            split_blocks = vertex_to_decode[vertex_actual]

            split_block_count = vertex_quantity[vertex_actual]
            start_b = 0
            end_b = 4
            vert_split_4b = []
            while split_block_count > 0:
                split_it = split_blocks[start_b:end_b]
                vert_split_4b.append(split_it)
                split_block_count -= 1
                start_b += 4
                end_b += 4
            
            n_index = 0
            for search_index in vert_split_4b:
                if search_index[3] == 1:
                    break
                else:
                    pass
                n_index += 1
            
            real_middle_postion = n_index - 1
            block_low_split = vert_split_4b[real_middle_postion:]
            block_high_split = vert_split_4b[:real_middle_postion]

            #### SPLIT BLOCK IN A HALF END ####
            ###################################
            #////////////////////////////////#
            ##################################
            #### START DECODING OF VERTEX ####

            vertex_in_obj = []
            for vertex_decoded_block in block_low_split: # HERE I LOOP TO GET DECODING

                w_index_low = np.uint(vertex_decoded_block[3]) # THIS IS THE W VALUE FOR INDICATING THE INDEX FOR THE NECESSARY HIGH VERTEX BLOCK, this is only present in CTMD files
                get_high_vertex = block_high_split[w_index_low] # HIGH VERTEX BLOCK
                # Since the structure remains as a Standard Vertex, each byte represent x, y and z values
                x_high = get_high_vertex[0] << 8
                y_high = get_high_vertex[1] << 8
                z_high = get_high_vertex[2] << 8
                x_value = np.short(vertex_decoded_block[0] + x_high)
                y_value = np.short(vertex_decoded_block[1] + y_high)
                z_value = np.short(vertex_decoded_block[2] + z_high)
                vertex_values = [x_value, y_value, z_value]
                vertex_in_obj.append(vertex_values)
            vertex_decoded.append(vertex_in_obj)"""

    def normal_decoder(self):
        global normal_decoded
        normal_decoded = []

        normal_to_decode = custom_tmd_structure.cnormal_block_byte # BLOCK BYTES OF VERTEX FOR EACH OBJECT
        normal_quantity = custom_tmd_structure.cnormal_number_int # QUANTITY OF VERTEX IN EACH OBJECT
        number_of_objects = custom_tmd.ctmd_nobj_expected # TOTAL NUMBER OF OBJECTS IN THE CTMD

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

    def cprimitive_types_depacker(self, tmd_attribute): # THIS IS A SECTION FOR CALCULATE THE QUANTITY OF PRIMITIVES PACKETS IN EACH PRIMITIVE BLOCK
        self.self = self
        self.tmd_attribute = tmd_attribute

        block_obj_primitives = custom_tmd_structure.cprimitive_block_byte # Complete block of Primtives
        num_of_prim_in_obj = custom_tmd_structure.cprimitive_number_int # Number of Primitives in each object
        num_obj_ctmd = custom_tmd.ctmd_nobj_expected # Total number of Objects in the CTMD
        total_original_primitives = custom_tmd_structure.cprimitive_number_total

        processed_prim_block = [] # CTMD CONVERTED BUT IN HEX

        for p_block_num in range(0, num_obj_ctmd): # HERE I LOOP IN THE NUMBER OF OBJECT AND PRIMITIVE BLOCK
            num_packet_prim = block_obj_primitives[p_block_num] # CURRENT BLOCK OF PRIMITIVES IN THE OBJECT
            num_prims = num_of_prim_in_obj[p_block_num]
            obj_prim_processed = []
            total_prims_in_obj = num_of_prim_in_obj[p_block_num]
            # IF the Number of packets in the TOP of the block is equal to the Number of Primitives this will be executed
            if num_packet_prim[0] == num_prims:
                print(f'////////========SINGLE PRIMITIVE PROCESSING========\\\\\\\\')
                print(f'============|||Object Number: {p_block_num}|||============')
                
                if self.tmd_attribute == 1:
                    attribute_hex = 0x14000040
                elif self.tmd_attribute == 2:
                    attribute_hex = 0x14000000
                elif self.tmd_attribute == 3:
                    attribute_hex = 0x50000000
                elif self.tmd_attribute == 4:
                    attribute_hex = 0x64000040
                elif self.tmd_attribute == 5:
                    attribute_hex = 0x54000000
                else:
                    attribute_hex = 0x14000000
                
                if (attribute_hex & 0x40000000) == 0:
                    mode_prim_single = 0x00
                else:
                    mode_prim_single = 0x12
                
                type_len = int.from_bytes(num_packet_prim[0:2], 'little', signed=False)
                type_command = int.from_bytes(num_packet_prim[0:4], 'little', signed=False)

                new_prim_command_single = np.right_shift(type_command, 24) & np.uint(0x3e) | mode_prim_single
                index_render_single = np.right_shift(type_command, 14) & np.uint(0x20) | np.right_shift(type_command, 24) & np.uint(0xf) | np.right_shift(type_command, 18) & np.uint(0x1) | mode_prim_single
                print(f'New Primitive Command: {new_prim_command_single}, Index of Renderer: {index_render_single},\n Total Primitives in Block: {total_prims_in_obj}')
                
                not_possible_render = [16, 17, 20, 21, 24, 25, 28, 29, 48, 49, 52, 53, 56, 57, 60, 61]

                if (index_render_single == 0) or (index_render_single == 2) or (index_render_single == 18):
                    print(f'Renderer 1')
                elif (index_render_single == 1) or (index_render_single == 3) or (index_render_single == 19):
                    print(f'Renderer 2')
                elif (index_render_single == 4) or (index_render_single == 6):
                    print(f'Renderer 3')
                elif (index_render_single == 5) or (index_render_single == 7):
                    print(f'Renderer 4')
                elif (index_render_single == 8) or (index_render_single == 10) or (index_render_single == 26):
                    print(f'Renderer 5')
                elif (index_render_single == 9) or (index_render_single == 11) or (index_render_single == 27):
                    print(f'Renderer 6')
                elif (index_render_single == 12) or (index_render_single == 14):
                    print(f'Renderer 7')
                elif (index_render_single == 13) or (index_render_single == 15):
                    print(f'Renderer 8')
                elif (index_render_single == 22):
                    print(f'Renderer 9')
                elif (index_render_single == 23):
                    print(f'Renderer 10')
                elif (index_render_single == 30):
                    print(f'Renderer 11')
                elif (index_render_single == 31):
                    print(f'Renderer 12')
                # From this point to below all had unpackers
                elif (index_render_single == 32) or (index_render_single == 34) or (index_render_single == 50):
                    print(f'Renderer 13 Single Block, need to be unpacked')
                    PrimitiveDepacker.custom_primitives_depacker(unpacked_length=16, custom_primitive_count=type_len, custom_primitive_packet=num_packet_prim[4:])
                    prim_header_13_single = f'render_13'
                    render_13_single = prim_header_13_single, custom_primitive_depacked
                    obj_prim_processed.append(render_13_single)
                elif (index_render_single == 33) or (index_render_single == 35) or (index_render_single == 51):
                    print(f'Renderer 14 Single Block, need to be unpacked')
                    PrimitiveDepacker.custom_primitives_depacker(unpacked_length=24, custom_primitive_count=type_len, custom_primitive_packet=num_packet_prim[4:])
                    prim_header_14_single = f'render_14'
                    render_14_single = prim_header_14_single, custom_primitive_depacked
                    obj_prim_processed.append(render_14_single)
                elif (index_render_single == 36) or (index_render_single == 38):
                    print(f'Renderer 15 Single Block, need to be unpacked')
                    PrimitiveDepacker.custom_primitives_depacker(unpacked_length=24, custom_primitive_count=type_len, custom_primitive_packet=num_packet_prim[4:])
                    prim_header_15_single = f'render_15'
                    render_15_single = prim_header_15_single, custom_primitive_depacked
                    obj_prim_processed.append(render_15_single)
                elif (index_render_single == 37) or (index_render_single == 39):
                    print(f'Renderer 16 Single Block, need to be unpacked')
                    PrimitiveDepacker.custom_primitives_depacker(unpacked_length=32, custom_primitive_count=type_len, custom_primitive_packet=num_packet_prim[4:])
                    prim_header_16_single = f'render_16'
                    render_16_single = prim_header_16_single, custom_primitive_depacked
                    obj_prim_processed.append(render_16_single)
                elif (index_render_single == 40) or (index_render_single == 42) or (index_render_single == 58):
                    print(f'Renderer 17 Single Block, need to be unpacked')
                    PrimitiveDepacker.custom_primitives_depacker(unpacked_length=20, custom_primitive_count=type_len, custom_primitive_packet=num_packet_prim[4:])
                    prim_header_17_single = f'render_17'
                    render_17_single = prim_header_17_single, custom_primitive_depacked
                    obj_prim_processed.append(render_17_single)
                elif (index_render_single == 41) or (index_render_single == 43) or (index_render_single == 59):
                    print(f'Renderer 18 Single Block, need to be unpacked')
                    PrimitiveDepacker.custom_primitives_depacker(unpacked_length=32, custom_primitive_count=type_len, custom_primitive_packet=num_packet_prim[4:])
                    prim_header_18_single = f'render_18'
                    render_18_single = prim_header_18_single, custom_primitive_depacked
                    obj_prim_processed.append(render_18_single)
                elif (index_render_single == 44) or (index_render_single == 46):
                    print(f'Renderer 19 Single Block, need to be unpacked')
                    PrimitiveDepacker.custom_primitives_depacker(unpacked_length=32, custom_primitive_count=type_len, custom_primitive_packet=num_packet_prim[4:])
                    prim_header_19_single = 'render_19'
                    render_19_single = prim_header_19_single, custom_primitive_depacked
                    obj_prim_processed.append(render_19_single)
                elif (index_render_single == 45) or (index_render_single == 47):
                    print(f'Renderer 20 Single Block, need to be unpacked')
                    PrimitiveDepacker.custom_primitives_depacker(unpacked_length=40, custom_primitive_count=type_len, custom_primitive_packet=num_packet_prim[4:])
                    prim_header_20_single = f'render_20'
                    render_20_single = prim_header_20_single, custom_primitive_depacked
                    obj_prim_processed.append(render_20_single)
                elif (index_render_single == 54):
                    print(f'Renderer 21 Single Block, need to be unpacked')
                    PrimitiveDepacker.custom_primitives_depacker(unpacked_length=24, custom_primitive_count=type_len, custom_primitive_packet=num_packet_prim[4:])
                    prim_header_21_single = f'render_21'
                    render_21_single = prim_header_21_single, custom_primitive_depacked
                    obj_prim_processed.append(render_21_single)
                elif (index_render_single == 55):
                    print(f'Renderer 22 Single Block, need to be unpacked')
                    PrimitiveDepacker.custom_primitives_depacker(unpacked_length=32, custom_primitive_count=type_len, custom_primitive_packet=num_packet_prim[4:])
                    prim_header_22_single = f'render_22'
                    render_22_single = prim_header_22_single, custom_primitive_depacked
                    obj_prim_processed.append(render_22_single)
                elif (index_render_single == 62):
                    print(f'Renderer 23 Single Block, need to be unpacked')
                    PrimitiveDepacker.custom_primitives_depacker(unpacked_length=32, custom_primitive_count=type_len, custom_primitive_packet=num_packet_prim[4:])
                    prim_header_23_single = f'render_23'
                    render_23_single = prim_header_23_single, custom_primitive_depacked
                    obj_prim_processed.append(render_23_single)
                elif (index_render_single == 63):
                    print(f'Renderer 24 Single Block, need to be unpacked')
                    PrimitiveDepacker.custom_primitives_depacker(unpacked_length=40, custom_primitive_count=type_len, custom_primitive_packet=num_packet_prim[4:])
                    prim_header_24_single = f'render_24'
                    render_24_single = prim_header_24_single, custom_primitive_depacked
                    obj_prim_processed.append(render_24_single)
                elif index_render_single in not_possible_render:
                    print(f'Index Render Number: {index_render_single} is not a possible value')
                else:
                    print(f'Index Render Number: {index_render_single} do not exist!!, exiting the Tool...')
                    exit()   

            # SO if the Number of packets in the TOP is not equal to the Number of Primtives this will be executed
            else:
                try:
                    print(f'////////========MULTI PRIMITIVE PROCESSING========\\\\\\\\') 
                    MultiPrimitivesChecker.multi_prim_checker(check_multi_prim=num_packet_prim, number_of_prims=num_prims)
                    primblock_split = split_multiprim_blocks
                    print(f'============|||Object Number: {p_block_num}|||============')

                    for single_type in primblock_split:
                        print(single_type[0:4])

                        if self.tmd_attribute == 1:
                            attribute_hex = 0x1400_0040
                        elif self.tmd_attribute == 2:
                            attribute_hex = 0x1400_0000
                        elif self.tmd_attribute == 3:
                            attribute_hex = 0x5000_0000
                        elif self.tmd_attribute == 4:
                            attribute_hex = 0x6400_0040
                        elif self.tmd_attribute == 5:
                            attribute_hex = 0x5400_0000
                        else:
                            attribute_hex = 0x1400_0000
                        
                        if (attribute_hex & 0x4000_0000) == 0:
                            mode_prim = 0x00
                        else:
                            mode_prim = 0x12
                        
                        single_type_len = int.from_bytes(single_type[0:2], 'little', signed=False)
                        prim_type_command = int.from_bytes(single_type[0:4], 'little', signed=False)

                        new_prim_command = np.right_shift(prim_type_command, 24) & 0x3e | mode_prim
                        index_render = np.right_shift(prim_type_command, 14) & 0x20 | np.right_shift(prim_type_command, 24) & 0xf | np.right_shift(prim_type_command, 18) & 0x1 | mode_prim
                        print(f'New Primitive Command: {new_prim_command}, Index of Renderer: {index_render},\nQuantity of Prims to Convert: {single_type_len}, Total Prims: {total_prims_in_obj}')
                        
                        not_possible_render = [16, 17, 20, 21, 24, 25, 28, 29, 48, 49, 52, 53, 56, 57, 60, 61]

                        if (index_render == 0) or (index_render == 2) or (index_render == 18):
                            print(f'Renderer 1')
                        elif (index_render == 1) or (index_render == 3) or (index_render == 19):
                            print(f'Renderer 2')
                        elif (index_render == 4) or (index_render == 6):
                            print(f'Renderer 3')
                        elif (index_render == 5) or (index_render == 7):
                            print(f'Renderer 4')
                        elif (index_render == 8) or (index_render == 10) or (index_render == 26):
                            print(f'Renderer 5')
                        elif (index_render == 9) or (index_render == 11) or (index_render == 27):
                            print(f'Renderer 6')
                        elif (index_render == 12) or (index_render == 14):
                            print(f'Renderer 7')
                        elif (index_render == 13) or (index_render == 15):
                            print(f'Renderer 8')
                        elif (index_render == 22):
                            print(f'Renderer 9')
                        elif (index_render == 23):
                            print(f'Renderer 10')
                        elif (index_render == 30):
                            print(f'Renderer 11')
                        elif (index_render == 31):
                            print(f'Renderer 12')
                        # From this point to below all had unpackers
                        elif (index_render == 32) or (index_render == 34) or (index_render == 50): # THIS IS UNPACKING FUN_800e0848
                            print(f'Renderer 13 Multi Block, need to be unpacked')
                            PrimitiveDepacker.custom_primitives_depacker(unpacked_length=16, custom_primitive_count=single_type_len, custom_primitive_packet=single_type[4:])
                            prim_header_13 = f'render_13'
                            render_13 = prim_header_13, custom_primitive_depacked
                            obj_prim_processed.append(render_13)
                        elif (index_render == 33) or (index_render == 35) or (index_render == 51):
                            print(f'Renderer 14 Multi Block, need to be unpacked')
                            PrimitiveDepacker.custom_primitives_depacker(unpacked_length=24, custom_primitive_count=single_type_len, custom_primitive_packet=single_type[4:])
                            prim_header_14 = f'render_14'
                            render_14 = prim_header_14, custom_primitive_depacked
                            obj_prim_processed.append(render_14)
                        elif (index_render == 36) or (index_render == 38):
                            print(f'Renderer 15 Multi Block, need to be unpacked')
                            PrimitiveDepacker.custom_primitives_depacker(unpacked_length=24, custom_primitive_count=single_type_len, custom_primitive_packet=single_type[4:])
                            prim_header_15 = f'render_15'
                            render_15 = prim_header_15, custom_primitive_depacked
                            obj_prim_processed.append(render_15)
                        elif (index_render == 37) or (index_render == 39):
                            print(f'Renderer 16 Multi Block, need to be unpacked')
                            PrimitiveDepacker.custom_primitives_depacker(unpacked_length=32, custom_primitive_count=single_type_len, custom_primitive_packet=single_type[4:])
                            prim_header_16 = f'render_16'
                            render_16 = prim_header_16, custom_primitive_depacked
                            obj_prim_processed.append(render_16)
                        elif (index_render == 40) or (index_render == 42) or (index_render == 58):
                            print(f'Renderer 17 Multi Block, need to be unpacked')
                            PrimitiveDepacker.custom_primitives_depacker(unpacked_length=20, custom_primitive_count=single_type_len, custom_primitive_packet=single_type[4:])
                            prim_header_17 = f'render_17'
                            render_17 = prim_header_17, custom_primitive_depacked
                            obj_prim_processed.append(render_17)
                        elif (index_render == 41) or (index_render == 43) or (index_render == 59):
                            print(f'Renderer 18 Multi Block, need to be unpacked')
                            PrimitiveDepacker.custom_primitives_depacker(unpacked_length=32, custom_primitive_count=single_type_len, custom_primitive_packet=single_type[4:])
                            prim_header_18 = f'render_18'
                            render_18 = prim_header_18, custom_primitive_depacked
                            obj_prim_processed.append(render_18)
                        elif (index_render == 44) or (index_render == 46):
                            print(f'Renderer 19 Multi Block, need to be unpacked')
                            PrimitiveDepacker.custom_primitives_depacker(unpacked_length=32, custom_primitive_count=single_type_len, custom_primitive_packet=single_type[4:])
                            prim_header_19 = 'render_19'
                            render_19 = prim_header_19, custom_primitive_depacked
                            obj_prim_processed.append(render_19)
                        elif (index_render == 45) or (index_render == 47):
                            print(f'Renderer 20 Multi Block, need to be unpacked')
                            PrimitiveDepacker.custom_primitives_depacker(unpacked_length=40, custom_primitive_count=single_type_len, custom_primitive_packet=single_type[4:])
                            prim_header_20 = f'render_20'
                            render_20 = prim_header_20, custom_primitive_depacked
                            obj_prim_processed.append(render_20)
                        elif (index_render == 54):
                            print(f'Renderer 21 Multi Block, need to be unpacked')
                            PrimitiveDepacker.custom_primitives_depacker(unpacked_length=24, custom_primitive_count=single_type_len, custom_primitive_packet=single_type[4:])
                            prim_header_21 = f'render_21'
                            render_21 = prim_header_21, custom_primitive_depacked
                            obj_prim_processed.append(render_21)
                        elif (index_render == 55):
                            print(f'Renderer 22 Multi Block, need to be unpacked')
                            PrimitiveDepacker.custom_primitives_depacker(unpacked_length=32, custom_primitive_count=single_type_len, custom_primitive_packet=single_type[4:])
                            prim_header_22 = f'render_22'
                            render_22 = prim_header_22, custom_primitive_depacked
                            obj_prim_processed.append(render_22)
                        elif (index_render == 62):
                            print(f'Renderer 23 Multi Block, need to be unpacked')
                            PrimitiveDepacker.custom_primitives_depacker(unpacked_length=32, custom_primitive_count=single_type_len, custom_primitive_packet=single_type[4:])
                            prim_header_23 = f'render_23'
                            render_23 = prim_header_23, custom_primitive_depacked
                            obj_prim_processed.append(render_23)
                        elif (index_render == 63):
                            print(f'Renderer 24 Multi Block, need to be unpacked')
                            PrimitiveDepacker.custom_primitives_depacker(unpacked_length=40, custom_primitive_count=single_type_len, custom_primitive_packet=single_type[4:])
                            prim_header_24 = f'render_24'
                            render_24 = prim_header_24, custom_primitive_depacked
                            obj_prim_processed.append(render_24)
                        elif index_render in not_possible_render:
                            print(f'Index Render Number: {index_render} is not a possible value')
                        else:
                            print(f'Index Render Number: {index_render} do not exist!!, exiting the Tool...')
                            exit()
                except ValueError:
                    print(f'ERROR |||| Object Number {p_block_num} Have no Primitive Block or is 0 ||||')
            processed_prim_block.append(obj_prim_processed)
        
        #print(processed_prim_block)
        global primitive_block_dict
        primitive_block_dict = [] # CTMD CONVERTED INTO READABLE FORM

        prim_dec_block_num = 0
        for prim_dec_block in processed_prim_block:
            prim_block_inner_obj = []
            for prim_d_b in prim_dec_block:
                if prim_d_b[0] == f'render_13':
                    for prim_db in prim_d_b[1]:
                        byte_array = b''.join(prim_db)
                        lsc3vntgs = {"lsc3vntgs":b'\x06\x04\x00\x30', 
                            "r0":int.from_bytes(byte_array[0:1], byteorder='little', signed=False), "g0":int.from_bytes(byte_array[1:2], byteorder='little', signed=False), "b0":int.from_bytes(byte_array[2:3], byteorder='little', signed=False), "pad0":int.from_bytes(byte_array[3:4], byteorder='little', signed=False), 
                            "normal0":int.from_bytes(byte_array[4:6], byteorder='little', signed=False), "vertex0":int.from_bytes(byte_array[6:8], byteorder='little', signed=False), 
                            "normal1":int.from_bytes(byte_array[8:10], byteorder='little', signed=False), "vertex1":int.from_bytes(byte_array[10:12], byteorder='little', signed=False), 
                            "normal2":int.from_bytes(byte_array[12:14], byteorder='little', signed=False), "vertex2":int.from_bytes(byte_array[14:16], byteorder='little', signed=False)}
                        prim_block_inner_obj.append(lsc3vntgs)

                elif prim_d_b[0] == f'render_14':
                    for prim_db in prim_d_b[1]:
                        byte_array = b''.join(prim_db)
                        lsc3vntgg = {"lsc3vntgg":b'\x06\x06\x04\x30', 
                            "r0":int.from_bytes(byte_array[0:1], byteorder='little', signed=False), "g0":int.from_bytes(byte_array[1:2], byteorder='little', signed=False), "b0":int.from_bytes(byte_array[2:3], byteorder='little', signed=False), "pad0":byte_array[3:4], 
                            "r1":int.from_bytes(byte_array[4:5], byteorder='little', signed=False), "g1":int.from_bytes(byte_array[5:6], byteorder='little', signed=False), "b1":int.from_bytes(byte_array[6:7], byteorder='little', signed=False), "pad1":byte_array[7:8], 
                            "r2":int.from_bytes(byte_array[8:9], byteorder='little', signed=False), "g2":int.from_bytes(byte_array[9:10], byteorder='little', signed=False), "b2":int.from_bytes(byte_array[10:11], byteorder='little', signed=False), "pad2":byte_array[11:12], 
                            "normal0":int.from_bytes(byte_array[12:14], byteorder='little', signed=False), "vertex0":int.from_bytes(byte_array[14:16], byteorder='little', signed=False), 
                            "normal1":int.from_bytes(byte_array[16:18], byteorder='little', signed=False), "vertex1":int.from_bytes(byte_array[18:20], byteorder='little', signed=False), 
                            "normal2":int.from_bytes(byte_array[20:22], byteorder='little', signed=False), "vertex2":int.from_bytes(byte_array[22:24], byteorder='little', signed=False)}
                        prim_block_inner_obj.append(lsc3vntgg)
                
                elif prim_d_b[0] == f'render_15':
                    for prim_db in prim_d_b[1]:
                        byte_array = b''.join(prim_db)
                        lsc3vgt = {"lsc3vgt":b'\x09\x06\x00\x34', 
                            "u0":(int.from_bytes(byte_array[0:1], byteorder='little', signed=False) / 256), "v0":(int.from_bytes(byte_array[1:2], byteorder='little', signed=False) / 256), "cba":byte_array[2:4], 
                            "u1":(int.from_bytes(byte_array[4:5], byteorder='little', signed=False) / 256), "v1":(int.from_bytes(byte_array[5:6], byteorder='little', signed=False) / 256), "tsb":byte_array[6:8], 
                            "u2":(int.from_bytes(byte_array[8:9], byteorder='little', signed=False) / 256), "v2":(int.from_bytes(byte_array[9:10], byteorder='little', signed=False) / 256), "pad0":byte_array[10:12], 
                            "normal0":int.from_bytes(byte_array[12:14], byteorder='little', signed=False), "vertex0":int.from_bytes(byte_array[14:16], byteorder='little', signed=False), 
                            "normal1":int.from_bytes(byte_array[16:18], byteorder='little', signed=False), "vertex1":int.from_bytes(byte_array[18:20], byteorder='little', signed=False), 
                            "normal2":int.from_bytes(byte_array[20:22], byteorder='little', signed=False), "vertex2":int.from_bytes(byte_array[22:24], byteorder='little', signed=False)}
                        prim_block_inner_obj.append(lsc3vgt)
                
                elif prim_d_b[0] == f'render_16':
                    for prim_db in prim_d_b[1]:
                        byte_array = b''.join(prim_db)
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
                    for prim_db in prim_d_b[1]:
                        byte_array = b''.join(prim_db)
                        lsc4vntgs = {"lsc4vntgs": b'\x08\x05\x00\x38', 
                            "r0":int.from_bytes(byte_array[0:1], byteorder='little', signed=False), "g0":int.from_bytes(byte_array[1:2], byteorder='little', signed=False), "b0":int.from_bytes(byte_array[2:3], byteorder='little', signed=False), "pad0":int.from_bytes(byte_array[3:4], byteorder='little', signed=False), 
                            "normal0":int.from_bytes(byte_array[4:6], byteorder='little', signed=False), "vertex0":int.from_bytes(byte_array[6:8], byteorder='little', signed=False), 
                            "normal1":int.from_bytes(byte_array[8:10], byteorder='little', signed=False), "vertex1":int.from_bytes(byte_array[10:12], byteorder='little', signed=False), 
                            "normal2":int.from_bytes(byte_array[12:14], byteorder='little', signed=False), "vertex2":int.from_bytes(byte_array[14:16], byteorder='little', signed=False), 
                            "normal3":int.from_bytes(byte_array[16:18], byteorder='little', signed=False), "vertex3":int.from_bytes(byte_array[18:20], byteorder='little', signed=False)}
                        prim_block_inner_obj.append(lsc4vntgs)
                
                elif prim_d_b[0] == f'render_18':
                    for prim_db in prim_d_b[1]:
                        byte_array = b''.join(prim_db)
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
                    for prim_db in prim_d_b[1]:
                        byte_array = b''.join(prim_db)
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
                    for prim_db in prim_d_b[1]:
                        byte_array = b''.join(prim_db)
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
                    for prim_db in prim_d_b[1]:
                        byte_array = b''.join(prim_db)
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
                    for prim_db in prim_d_b[1]:
                        byte_array = b''.join(prim_db)
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
                    for prim_db in prim_d_b[1]:
                        byte_array = b''.join(prim_db)
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
                    for prim_db in prim_d_b[1]:
                        byte_array = b''.join(prim_db)
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

        total_objects_last = len(primitive_block_dict)
        total_prims_depacked = []
        for test_total in primitive_block_dict:
            total_prims_depacked.append(len(test_total))
        sum_prims_depacked = sum(total_prims_depacked)
        print(f'Number of Depacked Primitives: {sum_prims_depacked}, Number of Total Primitives: {total_original_primitives}, Total Objects: {total_objects_last}')
        if sum_prims_depacked != total_original_primitives:
            print(f'ERROR - Number of Primitives is not equal, report this bug')
            exit()

########################################
#### VERTEX DECODER AND INDEX FIXER #### # HERE I WILL CALCULATE THE NEW VERTEX INDEX, UPDATE IT AND ALSO THE REAL VERTEX TO BE USED IN THE MODELS
########################################
class CustomTmdVertexFixer:
    def __init__(self):
        self.self = CustomTmdVertexFixer

    def vertex_decoder_index_fix(self):
        primitive_index_fix = primitive_block_dict
        vertex_original = custom_tmd_structure.cvertex_block_byte # This is the original Block byte of Vertex
        vertex_num_original = custom_tmd_structure.cvertex_number_int # This is the total number of Vertices in the model
        vertex_num_sum = sum(vertex_num_original)
        print(f'Total Number of Vertices in the CTMD: {vertex_num_original} == {vertex_num_sum}')

        obj_number = 0
        for prims_inside_obj in primitive_index_fix:
            vertex_inside_obj = []
            if len(prims_inside_obj) == 0:
                print(prims_inside_obj)
            else:
                prim_number_inside = 0
                for prims_inside in prims_inside_obj:
                    if prims_inside.get('vertex3') != None:
                        index_0_4 = prims_inside.get('vertex0')
                        index_1_4 = prims_inside.get('vertex1')
                        index_2_4 = prims_inside.get('vertex2')
                        index_3_4 = prims_inside.get('vertex3')
                        if (index_0_4 > 1000) or (index_1_4 > 1000) or (index_2_4 > 1000) or (index_3_4 > 1000):
                            #pass
                            print(f'Abnormmal Values found in Object Number: {obj_number}, Primitive Number: {prim_number_inside}\nDetail Prim: {prims_inside}\nDetail Index: {index_0_4}, {index_1_4}, {index_2_4}, {index_3_4}')
                    else:
                        index_0 = prims_inside.get('vertex0')
                        index_1 = prims_inside.get('vertex1')
                        index_2 = prims_inside.get('vertex2')
                        if (index_0 > 1000) or (index_1 > 1000) or (index_2 > 1000):
                            #pass
                            print(f'Abnormmal Values found in Object Number: {obj_number}, Primitive Number: {prim_number_inside}\nDetail Prim: {prims_inside}\nDetail Index: {index_0}, {index_1}, {index_2}')
                    prim_number_inside += 1
            obj_number += 1
