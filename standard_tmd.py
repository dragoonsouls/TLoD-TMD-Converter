"""

Standard TMD Reader: This module read the Standard TMD Header data to be used

Copyright (C) 2022 DooMMetaL

"""

from struct import *

# Magic numbers used in most of the TMD Files

TMD_HEADER_1 = b'A\x00\x00\x00'
TMD_HEADER_2 = b'A\x01\x00\x00'
TMD_HEADER_3 = b'A\x00\x01\x00'
TMD_HEADER_4 = b'A\x00\x00\x01'
TMD_HEADER_5 = b'A\x00\x03\x00'


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

        with open(tmd_file, 'rb') as read_file:
            all_file = read_file.read()
            header_1_bool = all_file.find(TMD_HEADER_1)
            header_2_bool = all_file.find(TMD_HEADER_2)
            header_3_bool = all_file.find(TMD_HEADER_3)
            header_4_bool = all_file.find(TMD_HEADER_4)
            header_5_bool = all_file.find(TMD_HEADER_5)
            global last_mark_location # THIS VALUE IS THE LAST VALUE CHECKED IN THE HEADER
            global tmd_nobj_expected # THIS VALUE IS THE NUMBER OF OBJECTS IN INT NOTATION
            global tmd_start # THIS VALUE IS USED FOR SEEK() METHOD, IN THE VERTEX, NORMAL AND PRIMITIVE BLOCK READER
            global clut_data_start # THIS ONLY WORKS WITH STANDARD TMD INSIDE DEFF FILES

            # WRITE A PROPER ONE PLS!!!!

            if (header_1_bool != -1) and (header_1_bool < 24):
                tmd_start = all_file.find(TMD_HEADER_1) # OBTAINING THE POSITION OF THE TMD HEADER FIRST OCCURRENCE
                clut_data_start = all_file[0:tmd_start] # HERE I GET THE CLUT DATA FROM THE START OF THE FILE
                read_file.seek(tmd_start)
                read_header = read_file.read(4) # Here is reading the header itself

                if read_header == TMD_HEADER_1:
                    print("This is a Standard 0x 41 00 00 00 TMD File")
                else:
                    print("This is not a Standard TMD file")
                    exit()
                
                tmd_clut_prop = read_file.read(4) # Here i obtain the TMD - CLUT property values / FLAGS
                tmd_nobj_prop = read_file.read(4) # Here i obtain the TMD Number of Objects in file
                tmd_clut_prop_info = int.from_bytes(tmd_clut_prop, 'little')
                tmd_nobj_prop_info = int.from_bytes(tmd_nobj_prop, 'little')
                tmd_nobj_expected = int.from_bytes(tmd_nobj_prop, 'little')
                tmd_properties = f'FLAG Configuration: {tmd_clut_prop_info}, Number of Objects in the File: {tmd_nobj_prop_info}'
                last_mark_location = tmd_start + 12 # I HAVE TO BE WITH AN EYE ON THIS, MAY CAN FAIL
                print(tmd_properties)
            
            elif (header_2_bool != -1) and (header_2_bool < 24):
                tmd_start = all_file.find(TMD_HEADER_2) # OBTAINING THE POSITION OF THE TMD HEADER FIRST OCCURRENCE
                clut_data_start = all_file[0:tmd_start] # HERE I GET THE CLUT DATA FROM THE START OF THE FILE
                read_file.seek(tmd_start)
                read_header = read_file.read(4) # Here is reading the header itself

                if read_header == TMD_HEADER_2:
                    print("This is a Standard 0x 41 01 00 00 TMD File")
                else:
                    print("This is not a Standard TMD file")
                    exit()
                
                tmd_clut_prop = read_file.read(4) # Here i obtain the TMD - CLUT property values / FLAGS
                tmd_nobj_prop = read_file.read(4) # Here i obtain the TMD Number of Objects in file
                tmd_clut_prop_info = int.from_bytes(tmd_clut_prop, 'little')
                tmd_nobj_prop_info = int.from_bytes(tmd_nobj_prop, 'little')
                tmd_nobj_expected = int.from_bytes(tmd_nobj_prop, 'little')
                tmd_properties = f'FLAG Configuration: {tmd_clut_prop_info}, Number of Objects in the File: {tmd_nobj_prop_info}'
                last_mark_location = tmd_start + 12 # I HAVE TO BE WITH AN EYE ON THIS, MAY CAN FAIL
                print(tmd_properties)
            
            elif (header_3_bool != -1) and (header_3_bool < 24):
                tmd_start = all_file.find(TMD_HEADER_3) # OBTAINING THE POSITION OF THE TMD HEADER FIRST OCCURRENCE
                clut_data_start = all_file[0:tmd_start] # HERE I GET THE CLUT DATA FROM THE START OF THE FILE
                read_file.seek(tmd_start)
                read_header = read_file.read(4) # Here is reading the header itself

                if read_header == TMD_HEADER_3:
                    print("This is a Standard 0x 41 00 01 00 TMD File")
                else:
                    print("This is not a Standard TMD file")
                    exit()
                
                tmd_clut_prop = read_file.read(4) # Here i obtain the TMD - CLUT property values / FLAGS
                tmd_nobj_prop = read_file.read(4) # Here i obtain the TMD Number of Objects in file
                tmd_clut_prop_info = int.from_bytes(tmd_clut_prop, 'little')
                tmd_nobj_prop_info = int.from_bytes(tmd_nobj_prop, 'little')
                tmd_nobj_expected = int.from_bytes(tmd_nobj_prop, 'little')
                tmd_properties = f'FLAG Configuration: {tmd_clut_prop_info}, Number of Objects in the File: {tmd_nobj_prop_info}'
                last_mark_location = tmd_start + 12 # I HAVE TO BE WITH AN EYE ON THIS, MAY CAN FAIL
                print(tmd_properties)
            
            elif (header_4_bool != -1) and (header_4_bool < 24):
                tmd_start = all_file.find(TMD_HEADER_4) # OBTAINING THE POSITION OF THE TMD HEADER FIRST OCCURRENCE
                clut_data_start = all_file[0:tmd_start] # HERE I GET THE CLUT DATA FROM THE START OF THE FILE
                read_file.seek(tmd_start)
                read_header = read_file.read(4) # Here is reading the header itself

                if read_header == TMD_HEADER_4:
                    print("This is a Standard 0x 41 00 00 01 TMD File")
                else:
                    print("This is not a Standard TMD file")
                    exit()
                
                tmd_clut_prop = read_file.read(4) # Here i obtain the TMD - CLUT property values / FLAGS
                tmd_nobj_prop = read_file.read(4) # Here i obtain the TMD Number of Objects in file
                tmd_clut_prop_info = int.from_bytes(tmd_clut_prop, 'little')
                tmd_nobj_prop_info = int.from_bytes(tmd_nobj_prop, 'little')
                tmd_nobj_expected = int.from_bytes(tmd_nobj_prop, 'little')
                tmd_properties = f'FLAG Configuration: {tmd_clut_prop_info}, Number of Objects in the File: {tmd_nobj_prop_info}'
                last_mark_location = tmd_start + 12 # I HAVE TO BE WITH AN EYE ON THIS, MAY CAN FAIL
                print(tmd_properties)
            
            elif (header_5_bool != -1) and (header_5_bool < 24):
                tmd_start = all_file.find(TMD_HEADER_5) # OBTAINING THE POSITION OF THE TMD HEADER FIRST OCCURRENCE
                clut_data_start = all_file[0:tmd_start] # HERE I GET THE CLUT DATA FROM THE START OF THE FILE
                read_file.seek(tmd_start)
                read_header = read_file.read(4) # Here is reading the header itself

                if read_header == TMD_HEADER_5:
                    print("This is a Standard 0x 41 00 03 00 TMD File")
                else:
                    print("This is not a Standard TMD file")
                    exit()
                
                tmd_clut_prop = read_file.read(4) # Here i obtain the TMD - CLUT property values / FLAGS
                tmd_nobj_prop = read_file.read(4) # Here i obtain the TMD Number of Objects in file
                tmd_clut_prop_info = int.from_bytes(tmd_clut_prop, 'little')
                tmd_nobj_prop_info = int.from_bytes(tmd_nobj_prop, 'little')
                tmd_nobj_expected = int.from_bytes(tmd_nobj_prop, 'little')
                tmd_properties = f'FLAG Configuration: {tmd_clut_prop_info}, Number of Objects in the File: {tmd_nobj_prop_info}'
                last_mark_location = tmd_start + 12 # I HAVE TO BE WITH AN EYE ON THIS, MAY CAN FAIL
                print(tmd_properties)
            
            else:
                print("This is not a Standard TMD file or Header is not correct/documented - HIGHLY RECOMMENDED: Check manually the file")