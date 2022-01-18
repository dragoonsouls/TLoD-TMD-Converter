"""

Standard TMD Structure Reader: This module read the Standard TMD structure data to be used
split from the header, because this module has to be very flexible and easy to update

Copyright (C) 2021 DooMMetaL

"""

import struct
import standard_tmd # USING THE VARIABLES FROM HERE, DUE TO BE MORE EASY TO CATCH FROM THE GLOBAL SCOPE
import itertools


class StandardTmdStructure:
    def __init__(self, object_list, object_list_conversion, vertex_block_read, normal_block_read, primitive_block_read):
        self.self = StandardTmdStructure
        self.object_list = object_list
        self.object_list_conversion = object_list_conversion
        self.vertex_block_read = vertex_block_read
        self.normal_block_read = normal_block_read
        self.primitive_block_read = primitive_block_read


    def object_list_reader(self): # READ THE DATA FROM THE OBJECT TABLE AND SPLIT IT IN OBJECT NUMBER 
        with open(standard_tmd.tmd_file, 'rb') as object_reader:
            object_reader.seek(standard_tmd.last_mark_location)
            object_table_read = standard_tmd.tmd_nobj_expected * 28 # TOTAL OBJECT TABLE READING LENGTH
            object_table = object_reader.read(object_table_read) # HERE IS READING THE TABLE IN GOOD SHAPE
            
            global object_data
            object_data = [] # OBJECT DATA SPLIT IN OBJECTS LENGTH (28 BYTES)

            object_count = standard_tmd.tmd_nobj_expected
            start_counter = 0
            end_counter = 28
            while object_count > 0:
                object_row = object_table[start_counter:end_counter]
                object_data.append(object_row)
                start_counter += 28
                end_counter += 28
                object_count -= 1

    def object_list_converter(self): # CONVERT THE BINARY DATA INTO INTEGERS AND SPLIT BY OBJECT NUMBER
        vertex_address_bytes = []
        vertex_number_bytes = []
        normal_address_bytes = []
        normal_number_bytes = []
        primitive_address_bytes = []
        primitive_number_bytes = []

        for single_object in object_data: # THE LAST VALUE - SCALE - IS IGNORED CORRESPONDING TO VALUE single_object[24:28]
            vertex_address_bytes.append(single_object[0:4])
            vertex_number_bytes.append(single_object[4:8])
            normal_address_bytes.append(single_object[8:12])
            normal_number_bytes.append(single_object[12:16])
            primitive_address_bytes.append(single_object[16:20])
            primitive_number_bytes.append(single_object[20:24])

        global vertex_address_str
        global vertex_address_int
        global vertex_number_str
        global vertex_number_int
        global normal_address_str
        global normal_address_int
        global normal_number_str
        global normal_number_int
        global primitive_address_str
        global primitive_address_int
        global primitive_number_str
        global primitive_number_int
        global primitive_next_addres_int # NEED THIS VALUES BECAUSE PRIMITIVES ARE NOT SO REGULAR TO DIVIDE EFFICIENTLY THE BLOCKS

        vertex_address_str = []
        vertex_address_int = []
        vertex_number_str = []
        vertex_number_int = []

        normal_address_str = []
        normal_address_int = []
        normal_number_str = []
        normal_number_int = []

        primitive_address_str = []
        primitive_address_int = []
        primitive_number_str = []
        primitive_number_int = []

        

        for vertex_add_bin in vertex_address_bytes:
            vertex_address_raw = struct.unpack('<I', vertex_add_bin)
            vertex_address_corrected = str(vertex_address_raw).replace("(", "").replace(")", "").replace(",", "")
            vertex_address_integer = int(vertex_address_corrected)
            vertex_address_str.append(vertex_address_corrected)
            vertex_address_int.append(vertex_address_integer)
        
        for vertex_num_bin in vertex_number_bytes:
            vertex_number_raw = struct.unpack('<I', vertex_num_bin)
            vertex_number_corrected = str(vertex_number_raw).replace("(", "").replace(")", "").replace(",", "")
            vertex_number_integer = int(vertex_number_corrected)
            vertex_number_str.append(vertex_number_corrected)
            vertex_number_int.append(vertex_number_integer)
            
        for normal_add_bin in normal_address_bytes:
            normal_address_raw = struct.unpack('<I', normal_add_bin)
            normal_address_corrected = str(normal_address_raw).replace("(", "").replace(")", "").replace(",", "")
            normal_address_integer = int(normal_address_corrected)
            normal_address_str.append(normal_address_corrected)
            normal_address_int.append(normal_address_integer)

        for normal_num_bin in normal_number_bytes:
            normal_number_raw = struct.unpack('<I', normal_num_bin)
            normal_number_corrected = str(normal_number_raw).replace("(", "").replace(")", "").replace(",", "")
            normal_number_integer = int(normal_number_corrected)
            normal_number_str.append(normal_number_corrected)
            normal_number_int.append(normal_number_integer)

        for primitive_add_bin in primitive_address_bytes:
            primitive_address_raw = struct.unpack('<I', primitive_add_bin)
            primitive_address_corrected = str(primitive_address_raw).replace("(", "").replace(")", "").replace(",", "")
            primitive_address_integer = int(primitive_address_corrected)
            primitive_address_str.append(primitive_address_corrected)
            primitive_address_int.append(primitive_address_integer)

        for primitive_num_bin in primitive_number_bytes:
            primitive_number_raw = struct.unpack('<I', primitive_num_bin)
            primitive_number_corrected = str(primitive_number_raw).replace("(", "").replace(")", "").replace(",", "")
            primitive_number_integer = int(primitive_number_corrected)
            primitive_number_str.append(primitive_number_corrected)
            primitive_number_int.append(primitive_number_integer)
        
        global vertex_addnum_zip
        global normal_addnum_zip
        global primitive_addnum_zip

        vertex_addnum_zip = zip(vertex_address_int, vertex_number_int)
        normal_addnum_zip = zip(normal_address_int, normal_number_int)
        primitive_next_add = primitive_address_int.copy()
        primitive_next_address_int = primitive_next_add[1:]
                
        counter_value = 1
        while counter_value > 0:
            last_value = vertex_address_int[0] # THE FIRST VERTEX ADDRESS IS EQUAL TO THE LAST VALUE FOR PRIMITIVE
            primitive_next_address_int.append(last_value)
            counter_value -= 1

        primitive_addnum_zip = zip(primitive_address_int, primitive_next_address_int, primitive_number_int) # NEED THIS VALUES BECAUSE PRIMITIVES ARE NOT SO REGULAR TO DIVIDE EFFICIENTLY THE BLOCKS
        
        # TOTAL NUMBERS OF VERTEX/NORMAL/PRIMITIVE IN THE WHOLE FILE -> THIS IS SEND TO THE WRITER FOR THE INFORMER
        global vertex_number_total
        global normal_number_total
        global primitive_number_total
        vertex_number_accumulated = list(itertools.accumulate(vertex_number_int))
        vertex_number_total = vertex_number_accumulated[(standard_tmd.tmd_nobj_expected - 1)]
        normal_number_accumulated = list(itertools.accumulate(normal_number_int))
        normal_number_total = normal_number_accumulated[(standard_tmd.tmd_nobj_expected - 1)]
        primitive_number_accumulated = list(itertools.accumulate(primitive_number_int))
        primitive_number_total = primitive_number_accumulated[(standard_tmd.tmd_nobj_expected - 1)]






    def vertex_block_extractor(self):                           # EXTRACT THE VERTEX BLOCK FOR EACH OBJECT AND LATER BEING TRANSLATED TO A BLOCK
        with open(standard_tmd.tmd_file, 'rb') as vertex_block:
            global vertex_block_byte
            vertex_block_byte = []
            for vertex_byte in vertex_addnum_zip:
                vertex_add = (int(str(vertex_byte[0:1]).replace("(", "").replace(")", "").replace(",", "")) + standard_tmd.tmd_start + 12)
                vertex_num = int(str(vertex_byte[1:2]).replace("(", "").replace(")", "").replace(",", ""))
                vertex_length = vertex_num * 8 # !!!!FOR CUSTOM THIS VALUE MUST CHANGE!!!!
                vertex_block.seek(vertex_add)
                vertex_piece = vertex_block.read(vertex_length)
                vertex_block_byte.append(vertex_piece)

    def normal_block_extractor(self):
        with open(standard_tmd.tmd_file, 'rb') as normal_block:
            global normal_block_byte
            normal_block_byte = []
            for normal_byte in normal_addnum_zip:
                normal_add = (int(str(normal_byte[0:1]).replace("(", "").replace(")", "").replace(",", "")) + standard_tmd.tmd_start + 12)
                normal_num = int(str(normal_byte[1:2]).replace("(", "").replace(")", "").replace(",", ""))
                normal_length = normal_num * 8 # !!!!FOR CUSTOM THIS VALUE MUST CHANGE!!!!
                normal_block.seek(normal_add)
                normal_piece = normal_block.read(normal_length)
                normal_block_byte.append(normal_piece)
    
    def primitive_block_extractor(self):
        with open(standard_tmd.tmd_file, 'rb') as primitive_block:
            global primitive_block_byte
            primitive_block_byte = []
            for primitive_byte in primitive_addnum_zip:
                primitive_add = (int(str(primitive_byte[0:1]).replace("(", "").replace(")", "").replace(",", "")) + standard_tmd.tmd_start + 12)
                primitive_add_end = (int(str(primitive_byte[1:2]).replace("(", "").replace(")", "").replace(",", "")) + standard_tmd.tmd_start + 12)
                primitive_num = (str(primitive_byte[2:3]).replace("(", "").replace(")", "").replace(",", ""))
                primitive_block_length = primitive_add_end - primitive_add
                primitive_block.seek(primitive_add)
                primitive_piece = primitive_block.read(primitive_block_length)
                primitive_block_byte.append(primitive_piece)
