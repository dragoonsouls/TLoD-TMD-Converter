"""

Custom TMD Structure Reader: This module read the Custom TMD structure data to be used
split from the header, because this module has to be very flexible and easy to update

Copyright (C) 2021 DooMMetaL

"""

import custom_tmd
import itertools


""" KEEP IN MIND:
THE CUSTOM TMD'S HAVE DIFFERENCE IN LEGTH OF READING, THE VERTEX BLOCK -EACH VERTEX-
INSTEAD OF HAVE 8 BYTES LENGTH, IN CUSTOM TMD HAVE 4, SO FOR EXAMPLE

X ; Y
Z ; IGNORED

STANDARD TMD

00 01 ; 20 AB
CC 8F ; 00 00

CUSTOM TMD

40 ; 8A
EC ; 0A (AND YES THE "IGNORED" PAD_VERTEX HAVE A NUMBER IN REALATION WITH THE MAXIMUM VERTEX NUMBER PER OBJECT, USUALLY THE HALF OF THE MAXIMUM)

"""

class CustomTmdStructure:
    def __init__(self,  c_object_list):#, c_object_list_conversion, c_vertex_block_read, c_normal_block_read, c_primitive_block_read):
        self.self = CustomTmdStructure
        self.c_object_list = c_object_list
    
    def c_object_list_reader(self): # READ THE DATA FROM THE OBJECT TABLE AND SPLIT IT IN OBJECT NUMBER
        with open(custom_tmd.custom_tmd_file, 'rb') as custom_object_reader:
            custom_object_reader.seek(custom_tmd.last_mark_location_c)
            custom_object_table_read = custom_tmd.ctmd_nobj_expected * 28 # TOTAL OBJECT TABLE READING LENGTH
            custom_object_table = custom_object_reader.read(custom_object_table_read) # HERE IS READING THE TABLE IN GOOD SHAPE

            global custom_object_data
            custom_object_data = [] # OBJECT DATA SPLIT IN OBJECTS LENGTH (28 BYTES)
            
            custom_object_count = custom_tmd.ctmd_nobj_expected
            start_counter = 0
            end_counter = 28
            while custom_object_count > 0:
                c_object_row = custom_object_table[start_counter:end_counter]
                custom_object_data.append(c_object_row)
                start_counter += 28
                end_counter += 28
                custom_object_count -= 1
    
    def c_object_list_converter(self):
        cvertex_address_bytes = []
        cvertex_number_bytes = []
        cnormal_address_bytes = []
        cnormal_number_bytes = []
        cprimitive_address_bytes = []
        cprimitive_number_bytes = []

        for single_object in custom_object_data: # THE LAST VALUE - SCALE - IS IGNORED CORRESPONDING TO VALUE single_object[24:28]
            cvertex_address_bytes.append(single_object[0:4])
            cvertex_number_bytes.append(single_object[4:8])
            cnormal_address_bytes.append(single_object[8:12])
            cnormal_number_bytes.append(single_object[12:16])
            cprimitive_address_bytes.append(single_object[16:20])
            cprimitive_number_bytes.append(single_object[20:24])

        global cvertex_address_int
        global cvertex_number_int
        global cnormal_address_int
        global cnormal_number_int
        global cprimitive_address_int
        global cprimitive_number_int
        global cprimitive_next_addres_int # NEED THIS VALUES BECAUSE PRIMITIVES ARE NOT SO REGULAR TO DIVIDE EFFICIENTLY THE BLOCKS??? is this good???

        cvertex_address_int = []
        cvertex_number_int = []

        cnormal_address_int = []
        cnormal_number_int = []

        cprimitive_address_int = []
        cprimitive_number_int = []

        for cvertex_add_bin in cvertex_address_bytes:
            cv_a_b = int.from_bytes(cvertex_add_bin, 'little')
            cvertex_address_int.append(cv_a_b)
        
        for cvertex_num_bin in cvertex_number_bytes:
            cv_n_b = int.from_bytes(cvertex_num_bin, 'little')
            cvertex_number_int.append(cv_n_b)
        
        for cnormal_add_bin in cnormal_address_bytes:
            cn_a_b = int.from_bytes(cnormal_add_bin, 'little')
            cnormal_address_int.append(cn_a_b)
        
        for cnormal_num_bin in cnormal_number_bytes:
            cn_n_b = int.from_bytes(cnormal_num_bin, 'little')
            cnormal_number_int.append(cn_n_b)
        
        for cprimitive_add_bin in cprimitive_address_bytes:
            cp_a_b = int.from_bytes(cprimitive_add_bin, 'little')
            cprimitive_address_int.append(cp_a_b)
        
        for cprimitive_num_bin in cprimitive_number_bytes:
            cp_n_b = int.from_bytes(cprimitive_num_bin, 'little')
            cprimitive_number_int.append(cp_n_b)
        
        # THIS PRINT OF ALL THE ADDRESS AND NUMBERS COULD BE USEFUL IN THE NEXT FILES

        global cvertex_addnum_zip
        global cnormal_addnum_zip
        global cprimitive_addnum_zip

        cvertex_addnum_zip = zip(cvertex_address_int, cvertex_number_int)
        cnormal_addnum_zip = zip(cnormal_address_int, cnormal_number_int)
        cprimitive_next_add = cprimitive_address_int.copy()
        cprimitive_next_address_int = cprimitive_next_add[1:]
                
        counter_value = 1
        while counter_value > 0:
            last_value = cvertex_address_int[0] # THE FIRST VERTEX ADDRESS IS EQUAL TO THE LAST VALUE FOR PRIMITIVE
            cprimitive_next_address_int.append(last_value)
            counter_value -= 1

        cprimitive_addnum_zip = zip(cprimitive_address_int, cprimitive_next_address_int, cprimitive_number_int) # NEED THIS VALUES BECAUSE PRIMITIVES ARE NOT SO REGULAR TO DIVIDE EFFICIENTLY THE BLOCKS
        
        # TOTAL NUMBERS OF VERTEX/NORMAL/PRIMITIVE IN THE WHOLE FILE -> THIS IS SEND TO THE WRITER FOR THE INFORMER
        global cvertex_number_total
        global cnormal_number_total
        global cprimitive_number_total
        cvertex_number_accumulated = list(itertools.accumulate(cvertex_number_int))
        cvertex_number_total = cvertex_number_accumulated[(custom_tmd.ctmd_nobj_expected - 1)]
        cnormal_number_accumulated = list(itertools.accumulate(cnormal_number_int))
        cnormal_number_total = cnormal_number_accumulated[(custom_tmd.ctmd_nobj_expected - 1)]
        cprimitive_number_accumulated = list(itertools.accumulate(cprimitive_number_int))
        cprimitive_number_total = cprimitive_number_accumulated[(custom_tmd.ctmd_nobj_expected - 1)]

    def custom_vertex_block_extractor(self):
        with open(custom_tmd.custom_tmd_file, 'rb') as cvertex_block:
            global cvertex_block_byte
            cvertex_block_byte = []
            for cvertex_byte in cvertex_addnum_zip:
                vertex_add = (int(str(cvertex_byte[0:1]).replace("(", "").replace(")", "").replace(",", "")) + custom_tmd.ctmd_start + 12)
                vertex_num = int(str(cvertex_byte[1:2]).replace("(", "").replace(")", "").replace(",", ""))
                vertex_length = vertex_num * 4 # LENGTH OF VERTEX IS 4 BYTES IN CUSTOM TMDS
                cvertex_block.seek(vertex_add)
                vertex_piece = cvertex_block.read(vertex_length)
                cvertex_block_byte.append(vertex_piece)

    def custom_normal_block_extractor(self):
        with open(custom_tmd.custom_tmd_file, 'rb') as cnormal_block:
            global cnormal_block_byte
            cnormal_block_byte = []
            for cnormal_byte in cnormal_addnum_zip:
                normal_add = (int(str(cnormal_byte[0:1]).replace("(", "").replace(")", "").replace(",", "")) + custom_tmd.ctmd_start + 12)
                normal_num = int(str(cnormal_byte[1:2]).replace("(", "").replace(")", "").replace(",", ""))
                normal_length = normal_num * 4 # LENGTH OF NORMAL IS 4 BYTES IN CUSTOM TMDS
                cnormal_block.seek(normal_add)
                normal_piece = cnormal_block.read(normal_length)
                cnormal_block_byte.append(normal_piece)

    def custom_primitive_block_extractor(self):
        with open(custom_tmd.custom_tmd_file, 'rb') as cprimitive_block:
            global cprimitive_block_byte
            cprimitive_block_byte = []
            for cprimitive_byte in cprimitive_addnum_zip:
                primitive_add = (int(str(cprimitive_byte[0:1]).replace("(", "").replace(")", "").replace(",", "")) + custom_tmd.ctmd_start + 12)
                primitive_add_end = (int(str(cprimitive_byte[1:2]).replace("(", "").replace(")", "").replace(",", "")) + custom_tmd.ctmd_start + 12)
                primitive_num = (str(cprimitive_byte[2:3]).replace("(", "").replace(")", "").replace(",", ""))
                primitive_block_length = primitive_add_end - primitive_add
                cprimitive_block.seek(primitive_add)
                primitive_piece = cprimitive_block.read(primitive_block_length)
                cprimitive_block_byte.append(primitive_piece)