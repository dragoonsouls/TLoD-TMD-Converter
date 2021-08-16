"""

TMD Reader: This module read the TMD header data
to be used

TMD Structure: this function is for work with the TMD files itself.
For more information about how the TMD files internally are,
you can check this: https://imgur.com/a/OAgQDrO, a very graphic
explanation on how is the file structure

TMD LoD OBJ Writer
Here we got the writer of the files

Copyright (C) 2021 DooMMetaL

"""
import os
import sys
import argparse
from struct import *
from tmd_lod_config import *
from itertools import accumulate
from decimal import *

# Magic numbers used in most of the TMD Files

TMD_HEADER = b'A\x00\x00\x00' # Version 1.0, but also i found some headers like 41 00 00 01 or 41 01 00 00 which i don't know what it means


# Class itself

class MyTmdReader:
    def __init__(self):
        self.self = MyTmdReader
    
    def file_reader(self):
        
        try:
            print("Please, write the full path to the TMD file: ")
            global tmd_file
            input_path = input()
            tmd_file = input_path
        except OSError:
            print(tmd_file, " is not a valid path, exiting")
            exit()

        with open(tmd_file, 'rb') as readfile:
            all_file = readfile.read()
            tmd_start = all_file.find(TMD_HEADER) # Here will find the last 0x 41 00 00 00 this maybe can fail, have to check with other files
            readfile.seek(tmd_start)
            tmd_read_header = readfile.read(4) # Here is reading the header itself
            if tmd_read_header == TMD_HEADER:
                print("This is a TMD File")
            else:
                print("This is not a TMD File, exiting")
                exit()
            global last_mark_location
            global tmd_nobj_expected
            tmd_clut_prop = readfile.read(4) # Here i obtain the TMD - CLUT property values / FLAGS
            tmd_nobj_info = readfile.read(4) # Here i obtain the TMD Number of Objects in file
            tmd_nobj_info_int = unpack('<L', tmd_nobj_info) # Here is a conversion to list mode, for easy reading for the user
            tmd_nobj_expected_list = list(tmd_nobj_info)[0:1]
            tmd_nobj_extract = [str(integer) for integer in tmd_nobj_expected_list]
            join_nobj_str = "".join(tmd_nobj_extract)
            tmd_nobj_expected = int(join_nobj_str) # Here i get the NObj as integer for he use on the TMD Structure Class
            print("This TMD file have: ", ''.join(str(tmd_nobj_info_int)).replace("(", "").replace(")", "").replace(",", ""), " Objects inside")
            print("Remember that TMD objects have textured and untextured faces, that all part from the same object")
            last_mark_location = all_file.find(tmd_nobj_info) + 4 # This i need to use the continue reading for the structure Class
        
class TmdStructure:
    def __init__(self, object_list, object_separator):
        self.self = TmdStructure
        self.object_list = object_list

    
    def object_list_reader(self):
        with open(tmd_file, 'rb') as file_structure:
            file_reading = file_structure.read()
            tmd_begin = file_reading.find(TMD_HEADER)
            file_structure.seek(tmd_begin)
            tmd_read_head = file_structure.read(4)
            file_structure.seek(tmd_begin + 12)
            try:
                if tmd_read_head == TMD_HEADER:
                    length_of_read = 4 * 7 * tmd_nobj_expected # This take the max length of bytes in the NObj Block 
                    print("The NObj Bytes length is:", length_of_read, "(28 Bytes per object in Default in TMD files)")
                    global nobj_list_total
                    nobj_list = bytearray(list(file_structure.read(length_of_read))) # Here i take all the NObj block as a single ByteArray list
                    nobj_list_total = [nobj_list[0:28]]
                    counting_index = length_of_read
                    start_index_count = 0
                    end_index_count = 28
                    while end_index_count < counting_index:
                        start_index_count += 28
                        end_index_count += 28
                        block_data = nobj_list[start_index_count:end_index_count]
                        nobj_list_total.append(block_data)
                     #print(block_data)             
                    #print(nobj_list)
                    #print(nobj_list_total)
                else:
                    print("Nothing to do")
            except ValueError:
                print("are not the expected values")
                exit()

    def object_list_number(self): # Here i obtain the Bytearray enumerated
        global n_objects_num
        n_objects_num = []
        for data_number in enumerate(nobj_list_total):
            n_objects_num.append(data_number)
        #print(n_objects_num)    

    def data_property_reader(self): # Note ACTUALLY THE PRIMITIVES ARE NOT SUPPORTED OR IMPLEMENTED FURTHER ON THE CODE,
        primitives = []             # when i figure out what's going on with that, i will add them, SO FOR NOW,
        normals = []                # ONLY WILL SHOW PROPERTIES FROM THEM
        vertices = []
        for data in nobj_list_total:
            vertices_data, normals_data, primitives_data, long_scale = data[0:8], data[8:16], data[16:24], data[24:28] #Long_Scale data is ignored
            vertices.append(vertices_data), normals.append(normals_data), primitives.append(primitives_data)
            #print(vertices_data, normals_data, primitives_data)
        #print(vertices, normals, primitives)
        
        # VERTEX PROPERTIES
        global vertices_address
        global total_vertices_number
        global vertices_number
        vertices_number = []
        vertices_address = []
        for vertices_prop in vertices: # Here i split the Vertex Data in two, to later use them separately
            vertices_hexposition, vertices_quantity = vertices_prop[0:4], vertices_prop[4:8]
            vertices_quantity_int = unpack('<L', vertices_quantity)
            vertices_str = str(vertices_quantity_int).replace("(", "").replace(")", "").replace(",", "")
            vertices_clean = int(vertices_str)
            vertices_number.append(vertices_clean)
            vertices_address.append(vertices_hexposition)
        total_vertices_number = sum(vertices_number)
        #print(vertices_number)
        #print(total_vertices_number)

        # NORMAL PROPERTIES
        global normals_address
        global total_normals_number
        global normals_number
        normals_number = []
        normals_address = []
        for normals_prop in normals:
            normals_hexposition, normals_quantity = normals_prop[0:4], normals_prop[4:8]
            normals_quantity_int = unpack('<L', normals_quantity)
            normals_str = str(normals_quantity_int).replace("(", "").replace(")", "").replace(",", "")
            normals_clean = int(normals_str)
            normals_number.append(normals_clean)
            normals_address.append(normals_hexposition)
        total_normals_number = sum(normals_number)
        #print(normals_number)
        
        # PRIMITIVE PROPERTIES
        global primitives_address
        global total_primitives_number
        global primitives_number
        primitives_number = []
        primitives_address = []
        for primitives_prop in primitives:
            primitives_hexposition, primitives_quantity = primitives_prop[0:4], primitives_prop[4:8]
            primitives_quantity_int = unpack('<L', primitives_quantity)
            primitives_str = str(primitives_quantity_int).replace("(", "").replace(")", "").replace(",", "")
            primitives_clean = int(primitives_str)
            primitives_number.append(primitives_clean)
            primitives_address.append(primitives_hexposition)
        total_primitives_number = sum(primitives_number)
        #print(primitives_number)

        # ZIP of previous properties
        
        zip_properties = zip(vertices_number, normals_number, primitives_number)
        #print(list(zip_properties))

        # Enumerating the properties
        global tmd_objects_properties
        tmd_objects_properties = []
        for object_properties in enumerate(zip_properties):
            tmd_objects_properties.append(object_properties)
        #print(list(tmd_objects_properties))

    def data_property_show(self): # Casting ON SCREEN and a REPORT TXT FILE of the TMD properties and other interesting stuff
        for object_number, values in tmd_objects_properties:
            print("In Object number:", object_number)
            print("We have: ", "- Vertices: ", str(values[0:1]).replace("(", "").replace(")", "").replace(",", ""), " - Normals: ", str(values[1:2]).replace("(", "").replace(")", "").replace(",", ""), " - Primitives: ", str(values[2:3]).replace("(", "").replace(")", "").replace(",", ""))
        with open((tmd_file).strip('.bin') + ".txt", 'w') as file_report:
            file_name_first = "This report file is extracted from " + tmd_file.center(4) + " Using TMD_2_Obj, by DooMMetaL" + "\n" + "\n" + "\n"
            file_report.write(file_name_first)
            for object_number, values in tmd_objects_properties:
                obj_num = "In Object number:" + str(object_number) + "\n"
                val = "We have: " + "- Vertices: " + str(values[0:1]).replace("(", "").replace(")", "").replace(",", "") + " " + " - Normals: " + " " + str(values[1:2]).replace("(", "").replace(")", "").replace(",", "") + " " + " - Primitives: " + " " + str(values[2:3]).replace("(", "").replace(")", "").replace(",", "") + "\n" + "\n"
                file_report.write(obj_num)
                file_report.write(val)
            finish_text = "Total number of Vertices: " + str(total_vertices_number) + "\n" + "Total number of Normals: " + str(total_normals_number) + "\n" + "Total number of Primitives: " + str(total_primitives_number)
            file_report.write(finish_text)
        print("Total number of Vertices: ", total_vertices_number, " Total number of Normals: ", total_normals_number, " Total number of Primitives: ", total_primitives_number)

    def address_conversion(self): # This function will convert to a legible address to use in seek(), using as zip to do it all in same time
        # VERTEX ADRESSES
        global vertices_in_obj
        vertices_in_obj = []
        for vertices_pos in vertices_address: # Here i obtain the Vertices Addresses in Integer form
            vertices_pos_int = unpack('<L', vertices_pos)
            vertices_pos_str = str(vertices_pos_int).replace("(", "").replace(")", "").replace(",", "")
            vertices_pos_clean = int(vertices_pos_str)
            vertices_in_obj.append(vertices_pos_clean)
        #print(vertices_in_obj)

        #NORMAL ADDRESSES
        global normals_in_obj
        normals_in_obj = []
        for normals_pos in normals_address:
            normals_pos_int = unpack('<L', normals_pos)
            normals_pos_str = str(normals_pos_int).replace("(", "").replace(")", "").replace(",", "")
            normals_pos_clean = int(normals_pos_str)
            normals_in_obj.append(normals_pos_clean)
        #print(normals_in_obj)

        # PRIMITIVE ADDRESSES + NEXT PRIMITIVE ADDRESS
        global primitives_in_obj
        global prim_in_obj_and_length
        primitives_in_obj = []
        for primitives_pos in primitives_address:
            primitives_pos_int = unpack('<L', primitives_pos)
            primitives_pos_str = str(primitives_pos_int).replace("(", "").replace(")", "").replace(",", "")
            primitives_pos_clean = int(primitives_pos_str)
            primitives_in_obj.append(primitives_pos_clean)
        next_primitive_in_obj = primitives_in_obj[1::1]
        prev_primitive_in_obj = primitives_in_obj[0::1]
        zip_primitive_length = zip(prev_primitive_in_obj, next_primitive_in_obj)
        difference_length_primitives = []
        for next_value, prev_value in zip_primitive_length:
            difference_length_primitives.append(prev_value - next_value)
        last_primitive_value = primitives_in_obj[-1]
        first_vertex_value = vertices_in_obj[0]
        last_length_primitive = first_vertex_value - last_primitive_value
        difference_length_primitives.append(last_length_primitive)
        prim_in_obj_and_length = zip(primitives_in_obj, difference_length_primitives)
        #print(primitives_in_obj)
        #print(next_primitive_in_obj)
        #print(prev_primitive_in_obj)
        #print(list(zip_primitive_length))
        #print(last_primitive_value, first_vertex_value, last_length_primitive)
        #print(difference_length_primitives)
        #print(list(prim_in_obj_and_length))

        # ZIPPED VALUES - addlen [ADDRESSES - LENGTH] -
        global addlen_vertices_zipped
        global addlen_normals_zipped
        global addlen_primitives_zipped # Actually Not used or implemented until i figure out how the custom Primitives work
        addlen_vertices_zipped = zip(vertices_in_obj, vertices_number)
        addlen_normals_zipped = zip(normals_in_obj, normals_number)
        addlen_primitives_zipped = zip(primitives_in_obj, primitives_number)
        #print(list(addlen_vertices_zipped))

