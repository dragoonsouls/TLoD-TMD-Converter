"""

Standard TMD Reader: This module read the Standard TMD Header data to be used

Copyright (C) 2021 DooMMetaL

"""

from struct import *

# Magic numbers used in most of the TMD Files

TMD_HEADER_1 = b'A\x00\x00\x00'
TMD_HEADER_2 = b'A\x01\x00\x00'
TMD_HEADER_3 = b'A\x00\x01\x00'
TMD_HEADER_4 = b'A\x00\x00\x01'


# STANDARD TMD READER CLASS

class StandardTmdReader:
    def __init__(self):
        self.self = StandardTmdReader
    
    def data_reader(self):
        try:
            print("Please, write the full path to the TMD file: ")
            global tmd_file
            input_path = input()
            tmd_file = (input_path)

        except OSError:
            print("is not a valid path, exiting")
            exit()

        with open(tmd_file, 'rb') as readfile:
            all_file = readfile.read()
            header_1_bool = bool(all_file.find(TMD_HEADER_1)) # THIS FOUR BOOLS CHECKS IF THE TMD_HEADER IS FOUND, FALSE = IS THERE ; TRUE = ISN'T THERE
            header_2_bool = bool(all_file.find(TMD_HEADER_2))
            header_3_bool = bool(all_file.find(TMD_HEADER_3))
            header_4_bool = bool(all_file.find(TMD_HEADER_4))
            global last_mark_location # THIS VALUE IS THE LAST VALUE CHECKED IN THE HEADER
            global tmd_nobj_expected # THIS VALUE IS THE NUMBER OF OBJECTS IN INT NOTATION
            global tmd_start # THIS VALUE IS USED FOR SEEK() METHOD, IN THE VERTEX, NORMAL AND PRIMITIVE BLOCK READER 

            if header_1_bool == False:
                tmd_start = tmd_start = all_file.find(TMD_HEADER_1)
                readfile.seek(tmd_start)
                tmd_read_header = readfile.read(4) # Here is reading the header itself
                if tmd_read_header == TMD_HEADER_1:
                    print("This is a Standard 0x 41 00 00 00 TMD File")
                else:
                    print("This is not a TMD File, exiting")
                    exit()

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
                
            elif header_2_bool == False:
                tmd_start = tmd_start = all_file.find(TMD_HEADER_2)
                readfile.seek(tmd_start)
                tmd_read_header = readfile.read(4)
                if tmd_read_header == TMD_HEADER_2:
                    print("This is a Standard 0x 41 01 00 00 TMD File")
                else:
                    print("This is not a TMD File, exiting")
                    exit()
                tmd_clut_prop = readfile.read(4)
                tmd_nobj_info = readfile.read(4)
                tmd_nobj_info_int = unpack('<L', tmd_nobj_info)
                tmd_nobj_expected_list = list(tmd_nobj_info)[0:1]
                tmd_nobj_extract = [str(integer) for integer in tmd_nobj_expected_list]
                join_nobj_str = "".join(tmd_nobj_extract)
                tmd_nobj_expected = int(join_nobj_str)
                print("This TMD file have: ", ''.join(str(tmd_nobj_info_int)).replace("(", "").replace(")", "").replace(",", ""), " Objects inside")
                print("Remember that TMD objects have textured and untextured faces, that all part from the same object")
                last_mark_location = all_file.find(tmd_nobj_info) + 4

            elif header_3_bool == False:
                tmd_start = tmd_start = all_file.find(TMD_HEADER_3)
                readfile.seek(tmd_start)
                tmd_read_header = readfile.read(4)
                if tmd_read_header == TMD_HEADER_3:
                    print("This is a Standard 0x 41 00 01 00 TMD File")
                else:
                    print("This is not a TMD File, exiting")
                    exit()
                tmd_clut_prop = readfile.read(4) 
                tmd_nobj_info = readfile.read(4) 
                tmd_nobj_info_int = unpack('<L', tmd_nobj_info)
                tmd_nobj_expected_list = list(tmd_nobj_info)[0:1]
                tmd_nobj_extract = [str(integer) for integer in tmd_nobj_expected_list]
                join_nobj_str = "".join(tmd_nobj_extract)
                tmd_nobj_expected = int(join_nobj_str) 
                print("This TMD file have: ", ''.join(str(tmd_nobj_info_int)).replace("(", "").replace(")", "").replace(",", ""), " Objects inside")
                print("Remember that TMD objects have textured and untextured faces, that all part from the same object")
                last_mark_location = all_file.find(tmd_nobj_info) + 4 

            elif header_4_bool == False:
                tmd_start = tmd_start = all_file.find(TMD_HEADER_4) 
                readfile.seek(tmd_start)
                tmd_read_header = readfile.read(4) 
                if tmd_read_header == TMD_HEADER_4:
                    print("This is a Standard 0x 41 00 00 01 TMD File")
                else:
                    print("This is not a TMD File, exiting")
                    exit()
                tmd_clut_prop = readfile.read(4) 
                tmd_nobj_info = readfile.read(4) 
                tmd_nobj_info_int = unpack('<L', tmd_nobj_info) 
                tmd_nobj_expected_list = list(tmd_nobj_info)[0:1]
                tmd_nobj_extract = [str(integer) for integer in tmd_nobj_expected_list]
                join_nobj_str = "".join(tmd_nobj_extract)
                tmd_nobj_expected = int(join_nobj_str) 
                print("This TMD file have: ", ''.join(str(tmd_nobj_info_int)).replace("(", "").replace(")", "").replace(",", ""), " Objects inside")
                print("Remember that TMD objects have textured and untextured faces, that all part from the same object")
                last_mark_location = all_file.find(tmd_nobj_info) + 4 
            else:
                print("This is not a TMD file or Header is not correct")