class Obj_Writer:
    def __init__(self, write_to_file):
        self.self = Obj_Writer
        self.write_to_file = write_to_file

    def read_from_address(self):
        with open(tmd_file, 'rb') as reading_address:
            file_reading_all = reading_address.read()
            tmd_begin = file_reading_all.find(TMD_HEADER)
            reading_address.seek(tmd_begin)
            tmd_read_head = reading_address.read(4)
            reading_address.seek(tmd_begin + 12) # This is starting position
            tmd_start = (tmd_begin + 12) # This is the starting position for seek() reset

            # VERTEX ADDRESS READING
            global vertices_block
            vertices_block = []
            for vertices_add, vertices_len in addlen_vertices_zipped:
                reading_address.seek(vertices_add + tmd_start)
                length_of_read = vertices_len * 8
                vertices = reading_address.read(length_of_read)
                start_vertex = vertices[0:8]
                vertices_block.append(start_vertex)
                end_of_count = length_of_read
                start_index_count = 0
                end_index_count = 8
                while end_index_count < end_of_count:
                    start_index_count += 8
                    end_index_count += 8
                    vertex_sep = vertices[start_index_count: end_index_count]
                    vertices_block.append(vertex_sep)
            #print(list(enumerate(list(vertices_block))))

            # NORMAL ADDRESS READING
            global normals_block
            normals_block = []
            for normals_add, normals_len in addlen_normals_zipped:
                reading_address.seek(normals_add + tmd_start)
                length_of_read = normals_len * 8
                normals = reading_address.read(length_of_read)
                start_normal = normals[0:8]
                normals_block.append(start_normal)
                end_of_count = length_of_read
                start_index_count = 0
                end_index_count = 8
                while end_index_count < end_of_count:
                    start_index_count += 8
                    end_index_count += 8
                    normal_sep = normals[start_index_count: end_index_count]
                    normals_block.append(normal_sep)
            #print(list(enumerate(normals_block)))

            # PRIMITIVES ADDRESS READING
            # Primitives use u_char and are different in length so i have to make another function here
            global primitives_block
            global primitives_block_enum # I will split the primitives into objects pieces to look how they behave
            global primitives_block_enum_2 # Copy to test
            global primitives_block_enum_tc # This is a Copy for using in the Texture Coordinate calculation
            primitives_block = []
            for primitives_add, primitives_len in prim_in_obj_and_length: # Here i got the actual address and length of each value
                reading_address.seek(primitives_add + tmd_start) # Seek position correct
                block_of_read = reading_address.read(primitives_len)
                primitives_block.append(block_of_read)
                #print(primitives_add, primitives_len)
            primitives_block_enum = enumerate(primitives_block)
            primitives_block_enum_2 = enumerate(primitives_block)
            primitives_block_enum_tc = enumerate(primitives_block)
            #print(list(enumerate(primitives_block)))
            #print(list(primitives_block_enum))
                
    
    def obj_converter(self):
        with open((tmd_file).strip('.bin') + ".obj", 'w') as file_write:
            first_name_file = "# " + "This OBJ is extracted from " + tmd_file.center(4) + " Using TMD_2_Obj, by DooMMetaL" + "\n" + "\n" + "\n"
            file_write.write(first_name_file)
            mat_lib = "mtllib" + " " + ((tmd_file).strip('.bin') + ".mtl") + "\n" + "\n"
            file_write.write(mat_lib)

            # VERTEX WRITER
            vertex_info = "# Here start the Vertex Block of the model" + "\n" + "\n"
            file_write.write(vertex_info)
            vertex_splitted = []
            for vertex in vertices_block:
                v_x = vertex[0:2]
                v_y = vertex[2:4]
                v_z = vertex[4:6]
                short_pad = vertex[6:8] # This is ignored in the model
                ver_x = unpack('<h', v_x) #int.from_bytes(v_x, byteorder='little', signed=True) #unpack('<h', v_x)
                ver_y = unpack('<h', v_y) #int.from_bytes(v_y, byteorder='little', signed=True) #unpack('<h', v_y)
                ver_z = unpack('<h', v_z) #int.from_bytes(v_z, byteorder='little', signed=True) #unpack('<h', v_z)
                vertex_each = [ver_x, ver_y, ver_z]
                vertex_splitted.append(vertex_each)
                #print(vertex)
            for vertex_x, vertex_y, vertex_z in vertex_splitted:
                vert_x = str(vertex_x).replace("(", "").replace(")", "").replace(",", "")
                vert_y = str(vertex_y).replace("(", "").replace(")", "").replace(",", "")
                vert_z = str(vertex_z).replace("(", "").replace(")", "").replace(",", "")
                vertex_x = str(float(int(vert_x) / 1000))
                vertex_y = str(float(int(vert_y) / 1000))
                vertex_z = str(float(int(vert_z) / 1000))
                v = "v" + " " + vertex_x + " " + vertex_y + " " + vertex_z + " " + str(1.0) + "\n"
                file_write.write(v)
                #print(v_x, v_y, v_z)
            number_of_vertices = len(vertices_block)
            file_write.write("# " + str(number_of_vertices) + " " + "Vertices" + "\n" + "\n")

            # TEXTURE COORDINATE WRITER
            global texture_coordinate_num # HERE IS THE VALUE TO CALCULATE
            global tc_total # TOTAL VT COORDINATES IN THE FILE 
            texture_coordinates_info = "# Here start the Texture Coordinates Block of the model" + "\n" + "\n"
            file_write.write(texture_coordinates_info)
            texture_coordinate_num = []
            for numeration_prim, prim_block in primitives_block_enum_tc:
                
                total_count_tc = []
                each_vt_obj = "\n" + "# Texture Coordinates for Object" + " " + str(numeration_prim) + "\n"
                file_write.write(each_vt_obj)

                # Packet Configuration of 3 Vertex Polygon with Light Source Calculation
                lsc_three_vertex_gouraud_textured = b'\x09\x06\x00\x34' # NO FIFTH VALUE to check, FIFTH value correspond to CBA // 3 VERTEX GOURAUD TEXTURED - ok
                lsc_three_vertex_flat_textured = b'\x07\x05\x00\x24' # NO FIFTH VALUE to check, FIFTH value correspond to CBA // 3 VERTEX FLAT TEXTURED - ok
                new_lsc_three_vertex_gouraud = b'\x09\x06\x02\x34' # NEW 3 VERTEX GOURAUD TEXTURED - ok
                new_lsc_three_vertex_gouraud_2 = b'\x09\x06\x00\x36' # NEW 3 VERTEX GOURAUD TEXTURED - ok

                # Packet Configuration for 4 Vertex Polygon with Light Source Calculation
                lsc_four_vertex_gouraud_textured = b'\x0c\x08\x00\x3c' # NO FIFTH VALUE to check, FIFTH value correspond to CBA // 4 VERTEX GOURAUD TEXTURED - ok
                lsc_four_vertex_flat_textured = b'\x09\x07\x00\x2c' # NO FIFTH VALUE to check, FIFTH value to correspond to CBA // 4 VERTEX FLAT TEXTURED - ok
                new_lsc_four_vertex_gouraud_textured = b'\x0c\x08\x00\x3e' # NEW TYPE OF PACKET a 4 VERTEX GOURAUD TEXTURED - ok
                new_lsc_four_vertex_gouraud_textured_2 = b'\x0c\x08\x02\x3c' # NEW TYPE OF PACKET a 4 VERTEX GOURAUD TEXTURED - ok

                # Packet configuration for 3 Vertex Polygon with No Light Source Calculation
                nlsc_three_vertex_gradation_textured = b'\x09\x08\x01\x35' # NO FIFTH VALUE to check, FIFTH value correspond to CBA // 3 VERTEX GRADATION TEXTURED - ok
                nlsc_three_vertex_flat_textured = b'\x07\x06\x01\x25' # NO FIFTH VALUE to check, FIFTH value correspond to CBA // 3 VERTEX FLAT TEXTURED -ok
                new_nlsc_three_vertex_gradation_textured = b'\x09\x08\x01\x37' # NEW TYPE OF PACKET a 3 VERTEX GRADATION TEXTURED - ok

                # Packet Configuration for 4 Vertex Polygon with No Light Source Calculation
                nlsc_four_vertex_gradation_textured = b'\x0c\x0a\x01\x3d' # NO FIFTH VALUE to check, FIFTH value correspond to CBA // 4 VERTEX GRADATION TEXTURED - ok
                nlsc_four_vertex_flat_textured = b'\x09\x07\x01\x2d' # NO FIFTH VALUE to check, FIFTH value correspond to CBA // 4 VERTEX FLAT TEXTURED - ok
                new_nlsc_four_vertex_gradation_textured = b'\x0c\x0a\x01\x3f' # NEW TYPE OF PACKET a 4 VERTEX GRADATION TEXTURED - ok

                # Packet Configuration for Sprites # I WILL IGNORE THIS UNTIL I FOUND SOME TMD THAT USE THIS CONFIGURATION
                sp_1x1 = b'\x04\x02\x01\x6c' # NO FIFTH VALUE to check, FIFTH value correspond to TSB // SPRITE 1X1 
                sp_free_size = b'\x05\x03\x01\x64' # NO FIFTH VALUE to check, FIFTH value correspond to TSB // SPRITE FREE SIZE 
                sp_16x16 = b'\x04\x02\x01\x7c' # NO FIFTH VALUE to check, FIFTH value correspond to TSB // SPRITE 16X16 
                sp_8x8 = b'\x04\x02\x01\x74' # NO FIFTH VALUE to check, FIFTH value correspond to TSB // SPRITE 8X8 

                # Here i will copy all the textured primitives listed later in the file

                ####################################################################################################################

                # Extracting LSC 3 VERTEX GOURAUD TEXTURED // WORKING AS INTENDED
                count_lsc_3v_g_t = prim_block.count(lsc_three_vertex_gouraud_textured)
                position_prim_lsc_3v_g_t = prim_block.find(lsc_three_vertex_gouraud_textured)
                total_count_tc.append(count_lsc_3v_g_t * 3)

                while count_lsc_3v_g_t > 0:
                    count_lsc_3v_g_t -= 1
                    start_position_prim = position_prim_lsc_3v_g_t + 4
                    end_position_prim = start_position_prim + 24
                    primitive_lsc_3v_g_t = prim_block[start_position_prim : end_position_prim]
                    position_prim_lsc_3v_g_t += 28
                    u_0 = primitive_lsc_3v_g_t[0:1] # U value = X in 3D - texture coordinate
                    v_0 = primitive_lsc_3v_g_t[1:2] # V value = Y in 3D - texture coordinate (need 1 - n because is inverted)
                    cba_value = primitive_lsc_3v_g_t[2:4] # CBA = CLUT position of texture in VRAM
                    u_1 = primitive_lsc_3v_g_t[4:5]
                    v_1 = primitive_lsc_3v_g_t[5:6]
                    tsb_value = primitive_lsc_3v_g_t[6:8] # TSB = Information and properties of texture/sprite to be applied to the geometry
                    u_2 = primitive_lsc_3v_g_t[8:9]
                    v_2 = primitive_lsc_3v_g_t[9:10]
                    value_not_used = primitive_lsc_3v_g_t[10:12]
                    normal_0 = primitive_lsc_3v_g_t[12:14]
                    vertex_0 = primitive_lsc_3v_g_t[14:16]
                    normal_1 = primitive_lsc_3v_g_t[16:18]
                    vertex_1 = primitive_lsc_3v_g_t[18:20]
                    normal_2 = primitive_lsc_3v_g_t[20:22]
                    vertex_2 = primitive_lsc_3v_g_t[22:24]

                    u_2_to_num = str(unpack('<B', u_2)).replace("(", "").replace(")", "").replace(",", "")
                    u_2_num = float(u_2_to_num) / 256
                    v_2_to_num = str(unpack('<B', v_2)).replace("(", "").replace(")", "").replace(",", "")
                    v_2_num = float(v_2_to_num) / 256
                    u_1_to_num = str(unpack('<B', u_1)).replace("(", "").replace(")", "").replace(",", "")
                    u_1_num = float(u_1_to_num) / 256
                    v_1_to_num = str(unpack('<B', v_1)).replace("(", "").replace(")", "").replace(",", "")
                    v_1_num = float(v_1_to_num) / 256
                    u_0_to_num = str(unpack('<B', u_0)).replace("(", "").replace(")", "").replace(",", "")
                    u_0_num = float(u_0_to_num) / 256
                    v_0_to_num = str(unpack('<B', v_0)).replace("(", "").replace(")", "").replace(",", "")
                    v_0_num = float(v_0_to_num) / 256

                    # OBJ UV Writer
                    write_UV_lsc_3v_g_t_0 = "vt" + " " + str(u_2_num) + " " + str(1 - v_2_num) + "\n"
                    write_UV_lsc_3v_g_t_1 = "vt" + " " + str(u_1_num) + " " + str(1 - v_1_num) + "\n"
                    write_UV_lsc_3v_g_t_2 = "vt" + " " + str(u_0_num) + " " + str(1 - v_0_num) + "\n"
                    
                    file_write.write(write_UV_lsc_3v_g_t_0)
                    file_write.write(write_UV_lsc_3v_g_t_1)
                    file_write.write(write_UV_lsc_3v_g_t_2)
                    #print(u_0, v_0, "in obj n ", numeration_prim)
                    #print(u_1, v_1, "in obj n ", numeration_prim)
                    #print(u_2, v_2, "in obj n ", numeration_prim)

                ####################################################################################################################

                # Extracting LSC 3 VERTEX FLAT TEXTURED
                count_lsc_3v_f_t = prim_block.count(lsc_three_vertex_flat_textured)
                position_prim_lsc_3v_f_t = prim_block.find(lsc_three_vertex_flat_textured)
                total_count_tc.append(count_lsc_3v_f_t * 3)

                while count_lsc_3v_f_t > 0:
                    count_lsc_3v_f_t -= 1
                    start_position_prim = position_prim_lsc_3v_f_t + 4
                    end_position_prim = start_position_prim + 20
                    primitive_lsc_3v_f_t = prim_block[start_position_prim : end_position_prim]
                    position_prim_lsc_3v_f_t += 24
                    u_0 = primitive_lsc_3v_f_t[0:1]
                    v_0 = primitive_lsc_3v_f_t[1:2]
                    cba_value = primitive_lsc_3v_f_t[2:4]
                    u_1 = primitive_lsc_3v_f_t[4:5]
                    v_1 = primitive_lsc_3v_f_t[5:6]
                    tsb_value = primitive_lsc_3v_f_t[6:8]
                    u_2 = primitive_lsc_3v_f_t[8:9]
                    v_2 = primitive_lsc_3v_f_t[9:10]
                    value_not_used = primitive_lsc_3v_f_t[10:12]
                    normal_0 = primitive_lsc_3v_f_t[12:14]
                    vertex_0 = primitive_lsc_3v_f_t[14:16]
                    vertex_1 = primitive_lsc_3v_f_t[16:18]
                    vertex_2 = primitive_lsc_3v_f_t[18:20]

                    u_2_to_num = str(unpack('<B', u_2)).replace("(", "").replace(")", "").replace(",", "")
                    u_2_num = float(u_2_to_num) / 256
                    v_2_to_num = str(unpack('<B', v_2)).replace("(", "").replace(")", "").replace(",", "")
                    v_2_num = float(v_2_to_num) / 256
                    u_1_to_num = str(unpack('<B', u_1)).replace("(", "").replace(")", "").replace(",", "")
                    u_1_num = float(u_1_to_num) / 256
                    v_1_to_num = str(unpack('<B', v_1)).replace("(", "").replace(")", "").replace(",", "")
                    v_1_num = float(v_1_to_num) / 256
                    u_0_to_num = str(unpack('<B', u_0)).replace("(", "").replace(")", "").replace(",", "")
                    u_0_num = float(u_0_to_num) / 256
                    v_0_to_num = str(unpack('<B', v_0)).replace("(", "").replace(")", "").replace(",", "")
                    v_0_num = float(v_0_to_num) / 256

                    # OBJ UV Writer
                    write_UV_lsc_3v_f_t_0 = "vt" + " " + str(u_2_num) + " " + str(1 - v_2_num) + "\n" # Here i put initially u and v 2
                    write_UV_lsc_3v_f_t_1 = "vt" + " " + str(u_1_num) + " " + str(1 - v_1_num) + "\n" # i won't change this
                    write_UV_lsc_3v_f_t_2 = "vt" + " " + str(u_0_num) + " " + str(1 - v_0_num) + "\n" # here was the u and v 0
                    
                    file_write.write(write_UV_lsc_3v_f_t_0)
                    file_write.write(write_UV_lsc_3v_f_t_1)
                    file_write.write(write_UV_lsc_3v_f_t_2)


                ####################################################################################################################

                # Extracting LSC NEW 3 VERTEX GOURAUD TEXTURED
                count_n_lsc_3v_g_t = prim_block.count(new_lsc_three_vertex_gouraud)
                position_prim_n_lsc_3v_g_t = prim_block.find(new_lsc_three_vertex_gouraud)
                total_count_tc.append(count_n_lsc_3v_g_t * 3)

                while count_n_lsc_3v_g_t > 0:
                    count_n_lsc_3v_g_t -= 1
                    start_position_prim = position_prim_n_lsc_3v_g_t + 4
                    end_position_prim = start_position_prim + 24
                    primitive_n_lsc_3v_g_t = prim_block[start_position_prim : end_position_prim]
                    position_prim_n_lsc_3v_g_t += 28
                    u_0 = primitive_n_lsc_3v_g_t[0:1]
                    v_0 = primitive_n_lsc_3v_g_t[1:2]
                    cba_value = primitive_n_lsc_3v_g_t[2:4]
                    u_1 = primitive_n_lsc_3v_g_t[4:5]
                    v_1 = primitive_n_lsc_3v_g_t[5:6]
                    tsb_value = primitive_n_lsc_3v_g_t[6:8]
                    u_2 = primitive_n_lsc_3v_g_t[8:9]
                    v_2 = primitive_n_lsc_3v_g_t[9:10]
                    value_not_used = primitive_n_lsc_3v_g_t[10:12]
                    normal_0 = primitive_n_lsc_3v_g_t[12:14]
                    vertex_0 = primitive_n_lsc_3v_g_t[14:16]
                    normal_1 = primitive_n_lsc_3v_g_t[16:18]
                    vertex_1 = primitive_n_lsc_3v_g_t[18:20]
                    normal_2 = primitive_n_lsc_3v_g_t[20:22]
                    vertex_2 = primitive_n_lsc_3v_g_t[22:24]

                    u_2_to_num = str(unpack('<B', u_2)).replace("(", "").replace(")", "").replace(",", "")
                    u_2_num = float(u_2_to_num) / 256
                    v_2_to_num = str(unpack('<B', v_2)).replace("(", "").replace(")", "").replace(",", "")
                    v_2_num = float(v_2_to_num) / 256
                    u_1_to_num = str(unpack('<B', u_1)).replace("(", "").replace(")", "").replace(",", "")
                    u_1_num = float(u_1_to_num) / 256
                    v_1_to_num = str(unpack('<B', v_1)).replace("(", "").replace(")", "").replace(",", "")
                    v_1_num = float(v_1_to_num) / 256
                    u_0_to_num = str(unpack('<B', u_0)).replace("(", "").replace(")", "").replace(",", "")
                    u_0_num = float(u_0_to_num) / 256
                    v_0_to_num = str(unpack('<B', v_0)).replace("(", "").replace(")", "").replace(",", "")
                    v_0_num = float(v_0_to_num) / 256

                    # OBJ UV Writer
                    write_UV_n_lsc_3v_g_t_0 = "vt" + " " + str(u_2_num) + " " + str(1 - v_2_num) + "\n"
                    write_UV_n_lsc_3v_g_t_1 = "vt" + " " + str(u_1_num) + " " + str(1 - v_1_num) + "\n"
                    write_UV_n_lsc_3v_g_t_2 = "vt" + " " + str(u_0_num) + " " + str(1 - v_0_num) + "\n"
                    
                    file_write.write(write_UV_n_lsc_3v_g_t_0)
                    file_write.write(write_UV_n_lsc_3v_g_t_1)
                    file_write.write(write_UV_n_lsc_3v_g_t_2)
                  
                ####################################################################################################################

                # Extracting LSC 2nd NEW 3 VERTEX GOURAUD TEXTURED
                count_n_lsc_3v_g_t_2 = prim_block.count(new_lsc_three_vertex_gouraud_2)
                position_prim_n_lsc_3v_g_t_2 = prim_block.find(new_lsc_three_vertex_gouraud_2)
                total_count_tc.append(count_n_lsc_3v_g_t_2 * 3)

                while count_n_lsc_3v_g_t_2 > 0:
                    count_n_lsc_3v_g_t_2 -= 1
                    start_position_prim = position_prim_n_lsc_3v_g_t_2 + 4
                    end_position_prim = start_position_prim + 24
                    primitive_n_lsc_3v_g_t_2 = prim_block[start_position_prim : end_position_prim]
                    position_prim_n_lsc_3v_g_t_2 += 28
                    u_0 = primitive_n_lsc_3v_g_t_2[0:1]
                    v_0 = primitive_n_lsc_3v_g_t_2[1:2]
                    cba_value = primitive_n_lsc_3v_g_t_2[2:4]
                    u_1 = primitive_n_lsc_3v_g_t_2[4:5]
                    v_1 = primitive_n_lsc_3v_g_t_2[5:6]
                    tsb_value = primitive_n_lsc_3v_g_t_2[6:8]
                    u_2 = primitive_n_lsc_3v_g_t_2[8:9]
                    v_2 = primitive_n_lsc_3v_g_t_2[9:10]
                    value_not_used = primitive_n_lsc_3v_g_t_2[10:12]
                    normal_0 = primitive_n_lsc_3v_g_t_2[12:14]
                    vertex_0 = primitive_n_lsc_3v_g_t_2[14:16]
                    normal_1 = primitive_n_lsc_3v_g_t_2[16:18]
                    vertex_1 = primitive_n_lsc_3v_g_t_2[18:20]
                    normal_2 = primitive_n_lsc_3v_g_t_2[20:22]
                    vertex_2 = primitive_n_lsc_3v_g_t_2[22:24]


                    u_2_to_num = str(unpack('<B', u_2)).replace("(", "").replace(")", "").replace(",", "")
                    u_2_num = float(u_2_to_num) / 256
                    v_2_to_num = str(unpack('<B', v_2)).replace("(", "").replace(")", "").replace(",", "")
                    v_2_num = float(v_2_to_num) / 256
                    u_1_to_num = str(unpack('<B', u_1)).replace("(", "").replace(")", "").replace(",", "")
                    u_1_num = float(u_1_to_num) / 256
                    v_1_to_num = str(unpack('<B', v_1)).replace("(", "").replace(")", "").replace(",", "")
                    v_1_num = float(v_1_to_num) / 256
                    u_0_to_num = str(unpack('<B', u_0)).replace("(", "").replace(")", "").replace(",", "")
                    u_0_num = float(u_0_to_num) / 256
                    v_0_to_num = str(unpack('<B', v_0)).replace("(", "").replace(")", "").replace(",", "")
                    v_0_num = float(v_0_to_num) / 256

                    # OBJ UV Writer
                    write_UV_n_lsc_3v_g_t_2_0 = "vt" + " " + str(u_2_num) + " " + str(1 - v_2_num) + "\n"
                    write_UV_n_lsc_3v_g_t_2_1 = "vt" + " " + str(u_1_num) + " " + str(1 - v_1_num) + "\n"
                    write_UV_n_lsc_3v_g_t_2_2 = "vt" + " " + str(u_0_num) + " " + str(1 - v_0_num) + "\n"
                    
                    file_write.write(write_UV_n_lsc_3v_g_t_2_0)
                    file_write.write(write_UV_n_lsc_3v_g_t_2_1)
                    file_write.write(write_UV_n_lsc_3v_g_t_2_2)

                ####################################################################################################################

                # Extracting LSC 4 VERTEX GOURAUD TEXTURED // WORKING AS INTENDED
                count_lsc_4v_g_t = prim_block.count(lsc_four_vertex_gouraud_textured)
                position_prim_lsc_4v_g_t = prim_block.find(lsc_four_vertex_gouraud_textured)
                total_count_tc.append(count_lsc_4v_g_t * 4)

                while count_lsc_4v_g_t > 0:
                    count_lsc_4v_g_t -= 1
                    start_position_prim = position_prim_lsc_4v_g_t + 4
                    end_position_prim = start_position_prim + 32
                    primitive_lsc_4v_g_t = prim_block[start_position_prim : end_position_prim]
                    position_prim_lsc_4v_g_t += 36
                    u_0 = primitive_lsc_4v_g_t[0:1]
                    v_0 = primitive_lsc_4v_g_t[1:2]
                    cba_value = primitive_lsc_4v_g_t[2:4]
                    u_1 = primitive_lsc_4v_g_t[4:5]
                    v_1 = primitive_lsc_4v_g_t[5:6]
                    tsb_value = primitive_lsc_4v_g_t[6:8]
                    u_2 = primitive_lsc_4v_g_t[8:9]
                    v_2 = primitive_lsc_4v_g_t[9:10]
                    value_not_used_0 = primitive_lsc_4v_g_t[10:12]
                    u_3 = primitive_lsc_4v_g_t[12:13]
                    v_3 = primitive_lsc_4v_g_t[13:14]
                    value_not_used_1 = primitive_lsc_4v_g_t[14:16]
                    normal_0 = primitive_lsc_4v_g_t[16:18]
                    vertex_0 = primitive_lsc_4v_g_t[18:20]
                    normal_1 = primitive_lsc_4v_g_t[20:22]
                    vertex_1 = primitive_lsc_4v_g_t[22:24]
                    normal_2 = primitive_lsc_4v_g_t[24:26]
                    vertex_2 = primitive_lsc_4v_g_t[26:28]
                    normal_3 = primitive_lsc_4v_g_t[28:30]
                    vertex_3 = primitive_lsc_4v_g_t[30:32]
                    
                    u_0_to_num = str(unpack('<B', u_0)).replace("(", "").replace(")", "").replace(",", "")
                    u_0_num = float(u_0_to_num) / 256
                    v_0_to_num = str(unpack('<B', v_0)).replace("(", "").replace(")", "").replace(",", "")
                    v_0_num = float(v_0_to_num) / 256
                    u_2_to_num = str(unpack('<B', u_2)).replace("(", "").replace(")", "").replace(",", "")
                    u_2_num = float(u_2_to_num) / 256
                    v_2_to_num = str(unpack('<B', v_2)).replace("(", "").replace(")", "").replace(",", "")
                    v_2_num = float(v_2_to_num) / 256
                    u_3_to_num = str(unpack('<B', u_3)).replace("(", "").replace(")", "").replace(",", "")
                    u_3_num = float(u_3_to_num) / 256
                    v_3_to_num = str(unpack('<B', v_3)).replace("(", "").replace(")", "").replace(",", "")
                    v_3_num = float(v_3_to_num) / 256
                    u_1_to_num = str(unpack('<B', u_1)).replace("(", "").replace(")", "").replace(",", "")
                    u_1_num = float(u_1_to_num) / 256
                    v_1_to_num = str(unpack('<B', v_1)).replace("(", "").replace(")", "").replace(",", "")
                    v_1_num = float(v_1_to_num) / 256

                    #OBJ UV Writer
                    write_UV_lsc_4v_g_t_0 = "vt" + " " + str(u_0_num) + " " + str(1 - v_0_num) + "\n"
                    write_UV_lsc_4v_g_t_1 = "vt" + " " + str(u_2_num) + " " + str(1 - v_2_num) + "\n"
                    write_UV_lsc_4v_g_t_2 = "vt" + " " + str(u_3_num) + " " + str(1 - v_3_num) + "\n"
                    write_UV_lsc_4v_g_t_3 = "vt" + " " + str(u_1_num) + " " + str(1 - v_1_num) + "\n"

                    file_write.write(write_UV_lsc_4v_g_t_0)
                    file_write.write(write_UV_lsc_4v_g_t_1)
                    file_write.write(write_UV_lsc_4v_g_t_2)
                    file_write.write(write_UV_lsc_4v_g_t_3)

                    #print(u_0, v_0, "in obj n ", numeration_prim)
                    #print(u_1, v_1, "in obj n ", numeration_prim)
                    #print(u_2, v_2, "in obj n ", numeration_prim)
                    #print(u_3, v_3, "in obj n ", numeration_prim)

                    #print(u_2, v_2, "Primitive in OBJ n ", str(numeration_prim))
                    ######!!! NEED MORE CODE !!!###### NO OLVIDAR MODIFICAR EL V_N_NUM DE TODOS PORQUE ESTAN MAL, EN SU MAYORIA POR COPIAR Y PEGAR PUSE U_0_TO_NUM


                ####################################################################################################################

                # Extracting LSC 4 VERTEX FLAT TEXTURED // WORKING AS INTENDED
                count_lsc_4v_f_t = prim_block.count(lsc_four_vertex_flat_textured)
                position_prim_lsc_4v_f_t = prim_block.find(lsc_four_vertex_flat_textured)
                total_count_tc.append(count_lsc_4v_f_t * 4)

                while count_lsc_4v_f_t > 0:
                    count_lsc_4v_f_t -= 1
                    start_position_prim = position_prim_lsc_4v_f_t + 4
                    end_position_prim = start_position_prim + 28
                    primitive_lsc_4v_f_t = prim_block[start_position_prim : end_position_prim]
                    position_prim_lsc_4v_f_t += 32
                    u_0 = primitive_lsc_4v_f_t[0:1]
                    v_0 = primitive_lsc_4v_f_t[1:2]
                    cba_value = primitive_lsc_4v_f_t[2:4]
                    u_1 = primitive_lsc_4v_f_t[4:5]
                    v_1 = primitive_lsc_4v_f_t[5:6]
                    tsb_value = primitive_lsc_4v_f_t[6:8]
                    u_2 = primitive_lsc_4v_f_t[8:9]
                    v_2 = primitive_lsc_4v_f_t[9:10]
                    value_not_used_0 = primitive_lsc_4v_f_t[10:12]
                    u_3 = primitive_lsc_4v_f_t[12:13]
                    v_3 = primitive_lsc_4v_f_t[13:14]
                    value_not_used_1 = primitive_lsc_4v_f_t[14:16]
                    normal_0 = primitive_lsc_4v_f_t[16:18]
                    vertex_0 = primitive_lsc_4v_f_t[18:20]
                    vertex_1 = primitive_lsc_4v_f_t[20:22]
                    vertex_2 = primitive_lsc_4v_f_t[22:24]
                    vertex_3 = primitive_lsc_4v_f_t[24:26]
                    value_not_used_2 = primitive_lsc_4v_f_t[26:28]
                    
                    u_0_to_num = str(unpack('<B', u_0)).replace("(", "").replace(")", "").replace(",", "")
                    u_0_num = float(u_0_to_num) / 256
                    v_0_to_num = str(unpack('<B', v_0)).replace("(", "").replace(")", "").replace(",", "")
                    v_0_num = float(v_0_to_num) / 256
                    u_2_to_num = str(unpack('<B', u_2)).replace("(", "").replace(")", "").replace(",", "")
                    u_2_num = float(u_2_to_num) / 256
                    v_2_to_num = str(unpack('<B', v_2)).replace("(", "").replace(")", "").replace(",", "")
                    v_2_num = float(v_2_to_num) / 256
                    u_3_to_num = str(unpack('<B', u_3)).replace("(", "").replace(")", "").replace(",", "")
                    u_3_num = float(u_3_to_num) / 256
                    v_3_to_num = str(unpack('<B', v_3)).replace("(", "").replace(")", "").replace(",", "")
                    v_3_num = float(v_3_to_num) / 256
                    u_1_to_num = str(unpack('<B', u_1)).replace("(", "").replace(")", "").replace(",", "")
                    u_1_num = float(u_1_to_num) / 256
                    v_1_to_num = str(unpack('<B', v_1)).replace("(", "").replace(")", "").replace(",", "")
                    v_1_num = float(v_1_to_num) / 256

                    #OBJ UV Writer
                    write_UV_lsc_4v_f_t_0 = "vt" + " " + str(u_0_num) + " " + str(1 - v_0_num) + "\n"
                    write_UV_lsc_4v_f_t_1 = "vt" + " " + str(u_2_num) + " " + str(1 - v_2_num) + "\n"
                    write_UV_lsc_4v_f_t_2 = "vt" + " " + str(u_3_num) + " " + str(1 - v_3_num) + "\n"
                    write_UV_lsc_4v_f_t_3 = "vt" + " " + str(u_1_num) + " " + str(1 - v_1_num) + "\n"

                    file_write.write(write_UV_lsc_4v_f_t_0)
                    file_write.write(write_UV_lsc_4v_f_t_1)
                    file_write.write(write_UV_lsc_4v_f_t_2)
                    file_write.write(write_UV_lsc_4v_f_t_3)

                ####################################################################################################################

                # Extracting LSC NEW TYPE OF PACKET a 4 VERTEX GOURAUD TEXTURED
                count_n_lsc_4v_g_t = prim_block.count(new_lsc_four_vertex_gouraud_textured)
                position_prim_n_lsc_4v_g_t = prim_block.find(new_lsc_four_vertex_gouraud_textured)
                total_count_tc.append(count_n_lsc_4v_g_t * 4)

                while count_n_lsc_4v_g_t > 0:
                    count_n_lsc_4v_g_t -= 1
                    start_position_prim = position_prim_n_lsc_4v_g_t + 4
                    end_position_prim = start_position_prim + 32
                    primitive_n_lsc_4v_g_t = prim_block[start_position_prim : end_position_prim]
                    position_prim_n_lsc_4v_g_t += 36
                    u_0 = primitive_n_lsc_4v_g_t[0:1]
                    v_0 = primitive_n_lsc_4v_g_t[1:2]
                    cba_value = primitive_n_lsc_4v_g_t[2:4]
                    u_1 = primitive_n_lsc_4v_g_t[4:5]
                    v_1 = primitive_n_lsc_4v_g_t[5:6]
                    tsb_value = primitive_n_lsc_4v_g_t[6:8]
                    u_2 = primitive_n_lsc_4v_g_t[8:9]
                    v_2 = primitive_n_lsc_4v_g_t[9:10]
                    value_not_used_0 = primitive_n_lsc_4v_g_t[10:12]
                    u_3 = primitive_n_lsc_4v_g_t[12:13]
                    v_3 = primitive_n_lsc_4v_g_t[13:14]
                    value_not_used_1 = primitive_n_lsc_4v_g_t[14:16]
                    normal_0 = primitive_n_lsc_4v_g_t[16:18]
                    vertex_0 = primitive_n_lsc_4v_g_t[18:20]
                    normal_1 = primitive_n_lsc_4v_g_t[20:22]
                    vertex_1 = primitive_n_lsc_4v_g_t[22:24]
                    normal_2 = primitive_n_lsc_4v_g_t[24:26]
                    vertex_2 = primitive_n_lsc_4v_g_t[26:28]
                    normal_3 = primitive_n_lsc_4v_g_t[28:30]
                    vertex_3 = primitive_n_lsc_4v_g_t[30:32]
                    
                    u_0_to_num = str(unpack('<B', u_0)).replace("(", "").replace(")", "").replace(",", "")
                    u_0_num = float(u_0_to_num) / 256
                    v_0_to_num = str(unpack('<B', v_0)).replace("(", "").replace(")", "").replace(",", "")
                    v_0_num = float(v_0_to_num) / 256
                    u_2_to_num = str(unpack('<B', u_2)).replace("(", "").replace(")", "").replace(",", "")
                    u_2_num = float(u_2_to_num) / 256
                    v_2_to_num = str(unpack('<B', v_2)).replace("(", "").replace(")", "").replace(",", "")
                    v_2_num = float(v_2_to_num) / 256
                    u_3_to_num = str(unpack('<B', u_3)).replace("(", "").replace(")", "").replace(",", "")
                    u_3_num = float(u_3_to_num) / 256
                    v_3_to_num = str(unpack('<B', v_3)).replace("(", "").replace(")", "").replace(",", "")
                    v_3_num = float(v_3_to_num) / 256
                    u_1_to_num = str(unpack('<B', u_1)).replace("(", "").replace(")", "").replace(",", "")
                    u_1_num = float(u_1_to_num) / 256
                    v_1_to_num = str(unpack('<B', v_1)).replace("(", "").replace(")", "").replace(",", "")
                    v_1_num = float(v_1_to_num) / 256

                    #OBJ UV Writer
                    write_UV_n_lsc_4v_g_t_0 = "vt" + " " + str(u_0_num) + " " + str(1 - v_0_num) + "\n"
                    write_UV_n_lsc_4v_g_t_1 = "vt" + " " + str(u_2_num) + " " + str(1 - v_2_num) + "\n"
                    write_UV_n_lsc_4v_g_t_2 = "vt" + " " + str(u_3_num) + " " + str(1 - v_3_num) + "\n"
                    write_UV_n_lsc_4v_g_t_3 = "vt" + " " + str(u_1_num) + " " + str(1 - v_1_num) + "\n"

                    file_write.write(write_UV_n_lsc_4v_g_t_0)
                    file_write.write(write_UV_n_lsc_4v_g_t_1)
                    file_write.write(write_UV_n_lsc_4v_g_t_2)
                    file_write.write(write_UV_n_lsc_4v_g_t_3)

                ####################################################################################################################

                # Extracting LSC 2ND NEW TYPE OF PACKET a 4 VERTEX GOURAUD TEXTURED
                count_n_lsc_4v_g_t_2 = prim_block.count(new_lsc_four_vertex_gouraud_textured_2)
                position_prim_n_lsc_4v_g_t_2 = prim_block.find(new_lsc_four_vertex_gouraud_textured_2)
                total_count_tc.append(count_n_lsc_4v_g_t_2 * 4)

                while count_n_lsc_4v_g_t_2 > 0:
                    count_n_lsc_4v_g_t_2 -= 1
                    start_position_prim = position_prim_n_lsc_4v_g_t_2 + 4
                    end_position_prim = start_position_prim + 32
                    primitive_n_lsc_4v_g_t_2 = prim_block[start_position_prim : end_position_prim]
                    position_prim_n_lsc_4v_g_t_2 += 36
                    u_0 = primitive_n_lsc_4v_g_t_2[0:1]
                    v_0 = primitive_n_lsc_4v_g_t_2[1:2]
                    cba_value = primitive_n_lsc_4v_g_t_2[2:4]
                    u_1 = primitive_n_lsc_4v_g_t_2[4:5]
                    v_1 = primitive_n_lsc_4v_g_t_2[5:6]
                    tsb_value = primitive_n_lsc_4v_g_t_2[6:8]
                    u_2 = primitive_n_lsc_4v_g_t_2[8:9]
                    v_2 = primitive_n_lsc_4v_g_t_2[9:10]
                    value_not_used_0 = primitive_n_lsc_4v_g_t_2[10:12]
                    u_3 = primitive_n_lsc_4v_g_t_2[12:13]
                    v_3 = primitive_n_lsc_4v_g_t_2[13:14]
                    value_not_used_1 = primitive_n_lsc_4v_g_t_2[14:16]
                    normal_0 = primitive_n_lsc_4v_g_t_2[16:18]
                    vertex_0 = primitive_n_lsc_4v_g_t_2[18:20]
                    normal_1 = primitive_n_lsc_4v_g_t_2[20:22]
                    vertex_1 = primitive_n_lsc_4v_g_t_2[22:24]
                    normal_2 = primitive_n_lsc_4v_g_t_2[24:26]
                    vertex_2 = primitive_n_lsc_4v_g_t_2[26:28]
                    normal_3 = primitive_n_lsc_4v_g_t_2[28:30]
                    vertex_3 = primitive_n_lsc_4v_g_t_2[30:32]
                    
                    u_0_to_num = str(unpack('<B', u_0)).replace("(", "").replace(")", "").replace(",", "")
                    u_0_num = float(u_0_to_num) / 256
                    v_0_to_num = str(unpack('<B', v_0)).replace("(", "").replace(")", "").replace(",", "")
                    v_0_num = float(v_0_to_num) / 256
                    u_2_to_num = str(unpack('<B', u_2)).replace("(", "").replace(")", "").replace(",", "")
                    u_2_num = float(u_2_to_num) / 256
                    v_2_to_num = str(unpack('<B', v_2)).replace("(", "").replace(")", "").replace(",", "")
                    v_2_num = float(v_2_to_num) / 256
                    u_3_to_num = str(unpack('<B', u_3)).replace("(", "").replace(")", "").replace(",", "")
                    u_3_num = float(u_3_to_num) / 256
                    v_3_to_num = str(unpack('<B', v_3)).replace("(", "").replace(")", "").replace(",", "")
                    v_3_num = float(v_3_to_num) / 256
                    u_1_to_num = str(unpack('<B', u_1)).replace("(", "").replace(")", "").replace(",", "")
                    u_1_num = float(u_1_to_num) / 256
                    v_1_to_num = str(unpack('<B', v_1)).replace("(", "").replace(")", "").replace(",", "")
                    v_1_num = float(v_1_to_num) / 256

                    #OBJ UV Writer
                    write_UV_n_lsc_4v_g_t_2_0 = "vt" + " " + str(u_0_num) + " " + str(1 - v_0_num) + "\n"
                    write_UV_n_lsc_4v_g_t_2_1 = "vt" + " " + str(u_2_num) + " " + str(1 - v_2_num) + "\n"
                    write_UV_n_lsc_4v_g_t_2_2 = "vt" + " " + str(u_3_num) + " " + str(1 - v_3_num) + "\n"
                    write_UV_n_lsc_4v_g_t_2_3 = "vt" + " " + str(u_1_num) + " " + str(1 - v_1_num) + "\n"

                    file_write.write(write_UV_n_lsc_4v_g_t_2_0)
                    file_write.write(write_UV_n_lsc_4v_g_t_2_1)
                    file_write.write(write_UV_n_lsc_4v_g_t_2_2)
                    file_write.write(write_UV_n_lsc_4v_g_t_2_3)

                ####################################################################################################################

                # Extracting NLSC 3 VERTEX GRADATION TEXTURED
                count_nlsc_3v_g_t = prim_block.count(nlsc_three_vertex_gradation_textured)
                position_prim_nlsc_3v_g_t = prim_block.find(nlsc_three_vertex_gradation_textured)
                total_count_tc.append(count_nlsc_3v_g_t * 3)

                while count_nlsc_3v_g_t > 0:
                    count_nlsc_3v_g_t -= 1
                    start_position_prim = position_prim_nlsc_3v_g_t + 4
                    end_position_prim = start_position_prim + 32
                    primitive_nlsc_3v_g_t = prim_block[start_position_prim : end_position_prim]
                    position_prim_nlsc_3v_g_t += 36
                    u_0 = primitive_nlsc_3v_g_t[0:1]
                    v_0 = primitive_nlsc_3v_g_t[1:2]
                    cba_value = primitive_nlsc_3v_g_t[2:4]
                    u_1 = primitive_nlsc_3v_g_t[4:5]
                    v_1 = primitive_nlsc_3v_g_t[5:6]
                    tsb_value = primitive_nlsc_3v_g_t[6:8]
                    u_2 = primitive_nlsc_3v_g_t[8:9]
                    v_2 = primitive_nlsc_3v_g_t[9:10]
                    value_not_used_0 = primitive_nlsc_3v_g_t[10:12]
                    red_value_0 = primitive_nlsc_3v_g_t[12:13]
                    green_value_0 = primitive_nlsc_3v_g_t[13:14]
                    blue_value_0 = primitive_nlsc_3v_g_t[14:15]
                    value_not_used_1 = primitive_nlsc_3v_g_t[15:16]
                    red_value_1 = primitive_nlsc_3v_g_t[16:17]
                    green_value_1 = primitive_nlsc_3v_g_t[17:18]
                    blue_value_1 = primitive_nlsc_3v_g_t[18:19]
                    value_not_used_2 = primitive_nlsc_3v_g_t[19:20]
                    red_value_2 = primitive_nlsc_3v_g_t[20:21]
                    green_value_2 = primitive_nlsc_3v_g_t[21:22]
                    blue_value_2 = primitive_nlsc_3v_g_t[22:23]
                    value_not_used_3 = primitive_nlsc_3v_g_t[23:24]
                    vertex_0 = primitive_nlsc_3v_g_t[24:26]
                    vertex_1 = primitive_nlsc_3v_g_t[26:28]
                    vertex_2 = primitive_nlsc_3v_g_t[28:30]
                    value_not_used_4 = primitive_nlsc_3v_g_t[30:32]

                    u_2_to_num = str(unpack('<B', u_2)).replace("(", "").replace(")", "").replace(",", "")
                    u_2_num = float(u_2_to_num) / 256
                    v_2_to_num = str(unpack('<B', v_2)).replace("(", "").replace(")", "").replace(",", "")
                    v_2_num = float(v_2_to_num) / 256
                    u_1_to_num = str(unpack('<B', u_1)).replace("(", "").replace(")", "").replace(",", "")
                    u_1_num = float(u_1_to_num) / 256
                    v_1_to_num = str(unpack('<B', v_1)).replace("(", "").replace(")", "").replace(",", "")
                    v_1_num = float(v_1_to_num) / 256
                    u_0_to_num = str(unpack('<B', u_0)).replace("(", "").replace(")", "").replace(",", "")
                    u_0_num = float(u_0_to_num) / 256
                    v_0_to_num = str(unpack('<B', v_0)).replace("(", "").replace(")", "").replace(",", "")
                    v_0_num = float(v_0_to_num) / 256

                    # OBJ UV Writer
                    write_UV_nlsc_3v_g_t_0 = "vt" + " " + str(u_2_num) + " " + str(1 - v_2_num) + "\n"
                    write_UV_nlsc_3v_g_t_1 = "vt" + " " + str(u_1_num) + " " + str(1 - v_1_num) + "\n"
                    write_UV_nlsc_3v_g_t_2 = "vt" + " " + str(u_0_num) + " " + str(1 - v_0_num) + "\n"
                    
                    file_write.write(write_UV_nlsc_3v_g_t_0)
                    file_write.write(write_UV_nlsc_3v_g_t_1)
                    file_write.write(write_UV_nlsc_3v_g_t_2)

                ####################################################################################################################

                # Extracting NLSC 3 VERTEX FLAT TEXTURED
                count_nlsc_3v_f_t = prim_block.count(nlsc_three_vertex_flat_textured)
                position_prim_nlsc_3v_f_t = prim_block.find(nlsc_three_vertex_flat_textured)
                total_count_tc.append(count_nlsc_3v_f_t * 3)

                while count_nlsc_3v_f_t > 0:
                    count_nlsc_3v_f_t -= 1
                    start_position_prim = position_prim_nlsc_3v_f_t + 4
                    end_position_prim = start_position_prim + 24
                    primitive_nlsc_3v_f_t = prim_block[start_position_prim : end_position_prim]
                    position_prim_nlsc_3v_f_t += 28
                    u_0 = primitive_nlsc_3v_f_t[0:1]
                    v_0 = primitive_nlsc_3v_f_t[1:2]
                    cba_value = primitive_nlsc_3v_f_t[2:4]
                    u_1 = primitive_nlsc_3v_f_t[4:5]
                    v_1 = primitive_nlsc_3v_f_t[5:6]
                    tsb_value = primitive_nlsc_3v_f_t[6:8]
                    u_2 = primitive_nlsc_3v_f_t[8:9]
                    v_2 = primitive_nlsc_3v_f_t[9:10]
                    value_not_used_0 = primitive_nlsc_3v_f_t[10:12]
                    red_value = primitive_nlsc_3v_f_t[12:13]
                    green_value = primitive_nlsc_3v_f_t[13:14]
                    blue_value = primitive_nlsc_3v_f_t[14:15]
                    value_not_used_1 = primitive_nlsc_3v_f_t[15:16]
                    vertex_0 = primitive_nlsc_3v_f_t[16:18]
                    vertex_1 = primitive_nlsc_3v_f_t[18:20]
                    vertex_2 = primitive_nlsc_3v_f_t[20:22]
                    value_not_used_2 = primitive_nlsc_3v_f_t[22:24]

                    u_2_to_num = str(unpack('<B', u_2)).replace("(", "").replace(")", "").replace(",", "")
                    u_2_num = float(u_2_to_num) / 256
                    v_2_to_num = str(unpack('<B', v_2)).replace("(", "").replace(")", "").replace(",", "")
                    v_2_num = float(v_2_to_num) / 256
                    u_1_to_num = str(unpack('<B', u_1)).replace("(", "").replace(")", "").replace(",", "")
                    u_1_num = float(u_1_to_num) / 256
                    v_1_to_num = str(unpack('<B', v_1)).replace("(", "").replace(")", "").replace(",", "")
                    v_1_num = float(v_1_to_num) / 256
                    u_0_to_num = str(unpack('<B', u_0)).replace("(", "").replace(")", "").replace(",", "")
                    u_0_num = float(u_0_to_num) / 256
                    v_0_to_num = str(unpack('<B', v_0)).replace("(", "").replace(")", "").replace(",", "")
                    v_0_num = float(v_0_to_num) / 256

                    # OBJ UV Writer
                    write_UV_nlsc_3v_f_t_0 = "vt" + " " + str(u_2_num) + " " + str(1 - v_2_num) + "\n"
                    write_UV_nlsc_3v_f_t_1 = "vt" + " " + str(u_1_num) + " " + str(1 - v_1_num) + "\n"
                    write_UV_nlsc_3v_f_t_2 = "vt" + " " + str(u_0_num) + " " + str(1 - v_0_num) + "\n"
                    
                    file_write.write(write_UV_nlsc_3v_f_t_0)
                    file_write.write(write_UV_nlsc_3v_f_t_1)
                    file_write.write(write_UV_nlsc_3v_f_t_2)

                ####################################################################################################################

                # Extracting NLSC NEW TYPE OF PACKET a 3 VERTEX GRADATION TEXTURED
                count_n_nlsc_3v_g_t = prim_block.count(new_nlsc_three_vertex_gradation_textured)
                position_prim_n_nlsc_3v_g_t = prim_block.find(new_nlsc_three_vertex_gradation_textured)
                total_count_tc.append(count_n_nlsc_3v_g_t * 3)

                while count_n_nlsc_3v_g_t > 0:
                    count_n_nlsc_3v_g_t -= 1
                    start_position_prim = position_prim_n_nlsc_3v_g_t + 4
                    end_position_prim = start_position_prim + 32
                    primitive_n_nlsc_3v_g_t = prim_block[start_position_prim : end_position_prim]
                    position_prim_n_nlsc_3v_g_t += 36
                    u_0 = primitive_n_nlsc_3v_g_t[0:1]
                    v_0 = primitive_n_nlsc_3v_g_t[1:2]
                    cba_value = primitive_n_nlsc_3v_g_t[2:4]
                    u_1 = primitive_n_nlsc_3v_g_t[4:5]
                    v_1 = primitive_n_nlsc_3v_g_t[5:6]
                    tsb_value = primitive_n_nlsc_3v_g_t[6:8]
                    u_2 = primitive_n_nlsc_3v_g_t[8:9]
                    v_2 = primitive_n_nlsc_3v_g_t[9:10]
                    value_not_used_0 = primitive_n_nlsc_3v_g_t[10:12]
                    red_value_0 = primitive_n_nlsc_3v_g_t[12:13]
                    green_value_0 = primitive_n_nlsc_3v_g_t[13:14]
                    blue_value_0 = primitive_n_nlsc_3v_g_t[14:15]
                    value_not_used_1 = primitive_n_nlsc_3v_g_t[15:16]
                    red_value_1 = primitive_n_nlsc_3v_g_t[16:17]
                    green_value_1 = primitive_n_nlsc_3v_g_t[17:18]
                    blue_value_1 = primitive_n_nlsc_3v_g_t[18:19]
                    value_not_used_2 = primitive_n_nlsc_3v_g_t[19:20]
                    red_value_2 = primitive_n_nlsc_3v_g_t[20:21]
                    green_value_2 = primitive_n_nlsc_3v_g_t[21:22]
                    blue_value_2 = primitive_n_nlsc_3v_g_t[22:23]
                    value_not_used_3 = primitive_n_nlsc_3v_g_t[23:24]
                    vertex_0 = primitive_n_nlsc_3v_g_t[24:26]
                    vertex_1 = primitive_n_nlsc_3v_g_t[26:28]
                    vertex_2 = primitive_n_nlsc_3v_g_t[28:30]
                    value_not_used_4 = primitive_n_nlsc_3v_g_t[30:32]

                    u_2_to_num = str(unpack('<B', u_2)).replace("(", "").replace(")", "").replace(",", "")
                    u_2_num = float(u_2_to_num) / 256
                    v_2_to_num = str(unpack('<B', v_2)).replace("(", "").replace(")", "").replace(",", "")
                    v_2_num = float(v_2_to_num) / 256
                    u_1_to_num = str(unpack('<B', u_1)).replace("(", "").replace(")", "").replace(",", "")
                    u_1_num = float(u_1_to_num) / 256
                    v_1_to_num = str(unpack('<B', v_1)).replace("(", "").replace(")", "").replace(",", "")
                    v_1_num = float(v_1_to_num) / 256
                    u_0_to_num = str(unpack('<B', u_0)).replace("(", "").replace(")", "").replace(",", "")
                    u_0_num = float(u_0_to_num) / 256
                    v_0_to_num = str(unpack('<B', v_0)).replace("(", "").replace(")", "").replace(",", "")
                    v_0_num = float(v_0_to_num) / 256

                    # OBJ UV Writer
                    write_UV_n_nlsc_3v_g_t_0 = "vt" + " " + str(u_2_num) + " " + str(1 - v_2_num) + "\n"
                    write_UV_n_nlsc_3v_g_t_1 = "vt" + " " + str(u_1_num) + " " + str(1 - v_1_num) + "\n"
                    write_UV_n_nlsc_3v_g_t_2 = "vt" + " " + str(u_0_num) + " " + str(1 - v_0_num) + "\n"
                    
                    file_write.write(write_UV_n_nlsc_3v_g_t_0)
                    file_write.write(write_UV_n_nlsc_3v_g_t_1)
                    file_write.write(write_UV_n_nlsc_3v_g_t_2)

                ####################################################################################################################

                # Extracting NLSC 4 VERTEX GRADATION TEXTURED
                count_nlsc_4v_g_t = prim_block.count(nlsc_four_vertex_gradation_textured)
                position_prim_nlsc_4v_g_t = prim_block.find(nlsc_four_vertex_gradation_textured)
                total_count_tc.append(count_nlsc_4v_g_t * 4)

                while count_nlsc_4v_g_t > 0:
                    count_nlsc_4v_g_t -= 1
                    start_position_prim = position_prim_nlsc_4v_g_t + 4
                    end_position_prim = position_prim_nlsc_4v_g_t + 40
                    primitive_nlsc_4v_g_t = prim_block[start_position_prim : end_position_prim]
                    position_prim_nlsc_4v_g_t += 44
                    u_0 = primitive_nlsc_4v_g_t[0:1]
                    v_0 = primitive_nlsc_4v_g_t[1:2]
                    cba_value = primitive_nlsc_4v_g_t[2:4]
                    u_1 = primitive_nlsc_4v_g_t[4:5]
                    v_1 = primitive_nlsc_4v_g_t[5:6]
                    tsb_value = primitive_nlsc_4v_g_t[6:8]
                    u_2 = primitive_nlsc_4v_g_t[8:9]
                    v_2 = primitive_nlsc_4v_g_t[9:10]
                    value_not_used_0 = primitive_nlsc_4v_g_t[10:12]
                    u_3 = primitive_nlsc_4v_g_t[12:13]
                    v_3 = primitive_nlsc_4v_g_t[13:14]
                    value_not_used_1 = primitive_nlsc_4v_g_t[14:16]
                    red_value_0 = primitive_nlsc_4v_g_t[16:17]
                    green_value_0 = primitive_nlsc_4v_g_t[17:18]
                    blue_value_0 = primitive_nlsc_4v_g_t[18:19]
                    value_not_used_2 = primitive_nlsc_4v_g_t[19:20]
                    red_value_1 = primitive_nlsc_4v_g_t[20:21]
                    green_value_1 = primitive_nlsc_4v_g_t[21:22]
                    blue_value_1 = primitive_nlsc_4v_g_t[22:23]
                    value_not_used_3 = primitive_nlsc_4v_g_t[23:24]
                    red_value_2 = primitive_nlsc_4v_g_t[24:25]
                    green_value_2 = primitive_nlsc_4v_g_t[25:26]
                    blue_value_2 = primitive_nlsc_4v_g_t[26:27]
                    value_not_used_4 = primitive_nlsc_4v_g_t[27:28]
                    red_value_3 = primitive_nlsc_4v_g_t[28:29]
                    green_value_3 = primitive_nlsc_4v_g_t[29:30]
                    blue_value_3 = primitive_nlsc_4v_g_t[30:31]
                    value_not_used_5 = primitive_nlsc_4v_g_t[31:32]
                    vertex_0 = primitive_nlsc_4v_g_t[32:34]
                    vertex_1 = primitive_nlsc_4v_g_t[34:36]
                    vertex_2 = primitive_nlsc_4v_g_t[36:38]
                    vertex_3 = primitive_nlsc_4v_g_t[38:40]

                    u_0_to_num = str(unpack('<B', u_0)).replace("(", "").replace(")", "").replace(",", "")
                    u_0_num = float(u_0_to_num) / 256
                    v_0_to_num = str(unpack('<B', v_0)).replace("(", "").replace(")", "").replace(",", "")
                    v_0_num = float(v_0_to_num) / 256
                    u_2_to_num = str(unpack('<B', u_2)).replace("(", "").replace(")", "").replace(",", "")
                    u_2_num = float(u_2_to_num) / 256
                    v_2_to_num = str(unpack('<B', v_2)).replace("(", "").replace(")", "").replace(",", "")
                    v_2_num = float(v_2_to_num) / 256
                    u_3_to_num = str(unpack('<B', u_3)).replace("(", "").replace(")", "").replace(",", "")
                    u_3_num = float(u_3_to_num) / 256
                    v_3_to_num = str(unpack('<B', v_3)).replace("(", "").replace(")", "").replace(",", "")
                    v_3_num = float(v_3_to_num) / 256
                    u_1_to_num = str(unpack('<B', u_1)).replace("(", "").replace(")", "").replace(",", "")
                    u_1_num = float(u_1_to_num) / 256
                    v_1_to_num = str(unpack('<B', v_1)).replace("(", "").replace(")", "").replace(",", "")
                    v_1_num = float(v_1_to_num) / 256

                    #OBJ UV Writer
                    write_UV_nlsc_4v_g_t_0 = "vt" + " " + str(u_0_num) + " " + str(1 - v_0_num) + "\n"
                    write_UV_nlsc_4v_g_t_1 = "vt" + " " + str(u_2_num) + " " + str(1 - v_2_num) + "\n"
                    write_UV_nlsc_4v_g_t_2 = "vt" + " " + str(u_3_num) + " " + str(1 - v_3_num) + "\n"
                    write_UV_nlsc_4v_g_t_3 = "vt" + " " + str(u_1_num) + " " + str(1 - v_1_num) + "\n"

                    file_write.write(write_UV_nlsc_4v_g_t_0)
                    file_write.write(write_UV_nlsc_4v_g_t_1)
                    file_write.write(write_UV_nlsc_4v_g_t_2)
                    file_write.write(write_UV_nlsc_4v_g_t_3)

                ####################################################################################################################

                # Extracting NLSC 4 VERTEX FLAT TEXTURED
                count_nlsc_4v_f_t = prim_block.count(nlsc_four_vertex_flat_textured)
                position_prim_nlsc_4v_f_t = prim_block.find(nlsc_four_vertex_flat_textured)
                total_count_tc.append(count_nlsc_4v_f_t * 4)

                while count_nlsc_4v_f_t > 0:
                    count_nlsc_4v_f_t -= 1
                    start_position_prim = position_prim_nlsc_4v_f_t + 4
                    end_position_prim = start_position_prim + 28
                    primitive_nlsc_4v_f_t = prim_block[start_position_prim : end_position_prim]
                    position_prim_nlsc_4v_f_t += 32
                    u_0 = primitive_nlsc_4v_f_t[0:1]
                    v_0 = primitive_nlsc_4v_f_t[1:2]
                    cba_value = primitive_nlsc_4v_f_t[2:4]
                    u_1 = primitive_nlsc_4v_f_t[4:5]
                    v_1 = primitive_nlsc_4v_f_t[5:6]
                    tsb_value = primitive_nlsc_4v_f_t[6:8]
                    u_2 = primitive_nlsc_4v_f_t[8:9]
                    v_2 = primitive_nlsc_4v_f_t[9:10]
                    value_not_used_0 = primitive_nlsc_4v_f_t[10:12]
                    u_3 = primitive_nlsc_4v_f_t[12:13]
                    v_3 = primitive_nlsc_4v_f_t[13:14]
                    value_not_used_1 = primitive_nlsc_4v_f_t[14:16]
                    red_value = primitive_nlsc_4v_f_t[16:17]
                    green_value = primitive_nlsc_4v_f_t[17:18]
                    blue_value = primitive_nlsc_4v_f_t[18:19]
                    value_not_used_2 = primitive_nlsc_4v_f_t[19:20]
                    vertex_0 = primitive_nlsc_4v_f_t[20:22]
                    vertex_1 = primitive_nlsc_4v_f_t[22:24]
                    vertex_2 = primitive_nlsc_4v_f_t[24:26]
                    vertex_3 = primitive_nlsc_4v_f_t[26:28]

                    u_0_to_num = str(unpack('<B', u_0)).replace("(", "").replace(")", "").replace(",", "")
                    u_0_num = float(u_0_to_num) / 256
                    v_0_to_num = str(unpack('<B', v_0)).replace("(", "").replace(")", "").replace(",", "")
                    v_0_num = float(v_0_to_num) / 256
                    u_2_to_num = str(unpack('<B', u_2)).replace("(", "").replace(")", "").replace(",", "")
                    u_2_num = float(u_2_to_num) / 256
                    v_2_to_num = str(unpack('<B', v_2)).replace("(", "").replace(")", "").replace(",", "")
                    v_2_num = float(v_2_to_num) / 256
                    u_3_to_num = str(unpack('<B', u_3)).replace("(", "").replace(")", "").replace(",", "")
                    u_3_num = float(u_3_to_num) / 256
                    v_3_to_num = str(unpack('<B', v_3)).replace("(", "").replace(")", "").replace(",", "")
                    v_3_num = float(v_3_to_num) / 256
                    u_1_to_num = str(unpack('<B', u_1)).replace("(", "").replace(")", "").replace(",", "")
                    u_1_num = float(u_1_to_num) / 256
                    v_1_to_num = str(unpack('<B', v_1)).replace("(", "").replace(")", "").replace(",", "")
                    v_1_num = float(v_1_to_num) / 256

                    #OBJ UV Writer
                    write_UV_nlsc_4v_f_t_0 = "vt" + " " + str(u_0_num) + " " + str(1 - v_0_num) + "\n"
                    write_UV_nlsc_4v_f_t_1 = "vt" + " " + str(u_2_num) + " " + str(1 - v_2_num) + "\n"
                    write_UV_nlsc_4v_f_t_2 = "vt" + " " + str(u_3_num) + " " + str(1 - v_3_num) + "\n"
                    write_UV_nlsc_4v_f_t_3 = "vt" + " " + str(u_1_num) + " " + str(1 - v_1_num) + "\n"

                    file_write.write(write_UV_nlsc_4v_f_t_0)
                    file_write.write(write_UV_nlsc_4v_f_t_1)
                    file_write.write(write_UV_nlsc_4v_f_t_2)
                    file_write.write(write_UV_nlsc_4v_f_t_3)

                ####################################################################################################################

                # Extracting NLSC NEW TYPE OF PACKET a 4 VERTEX GRADATION TEXTURED
                count_n_nlsc_4v_g_t = prim_block.count(new_nlsc_four_vertex_gradation_textured)
                position_prim_n_nlsc_4v_g_t = prim_block.find(new_nlsc_four_vertex_gradation_textured)
                total_count_tc.append(count_n_nlsc_4v_g_t * 4)

                while count_n_nlsc_4v_g_t > 0:
                    count_n_nlsc_4v_g_t -= 1
                    start_position_prim = position_prim_n_nlsc_4v_g_t + 4
                    end_position_prim = start_position_prim + 40
                    primitive_n_nlsc_4v_g_t = prim_block[start_position_prim : end_position_prim]
                    position_prim_n_nlsc_4v_g_t += 44
                    u_0 = primitive_n_nlsc_4v_g_t[0:1]
                    v_0 = primitive_n_nlsc_4v_g_t[1:2]
                    cba_value = primitive_n_nlsc_4v_g_t[2:4]
                    u_1 = primitive_n_nlsc_4v_g_t[4:5]
                    v_1 = primitive_n_nlsc_4v_g_t[5:6]
                    tsb_value = primitive_n_nlsc_4v_g_t[6:8]
                    u_2 = primitive_n_nlsc_4v_g_t[8:9]
                    v_2 = primitive_n_nlsc_4v_g_t[9:10]
                    value_not_used_0 = primitive_n_nlsc_4v_g_t[10:12]
                    u_3 = primitive_n_nlsc_4v_g_t[12:13]
                    v_3 = primitive_n_nlsc_4v_g_t[13:14]
                    value_not_used_1 = primitive_n_nlsc_4v_g_t[14:16]
                    red_value_0 = primitive_n_nlsc_4v_g_t[16:17]
                    green_value_0 = primitive_n_nlsc_4v_g_t[17:18]
                    blue_value_0 = primitive_n_nlsc_4v_g_t[18:19]
                    value_not_used_2 = primitive_n_nlsc_4v_g_t[19:20]
                    red_value_1 = primitive_n_nlsc_4v_g_t[20:21]
                    green_value_1 = primitive_n_nlsc_4v_g_t[21:22]
                    blue_value_1 = primitive_n_nlsc_4v_g_t[22:23]
                    value_not_used_3 = primitive_n_nlsc_4v_g_t[23:24]
                    red_value_2 = primitive_n_nlsc_4v_g_t[24:25]
                    green_value_2 = primitive_n_nlsc_4v_g_t[25:26]
                    blue_value_2 = primitive_n_nlsc_4v_g_t[26:27]
                    value_not_used_4 = primitive_n_nlsc_4v_g_t[27:28]
                    red_value_3 = primitive_n_nlsc_4v_g_t[28:29]
                    green_value_3 = primitive_n_nlsc_4v_g_t[29:30]
                    blue_value_3 = primitive_n_nlsc_4v_g_t[30:31]
                    value_not_used_5 = primitive_n_nlsc_4v_g_t[31:32]
                    vertex_0 = primitive_n_nlsc_4v_g_t[32:34]
                    vertex_1 = primitive_n_nlsc_4v_g_t[34:36]
                    vertex_2 = primitive_n_nlsc_4v_g_t[36:38]
                    vertex_3 = primitive_n_nlsc_4v_g_t[38:40]

                    u_0_to_num = str(unpack('<B', u_0)).replace("(", "").replace(")", "").replace(",", "")
                    u_0_num = float(u_0_to_num) / 256
                    v_0_to_num = str(unpack('<B', v_0)).replace("(", "").replace(")", "").replace(",", "")
                    v_0_num = float(v_0_to_num) / 256
                    u_2_to_num = str(unpack('<B', u_2)).replace("(", "").replace(")", "").replace(",", "")
                    u_2_num = float(u_2_to_num) / 256
                    v_2_to_num = str(unpack('<B', v_2)).replace("(", "").replace(")", "").replace(",", "")
                    v_2_num = float(v_2_to_num) / 256
                    u_3_to_num = str(unpack('<B', u_3)).replace("(", "").replace(")", "").replace(",", "")
                    u_3_num = float(u_3_to_num) / 256
                    v_3_to_num = str(unpack('<B', v_3)).replace("(", "").replace(")", "").replace(",", "")
                    v_3_num = float(v_3_to_num) / 256
                    u_1_to_num = str(unpack('<B', u_1)).replace("(", "").replace(")", "").replace(",", "")
                    u_1_num = float(u_1_to_num) / 256
                    v_1_to_num = str(unpack('<B', v_1)).replace("(", "").replace(")", "").replace(",", "")
                    v_1_num = float(v_1_to_num) / 256

                    #OBJ UV Writer
                    write_UV_n_nlsc_4v_g_t_0 = "vt" + " " + str(u_0_num) + " " + str(1 - v_0_num) + "\n"
                    write_UV_n_nlsc_4v_g_t_1 = "vt" + " " + str(u_2_num) + " " + str(1 - v_2_num) + "\n"
                    write_UV_n_nlsc_4v_g_t_2 = "vt" + " " + str(u_3_num) + " " + str(1 - v_3_num) + "\n"
                    write_UV_n_nlsc_4v_g_t_3 = "vt" + " " + str(u_1_num) + " " + str(1 - v_1_num) + "\n"

                    file_write.write(write_UV_n_nlsc_4v_g_t_0)
                    file_write.write(write_UV_n_nlsc_4v_g_t_1)
                    file_write.write(write_UV_n_nlsc_4v_g_t_2)
                    file_write.write(write_UV_n_nlsc_4v_g_t_3)
                
                summatory_tc = sum(total_count_tc)
                texture_coordinate_num.append(summatory_tc)
                #print(summatory_tc)
            tc_total = sum(texture_coordinate_num)
            print(texture_coordinate_num)
            #print(tc_total)
            file_write.write("# " + str(tc_total) + " " + "Texture Coordinates" + "\n" + "\n")
                    ############################# END OF TEXTURE COORDINATE LOOP #############################

            # NORMAL WRITER
            normal_info = "\n" + "# Here start the Normal Block of the model" + "\n" + "\n"
            file_write.write(normal_info)
            normal_splitted = []
            for normal in normals_block:
                n_x = normal[0:2]
                n_y = normal[2:4]
                n_z = normal[4:6]
                short_pad = normal[6:8] # This is ignored in the model
                nor_x = unpack('<h', n_x) #int.from_bytes(v_x, byteorder='little', signed=True) #unpack('<h', v_x)
                nor_y = unpack('<h', n_y) #int.from_bytes(v_y, byteorder='little', signed=True) #unpack('<h', v_y)
                nor_z = unpack('<h', n_z) #int.from_bytes(v_z, byteorder='little', signed=True) #unpack('<h', v_z)
                normal_each = [nor_x, nor_y, nor_z]
                normal_splitted.append(normal_each)
                #print(normal)
            for normal_x, normal_y, normal_z in normal_splitted:
                norm_x = str(normal_x).replace("(", "").replace(")", "").replace(",", "")
                norm_y = str(normal_y).replace("(", "").replace(")", "").replace(",", "")
                norm_z = str(normal_z).replace("(", "").replace(")", "").replace(",", "")
                normal_x = str(float(int(norm_x) / 1000))
                normal_y = str(float(int(norm_y) / 1000))
                normal_z = str(float(int(norm_z) / 1000))
                n = "vn" + " " + normal_x + " " + normal_y + " " + normal_z + "\n"
                file_write.write(n)
                #print(n_x, n_y, n_z)
            number_of_normals = len(normals_block)
            file_write.write("# " + str(number_of_normals) + " " + "Normals" + "\n" + "\n")

            # PRIMITIVE WRITER - THIS WILL BE TOO EXPERIMENTAL

            primitive_info = "# Here Starts the Face/Primitives Block of the model" + "\n" + "\n"
            file_write.write(primitive_info)
            new_vertices_count = vertices_number.copy()
            number_0 = 1
            new_vertices_count.insert(0, number_0)
            addition_number_0 = new_vertices_count
            #print(addition_number_0)
            new_texture_coord_count = texture_coordinate_num.copy()
            number_1 = 1
            new_texture_coord_count.insert(0, number_1)
            addition_number_1 = new_texture_coord_count
           

            for numeration, prim_block in primitives_block_enum:

                # Packet Configuration of 3 Vertex Polygon with Light Source Calculation
                lsc_three_vertex_gouraud_no_textured_solid = b'\x06\x04\x00\x30'      # 3 VERTEX GOURAUD NO TEXTURED SOLID - ok
                lsc_three_vertex_flat_no_textured_solid =  b'\x04\x03\x00\x20'        # 3 VERTEX FLAT NO TEXTURED SOLID - ok
                lsc_three_vertex_gouraud_no_textured_gradation = b'\x06\x06\x04\x30'  # 3 VERTEX GOURAUD NO TEXTURED GRADATION - ok
                lsc_three_vertex_flat_no_textured_gradation = b'\x06\x05\x04\x20'     # 3 VERTEX FLAT NO TEXTURED GRADATION - ok
                lsc_three_vertex_gouraud_textured = b'\x09\x06\x00\x34' # NO FIFTH VALUE to check, FIFTH value correspond to CBA // 3 VERTEX GOURAUD TEXTURED - ok
                lsc_three_vertex_flat_textured = b'\x07\x05\x00\x24' # NO FIFTH VALUE to check, FIFTH value correspond to CBA // 3 VERTEX FLAT TEXTURED - ok
                new_lsc_three_vertex_gouraud = b'\x09\x06\x02\x34' # NEW 3 VERTEX GOURAUD TEXTURED - ok
                new_lsc_three_vertex_gouraud_2 = b'\x09\x06\x00\x36' # NEW 3 VERTEX GOURAUD TEXTURED - ok

                # Packet Configuration for 4 Vertex Polygon with Light Source Calculation
                lsc_four_vertex_gouraud_no_textured_solid = b'\x08\x05\x00\x38'       # 4 VERTEX GOURAUD NO TEXTURED SOLID - ok
                lsc_four_vertex_flat_no_textured_solid = b'\x05\x04\x00\x28'          # 4 VERTEX FLAT NO TEXTURED SOLID - ok
                lsc_four_vertex_gouraud_no_textured_gradation = b'\x08\x08\x04\x38'   # 4 VERTEX GOURAUD NO TEXTURED GRADATION - ok
                lsc_four_vertex_flat_no_textured_gradation = b'\x08\x07\x04\x28'      # 4 VERTEX FLAT NO TEXTURED GRADATION - ok
                lsc_four_vertex_gouraud_textured = b'\x0c\x08\x00\x3c' # NO FIFTH VALUE to check, FIFTH value correspond to CBA // 4 VERTEX GOURAUD TEXTURED - ok
                lsc_four_vertex_flat_textured = b'\x09\x07\x00\x2c' # NO FIFTH VALUE to check, FIFTH value to correspond to CBA // 4 VERTEX FLAT TEXTURED - ok
                new_lsc_four_vertex_gouraud_textured = b'\x0c\x08\x00\x3e' # NEW TYPE OF PACKET a 4 VERTEX GOURAUD TEXTURED - ok
                new_lsc_four_vertex_gouraud_textured_2 = b'\x0c\x08\x02\x3c' # NEW TYPE OF PACKET a 4 VERTEX GOURAUD TEXTURED - ok
                new_lsc_four_vertex_gouraud_no_textured_solid = b'\x08\x05\x00\x3a' # NEW 4 VERTEX GOURAUD NO TEXTURED SOLID - ok

                # Packet configuration for 3 Vertex Polygon with No Light Source Calculation
                nlsc_three_vertex_gradation_no_textured = b'\x06\x05\x01\x31'         # 3 VERTEX GRADATION NO TEXTURED - ok
                nlsc_three_vertex_flat_no_textured = b'\x04\x03\x01\x21'              # 3 VERTEX FLAT NO TEXTURED - ok 
                nlsc_three_vertex_gradation_textured = b'\x09\x08\x01\x35' # NO FIFTH VALUE to check, FIFTH value correspond to CBA // 3 VERTEX GRADATION TEXTURED - ok
                nlsc_three_vertex_flat_textured = b'\x07\x06\x01\x25' # NO FIFTH VALUE to check, FIFTH value correspond to CBA // 3 VERTEX FLAT TEXTURED - ok
                new_nlsc_three_vertex_gradation_textured = b'\x09\x08\x01\x37' # NEW TYPE OF PACKET a 3 VERTEX GRADATION TEXTURED - ok

                # Packet Configuration for 4 Vertex Polygon with No Light Source Calculation
                nlsc_four_vertex_gradation_no_textured = b'\x08\x06\x01\x39'          # 4 VERTEX GRADATION NO TEXTURED - ok
                nlsc_four_vertex_flat_no_textured = b'\x05\x03\x01\x29'                    # 4 VERTEX FLAT NO TEXTURED - ok
                nlsc_four_vertex_gradation_textured = b'\x0c\x0a\x01\x3d' # NO FIFTH VALUE to check, FIFTH value correspond to CBA // 4 VERTEX GRADATION TEXTURED - ok
                nlsc_four_vertex_flat_textured = b'\x09\x07\x01\x2d' # NO FIFTH VALUE to check, FIFTH value correspond to CBA // 4 VERTEX FLAT TEXTURED - ok
                new_nlsc_four_vertex_gradation_textured = b'\x0c\x0a\x01\x3f' # NEW TYPE OF PACKET a 4 VERTEX GRADATION TEXTURED - ok

                # Packet Configuration for “Straight Line”
                sl_gradation_on = b'\x04\x03\x01\x50'                                 # STRAIGHT LINE GRADATION ON - ok
                sl_gradation_off = b'\x03\x02\x01\x40'                                # STRAIGHT LINE GRADATION OFF - ok

                # Packet Configuration for Sprites
                sp_1x1 = b'\x04\x02\x01\x6c' # NO FIFTH VALUE to check, FIFTH value correspond to TSB // SPRITE 1X1 - ok
                sp_free_size = b'\x05\x03\x01\x64' # NO FIFTH VALUE to check, FIFTH value correspond to TSB // SPRITE FREE SIZE - ok
                sp_16x16 = b'\x04\x02\x01\x7c' # NO FIFTH VALUE to check, FIFTH value correspond to TSB // SPRITE 16X16 - ok
                sp_8x8 = b'\x04\x02\x01\x74' # NO FIFTH VALUE to check, FIFTH value correspond to TSB // SPRITE 8X8 - ok

                object_number = "\n" + "# Primitives from Object number " + " " + str(numeration) + "\n" + "\n"
                file_write.write(object_number)

                face_header = "g" + " " + "Object_Number_" + str(numeration) + "\n" + "usemtl" + " " + "Object_Num" + " " + str(numeration) + "\n"
                file_write.write(face_header)

                # Vertices used counter
                pn = list(accumulate(addition_number_0))
                p = pn[numeration]
                #print(numeration)
                #print(p)
                tn = list(accumulate(addition_number_1))
                t = tn[numeration]
                #print(t)



                ############################################# LIGHT SOURCE CALCULATION #############################################

                # Extracting LSC 3 VERTEX GOURAUD NO TEXTURED SOLID PRIMITIVE // WORKING AS INTENDED
                count_lsc_3v_g_n_s = prim_block.count(lsc_three_vertex_gouraud_no_textured_solid)
                position_prim_lsc_3v_g_n_s = prim_block.find(lsc_three_vertex_gouraud_no_textured_solid)

                while count_lsc_3v_g_n_s > 0:
                    count_lsc_3v_g_n_s -= 1
                    start_position_prim = position_prim_lsc_3v_g_n_s + 4
                    end_position_prim = start_position_prim + 16
                    primitive_lsc_3v_g_n_s = prim_block[start_position_prim : end_position_prim]
                    position_prim_lsc_3v_g_n_s += 20
                    red_value = primitive_lsc_3v_g_n_s[0:1]
                    green_value = primitive_lsc_3v_g_n_s[1:2]
                    blue_value = primitive_lsc_3v_g_n_s[2:3]
                    mode_value = primitive_lsc_3v_g_n_s[3:4]
                    normal_0 = primitive_lsc_3v_g_n_s[4:6]
                    vertex_0 = primitive_lsc_3v_g_n_s[6:8]
                    normal_1 = primitive_lsc_3v_g_n_s[8:10]
                    vertex_1 = primitive_lsc_3v_g_n_s[10:12]
                    normal_2 = primitive_lsc_3v_g_n_s[12:14]
                    vertex_2 = primitive_lsc_3v_g_n_s[14:16]
                    #print(primitive_lsc_3v_g_n_s)

                    # OBJ Writer
                    write_primitive_lsc_3v_g_n_s = "f" + " " + str(sum(unpack('<H', vertex_2), p)).replace("(", "").replace(")", "").replace(",", "") + " " + str(sum(unpack('<H', vertex_1), p)).replace("(", "").replace(")", "").replace(",", "") + " " + str(sum(unpack('<H', vertex_0), p)).replace("(", "").replace(")", "").replace(",", "") + "\n"
                    file_write.write(write_primitive_lsc_3v_g_n_s)

                ####################################################################################################################

                # Extracting LSC 3 VERTEX FLAT NO TEXTURED SOLID // WORKING AS INTENDED
                count_lsc_3v_f_n_t_s = prim_block.count(lsc_three_vertex_flat_no_textured_solid)
                position_prim_lsc_3v_f_n_t_s = prim_block.find(lsc_three_vertex_flat_no_textured_solid)
                
                while count_lsc_3v_f_n_t_s > 0:
                    count_lsc_3v_f_n_t_s-= 1
                    start_position_prim = position_prim_lsc_3v_f_n_t_s + 4
                    end_position_prim = start_position_prim + 12
                    primitive_lsc_3v_f_n_t_s = prim_block[start_position_prim : end_position_prim]
                    position_prim_lsc_3v_f_n_t_s += 16
                    red_value = primitive_lsc_3v_f_n_t_s[0:1]
                    green_value = primitive_lsc_3v_f_n_t_s[1:2]
                    blue_value = primitive_lsc_3v_f_n_t_s[2:3]
                    mode_value = primitive_lsc_3v_f_n_t_s[3:4]
                    normal_0 = primitive_lsc_3v_f_n_t_s[4:6]
                    vertex_0 = primitive_lsc_3v_f_n_t_s[6:8]
                    vertex_1 = primitive_lsc_3v_f_n_t_s[8:10]
                    vertex_2 = primitive_lsc_3v_f_n_t_s[10:12]
                    #print(primitive_lsc_3v_f_n_t_s)

                    # OBJ Writer
                    write_primitive_lsc_3v_f_n_t_s = "f" + " " + str(sum(unpack('<H', vertex_2), p)).replace("(", "").replace(")", "").replace(",", "") + " " + str(sum(unpack('<H', vertex_1), p)).replace("(", "").replace(")", "").replace(",", "") + " " + str(sum(unpack('<H', vertex_0), p)).replace("(", "").replace(")", "").replace(",", "") + "\n"
                    file_write.write(write_primitive_lsc_3v_f_n_t_s)

                ####################################################################################################################

                # Extracting LSC 3 VERTEX GOURAUD NO TEXTURED GRADATION // WORKING AS INTENDED
                count_lsc_3v_g_n_t_g = prim_block.count(lsc_three_vertex_gouraud_no_textured_gradation)
                position_prim_lsc_3v_g_n_t_g = prim_block.find(lsc_three_vertex_gouraud_no_textured_gradation)

                while count_lsc_3v_g_n_t_g > 0:
                    count_lsc_3v_g_n_t_g -= 1
                    start_position_prim = position_prim_lsc_3v_g_n_t_g + 4
                    end_position_prim = start_position_prim + 24
                    primitive_lsc_3v_g_n_t_g = prim_block[start_position_prim : end_position_prim]
                    position_prim_lsc_3v_g_n_t_g += 28
                    red_value_0 = primitive_lsc_3v_g_n_t_g[0:1]
                    green_value_0 = primitive_lsc_3v_g_n_t_g[1:2]
                    blue_value_0 = primitive_lsc_3v_g_n_t_g[2:3]
                    mode_value = primitive_lsc_3v_g_n_t_g[3:4]
                    red_value_1 = primitive_lsc_3v_g_n_t_g[4:5]
                    green_value_1 = primitive_lsc_3v_g_n_t_g[5:6]
                    blue_value_1 = primitive_lsc_3v_g_n_t_g[6:7]
                    value_not_used_0 = primitive_lsc_3v_g_n_t_g[7:8]
                    red_value_2 = primitive_lsc_3v_g_n_t_g[8:9]
                    green_value_2 = primitive_lsc_3v_g_n_t_g[9:10]
                    blue_value_2 = primitive_lsc_3v_g_n_t_g[10:11]
                    value_not_used_1 = primitive_lsc_3v_g_n_t_g[11:12]
                    normal_0 = primitive_lsc_3v_g_n_t_g[12:14]
                    vertex_0 = primitive_lsc_3v_g_n_t_g[14:16]
                    normal_1 = primitive_lsc_3v_g_n_t_g[16:18]
                    vertex_1 = primitive_lsc_3v_g_n_t_g[18:20]
                    normal_2 = primitive_lsc_3v_g_n_t_g[20:22]
                    vertex_2 = primitive_lsc_3v_g_n_t_g[22:24]
                    #print(primitive_lsc_3v_g_n_t_g)

                    # OBJ Writer
                    write_primitive_lsc_3v_g_n_t_g = "f" + " " + str(sum(unpack('<H', vertex_2), p)).replace("(", "").replace(")", "").replace(",", "") + " " + str(sum(unpack('<H', vertex_1), p)).replace("(", "").replace(")", "").replace(",", "") + " " + str(sum(unpack('<H', vertex_0), p)).replace("(", "").replace(")", "").replace(",", "") + "\n"
                    file_write.write(write_primitive_lsc_3v_g_n_t_g)

                ####################################################################################################################

                # Extracting LSC 3 VERTEX FLAT NO TEXTURED GRADATION // WORKING AS INTENDED
                count_lsc_3v_f_n_t_g = prim_block.count(lsc_three_vertex_flat_no_textured_gradation)
                position_prim_lsc_3v_f_n_t_g = prim_block.find(lsc_three_vertex_flat_no_textured_gradation)

                while count_lsc_3v_f_n_t_g > 0:
                    count_lsc_3v_f_n_t_g -= 1
                    start_position_prim = position_prim_lsc_3v_f_n_t_g + 4
                    end_position_prim = start_position_prim + 20
                    primitive_lsc_3v_f_n_t_g = prim_block[start_position_prim : end_position_prim]
                    position_prim_lsc_3v_f_n_t_g += 24
                    red_value_0 = primitive_lsc_3v_f_n_t_g[0:1]
                    green_value_0 = primitive_lsc_3v_f_n_t_g[1:2]
                    blue_value_0 = primitive_lsc_3v_f_n_t_g[2:3]
                    mode_value = primitive_lsc_3v_f_n_t_g[3:4]
                    red_value_1 = primitive_lsc_3v_f_n_t_g[4:5]
                    green_value_1 = primitive_lsc_3v_f_n_t_g[5:6]
                    blue_value_1 = primitive_lsc_3v_f_n_t_g[6:7]
                    value_not_used_0 = primitive_lsc_3v_f_n_t_g[7:8]
                    red_value_2 = primitive_lsc_3v_f_n_t_g[8:9]
                    green_value_2 = primitive_lsc_3v_f_n_t_g[9:10]
                    blue_value_2 = primitive_lsc_3v_f_n_t_g[10:11]
                    value_not_used_1 = primitive_lsc_3v_f_n_t_g[11:12]
                    normal_0 = primitive_lsc_3v_f_n_t_g[12:14]
                    vertex_0 = primitive_lsc_3v_f_n_t_g[14:16]
                    vertex_1 = primitive_lsc_3v_f_n_t_g[16:18]
                    vertex_2 = primitive_lsc_3v_f_n_t_g[18:20]

                    # OBJ Writer
                    write_primitive_lsc_3v_f_n_t_g = "f" + " " + str(sum(unpack('<H', vertex_2), p)).replace("(", "").replace(")", "").replace(",", "") + " " + str(sum(unpack('<H', vertex_1), p)).replace("(", "").replace(")", "").replace(",", "") + " " + str(sum(unpack('<H', vertex_0), p)).replace("(", "").replace(")", "").replace(",", "") + "\n"
                    file_write.write(write_primitive_lsc_3v_f_n_t_g)

                ####################################################################################################################

                # Extracting LSC 3 VERTEX GOURAUD TEXTURED // WORKING AS INTENDED
                count_lsc_3v_g_t = prim_block.count(lsc_three_vertex_gouraud_textured)
                position_prim_lsc_3v_g_t = prim_block.find(lsc_three_vertex_gouraud_textured)

                while count_lsc_3v_g_t > 0:
                    count_lsc_3v_g_t -= 1
                    start_position_prim = position_prim_lsc_3v_g_t + 4
                    end_position_prim = start_position_prim + 24
                    primitive_lsc_3v_g_t = prim_block[start_position_prim : end_position_prim]
                    position_prim_lsc_3v_g_t += 28
                    u_0 = primitive_lsc_3v_g_t[0:1] # U value = X in 3D - texture coordinate
                    v_0 = primitive_lsc_3v_g_t[1:2] # V value = Y in 3D - texture coordinate
                    cba_value = primitive_lsc_3v_g_t[2:4] # CBA = CLUT position of texture in VRAM
                    u_1 = primitive_lsc_3v_g_t[4:5]
                    v_1 = primitive_lsc_3v_g_t[5:6]
                    tsb_value = primitive_lsc_3v_g_t[6:8] # TSB = Information and properties of texture/sprite to be applied to the geometry
                    u_2 = primitive_lsc_3v_g_t[8:9]
                    v_2 = primitive_lsc_3v_g_t[9:10]
                    value_not_used = primitive_lsc_3v_g_t[10:12]
                    normal_0 = primitive_lsc_3v_g_t[12:14]
                    vertex_0 = primitive_lsc_3v_g_t[14:16]
                    normal_1 = primitive_lsc_3v_g_t[16:18]
                    vertex_1 = primitive_lsc_3v_g_t[18:20]
                    normal_2 = primitive_lsc_3v_g_t[20:22]
                    vertex_2 = primitive_lsc_3v_g_t[22:24]

                    # OBJ Writer
                    write_primitive_lsc_3v_g_t = "f" + " " + str(sum(unpack('<H', vertex_2), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t) + " " + str(sum(unpack('<H', vertex_1), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t + 1) + " " + str(sum(unpack('<H', vertex_0), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t + 2) + "\n"
                    file_write.write(write_primitive_lsc_3v_g_t)
                    t += 3

                ####################################################################################################################

                # Extracting LSC 3 VERTEX FLAT TEXTURED
                count_lsc_3v_f_t = prim_block.count(lsc_three_vertex_flat_textured)
                position_prim_lsc_3v_f_t = prim_block.find(lsc_three_vertex_flat_textured)

                while count_lsc_3v_f_t > 0:
                    count_lsc_3v_f_t -= 1
                    start_position_prim = position_prim_lsc_3v_f_t + 4
                    end_position_prim = start_position_prim + 20
                    primitive_lsc_3v_f_t = prim_block[start_position_prim : end_position_prim]
                    position_prim_lsc_3v_f_t += 24
                    u_0 = primitive_lsc_3v_f_t[0:1]
                    v_0 = primitive_lsc_3v_f_t[1:2]
                    cba_value = primitive_lsc_3v_f_t[2:4]
                    u_1 = primitive_lsc_3v_f_t[4:5]
                    v_1 = primitive_lsc_3v_f_t[5:6]
                    tsb_value = primitive_lsc_3v_f_t[6:8]
                    u_2 = primitive_lsc_3v_f_t[8:9]
                    v_2 = primitive_lsc_3v_f_t[9:10]
                    value_not_used = primitive_lsc_3v_f_t[10:12]
                    normal_0 = primitive_lsc_3v_f_t[12:14]
                    vertex_0 = primitive_lsc_3v_f_t[14:16]
                    vertex_1 = primitive_lsc_3v_f_t[16:18]
                    vertex_2 = primitive_lsc_3v_f_t[18:20]

                    # OBJ Writer
                    write_primitive_lsc_3v_f_t = "f" + " " + str(sum(unpack('<H', vertex_2), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t) + " " + str(sum(unpack('<H', vertex_1), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t + 1) + " " + str(sum(unpack('<H', vertex_0), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t + 2) + "\n"
                    file_write.write(write_primitive_lsc_3v_f_t)
                    t += 3

                ####################################################################################################################

                # Extracting LSC NEW 3 VERTEX GOURAUD TEXTURED
                count_n_lsc_3v_g_t = prim_block.count(new_lsc_three_vertex_gouraud)
                position_prim_n_lsc_3v_g_t = prim_block.find(new_lsc_three_vertex_gouraud)

                while count_n_lsc_3v_g_t > 0:
                    count_n_lsc_3v_g_t -= 1
                    start_position_prim = position_prim_n_lsc_3v_g_t + 4
                    end_position_prim = start_position_prim + 24
                    primitive_n_lsc_3v_g_t = prim_block[start_position_prim : end_position_prim]
                    position_prim_n_lsc_3v_g_t += 28
                    u_0 = primitive_n_lsc_3v_g_t[0:1]
                    v_0 = primitive_n_lsc_3v_g_t[1:2]
                    cba_value = primitive_n_lsc_3v_g_t[2:4]
                    u_1 = primitive_n_lsc_3v_g_t[4:5]
                    v_1 = primitive_n_lsc_3v_g_t[5:6]
                    tsb_value = primitive_n_lsc_3v_g_t[6:8]
                    u_2 = primitive_n_lsc_3v_g_t[8:9]
                    v_2 = primitive_n_lsc_3v_g_t[9:10]
                    value_not_used = primitive_n_lsc_3v_g_t[10:12]
                    normal_0 = primitive_n_lsc_3v_g_t[12:14]
                    vertex_0 = primitive_n_lsc_3v_g_t[14:16]
                    normal_1 = primitive_n_lsc_3v_g_t[16:18]
                    vertex_1 = primitive_n_lsc_3v_g_t[18:20]
                    normal_2 = primitive_n_lsc_3v_g_t[20:22]
                    vertex_2 = primitive_n_lsc_3v_g_t[22:24]

                    # OBJ Writer
                    write_primitive_n_lsc_3v_g_t = "f" + " " + str(sum(unpack('<H', vertex_2), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t) + " " + str(sum(unpack('<H', vertex_1), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t + 1) + " " + str(sum(unpack('<H', vertex_0), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t + 2) + "\n"
                    file_write.write(write_primitive_n_lsc_3v_g_t)
                    t += 3

                ####################################################################################################################

                # Extracting LSC 2nd NEW 3 VERTEX GOURAUD TEXTURED
                count_n_lsc_3v_g_t_2 = prim_block.count(new_lsc_three_vertex_gouraud_2)
                position_prim_n_lsc_3v_g_t_2 = prim_block.find(new_lsc_three_vertex_gouraud_2)

                while count_n_lsc_3v_g_t_2 > 0:
                    count_n_lsc_3v_g_t_2 -= 1
                    start_position_prim = position_prim_n_lsc_3v_g_t_2 + 4
                    end_position_prim = start_position_prim + 24
                    primitive_n_lsc_3v_g_t_2 = prim_block[start_position_prim : end_position_prim]
                    position_prim_n_lsc_3v_g_t_2 += 28
                    u_0 = primitive_n_lsc_3v_g_t_2[0:1]
                    v_0 = primitive_n_lsc_3v_g_t_2[1:2]
                    cba_value = primitive_n_lsc_3v_g_t_2[2:4]
                    u_1 = primitive_n_lsc_3v_g_t_2[4:5]
                    v_1 = primitive_n_lsc_3v_g_t_2[5:6]
                    tsb_value = primitive_n_lsc_3v_g_t_2[6:8]
                    u_2 = primitive_n_lsc_3v_g_t_2[8:9]
                    v_2 = primitive_n_lsc_3v_g_t_2[9:10]
                    value_not_used = primitive_n_lsc_3v_g_t_2[10:12]
                    normal_0 = primitive_n_lsc_3v_g_t_2[12:14]
                    vertex_0 = primitive_n_lsc_3v_g_t_2[14:16]
                    normal_1 = primitive_n_lsc_3v_g_t_2[16:18]
                    vertex_1 = primitive_n_lsc_3v_g_t_2[18:20]
                    normal_2 = primitive_n_lsc_3v_g_t_2[20:22]
                    vertex_2 = primitive_n_lsc_3v_g_t_2[22:24]

                    # OBJ Writer
                    write_primitive_n_lsc_3v_g_t_2 = "f" + " " + str(sum(unpack('<H', vertex_2), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t) + " " + str(sum(unpack('<H', vertex_1), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t + 1) + " " + str(sum(unpack('<H', vertex_0), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t + 2) + "\n"
                    file_write.write(write_primitive_n_lsc_3v_g_t_2)
                    t += 3

                ####################################################################################################################

                # Extracting LSC 4 VERTEX GOURAUD NO TEXTURED SOLID PRIMITIVE // WORKING AS INTENDED
                count_lsc_4v_g_n_t_s = prim_block.count(lsc_four_vertex_gouraud_no_textured_solid)
                position_prim_lsc_4v_g_n_t = prim_block.find(lsc_four_vertex_gouraud_no_textured_solid)

                while count_lsc_4v_g_n_t_s > 0:
                    count_lsc_4v_g_n_t_s -= 1
                    start_position_prim = position_prim_lsc_4v_g_n_t + 4
                    end_position_prim = start_position_prim + 20
                    primitive_lsc_4v_g_n_t_s = prim_block[start_position_prim : end_position_prim]
                    position_prim_lsc_4v_g_n_t += 24
                    red_value = primitive_lsc_4v_g_n_t_s[0:1]
                    green_value = primitive_lsc_4v_g_n_t_s[1:2]
                    blue_value = primitive_lsc_4v_g_n_t_s[2:3]
                    mode_value = primitive_lsc_4v_g_n_t_s[3:4]
                    normal_0 = primitive_lsc_4v_g_n_t_s[4:6]
                    vertex_0 = primitive_lsc_4v_g_n_t_s[6:8]
                    normal_1 = primitive_lsc_4v_g_n_t_s[8:10]
                    vertex_1 = primitive_lsc_4v_g_n_t_s[10:12]
                    normal_2 = primitive_lsc_4v_g_n_t_s[12:14]
                    vertex_2 = primitive_lsc_4v_g_n_t_s[14:16]
                    normal_3 = primitive_lsc_4v_g_n_t_s[16:18]
                    vertex_3 = primitive_lsc_4v_g_n_t_s[18:20]

                    # OBJ Writer
                    write_primitive_lsc_4v_g_n_t_s = "f" + " " + str(sum(unpack('<H', vertex_0), p)).replace("(", "").replace(")", "").replace(",", "") + " " + str(sum(unpack('<H', vertex_2), p)).replace("(", "").replace(")", "").replace(",", "") + " " + str(sum(unpack('<H', vertex_3), p)).replace("(", "").replace(")", "").replace(",", "") + " " + str(sum(unpack('<H', vertex_1), p)).replace("(", "").replace(")", "").replace(",", "") + "\n"
                    file_write.write(write_primitive_lsc_4v_g_n_t_s)
                    #print(vertex_0, vertex_1, vertex_2, vertex_3)

                ####################################################################################################################

                # Extracting LSC 4 VERTEX FLAT NO TEXTURED SOLID // WORKING AS INTENDED
                count_lsc_4v_f_n_t_s = prim_block.count(lsc_four_vertex_flat_no_textured_solid)
                position_prim_lsc_4v_f_n_t_s = prim_block.find(lsc_four_vertex_flat_no_textured_solid)

                while count_lsc_4v_f_n_t_s > 0:
                    count_lsc_4v_f_n_t_s -= 1
                    start_position_prim = position_prim_lsc_4v_f_n_t_s + 4
                    end_position_prim = start_position_prim + 16
                    primitive_lsc_4v_f_n_t_s = prim_block[start_position_prim : end_position_prim]
                    position_prim_lsc_4v_f_n_t_s += 20
                    red_value = primitive_lsc_4v_f_n_t_s[0:1]
                    green_value = primitive_lsc_4v_f_n_t_s[1:2]
                    blue_value = primitive_lsc_4v_f_n_t_s[2:3]
                    mode_value = primitive_lsc_4v_f_n_t_s[3:4]
                    normal_0 = primitive_lsc_4v_f_n_t_s[4:6]
                    vertex_0 = primitive_lsc_4v_f_n_t_s[6:8]
                    vertex_1 = primitive_lsc_4v_f_n_t_s[8:10]
                    vertex_2 = primitive_lsc_4v_f_n_t_s[10:12]
                    vertex_3 = primitive_lsc_4v_f_n_t_s[12:14]
                    value_not_used = primitive_lsc_4v_f_n_t_s[14:16]

                    # OBJ Writer
                    write_primitive_lsc_4v_f_n_t_s = "f" + " " + str(sum(unpack('<H', vertex_0), p)).replace("(", "").replace(")", "").replace(",", "") + " " + str(sum(unpack('<H', vertex_2), p)).replace("(", "").replace(")", "").replace(",", "") + " " + str(sum(unpack('<H', vertex_3), p)).replace("(", "").replace(")", "").replace(",", "") + " " + str(sum(unpack('<H', vertex_1), p)).replace("(", "").replace(")", "").replace(",", "") + "\n"
                    file_write.write(write_primitive_lsc_4v_f_n_t_s)

                ####################################################################################################################

                # Extracting LSC 4 VERTEX GOURAUD NO TEXTURED GRADATION // WORKING AS INTENDED
                count_lsc_4v_g_n_t_g = prim_block.count(lsc_four_vertex_gouraud_no_textured_gradation)
                position_prim_lsc_4v_g_n_t_g = prim_block.find(lsc_four_vertex_gouraud_no_textured_gradation)

                while count_lsc_4v_g_n_t_g > 0:
                    count_lsc_4v_g_n_t_g -= 1
                    start_position_prim = position_prim_lsc_4v_g_n_t_g + 4
                    end_position_prim = start_position_prim + 32
                    primitive_lsc_4v_g_n_t_g = prim_block[start_position_prim : end_position_prim]
                    position_prim_lsc_4v_g_n_t_g += 36
                    red_value_0 = primitive_lsc_4v_g_n_t_g[0:1]
                    green_value_0 = primitive_lsc_4v_g_n_t_g[1:2]
                    blue_value_0 = primitive_lsc_4v_g_n_t_g[2:3]
                    mode_value = primitive_lsc_4v_g_n_t_g[3:4]
                    red_value_1 = primitive_lsc_4v_g_n_t_g[4:5]
                    green_value_1 = primitive_lsc_4v_g_n_t_g[5:6]
                    blue_value_1 = primitive_lsc_4v_g_n_t_g[6:7]
                    value_not_used_0 = primitive_lsc_4v_g_n_t_g[7:8]
                    red_value_2 = primitive_lsc_4v_g_n_t_g[8:9]
                    green_value_2 = primitive_lsc_4v_g_n_t_g[9:10]
                    blue_value_2 = primitive_lsc_4v_g_n_t_g[10:11]
                    value_not_used_1 = primitive_lsc_4v_g_n_t_g[11:12]
                    red_value_3 = primitive_lsc_4v_g_n_t_g[12:13]
                    green_value_3 = primitive_lsc_4v_g_n_t_g[13:14]
                    blue_value_3 = primitive_lsc_4v_g_n_t_g[14:15]
                    value_not_used_2 = primitive_lsc_4v_g_n_t_g[15:16]
                    normal_0 = primitive_lsc_4v_g_n_t_g[16:18]
                    vertex_0 = primitive_lsc_4v_g_n_t_g[18:20]
                    normal_1 = primitive_lsc_4v_g_n_t_g[20:22]
                    vertex_1 = primitive_lsc_4v_g_n_t_g[22:24]
                    normal_2 = primitive_lsc_4v_g_n_t_g[24:26]
                    vertex_2 = primitive_lsc_4v_g_n_t_g[26:28]
                    normal_3 = primitive_lsc_4v_g_n_t_g[28:30]
                    vertex_3 = primitive_lsc_4v_g_n_t_g[30:32]

                    # OBJ Writer
                    write_primitive_lsc_4v_g_n_t_g = "f" + " " + str(sum(unpack('<H', vertex_0), p)).replace("(", "").replace(")", "").replace(",", "") + " " + str(sum(unpack('<H', vertex_2), p)).replace("(", "").replace(")", "").replace(",", "") + " " + str(sum(unpack('<H', vertex_3), p)).replace("(", "").replace(")", "").replace(",", "") + " " + str(sum(unpack('<H', vertex_1), p)).replace("(", "").replace(")", "").replace(",", "") + "\n"
                    file_write.write(write_primitive_lsc_4v_g_n_t_g)

                ####################################################################################################################

                # Extracting LSC 4 VERTEX FLAT NO TEXTURED GRADATION // WORKING AS INTENDED
                count_lsc_4v_f_n_t_g = prim_block.count(lsc_four_vertex_flat_no_textured_gradation)
                position_prim_lsc_4v_f_n_t_g = prim_block.find(lsc_four_vertex_flat_no_textured_gradation)

                while count_lsc_4v_f_n_t_g > 0:
                    count_lsc_4v_f_n_t_g -=1
                    start_position_prim = position_prim_lsc_4v_f_n_t_g + 4
                    end_position_prim = start_position_prim + 28
                    primitive_lsc_4v_f_n_t_g = prim_block[start_position_prim : end_position_prim]
                    position_prim_lsc_4v_f_n_t_g += 32
                    red_value_0 = primitive_lsc_4v_f_n_t_g[0:1]
                    green_value_0 = primitive_lsc_4v_f_n_t_g[1:2]
                    blue_value_0 = primitive_lsc_4v_f_n_t_g[2:3]
                    mode_value = primitive_lsc_4v_f_n_t_g[3:4]
                    red_value_1 = primitive_lsc_4v_f_n_t_g[4:5]
                    green_value_1 = primitive_lsc_4v_f_n_t_g[5:6]
                    blue_value_1 = primitive_lsc_4v_f_n_t_g[6:7]
                    value_not_used_0 = primitive_lsc_4v_f_n_t_g[7:8]
                    red_value_2 = primitive_lsc_4v_f_n_t_g[8:9]
                    green_value_2 = primitive_lsc_4v_f_n_t_g[9:10]
                    blue_value_2 = primitive_lsc_4v_f_n_t_g[10:11]
                    value_not_used_1 = primitive_lsc_4v_f_n_t_g[11:12]
                    red_value_3 = primitive_lsc_4v_f_n_t_g[12:13]
                    green_value_3 = primitive_lsc_4v_f_n_t_g[13:14]
                    blue_value_3 = primitive_lsc_4v_f_n_t_g[14:15]
                    value_not_used_2 = primitive_lsc_4v_f_n_t_g[15:16]
                    normal_0 = primitive_lsc_4v_f_n_t_g[16:18]
                    vertex_0 = primitive_lsc_4v_f_n_t_g[18:20]
                    vertex_1 = primitive_lsc_4v_f_n_t_g[20:22]
                    vertex_2 = primitive_lsc_4v_f_n_t_g[22:24]
                    vertex_3 = primitive_lsc_4v_f_n_t_g[24:26]
                    value_not_used_3 = primitive_lsc_4v_f_n_t_g[26:28]

                    # OBJ Write
                    write_primitive_lsc_4v_f_n_t_g = "f" + " " + str(sum(unpack('<H', vertex_0), p)).replace("(", "").replace(")", "").replace(",", "") + " " + str(sum(unpack('<H', vertex_2), p)).replace("(", "").replace(")", "").replace(",", "") + " " + str(sum(unpack('<H', vertex_3), p)).replace("(", "").replace(")", "").replace(",", "") + " " + str(sum(unpack('<H', vertex_1), p)).replace("(", "").replace(")", "").replace(",", "") + "\n"
                    file_write.write(write_primitive_lsc_4v_f_n_t_g)

                ####################################################################################################################

                # Extracting LSC 4 VERTEX GOURAUD TEXTURED // WORKING AS INTENDED
                count_lsc_4v_g_t = prim_block.count(lsc_four_vertex_gouraud_textured)
                position_prim_lsc_4v_g_t = prim_block.find(lsc_four_vertex_gouraud_textured)

                while count_lsc_4v_g_t > 0:
                    count_lsc_4v_g_t -= 1
                    start_position_prim = position_prim_lsc_4v_g_t + 4
                    end_position_prim = start_position_prim + 32
                    primitive_lsc_4v_g_t = prim_block[start_position_prim : end_position_prim]
                    position_prim_lsc_4v_g_t += 36
                    u_0 = primitive_lsc_4v_g_t[0:1]
                    v_0 = primitive_lsc_4v_g_t[1:2]
                    cba_value = primitive_lsc_4v_g_t[2:4]
                    u_1 = primitive_lsc_4v_g_t[4:5]
                    v_1 = primitive_lsc_4v_g_t[5:6]
                    tsb_value = primitive_lsc_4v_g_t[6:8]
                    u_2 = primitive_lsc_4v_g_t[8:9]
                    v_2 = primitive_lsc_4v_g_t[9:10]
                    value_not_used_0 = primitive_lsc_4v_g_t[10:12]
                    u_3 = primitive_lsc_4v_g_t[12:13]
                    v_3 = primitive_lsc_4v_g_t[13:14]
                    value_not_used_1 = primitive_lsc_4v_g_t[14:16]
                    normal_0 = primitive_lsc_4v_g_t[16:18]
                    vertex_0 = primitive_lsc_4v_g_t[18:20]
                    normal_1 = primitive_lsc_4v_g_t[20:22]
                    vertex_1 = primitive_lsc_4v_g_t[22:24]
                    normal_2 = primitive_lsc_4v_g_t[24:26]
                    vertex_2 = primitive_lsc_4v_g_t[26:28]
                    normal_3 = primitive_lsc_4v_g_t[28:30]
                    vertex_3 = primitive_lsc_4v_g_t[30:32]
                    
                    # OBJ Writer
                    write_primitive_lsc_4v_g_t = "f" + " " + str(sum(unpack('<H', vertex_0), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t) + " " + str(sum(unpack('<H', vertex_2), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t + 1) + " " + str(sum(unpack('<H', vertex_3), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t + 2) + " " + str(sum(unpack('<H', vertex_1), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t + 3) + "\n"
                    file_write.write(write_primitive_lsc_4v_g_t)
                    t += 4

                ####################################################################################################################

                # Extracting LSC 4 VERTEX FLAT TEXTURED // WORKING AS INTENDED
                count_lsc_4v_f_t = prim_block.count(lsc_four_vertex_flat_textured)
                position_prim_lsc_4v_f_t = prim_block.find(lsc_four_vertex_flat_textured)

                while count_lsc_4v_f_t > 0:
                    count_lsc_4v_f_t -= 1
                    start_position_prim = position_prim_lsc_4v_f_t + 4
                    end_position_prim = start_position_prim + 28
                    primitive_lsc_4v_f_t = prim_block[start_position_prim : end_position_prim]
                    position_prim_lsc_4v_f_t += 32
                    u_0 = primitive_lsc_4v_f_t[0:1]
                    v_0 = primitive_lsc_4v_f_t[1:2]
                    cba_value = primitive_lsc_4v_f_t[2:4]
                    u_1 = primitive_lsc_4v_f_t[4:5]
                    v_1 = primitive_lsc_4v_f_t[5:6]
                    tsb_value = primitive_lsc_4v_f_t[6:8]
                    u_2 = primitive_lsc_4v_f_t[8:9]
                    v_2 = primitive_lsc_4v_f_t[9:10]
                    value_not_used_0 = primitive_lsc_4v_f_t[10:12]
                    u_3 = primitive_lsc_4v_f_t[12:13]
                    v_3 = primitive_lsc_4v_f_t[13:14]
                    value_not_used_1 = primitive_lsc_4v_f_t[14:16]
                    normal_0 = primitive_lsc_4v_f_t[16:18]
                    vertex_0 = primitive_lsc_4v_f_t[18:20]
                    vertex_1 = primitive_lsc_4v_f_t[20:22]
                    vertex_2 = primitive_lsc_4v_f_t[22:24]
                    vertex_3 = primitive_lsc_4v_f_t[24:26]
                    value_not_used_2 = primitive_lsc_4v_f_t[26:28]

                    # OBJ Writer
                    write_primitive_lsc_4v_f_t = "f" + " " + str(sum(unpack('<H', vertex_0), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t) + " " + str(sum(unpack('<H', vertex_2), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t + 1) + " " + str(sum(unpack('<H', vertex_3), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t + 2) + " " + str(sum(unpack('<H', vertex_1), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t + 3) + "\n"
                    file_write.write(write_primitive_lsc_4v_f_t)
                    t += 4

                ####################################################################################################################

                # Extracting LSC NEW TYPE OF PACKET a 4 VERTEX GOURAUD TEXTURED
                count_n_lsc_4v_g_t = prim_block.count(new_lsc_four_vertex_gouraud_textured)
                position_prim_n_lsc_4v_g_t = prim_block.find(new_lsc_four_vertex_gouraud_textured)

                while count_n_lsc_4v_g_t > 0:
                    count_n_lsc_4v_g_t -= 1
                    start_position_prim = position_prim_n_lsc_4v_g_t + 4
                    end_position_prim = start_position_prim + 32
                    primitive_n_lsc_4v_g_t = prim_block[start_position_prim : end_position_prim]
                    position_prim_n_lsc_4v_g_t += 36
                    u_0 = primitive_n_lsc_4v_g_t[0:1]
                    v_0 = primitive_n_lsc_4v_g_t[1:2]
                    cba_value = primitive_n_lsc_4v_g_t[2:4]
                    u_1 = primitive_n_lsc_4v_g_t[4:5]
                    v_1 = primitive_n_lsc_4v_g_t[5:6]
                    tsb_value = primitive_n_lsc_4v_g_t[6:8]
                    u_2 = primitive_n_lsc_4v_g_t[8:9]
                    v_2 = primitive_n_lsc_4v_g_t[9:10]
                    value_not_used_0 = primitive_n_lsc_4v_g_t[10:12]
                    u_3 = primitive_n_lsc_4v_g_t[12:13]
                    v_3 = primitive_n_lsc_4v_g_t[13:14]
                    value_not_used_1 = primitive_n_lsc_4v_g_t[14:16]
                    normal_0 = primitive_n_lsc_4v_g_t[16:18]
                    vertex_0 = primitive_n_lsc_4v_g_t[18:20]
                    normal_1 = primitive_n_lsc_4v_g_t[20:22]
                    vertex_1 = primitive_n_lsc_4v_g_t[22:24]
                    normal_2 = primitive_n_lsc_4v_g_t[24:26]
                    vertex_2 = primitive_n_lsc_4v_g_t[26:28]
                    normal_3 = primitive_n_lsc_4v_g_t[28:30]
                    vertex_3 = primitive_n_lsc_4v_g_t[30:32]

                    # OBJ Writer
                    write_primitive_n_lsc_4v_g_t = "f" + " " + str(sum(unpack('<H', vertex_0), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t) + " " + str(sum(unpack('<H', vertex_2), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t + 1) + " " + str(sum(unpack('<H', vertex_3), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t + 2) + " " + str(sum(unpack('<H', vertex_1), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t + 3) + "\n"
                    file_write.write(write_primitive_n_lsc_4v_g_t)
                    t += 4 

                ####################################################################################################################

                # Extracting LSC 2ND NEW TYPE OF PACKET a 4 VERTEX GOURAUD TEXTURED
                count_n_lsc_4v_g_t_2 = prim_block.count(new_lsc_four_vertex_gouraud_textured_2)
                position_prim_n_lsc_4v_g_t_2 = prim_block.find(new_lsc_four_vertex_gouraud_textured_2)

                while count_n_lsc_4v_g_t_2 > 0:
                    count_n_lsc_4v_g_t_2 -= 1
                    start_position_prim = position_prim_n_lsc_4v_g_t_2 + 4
                    end_position_prim = start_position_prim + 32
                    primitive_n_lsc_4v_g_t_2 = prim_block[start_position_prim : end_position_prim]
                    position_prim_n_lsc_4v_g_t_2 += 36
                    u_0 = primitive_n_lsc_4v_g_t_2[0:1]
                    v_0 = primitive_n_lsc_4v_g_t_2[1:2]
                    cba_value = primitive_n_lsc_4v_g_t_2[2:4]
                    u_1 = primitive_n_lsc_4v_g_t_2[4:5]
                    v_1 = primitive_n_lsc_4v_g_t_2[5:6]
                    tsb_value = primitive_n_lsc_4v_g_t_2[6:8]
                    u_2 = primitive_n_lsc_4v_g_t_2[8:9]
                    v_2 = primitive_n_lsc_4v_g_t_2[9:10]
                    value_not_used_0 = primitive_n_lsc_4v_g_t_2[10:12]
                    u_3 = primitive_n_lsc_4v_g_t_2[12:13]
                    v_3 = primitive_n_lsc_4v_g_t_2[13:14]
                    value_not_used_1 = primitive_n_lsc_4v_g_t_2[14:16]
                    normal_0 = primitive_n_lsc_4v_g_t_2[16:18]
                    vertex_0 = primitive_n_lsc_4v_g_t_2[18:20]
                    normal_1 = primitive_n_lsc_4v_g_t_2[20:22]
                    vertex_1 = primitive_n_lsc_4v_g_t_2[22:24]
                    normal_2 = primitive_n_lsc_4v_g_t_2[24:26]
                    vertex_2 = primitive_n_lsc_4v_g_t_2[26:28]
                    normal_3 = primitive_n_lsc_4v_g_t_2[28:30]
                    vertex_3 = primitive_n_lsc_4v_g_t_2[30:32]

                    # OBJ Writer
                    write_primitive_n_lsc_4v_g_t_2 = "f" + " " + str(sum(unpack('<H', vertex_0), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t) + " " + str(sum(unpack('<H', vertex_2), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t + 1) + " " + str(sum(unpack('<H', vertex_3), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t + 2) + " " + str(sum(unpack('<H', vertex_1), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t + 3) + "\n"
                    file_write.write(write_primitive_n_lsc_4v_g_t_2)
                    t += 4

                ####################################################################################################################

                # Extracting LSC NEW 4 VERTEX GOURAUD NO TEXTURED SOLID
                count_n_lsc_4v_g_n_t_s = prim_block.count(new_lsc_four_vertex_gouraud_no_textured_solid)
                position_prim_n_lsc_4v_g_n_t_s = prim_block.find(new_lsc_four_vertex_gouraud_no_textured_solid)

                while count_n_lsc_4v_g_n_t_s > 0:
                    count_n_lsc_4v_g_n_t_s -= 1
                    start_position_prim = position_prim_n_lsc_4v_g_n_t_s + 4
                    end_position_prim = start_position_prim + 20
                    primitive_n_lsc_4v_g_n_t_s = prim_block[start_position_prim : end_position_prim]
                    position_prim_n_lsc_4v_g_n_t_s += 24
                    red_value = primitive_n_lsc_4v_g_n_t_s[0:1]
                    green_value = primitive_n_lsc_4v_g_n_t_s[1:2]
                    blue_value = primitive_n_lsc_4v_g_n_t_s[2:3]
                    mode_value = primitive_n_lsc_4v_g_n_t_s[3:4]
                    normal_0 = primitive_n_lsc_4v_g_n_t_s[4:6]
                    vertex_0 = primitive_n_lsc_4v_g_n_t_s[6:8]
                    normal_1 = primitive_n_lsc_4v_g_n_t_s[8:10]
                    vertex_1 = primitive_n_lsc_4v_g_n_t_s[10:12]
                    normal_2 = primitive_n_lsc_4v_g_n_t_s[12:14]
                    vertex_2 = primitive_n_lsc_4v_g_n_t_s[14:16]
                    normal_3 = primitive_n_lsc_4v_g_n_t_s[16:18]
                    vertex_3 = primitive_n_lsc_4v_g_n_t_s[18:20]

                    # OBJ Writer
                    write_primitive_n_lsc_4v_g_n_t_s = "f" + " " + str(sum(unpack('<H', vertex_0), p)).replace("(", "").replace(")", "").replace(",", "") + " " + str(sum(unpack('<H', vertex_2), p)).replace("(", "").replace(")", "").replace(",", "") + " " + str(sum(unpack('<H', vertex_3), p)).replace("(", "").replace(")", "").replace(",", "") + " " + str(sum(unpack('<H', vertex_1), p)).replace("(", "").replace(")", "").replace(",", "") + "\n"
                    file_write.write(write_primitive_n_lsc_4v_g_n_t_s)


                ########################################### NO LIGHT SOURCE CALCULATION ############################################

                ####################################################################################################################

                # Extracting NLSC 3 VERTEX GRADATION NO TEXTURED
                count_nlsc_3v_g_n_t = prim_block.count(nlsc_three_vertex_gradation_no_textured)
                position_prim_nlsc_3v_g_n_t = prim_block.find(nlsc_three_vertex_gradation_no_textured)

                while count_nlsc_3v_g_n_t > 0:
                    count_nlsc_3v_g_n_t -= 1
                    start_position_prim = position_prim_nlsc_3v_g_n_t + 4
                    end_position_prim = start_position_prim + 20
                    primitive_nlsc_3v_g_n_t = prim_block[start_position_prim : end_position_prim]
                    position_prim_nlsc_3v_g_n_t += 24
                    red_value_0 = primitive_nlsc_3v_g_n_t[0:1]
                    green_value_0 = primitive_nlsc_3v_g_n_t[1:2]
                    blue_value_0 = primitive_nlsc_3v_g_n_t[2:3]
                    mode_value = primitive_nlsc_3v_g_n_t[3:4]
                    red_value_1 = primitive_nlsc_3v_g_n_t[4:5]
                    green_value_1 = primitive_nlsc_3v_g_n_t[5:6]
                    blue_value_1 = primitive_nlsc_3v_g_n_t[6:7]
                    value_not_used_0 = primitive_nlsc_3v_g_n_t[7:8]
                    red_value_2 = primitive_nlsc_3v_g_n_t[8:9]
                    green_value_2 = primitive_nlsc_3v_g_n_t[9:10]
                    blue_value_2 = primitive_nlsc_3v_g_n_t[10:11]
                    value_not_used_1 = primitive_nlsc_3v_g_n_t[11:12]
                    vertex_0 = primitive_nlsc_3v_g_n_t[12:14]
                    vertex_1 = primitive_nlsc_3v_g_n_t[14:16]
                    vertex_2 = primitive_nlsc_3v_g_n_t[16:18]
                    value_not_used_2 = primitive_nlsc_3v_g_n_t[18:20]

                    # OBJ Writer
                    write_primitive_nlsc_3v_g_n_t = "f" + " " + str(sum(unpack('<H', vertex_2), p)).replace("(", "").replace(")", "").replace(",", "") + " " + str(sum(unpack('<H', vertex_1), p)).replace("(", "").replace(")", "").replace(",", "") + " " + str(sum(unpack('<H', vertex_0), p)).replace("(", "").replace(")", "").replace(",", "") + "\n"
                    file_write.write(write_primitive_nlsc_3v_g_n_t)

                ####################################################################################################################

                # Extracting NLSC 3 VERTEX FLAT NO TEXTURED
                count_nlsc_3v_f_n_t = prim_block.count(nlsc_three_vertex_flat_no_textured)
                position_prim_nlsc_3v_f_n_t = prim_block.find(nlsc_three_vertex_flat_no_textured)

                while count_nlsc_3v_f_n_t > 0:
                    count_nlsc_3v_f_n_t -= 1
                    start_position_prim = position_prim_nlsc_3v_f_n_t + 4
                    end_position_prim = start_position_prim + 12
                    primitive_nlsc_3v_f_n_t = prim_block[start_position_prim : end_position_prim]
                    position_prim_nlsc_3v_f_n_t += 16
                    red_value = primitive_nlsc_3v_f_n_t[0:1]
                    green_value = primitive_nlsc_3v_f_n_t[1:2]
                    blue_value = primitive_nlsc_3v_f_n_t[2:3]
                    mode_value = primitive_nlsc_3v_f_n_t[3:4]
                    vertex_0 = primitive_nlsc_3v_f_n_t[4:6]
                    vertex_1 = primitive_nlsc_3v_f_n_t[6:8]
                    vertex_2 = primitive_nlsc_3v_f_n_t[8:10]
                    value_not_used = primitive_nlsc_3v_f_n_t[10:12]

                    # OBJ Writer
                    write_primitive_nlsc_3v_f_n_t = "f" + " " + str(sum(unpack('<H', vertex_2), p)).replace("(", "").replace(")", "").replace(",", "") + " " + str(sum(unpack('<H', vertex_1), p)).replace("(", "").replace(")", "").replace(",", "") + " " + str(sum(unpack('<H', vertex_0), p)).replace("(", "").replace(")", "").replace(",", "") + "\n"
                    file_write.write(write_primitive_nlsc_3v_f_n_t)

                ####################################################################################################################

                # Extracting NLSC 3 VERTEX GRADATION TEXTURED
                count_nlsc_3v_g_t = prim_block.count(nlsc_three_vertex_gradation_textured)
                position_prim_nlsc_3v_g_t = prim_block.find(nlsc_three_vertex_gradation_textured)

                while count_nlsc_3v_g_t > 0:
                    count_nlsc_3v_g_t -= 1
                    start_position_prim = position_prim_nlsc_3v_g_t + 4
                    end_position_prim = start_position_prim + 32
                    primitive_nlsc_3v_g_t = prim_block[start_position_prim : end_position_prim]
                    position_prim_nlsc_3v_g_t += 36
                    u_0 = primitive_nlsc_3v_g_t[0:1]
                    v_0 = primitive_nlsc_3v_g_t[1:2]
                    cba_value = primitive_nlsc_3v_g_t[2:4]
                    u_1 = primitive_nlsc_3v_g_t[4:5]
                    v_1 = primitive_nlsc_3v_g_t[5:6]
                    tsb_value = primitive_nlsc_3v_g_t[6:8]
                    u_2 = primitive_nlsc_3v_g_t[8:9]
                    v_2 = primitive_nlsc_3v_g_t[9:10]
                    value_not_used_0 = primitive_nlsc_3v_g_t[10:12]
                    red_value_0 = primitive_nlsc_3v_g_t[12:13]
                    green_value_0 = primitive_nlsc_3v_g_t[13:14]
                    blue_value_0 = primitive_nlsc_3v_g_t[14:15]
                    value_not_used_1 = primitive_nlsc_3v_g_t[15:16]
                    red_value_1 = primitive_nlsc_3v_g_t[16:17]
                    green_value_1 = primitive_nlsc_3v_g_t[17:18]
                    blue_value_1 = primitive_nlsc_3v_g_t[18:19]
                    value_not_used_2 = primitive_nlsc_3v_g_t[19:20]
                    red_value_2 = primitive_nlsc_3v_g_t[20:21]
                    green_value_2 = primitive_nlsc_3v_g_t[21:22]
                    blue_value_2 = primitive_nlsc_3v_g_t[22:23]
                    value_not_used_3 = primitive_nlsc_3v_g_t[23:24]
                    vertex_0 = primitive_nlsc_3v_g_t[24:26]
                    vertex_1 = primitive_nlsc_3v_g_t[26:28]
                    vertex_2 = primitive_nlsc_3v_g_t[28:30]
                    value_not_used_4 = primitive_nlsc_3v_g_t[30:32]

                    # OBJ Writer
                    write_primitive_nlsc_3v_g_t = "f" + " " + str(sum(unpack('<H', vertex_2), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t) + " " + str(sum(unpack('<H', vertex_1), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t + 1) + " " + str(sum(unpack('<H', vertex_0), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t + 2) + "\n"
                    file_write.write(write_primitive_nlsc_3v_g_t)
                    t += 3

                ####################################################################################################################

                # Extracting NLSC 3 VERTEX FLAT TEXTURED
                count_nlsc_3v_f_t = prim_block.count(nlsc_three_vertex_flat_textured)
                position_prim_nlsc_3v_f_t = prim_block.find(nlsc_three_vertex_flat_textured)

                while count_nlsc_3v_f_t > 0:
                    count_nlsc_3v_f_t -= 1
                    start_position_prim = position_prim_nlsc_3v_f_t + 4
                    end_position_prim = start_position_prim + 24
                    primitive_nlsc_3v_f_t = prim_block[start_position_prim : end_position_prim]
                    position_prim_nlsc_3v_f_t += 28
                    u_0 = primitive_nlsc_3v_f_t[0:1]
                    v_0 = primitive_nlsc_3v_f_t[1:2]
                    cba_value = primitive_nlsc_3v_f_t[2:4]
                    u_1 = primitive_nlsc_3v_f_t[4:5]
                    v_1 = primitive_nlsc_3v_f_t[5:6]
                    tsb_value = primitive_nlsc_3v_f_t[6:8]
                    u_2 = primitive_nlsc_3v_f_t[8:9]
                    v_2 = primitive_nlsc_3v_f_t[9:10]
                    value_not_used_0 = primitive_nlsc_3v_f_t[10:12]
                    red_value = primitive_nlsc_3v_f_t[12:13]
                    green_value = primitive_nlsc_3v_f_t[13:14]
                    blue_value = primitive_nlsc_3v_f_t[14:15]
                    value_not_used_1 = primitive_nlsc_3v_f_t[15:16]
                    vertex_0 = primitive_nlsc_3v_f_t[16:18]
                    vertex_1 = primitive_nlsc_3v_f_t[18:20]
                    vertex_2 = primitive_nlsc_3v_f_t[20:22]
                    value_not_used_2 = primitive_nlsc_3v_f_t[22:24]

                    # OBJ Writer
                    write_primitive_nlsc_3v_f_t = "f" + " " + str(sum(unpack('<H', vertex_2), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t) + " " + str(sum(unpack('<H', vertex_1), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t + 1) + " " + str(sum(unpack('<H', vertex_0), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t + 2) + "\n"
                    file_write.write(write_primitive_nlsc_3v_f_t)
                    t += 3

                ####################################################################################################################

                # Extracting NLSC NEW TYPE OF PACKET a 3 VERTEX GRADATION TEXTURED
                count_n_nlsc_3v_g_t = prim_block.count(new_nlsc_three_vertex_gradation_textured)
                position_prim_n_nlsc_3v_g_t = prim_block.find(new_nlsc_three_vertex_gradation_textured)

                while count_n_nlsc_3v_g_t > 0:
                    count_n_nlsc_3v_g_t -= 1
                    start_position_prim = position_prim_n_nlsc_3v_g_t + 4
                    end_position_prim = start_position_prim + 32
                    primitive_n_nlsc_3v_g_t = prim_block[start_position_prim : end_position_prim]
                    position_prim_n_nlsc_3v_g_t += 36
                    u_0 = primitive_n_nlsc_3v_g_t[0:1]
                    v_0 = primitive_n_nlsc_3v_g_t[1:2]
                    cba_value = primitive_n_nlsc_3v_g_t[2:4]
                    u_1 = primitive_n_nlsc_3v_g_t[4:5]
                    v_1 = primitive_n_nlsc_3v_g_t[5:6]
                    tsb_value = primitive_n_nlsc_3v_g_t[6:8]
                    u_2 = primitive_n_nlsc_3v_g_t[8:9]
                    v_2 = primitive_n_nlsc_3v_g_t[9:10]
                    value_not_used_0 = primitive_n_nlsc_3v_g_t[10:12]
                    red_value_0 = primitive_n_nlsc_3v_g_t[12:13]
                    green_value_0 = primitive_n_nlsc_3v_g_t[13:14]
                    blue_value_0 = primitive_n_nlsc_3v_g_t[14:15]
                    value_not_used_1 = primitive_n_nlsc_3v_g_t[15:16]
                    red_value_1 = primitive_n_nlsc_3v_g_t[16:17]
                    green_value_1 = primitive_n_nlsc_3v_g_t[17:18]
                    blue_value_1 = primitive_n_nlsc_3v_g_t[18:19]
                    value_not_used_2 = primitive_n_nlsc_3v_g_t[19:20]
                    red_value_2 = primitive_n_nlsc_3v_g_t[20:21]
                    green_value_2 = primitive_n_nlsc_3v_g_t[21:22]
                    blue_value_2 = primitive_n_nlsc_3v_g_t[22:23]
                    value_not_used_3 = primitive_n_nlsc_3v_g_t[23:24]
                    vertex_0 = primitive_n_nlsc_3v_g_t[24:26]
                    vertex_1 = primitive_n_nlsc_3v_g_t[26:28]
                    vertex_2 = primitive_n_nlsc_3v_g_t[28:30]
                    value_not_used_4 = primitive_n_nlsc_3v_g_t[30:32]

                    # OBJ Writer
                    write_primitive_n_nlsc_3v_g_t = "f" + " " + str(sum(unpack('<H', vertex_2), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t) + " " + str(sum(unpack('<H', vertex_1), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t + 1) + " " + str(sum(unpack('<H', vertex_0), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t + 2) + "\n"
                    file_write.write(write_primitive_n_nlsc_3v_g_t)
                    t += 3

                ####################################################################################################################

                # Extracting NLSC 4 VERTEX GRADATION NO TEXTURED
                count_nlsc_4v_g_n_t = prim_block.count(nlsc_four_vertex_gradation_no_textured)
                position_prim_nlsc_4v_g_n_t = prim_block.find(nlsc_four_vertex_gradation_no_textured)

                while count_nlsc_4v_g_n_t > 0:
                    count_nlsc_4v_g_n_t -= 1
                    start_position_prim = position_prim_nlsc_4v_g_n_t + 4
                    end_position_prim = start_position_prim + 24
                    primitive_nlsc_4v_g_n_t = prim_block[start_position_prim : end_position_prim]
                    position_prim_nlsc_4v_g_n_t += 28
                    red_value_0 = primitive_nlsc_4v_g_n_t[0:1]
                    green_value_0 = primitive_nlsc_4v_g_n_t[1:2]
                    blue_value_0 = primitive_nlsc_4v_g_n_t[2:3]
                    mode_value = primitive_nlsc_4v_g_n_t[3:4]
                    red_value_1 = primitive_nlsc_4v_g_n_t[4:5]
                    green_value_1 = primitive_nlsc_4v_g_n_t[5:6]
                    blue_value_1 = primitive_nlsc_4v_g_n_t[6:7]
                    value_not_used_0 = primitive_nlsc_4v_g_n_t[7:8]
                    red_value_2 = primitive_nlsc_4v_g_n_t[8:9]
                    green_value_2 = primitive_nlsc_4v_g_n_t[9:10]
                    blue_value_2 = primitive_nlsc_4v_g_n_t[10:11]
                    value_not_used_1 = primitive_nlsc_4v_g_n_t[11:12]
                    red_value_3 = primitive_nlsc_4v_g_n_t[12:13]
                    green_value_3 = primitive_nlsc_4v_g_n_t[13:14]
                    blue_value_3 = primitive_nlsc_4v_g_n_t[14:15]
                    value_not_used_2 = primitive_nlsc_4v_g_n_t[15:16]
                    vertex_0 = primitive_nlsc_4v_g_n_t[16:18]
                    vertex_1 = primitive_nlsc_4v_g_n_t[18:20]
                    vertex_2 = primitive_nlsc_4v_g_n_t[20:22]
                    vertex_3 = primitive_nlsc_4v_g_n_t[22:24]

                    # OBJ Writer
                    write_primitive_nlsc_4v_g_n_t = "f" + " " + str(sum(unpack('<H', vertex_0), p)).replace("(", "").replace(")", "").replace(",", "") + " " + str(sum(unpack('<H', vertex_2), p)).replace("(", "").replace(")", "").replace(",", "") + " " + str(sum(unpack('<H', vertex_3), p)).replace("(", "").replace(")", "").replace(",", "") + " " + str(sum(unpack('<H', vertex_1), p)).replace("(", "").replace(")", "").replace(",", "") + "\n"
                    file_write.write(write_primitive_nlsc_4v_g_n_t)

                ####################################################################################################################

                # Extracting NLSC 4 VERTEX FLAT NO TEXTURED
                count_nlsc_4v_f_n_t = prim_block.count(nlsc_four_vertex_flat_no_textured)
                position_prim_nlsc_4v_f_n_t = prim_block.find(nlsc_four_vertex_flat_no_textured)

                while count_nlsc_4v_f_n_t > 0:
                    count_nlsc_4v_f_n_t -= 1
                    start_position_prim = position_prim_nlsc_4v_f_n_t + 4
                    end_position_prim = start_position_prim + 12
                    primitive_nlsc_4v_f_n_t = prim_block[start_position_prim : end_position_prim]
                    position_prim_nlsc_4v_f_n_t += 16
                    red_value = primitive_nlsc_4v_f_n_t[0:1]
                    green_value = primitive_nlsc_4v_f_n_t[1:2]
                    blue_value = primitive_nlsc_4v_f_n_t[2:3]
                    mode_value = primitive_nlsc_4v_f_n_t[3:4]
                    vertex_0 = primitive_nlsc_4v_f_n_t[4:6]
                    vertex_1 = primitive_nlsc_4v_f_n_t[6:8]
                    vertex_2 = primitive_nlsc_4v_f_n_t[8:10]
                    vertex_3 = primitive_nlsc_4v_f_n_t[10:12]

                    # OBJ Writer
                    write_primitive_nlsc_4v_f_n_t = "f" + " " + str(sum(unpack('<H', vertex_0), p)).replace("(", "").replace(")", "").replace(",", "") + " " + str(sum(unpack('<H', vertex_2), p)).replace("(", "").replace(")", "").replace(",", "") + " " + str(sum(unpack('<H', vertex_3), p)).replace("(", "").replace(")", "").replace(",", "") + " " + str(sum(unpack('<H', vertex_1), p)).replace("(", "").replace(")", "").replace(",", "") + "\n"
                    file_write.write(write_primitive_nlsc_4v_f_n_t)

                ####################################################################################################################

                # Extracting NLSC 4 VERTEX GRADATION TEXTURED
                count_nlsc_4v_g_t = prim_block.count(nlsc_four_vertex_gradation_textured)
                position_prim_nlsc_4v_g_t = prim_block.find(nlsc_four_vertex_gradation_textured)

                while count_nlsc_4v_g_t > 0:
                    count_nlsc_4v_g_t -= 1
                    start_position_prim = position_prim_nlsc_4v_g_t + 4
                    end_position_prim = position_prim_nlsc_4v_g_t + 40
                    primitive_nlsc_4v_g_t = prim_block[start_position_prim : end_position_prim]
                    position_prim_nlsc_4v_g_t += 44
                    u_0 = primitive_nlsc_4v_g_t[0:1]
                    v_0 = primitive_nlsc_4v_g_t[1:2]
                    cba_value = primitive_nlsc_4v_g_t[2:4]
                    u_1 = primitive_nlsc_4v_g_t[4:5]
                    v_1 = primitive_nlsc_4v_g_t[5:6]
                    tsb_value = primitive_nlsc_4v_g_t[6:8]
                    u_2 = primitive_nlsc_4v_g_t[8:9]
                    v_2 = primitive_nlsc_4v_g_t[9:10]
                    value_not_used_0 = primitive_nlsc_4v_g_t[10:12]
                    u_3 = primitive_nlsc_4v_g_t[12:13]
                    v_3 = primitive_nlsc_4v_g_t[13:14]
                    value_not_used_1 = primitive_nlsc_4v_g_t[14:16]
                    red_value_0 = primitive_nlsc_4v_g_t[16:17]
                    green_value_0 = primitive_nlsc_4v_g_t[17:18]
                    blue_value_0 = primitive_nlsc_4v_g_t[18:19]
                    value_not_used_2 = primitive_nlsc_4v_g_t[19:20]
                    red_value_1 = primitive_nlsc_4v_g_t[20:21]
                    green_value_1 = primitive_nlsc_4v_g_t[21:22]
                    blue_value_1 = primitive_nlsc_4v_g_t[22:23]
                    value_not_used_3 = primitive_nlsc_4v_g_t[23:24]
                    red_value_2 = primitive_nlsc_4v_g_t[24:25]
                    green_value_2 = primitive_nlsc_4v_g_t[25:26]
                    blue_value_2 = primitive_nlsc_4v_g_t[26:27]
                    value_not_used_4 = primitive_nlsc_4v_g_t[27:28]
                    red_value_3 = primitive_nlsc_4v_g_t[28:29]
                    green_value_3 = primitive_nlsc_4v_g_t[29:30]
                    blue_value_3 = primitive_nlsc_4v_g_t[30:31]
                    value_not_used_5 = primitive_nlsc_4v_g_t[31:32]
                    vertex_0 = primitive_nlsc_4v_g_t[32:34]
                    vertex_1 = primitive_nlsc_4v_g_t[34:36]
                    vertex_2 = primitive_nlsc_4v_g_t[36:38]
                    vertex_3 = primitive_nlsc_4v_g_t[38:40]

                    # OBJ Writer
                    write_primitive_nlsc_4v_g_t = "f" + " " + str(sum(unpack('<H', vertex_0), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t) + " " + str(sum(unpack('<H', vertex_2), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t + 1) + " " + str(sum(unpack('<H', vertex_3), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t + 2) + " " + str(sum(unpack('<H', vertex_1), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t + 3) + "\n"
                    file_write.write(write_primitive_nlsc_4v_g_t)
                    t += 4

                ####################################################################################################################

                # Extracting NLSC 4 VERTEX FLAT TEXTURED
                count_nlsc_4v_f_t = prim_block.count(nlsc_four_vertex_flat_textured)
                position_prim_nlsc_4v_f_t = prim_block.find(nlsc_four_vertex_flat_textured)

                while count_nlsc_4v_f_t > 0:
                    count_nlsc_4v_f_t -= 1
                    start_position_prim = position_prim_nlsc_4v_f_t + 4
                    end_position_prim = start_position_prim + 28
                    primitive_nlsc_4v_f_t = prim_block[start_position_prim : end_position_prim]
                    position_prim_nlsc_4v_f_t += 32
                    u_0 = primitive_nlsc_4v_f_t[0:1]
                    v_0 = primitive_nlsc_4v_f_t[1:2]
                    cba_value = primitive_nlsc_4v_f_t[2:4]
                    u_1 = primitive_nlsc_4v_f_t[4:5]
                    v_1 = primitive_nlsc_4v_f_t[5:6]
                    tsb_value = primitive_nlsc_4v_f_t[6:8]
                    u_2 = primitive_nlsc_4v_f_t[8:9]
                    v_2 = primitive_nlsc_4v_f_t[9:10]
                    value_not_used_0 = primitive_nlsc_4v_f_t[10:12]
                    u_3 = primitive_nlsc_4v_f_t[12:13]
                    v_3 = primitive_nlsc_4v_f_t[13:14]
                    value_not_used_1 = primitive_nlsc_4v_f_t[14:16]
                    red_value = primitive_nlsc_4v_f_t[16:17]
                    green_value = primitive_nlsc_4v_f_t[17:18]
                    blue_value = primitive_nlsc_4v_f_t[18:19]
                    value_not_used_2 = primitive_nlsc_4v_f_t[19:20]
                    vertex_0 = primitive_nlsc_4v_f_t[20:22]
                    vertex_1 = primitive_nlsc_4v_f_t[22:24]
                    vertex_2 = primitive_nlsc_4v_f_t[24:26]
                    vertex_3 = primitive_nlsc_4v_f_t[26:28]

                    # OBJ Writer
                    write_primitive_nlsc_4v_f_t = "f" + " " + str(sum(unpack('<H', vertex_0), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t) + " " + str(sum(unpack('<H', vertex_2), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t + 1) + " " + str(sum(unpack('<H', vertex_3), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t + 2) + " " + str(sum(unpack('<H', vertex_1), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t + 3) + "\n"
                    file_write.write(write_primitive_nlsc_4v_f_t)
                    t += 4

                ####################################################################################################################

                # Extracting NLSC NEW TYPE OF PACKET a 4 VERTEX GRADATION TEXTURED
                count_n_nlsc_4v_g_t = prim_block.count(new_nlsc_four_vertex_gradation_textured)
                position_prim_n_nlsc_4v_g_t = prim_block.find(new_nlsc_four_vertex_gradation_textured)

                while count_n_nlsc_4v_g_t > 0:
                    count_n_nlsc_4v_g_t -= 1
                    start_position_prim = position_prim_n_nlsc_4v_g_t + 4
                    end_position_prim = start_position_prim + 40
                    primitive_n_nlsc_4v_g_t = prim_block[start_position_prim : end_position_prim]
                    position_prim_n_nlsc_4v_g_t += 44
                    u_0 = primitive_n_nlsc_4v_g_t[0:1]
                    v_0 = primitive_n_nlsc_4v_g_t[1:2]
                    cba_value = primitive_n_nlsc_4v_g_t[2:4]
                    u_1 = primitive_n_nlsc_4v_g_t[4:5]
                    v_1 = primitive_n_nlsc_4v_g_t[5:6]
                    tsb_value = primitive_n_nlsc_4v_g_t[6:8]
                    u_2 = primitive_n_nlsc_4v_g_t[8:9]
                    v_2 = primitive_n_nlsc_4v_g_t[9:10]
                    value_not_used_0 = primitive_n_nlsc_4v_g_t[10:12]
                    u_3 = primitive_n_nlsc_4v_g_t[12:13]
                    v_3 = primitive_n_nlsc_4v_g_t[13:14]
                    value_not_used_1 = primitive_n_nlsc_4v_g_t[14:16]
                    red_value_0 = primitive_n_nlsc_4v_g_t[16:17]
                    green_value_0 = primitive_n_nlsc_4v_g_t[17:18]
                    blue_value_0 = primitive_n_nlsc_4v_g_t[18:19]
                    value_not_used_2 = primitive_n_nlsc_4v_g_t[19:20]
                    red_value_1 = primitive_n_nlsc_4v_g_t[20:21]
                    green_value_1 = primitive_n_nlsc_4v_g_t[21:22]
                    blue_value_1 = primitive_n_nlsc_4v_g_t[22:23]
                    value_not_used_3 = primitive_n_nlsc_4v_g_t[23:24]
                    red_value_2 = primitive_n_nlsc_4v_g_t[24:25]
                    green_value_2 = primitive_n_nlsc_4v_g_t[25:26]
                    blue_value_2 = primitive_n_nlsc_4v_g_t[26:27]
                    value_not_used_4 = primitive_n_nlsc_4v_g_t[27:28]
                    red_value_3 = primitive_n_nlsc_4v_g_t[28:29]
                    green_value_3 = primitive_n_nlsc_4v_g_t[29:30]
                    blue_value_3 = primitive_n_nlsc_4v_g_t[30:31]
                    value_not_used_5 = primitive_n_nlsc_4v_g_t[31:32]
                    vertex_0 = primitive_n_nlsc_4v_g_t[32:34]
                    vertex_1 = primitive_n_nlsc_4v_g_t[34:36]
                    vertex_2 = primitive_n_nlsc_4v_g_t[36:38]
                    vertex_3 = primitive_n_nlsc_4v_g_t[38:40]

                    # OBJ Writer
                    write_primitive_n_nlsc_4v_g_t = "f" + " " + str(sum(unpack('<H', vertex_0), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t) + " " + str(sum(unpack('<H', vertex_2), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t + 1) + " " + str(sum(unpack('<H', vertex_3), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t + 2) + " " + str(sum(unpack('<H', vertex_1), p)).replace("(", "").replace(")", "").replace(",", "") + "/" + str(t + 3) + "\n"
                    file_write.write(write_primitive_n_nlsc_4v_g_t)
                    t += 4

                ############################################## STRAIGHT LINE #######################################################

                ####################################################################################################################

                # Extracting STRAIGHT LINE GRADATION ON
                count_s_l_g_on = prim_block.count(sl_gradation_on)
                position_prim_s_l_g_on = prim_block.find(sl_gradation_on)

                while count_s_l_g_on > 0:
                    count_s_l_g_on -= 1
                    start_position_prim = position_prim_s_l_g_on + 4
                    end_position_prim = start_position_prim + 12
                    primitive_s_l_g_on = prim_block[start_position_prim : end_position_prim]
                    position_prim_s_l_g_on += 16
                    red_value_0 = primitive_s_l_g_on[0:1]
                    green_value_0 = primitive_s_l_g_on[1:2]
                    blue_value_0 = primitive_s_l_g_on[2:3]
                    mode_value = primitive_s_l_g_on[3:4]
                    red_value_1 = primitive_s_l_g_on[4:5]
                    green_value_1 = primitive_s_l_g_on[5:6]
                    blue_value_1 = primitive_s_l_g_on[6:7]
                    value_not_used = primitive_s_l_g_on[7:8]
                    vertex_0 = primitive_s_l_g_on[8:10]
                    vertex_1 = primitive_s_l_g_on[10:12]

                    # OBJ Writer
                    write_primitive_s_l_g_on = "f" + " " + str(sum(unpack('<H', vertex_0), (1))).replace("(", "").replace(")", "").replace(",", "") + " " + str(sum(unpack('<H', vertex_1), (1))).replace("(", "").replace(")", "").replace(",", "") + "\n"
                    file_write.write(write_primitive_s_l_g_on)

                ####################################################################################################################

                # Extracting STRAIGHT LINE GRADATION OFF
                count_s_l_g_off = prim_block.count(sl_gradation_off)
                position_prim_s_l_g_off = prim_block.find(sl_gradation_off)

                while count_s_l_g_off > 0:
                    count_s_l_g_off -= 1
                    start_position_prim = position_prim_s_l_g_off + 4
                    end_position_prim = start_position_prim + 8
                    primitive_s_l_g_off = prim_block[start_position_prim : end_position_prim]
                    count_s_l_g_off += 12
                    red_value = primitive_s_l_g_off[0:1]
                    green_value = primitive_s_l_g_off[1:2]
                    blue_value = primitive_s_l_g_off[2:3]
                    mode_value = primitive_s_l_g_off[3:4]
                    vertex_0 = primitive_s_l_g_off[4:6]
                    vertex_1 = primitive_s_l_g_off[6:8]

                    # OBJ Writer
                    write_primitive_s_l_g_off = "f" + " " + str(sum(unpack('<H', vertex_0), (1))).replace("(", "").replace(")", "").replace(",", "") + " " + str(sum(unpack('<H', vertex_1), (1))).replace("(", "").replace(")", "").replace(",", "") + "\n"
                    file_write.write(write_primitive_s_l_g_off)

                ################################################ 3D SPRITE #########################################################

                ####################################################################################################################

                # Extracting SPRITE 1X1
                count_s_p_1x1 = prim_block.count(sp_1x1)
                position_prim_s_p_1x1 = prim_block.find(sp_1x1)

                while count_s_p_1x1 > 0:
                    count_s_p_1x1 -= 1
                    start_position_prim = position_prim_s_p_1x1 + 4
                    end_position_prim = start_position_prim + 8
                    primitive_s_p_1x1 = prim_block[start_position_prim : end_position_prim]
                    position_prim_s_p_1x1 += 12
                    vertex_0 = primitive_s_p_1x1[0:2]
                    tsb_value = primitive_s_p_1x1[2:4]
                    u_0 = primitive_s_p_1x1[4:5]
                    v_0 = primitive_s_p_1x1[5:6]
                    cba_value = primitive_s_p_1x1[6:8]

                    # OBJ Writer
                    write_primitive_s_p_1x1 = "f" + " " + str(sum(unpack('<H', vertex_0), (1))).replace("(", "").replace(")", "").replace(",", "") + "\n"
                    file_write.write(write_primitive_s_p_1x1)

                ####################################################################################################################

                # Extracting SPRITE FREE SIZE
                count_s_p_free_size = prim_block.count(sp_free_size)
                position_prim_s_p_free_size = prim_block.find(sp_free_size)

                while count_s_p_free_size > 0:
                    count_s_p_free_size -= 1
                    start_position_prim = position_prim_s_p_free_size + 4
                    end_position_prim = position_prim_s_p_free_size + 12
                    primitive_s_p_free_size = prim_block[start_position_prim : end_position_prim]
                    position_prim_s_p_free_size += 16
                    vertex_0 = primitive_s_p_free_size[0:2]
                    tsb_value = primitive_s_p_free_size[2:4]
                    u_0 = primitive_s_p_free_size[4:5]
                    v_0 = primitive_s_p_free_size[5:6]
                    cba_value = primitive_s_p_free_size[6:8]
                    width = primitive_s_p_free_size[8:10] # Width of the sprite
                    height = primitive_s_p_free_size[10:12] # Height of the sprite

                    # OBJ Writer
                    write_primitive_s_p_free_size = "f" + " " + str(sum(unpack('<H', vertex_0), (1))).replace("(", "").replace(")", "").replace(",", "") + "\n"
                    file_write.write(write_primitive_s_p_free_size)

                ####################################################################################################################

                # Extracting SPRITE 16X16
                count_s_p_16x16 = prim_block.count(sp_16x16)
                position_prim_s_p_16x16 = prim_block.find(sp_16x16)

                while count_s_p_16x16 > 0:
                    count_s_p_16x16 -= 1
                    start_position_prim = position_prim_s_p_16x16 + 4
                    end_position_prim = start_position_prim + 8
                    primitive_s_p_16x16 = prim_block[start_position_prim : end_position_prim]
                    position_prim_s_p_16x16 += 12
                    vertex_0 = primitive_s_p_16x16[0:2]
                    tsb_value = primitive_s_p_16x16[2:4]
                    u_0 = primitive_s_p_16x16[4:5]
                    v_0 = primitive_s_p_16x16[5:6]
                    cba_value = primitive_s_p_16x16[6:8]

                    # OBJ Writer
                    write_primitive_s_p_16x16 = "f" + " " + str(sum(unpack('<H', vertex_0), (1))).replace("(", "").replace(")", "").replace(",", "") + "\n"
                    file_write.write(write_primitive_s_p_16x16)

                ####################################################################################################################

                # Extracting SPRITE 8X8
                count_s_p_8x8 = prim_block.count(sp_8x8)
                position_prim_s_p_8x8 = prim_block.find(sp_8x8)

                while count_s_p_8x8 > 0:
                    count_s_p_8x8 -= 1
                    start_position_prim = position_prim_s_p_8x8 + 4
                    end_position_prim = start_position_prim + 8
                    primitive_s_p_8x8 = prim_block[start_position_prim : end_position_prim]
                    position_prim_s_p_8x8 += 12
                    vertex_0 = primitive_s_p_8x8[0:2]
                    tsb_value = primitive_s_p_8x8[2:4]
                    u_0 = primitive_s_p_8x8[4:5]
                    v_0 = primitive_s_p_8x8[5:6]
                    cba_value = primitive_s_p_8x8[6:8]

                    # OBJ Writer
                    write_primitive_s_p_8x8 = "f" + " " + str(sum(unpack('<H', vertex_0), (1))).replace("(", "").replace(")", "").replace(",", "") + "\n"
                    file_write.write(write_primitive_s_p_8x8)



    def material_converter(self):           # Material for Object writer - Working as intended by now
        with open((tmd_file).strip('.bin') + ".mtl", 'w') as mat_write:
            first_name_file = "# " + "This OBJ is extracted from " + tmd_file.center(4) + " Using TMD_2_Obj, by DooMMetaL" + "\n" + "\n" + "\n"
            mat_write.write(first_name_file)
            header_of_mat = "# " + "\n" + "# " + (tmd_file.strip('.bin') + ".mtl") + "\n" + "# " + "\n" + "\n" + "\n" # Here i put the name of material
            mat_write.write(header_of_mat)
            for object_number, values in tmd_objects_properties:
                obj_num = "newmtl" + " " + "Object_Num" + " " + str(object_number) + "\n" + "illum 2" + "\n"
                kd = "Kd" + " " + "1.000000" + " " + "1.000000" + " " + "1.000000" + "\n"
                ka = "Ka" + " " + "0.000000" + " " + "0.000000" + " " + "0.000000" + "\n"
                ks = "Ks" + " " + "0.000000" + " " + "0.000000" + " " + "0.000000" + "\n"
                ke = "Ke" + " " + "0.000000" + " " + "0.000000" + " " + "0.000000" + "\n"
                ns = "Ns" + " " + "0.000000" + "\n" + "\n"
                mat_write.write(obj_num)
                mat_write.write(kd)
                mat_write.write(ka)
                mat_write.write(ks)
                mat_write.write(ke)
                mat_write.write(ns)

    def primitives_informer(self):               # PRIMITIVE INFORMER IN DUMP OF TEXT
        with open((tmd_file).strip('.bin') + ".dat", 'w') as prim_informer:
            first_name_file = "# " + "This OBJ is extracted from " + tmd_file.center(4) + " Using TMD_2_Obj, by DooMMetaL" + "\n" + "\n" + "\n"
            primitive_info = "# Primitives in each Object and final count" + "\n" + "\n"
            prim_informer.write(primitive_info)
            for num, prim_b in primitives_block_enum_2:

                # Packet Configuration of 3 Vertex Polygon with Light Source Calculation
                lsc_three_vertex_gouraud_no_textured_solid = b'\x06\x04\x00\x30'      # 3 VERTEX GOURAUD NO TEXTURED SOLID
                lsc_three_vertex_flat_no_textured_solid =  b'\x04\x03\x00\x20'        # 3 VERTEX FLAT NO TEXTURED SOLID
                lsc_three_vertex_gouraud_no_textured_gradation = b'\x06\x06\x04\x30'  # 3 VERTEX GOURAUD NO TEXTURED GRADATION
                lsc_three_vertex_flat_no_textured_gradation = b'\x06\x05\x04\x20'     # 3 VERTEX FLAT NO TEXTURED GRADATION
                lsc_three_vertex_gouraud_textured = b'\x09\x06\x00\x34' # NO FIFTH VALUE to check, FIFTH value correspond to CBA // 3 VERTEX GOURAUD TEXTURED 
                lsc_three_vertex_flat_textured = b'\x07\x05\x00\x24' # NO FIFTH VALUE to check, FIFTH value correspond to CBA // 3 VERTEX FLAT TEXTURED
                new_lsc_three_vertex_gouraud = b'\x09\x06\x02\x34' # NEW 3 VERTEX GOURAUD TEXTURED 
                new_lsc_three_vertex_gouraud_2 = b'\x09\x06\x00\x36' # NEW 3 VERTEX GOURAUD TEXTURED

                # Packet Configuration for 4 Vertex Polygon with Light Source Calculation
                lsc_four_vertex_gouraud_no_textured_solid = b'\x08\x05\x00\x38'       # 4 VERTEX GOURAUD NO TEXTURED SOLID
                lsc_four_vertex_flat_no_textured_solid = b'\x05\x04\x00\x28'          # 4 VERTEX FLAT NO TEXTURED SOLID
                lsc_four_vertex_gouraud_no_textured_gradation = b'\x08\x08\x04\x38'   # 4 VERTEX GOURAUD NO TEXTURED GRADATION
                lsc_four_vertex_flat_no_textured_gradation = b'\x08\x07\x04\x28'      # 4 VERTEX FLAT NO TEXTURED GRADATION
                lsc_four_vertex_gouraud_textured = b'\x0c\x08\x00\x3c' # NO FIFTH VALUE to check, FIFTH value correspond to CBA // 4 VERTEX GOURAUD TEXTURED
                lsc_four_vertex_flat_textured = b'\x09\x07\x00\x2c' # NO FIFTH VALUE to check, FIFTH value to correspond to CBA // 4 VERTEX FLAT TEXTURED
                new_lsc_four_vertex_gouraud_textured = b'\x0c\x08\x00\x3e' # NEW TYPE OF PACKET a 4 VERTEX GOURAUD TEXTURED
                new_lsc_four_vertex_gouraud_textured_2 = b'\x0c\x08\x02\x3c' # NEW TYPE OF PACKET a 4 VERTEX GOURAUD TEXTURED
                new_lsc_four_vertex_gouraud_no_textured_solid = b'\x08\x05\x00\x3a' # NEW 4 VERTEX GOURAUD NO TEXTURED SOLID

                # Packet configuration for 3 Vertex Polygon with No Light Source Calculation
                nlsc_three_vertex_gradation_no_textured = b'\x06\x05\x01\x31'         # 3 VERTEX GRADATION NO TEXTURED
                nlsc_three_vertex_flat_no_textured = b'\x04\x03\x01\x21'              # 3 VERTEX FLAT NO TEXTURED
                nlsc_three_vertex_gradation_textured = b'\x09\x08\x01\x35' # NO FIFTH VALUE to check, FIFTH value correspond to CBA // 3 VERTEX GRADATION TEXTURED 
                nlsc_three_vertex_flat_textured = b'\x07\x06\x01\x25' # NO FIFTH VALUE to check, FIFTH value correspond to CBA // 3 VERTEX FLAT TEXTURED
                new_nlsc_three_vertex_gradation_textured = b'\x09\x08\x01\x37' # NEW TYPE OF PACKET a 3 VERTEX GRADATION TEXTURED

                # Packet Configuration for 4 Vertex Polygon with No Light Source Calculation
                nlsc_four_vertex_gradation_no_textured = b'\x08\x06\x01\x39'          # 4 VERTEX GRADATION NO TEXTURED
                nlsc_four_vertex_flat_no_textured = b'\x05\x03\x01\x29'                    # 4 VERTEX FLAT NO TEXTURED
                nlsc_four_vertex_gradation_textured = b'\x0c\x0a\x01\x3d' # NO FIFTH VALUE to check, FIFTH value correspond to CBA // 4 VERTEX GRADATION TEXTURED
                nlsc_four_vertex_flat_textured = b'\x09\x07\x01\x2d' # NO FIFTH VALUE to check, FIFTH value correspond to CBA // 4 VERTEX FLAT TEXTURED
                new_nlsc_four_vertex_gradation_textured = b'\x0c\x0a\x01\x3f' # NEW 4 VERTEX GRADATION TEXTURED

                # Packet Configuration for “Straight Line”
                sl_gradation_on = b'\x04\x03\x01\x50'                                 # STRAIGHT LINE GRADATION ON
                sl_gradation_off = b'\x03\x02\x01\x40'                                # STRAIGHT LINE GRADATION OFF

                # Packet Configuration for Sprites
                sp_1x1 = b'\x04\x02\x01\x6c' # NO FIFTH VALUE to check, FIFTH value correspond to TSB // SPRITE 1X1
                sp_free_size = b'\x05\x03\x01\x64' # NO FIFTH VALUE to check, FIFTH value correspond to TSB // SPRITE FREE SIZE
                sp_16x16 = b'\x04\x02\x01\x7c' # NO FIFTH VALUE to check, FIFTH value correspond to TSB // SPRITE 16X16
                sp_8x8 = b'\x04\x02\x01\x74' # NO FIFTH VALUE to check, FIFTH value correspond to TSB // SPRITE 8X8

                primitives_number = "\n " + "\n" + "# Primitives from Object number " + " " + str(num) + "\n" + "\n"
                prim_informer.write(primitives_number)
                
                # Light Calculation
                counting_primitives_lsc_3_v_g_n_t_s = "# LSC 3 VERTEX GOURAUD NO TEXTURED SOLID" + " " + str(prim_b.count(lsc_three_vertex_gouraud_no_textured_solid)) + "\n"
                counting_primitives_lsc_3_v_f_n_t_s = "# LSC 3 VERTEX FLAT NO TEXTURED SOLID" + " " + str(prim_b.count(lsc_three_vertex_flat_no_textured_solid)) + "\n"
                counting_primitives_lsc_3_v_g_n_t_g = "# LSC 3 VERTEX GOURAUD NO TEXTURED GRADATION" + " " + str(prim_b.count(lsc_three_vertex_gouraud_no_textured_gradation)) + "\n"
                counting_primitives_lsc_3_v_f_n_t_g = "# LSC 3 VERTEX FLAT NO TEXTURED GRADATION" + " " + str(prim_b.count(lsc_three_vertex_flat_no_textured_gradation)) + "\n"
                counting_primitives_lsc_3_v_g_t = "# LSC 3 VERTEX GOURAUD TEXTURED" + " " + str(prim_b.count(lsc_three_vertex_gouraud_textured)) + "\n"
                counting_primitives_lsc_3_v_f_t = "# LSC 3 VERTEX FLAT TEXTURED" + " " + str(prim_b.count(lsc_three_vertex_flat_textured)) + "\n"
                counting_primitives_lsc_3_v_new_packet = "# LSC NEW 3 VERTEX GOURAUD TEXTURED" + " " + str(prim_b.count(new_lsc_three_vertex_gouraud)) + "\n"
                counting_primitives_lsc_3_v_new_packet_2 = "# LSC NEW 3 VERTEX GOURAUD TEXTURED" + " " + str(prim_b.count(new_lsc_three_vertex_gouraud_2)) + "\n"

                counting_primitives_lsc_4_v_g_n_t_s = "# LSC 4 VERTEX GOURAUD NO TEXTURED SOLID" + " " + str(prim_b.count(lsc_four_vertex_gouraud_no_textured_solid)) + "\n"
                counting_primitives_lsc_4_v_f_n_t_s = "# LSC 4 VERTEX FLAT NO TEXTURED SOLID" + " " + str(prim_b.count(lsc_four_vertex_flat_no_textured_solid)) + "\n"
                counting_primitives_lsc_4_v_g_n_t_g = "# LSC 4 VERTEX GOURAUD NO TEXTURED GRADATION" + " " + str(prim_b.count(lsc_four_vertex_gouraud_no_textured_gradation)) + "\n"
                counting_primitives_lsc_4_v_f_n_t_g = "# LSC 4 VERTEX FLAT NO TEXTURED GRADATION" + " " + str(prim_b.count(lsc_four_vertex_flat_no_textured_gradation)) + "\n"
                counting_primitives_lsc_4_v_g_t = "# LSC 4 VERTEX GOURAUD TEXTURED" + " " + str(prim_b.count(lsc_four_vertex_gouraud_textured)) + "\n"
                counting_primitives_lsc_4_v_f_t = "# LSC 4 VERTEX FLAT TEXTURED" + " " + str(prim_b.count(lsc_four_vertex_flat_textured)) + "\n"
                counting_primitives_lsc_4_v_new_packet = "# LSC NEW 4 VERTEX GOURAUD TEXTURED TYPE OF PACKET" + " " + str(prim_b.count(new_lsc_four_vertex_gouraud_textured)) + "\n"
                counting_primitives_lsc_4_v_new_packet_2 = "# LSC NEW 4 VERTEX GOURAUD TEXTURED TYPE OF PACKET" + " " + str(prim_b.count(new_lsc_four_vertex_gouraud_textured_2)) + "\n"
                counting_primitives_lsc_4_v_new_packet_3 = "# LSC NEW 4 VERTEX GOURAUD NO TEXTURED SOLID" + " " + str(prim_b.count(new_lsc_four_vertex_gouraud_no_textured_solid)) + "\n"
                
                # No Light Calculation
                counting_primitives_nlsc_3_v_g_n_t = "# NLSC 3 VERTEX GRADATION NO TEXTURED" + " " + str(prim_b.count(nlsc_three_vertex_gradation_no_textured)) + "\n"
                counting_primitives_nlsc_3_v_f_n_t = "# NLSC 3 VERTEX FLAT NO TEXTURED" + " " + str(prim_b.count(nlsc_three_vertex_flat_no_textured)) + "\n"
                counting_primitives_nlsc_3_v_g_t = "# NLSC 3 VERTEX GRADATION TEXTURED" + " " + str(prim_b.count(nlsc_three_vertex_gradation_textured)) + "\n"
                counting_primitives_nlsc_3_v_f_t = "# NLSC 3 VERTEX FLAT TEXTURED" + " " + str(prim_b.count(nlsc_three_vertex_flat_textured)) + "\n"
                counting_primitives_nlsc_3_v_new_packet = "# NLSC NEW 3 VERTEX GRADATION TEXTURED TYPE OF PACKET" + " " + str(prim_b.count(new_nlsc_three_vertex_gradation_textured)) + "\n"

                counting_primitives_nlsc_4_v_g_n_t = "# NLSC 4 VERTEX GRADATION NO TEXTURED" + " " + str(prim_b.count(nlsc_four_vertex_gradation_no_textured)) + "\n"
                counting_primitives_nlsc_4_v_n_t = "# NLSC 4 VERTEX FLAT NO TEXTURED" + " " + str(prim_b.count(nlsc_four_vertex_flat_no_textured)) + "\n"
                counting_primitives_nlsc_4_v_g_t = "# NLSC 4 VERTEX GRADATION TEXTURED" + " " + str(prim_b.count(nlsc_four_vertex_gradation_textured)) + "\n"
                counting_primitives_nlsc_4_v_f_t = "# NLSC 4 VERTEX FLAT TEXTURED" + " " + str(prim_b.count(nlsc_four_vertex_flat_textured)) + "\n"
                counting_primitives_nlsc_4_v_new_packet = "# NLSC 4 NEW VERTEX GRADATION TEXTURED" + " " + str(prim_b.count(new_nlsc_four_vertex_gradation_textured)) + "\n"
                
                # Other Primitives
                counting_primitives_s_l_g_on = "# STRAIGHT LINE GRADATION ON" + " " + str(prim_b.count(sl_gradation_on)) + "\n"
                counting_primitives_s_l_g_off = "# STRAIGHT LINE GRADATION OFF" + " " + str(prim_b.count(sl_gradation_off)) + "\n"

                counting_primitives_s_1x1 = "# SPRITE 1X1" + " " + str(prim_b.count(sp_1x1)) + "\n"
                counting_primitives_s_f_s = "# SPRITE FREE SIZE" + " " + str(prim_b.count(sp_free_size)) + "\n"
                counting_primitives_s_16x16 = "# SPRITE 16X16" + " " + str(prim_b.count(sp_16x16)) + "\n"
                counting_primitives_s_8x8 = "# SPRITE 8X8" + " " + str(prim_b.count(sp_8x8)) + "\n"

                first_result_count = prim_b.count(lsc_three_vertex_gouraud_no_textured_solid) + prim_b.count(lsc_three_vertex_flat_no_textured_solid) + prim_b.count(lsc_three_vertex_gouraud_no_textured_gradation) + prim_b.count(lsc_three_vertex_flat_no_textured_gradation) + prim_b.count(lsc_three_vertex_gouraud_textured) + prim_b.count(lsc_three_vertex_flat_textured)
                first_result_count_2 = prim_b.count(lsc_four_vertex_gouraud_no_textured_solid) + prim_b.count(lsc_four_vertex_flat_no_textured_solid) + prim_b.count(lsc_four_vertex_gouraud_no_textured_gradation) + prim_b.count(lsc_four_vertex_flat_no_textured_gradation) + prim_b.count(lsc_four_vertex_gouraud_textured) + prim_b.count(lsc_four_vertex_flat_textured)
                second_result_count = prim_b.count(nlsc_three_vertex_gradation_no_textured) + prim_b.count(nlsc_three_vertex_flat_no_textured) + prim_b.count(nlsc_three_vertex_gradation_textured) + prim_b.count(nlsc_three_vertex_flat_textured)
                third_result_count = prim_b.count(nlsc_four_vertex_gradation_no_textured) + prim_b.count(nlsc_four_vertex_flat_no_textured) + prim_b.count(nlsc_four_vertex_gradation_textured) + prim_b.count(nlsc_four_vertex_flat_textured)
                fourth_result_count = prim_b.count(sl_gradation_on) + prim_b.count(sl_gradation_off) + prim_b.count(sp_1x1) + prim_b.count(sp_free_size) + prim_b.count(sp_16x16) + prim_b.count(sp_8x8)
                new_packets = prim_b.count(new_lsc_four_vertex_gouraud_textured) + prim_b.count(new_nlsc_three_vertex_gradation_textured) + prim_b.count(new_lsc_four_vertex_gouraud_textured_2) + prim_b.count(new_lsc_three_vertex_gouraud) + prim_b.count(new_lsc_three_vertex_gouraud_2)
                new_packets_2 = prim_b.count(new_lsc_three_vertex_gouraud_2) + prim_b.count(new_lsc_four_vertex_gouraud_no_textured_solid) + prim_b.count(new_nlsc_four_vertex_gradation_textured)

                all_result = first_result_count + first_result_count_2 + second_result_count + third_result_count + fourth_result_count + new_packets + new_packets_2
                all_result_str = "Total Number of primitives in this Object is: " + str(all_result)

                prim_informer.write(counting_primitives_lsc_3_v_g_n_t_s)
                prim_informer.write(counting_primitives_lsc_3_v_f_n_t_s)
                prim_informer.write(counting_primitives_lsc_3_v_g_n_t_g)
                prim_informer.write(counting_primitives_lsc_3_v_f_n_t_g)
                prim_informer.write(counting_primitives_lsc_3_v_g_t)
                prim_informer.write(counting_primitives_lsc_3_v_f_t)
                prim_informer.write(counting_primitives_lsc_3_v_new_packet)
                prim_informer.write(counting_primitives_lsc_3_v_new_packet_2)

                prim_informer.write(counting_primitives_lsc_4_v_g_n_t_s)
                prim_informer.write(counting_primitives_lsc_4_v_f_n_t_s)
                prim_informer.write(counting_primitives_lsc_4_v_g_n_t_g)
                prim_informer.write(counting_primitives_lsc_4_v_f_n_t_g)
                prim_informer.write(counting_primitives_lsc_4_v_g_t)
                prim_informer.write(counting_primitives_lsc_4_v_f_t)
                prim_informer.write(counting_primitives_lsc_4_v_new_packet)
                prim_informer.write(counting_primitives_lsc_4_v_new_packet_2)
                prim_informer.write(counting_primitives_lsc_4_v_new_packet_3)

                prim_informer.write(counting_primitives_nlsc_3_v_g_n_t)
                prim_informer.write(counting_primitives_nlsc_3_v_f_n_t)
                prim_informer.write(counting_primitives_nlsc_3_v_g_t)
                prim_informer.write(counting_primitives_nlsc_3_v_f_t)
                prim_informer.write(counting_primitives_nlsc_3_v_new_packet)

                prim_informer.write(counting_primitives_nlsc_4_v_g_n_t)
                prim_informer.write(counting_primitives_nlsc_4_v_n_t)
                prim_informer.write(counting_primitives_nlsc_4_v_g_t)
                prim_informer.write(counting_primitives_nlsc_4_v_f_t)
                prim_informer.write(counting_primitives_nlsc_4_v_new_packet)

                prim_informer.write(counting_primitives_s_l_g_on)
                prim_informer.write(counting_primitives_s_l_g_off)

                prim_informer.write(counting_primitives_s_1x1)
                prim_informer.write(counting_primitives_s_f_s)
                prim_informer.write(counting_primitives_s_16x16)
                prim_informer.write(counting_primitives_s_8x8)

                prim_informer.write(all_result_str)
                print("Searching for primitives in Object number " + str(num))
                #print(prim_b)
                print(all_result)