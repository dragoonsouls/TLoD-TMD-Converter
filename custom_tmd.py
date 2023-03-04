"""

Custom TMD Reader: This module read the Custom TMD data to be used

Copyright (C) 2021 DooMMetaL

"""
#from struct import *

# Magic numbers used in most of the TMD Files

TMD_HEADER_1 = b'A\x00\x00\x00\x02\x00\x00\x00'
TMD_HEADER_2 = b'A\x01\x00\x00\x02\x00\x00\x00'
TMD_HEADER_3 = b'A\x00\x01\x00\x02\x00\x00\x00'
TMD_HEADER_4 = b'A\x00\x00\x01\x02\x00\x00\x00'
TMD_HEADER_5 = b'A\x00\x02\x00\x02\x00\x00\x00'
CMB_HEADER = b'\x43\x4D\x42\x20'
LMB_HEADER_0 = b'\x4C\x4D\x42\x00'
SAF_HEADER = b'\x0C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

# CUSTOM TMD CLASS

class CustomTmdReader:
    def __init__(self):
        self.self = CustomTmdReader
    
    def custom_data_reader(self):
        try:
            print("Please, write the full path to the Custom TMD file: ")
            global custom_tmd_file
            input_path = input()
            custom_tmd_file = (input_path)
        
        except OSError:
            print("This is not a valid path, exiting")
            exit()

        with open(custom_tmd_file, 'rb') as read_c_file:
            all_c_file = read_c_file.read()
            header_c_bool_1 = all_c_file.find(TMD_HEADER_1)
            header_c_bool_2 = all_c_file.find(TMD_HEADER_2)
            header_c_bool_3 = all_c_file.find(TMD_HEADER_3)
            header_c_bool_4 = all_c_file.find(TMD_HEADER_4)
            header_c_bool_5 = all_c_file.find(TMD_HEADER_5)
            global last_mark_location_c
            global ctmd_nobj_expected
            global ctmd_start
            global clut_data_start

            if header_c_bool_1 != -1:
                ctmd_start = all_c_file.find(TMD_HEADER_1) # OBTAINING THE POSITION OF THE TMD HEADER FIRST OCCURRENCE
                clut_data_start = all_c_file[0:ctmd_start] # HERE I GET THE CLUT DATA FROM THE START OF THE FILE
                read_c_file.seek(ctmd_start)
                read_c_header = read_c_file.read(8) # Here is reading the header itself

                if read_c_header == TMD_HEADER_1:
                    print("This is a common 0x 41 00 00 00 Custom TMD File")
                else:
                    print("This is not a Custom TMD file")
                    exit()
                
                ctmd_nobj_prop = read_c_file.read(4) # Here i obtain the TMD Number of Objects in file
                ctmd_clut_prop_info = 2
                ctmd_nobj_prop_info = int.from_bytes(ctmd_nobj_prop, 'little')
                ctmd_nobj_expected = int.from_bytes(ctmd_nobj_prop, 'little')
                ctmd_properties = f'FLAG Configuration: {ctmd_clut_prop_info}, Number of Objects in the File: {ctmd_nobj_prop_info}'
                last_mark_location_c = ctmd_start + 12 # I HAVE TO BE WITH AN EYE ON THIS, MAY CAN FAIL
                print(ctmd_properties)
            
            elif header_c_bool_2 != -1:
                ctmd_start = all_c_file.find(TMD_HEADER_2) # OBTAINING THE POSITION OF THE TMD HEADER FIRST OCCURRENCE
                clut_data_start = all_c_file[0:ctmd_start] # HERE I GET THE CLUT DATA FROM THE START OF THE FILE
                read_c_file.seek(ctmd_start)
                read_c_header = read_c_file.read(8) # Here is reading the header itself

                if read_c_header == TMD_HEADER_2:
                    print("This is a common 0x 41 01 00 00 Custom TMD File")
                else:
                    print("This is not a Custom TMD file")
                    exit()
                
                ctmd_nobj_prop = read_c_file.read(4) # Here i obtain the TMD Number of Objects in file
                ctmd_clut_prop_info = 2
                ctmd_nobj_prop_info = int.from_bytes(ctmd_nobj_prop, 'little')
                ctmd_nobj_expected = int.from_bytes(ctmd_nobj_prop, 'little')
                ctmd_properties = f'FLAG Configuration: {ctmd_clut_prop_info}, Number of Objects in the File: {ctmd_nobj_prop_info}'
                last_mark_location_c = ctmd_start + 12 # I HAVE TO BE WITH AN EYE ON THIS, MAY CAN FAIL
                print(ctmd_properties)
            
            elif header_c_bool_3 != -1:
                ctmd_start = all_c_file.find(TMD_HEADER_3) # OBTAINING THE POSITION OF THE TMD HEADER FIRST OCCURRENCE
                clut_data_start = all_c_file[0:ctmd_start] # HERE I GET THE CLUT DATA FROM THE START OF THE FILE
                read_c_file.seek(ctmd_start)
                read_c_header = read_c_file.read(8) # Here is reading the header itself

                if read_c_header == TMD_HEADER_3:
                    print("This is a common 0x 41 00 01 00 Custom TMD File")
                else:
                    print("This is not a Custom TMD file")
                    exit()
                
                ctmd_nobj_prop = read_c_file.read(4) # Here i obtain the TMD Number of Objects in file
                ctmd_clut_prop_info = 2
                ctmd_nobj_prop_info = int.from_bytes(ctmd_nobj_prop, 'little')
                ctmd_nobj_expected = int.from_bytes(ctmd_nobj_prop, 'little')
                ctmd_properties = f'FLAG Configuration: {ctmd_clut_prop_info}, Number of Objects in the File: {ctmd_nobj_prop_info}'
                last_mark_location_c = ctmd_start + 12 # I HAVE TO BE WITH AN EYE ON THIS, MAY CAN FAIL
                print(ctmd_properties)
            
            elif header_c_bool_4 != -1:
                ctmd_start = all_c_file.find(TMD_HEADER_4) # OBTAINING THE POSITION OF THE TMD HEADER FIRST OCCURRENCE
                clut_data_start = all_c_file[0:ctmd_start] # HERE I GET THE CLUT DATA FROM THE START OF THE FILE
                read_c_file.seek(ctmd_start)
                read_c_header = read_c_file.read(8) # Here is reading the header itself

                if read_c_header == TMD_HEADER_4:
                    print("This is a common 0x 41 00 00 01 Custom TMD File")
                else:
                    print("This is not a Custom TMD file")
                    exit()
                
                ctmd_nobj_prop = read_c_file.read(4) # Here i obtain the TMD Number of Objects in file
                ctmd_clut_prop_info = 2
                ctmd_nobj_prop_info = int.from_bytes(ctmd_nobj_prop, 'little')
                ctmd_nobj_expected = int.from_bytes(ctmd_nobj_prop, 'little')
                ctmd_properties = f'FLAG Configuration: {ctmd_clut_prop_info}, Number of Objects in the File: {ctmd_nobj_prop_info}'
                last_mark_location_c = ctmd_start + 12 # I HAVE TO BE WITH AN EYE ON THIS, MAY CAN FAIL
                print(ctmd_properties)
            
            elif header_c_bool_5 != -1:
                ctmd_start = all_c_file.find(TMD_HEADER_5) # OBTAINING THE POSITION OF THE TMD HEADER FIRST OCCURRENCE
                clut_data_start = all_c_file[0:ctmd_start] # HERE I GET THE CLUT DATA FROM THE START OF THE FILE
                read_c_file.seek(ctmd_start)
                read_c_header = read_c_file.read(8) # Here is reading the header itself

                if read_c_header == TMD_HEADER_5:
                    print("This is a common 0x 41 00 02 00 Custom TMD File")
                else:
                    print("This is not a Custom TMD file")
                    exit()
                
                ctmd_nobj_prop = read_c_file.read(4) # Here i obtain the TMD Number of Objects in file
                ctmd_clut_prop_info = 2
                ctmd_nobj_prop_info = int.from_bytes(ctmd_nobj_prop, 'little')
                ctmd_nobj_expected = int.from_bytes(ctmd_nobj_prop, 'little')
                ctmd_properties = f'FLAG Configuration: {ctmd_clut_prop_info}, Number of Objects in the File: {ctmd_nobj_prop_info}'
                last_mark_location_c = ctmd_start + 12 # I HAVE TO BE WITH AN EYE ON THIS, MAY CAN FAIL
                print(ctmd_properties)
            
            else:
                print("This is not a Custom TMD file or Header is not correct/documented - HIGHLY RECOMMENDED: Check manually the file")
        
        with open(custom_tmd_file, 'rb') as look_for_anim:
            all_anim_file = look_for_anim.read()
            header_anm_cmb = all_anim_file.find(CMB_HEADER)
            header_anm_lmb0 = all_anim_file.find(LMB_HEADER_0)
            header_anm_saf = all_anim_file.find(SAF_HEADER)

            global animation_bool
            global cmb_animation_block
            global cmb_animation_bool
            global lmb0_animation_bool
            global lmb0_animation_block
            global saf_animation_bool
            global saf_animation_block
            animation_bool = None
            cmb_animation_bool = None
            lmb0_animation_bool = None
            saf_animation_bool = None
            
            if header_anm_cmb != -1:
                print(f'CMB Animation Type Embedded in the file, automatically decoding...')
                cmb_animation_bool = True
                animation_bool = True
                cmb_start = all_anim_file.find(CMB_HEADER) # OBTAINING THE POSITION OF THE TMD HEADER FIRST OCCURRENCE
                cmb_animation_block = all_anim_file[cmb_start:]

            elif header_anm_lmb0 != -1:
                print(f'LMB Animation Type 0 Embedded in the file, automatically decoding...')
                lmb0_animation_bool = True
                animation_bool = True
                lmb0_start = all_anim_file.find(LMB_HEADER_0)
                lmb0_animation_block = all_anim_file[lmb0_start:]
            
            elif (header_anm_saf != -1) and (header_anm_saf < 256):
                next_saf_val = all_anim_file[(header_anm_saf + 4):]
                new_search_saf = next_saf_val.find(SAF_HEADER)
                current_saf_mark = new_search_saf + header_anm_saf + 4
                saf_header_block = all_anim_file[current_saf_mark:(current_saf_mark + 16)]
                saf_obj_num_hex = saf_header_block[12:14]
                saf_obj_num_int = int.from_bytes(saf_obj_num_hex, 'little', signed=False)
                if (header_anm_saf != 1) and (saf_obj_num_int == ctmd_nobj_expected):
                    print(f'SAF Animation Embedded in the file, automatically decoding...')
                    saf_animation_bool = True
                    animation_bool = True
                    saf_animation_block = all_anim_file[current_saf_mark:]
                else:
                    animation_bool = None

            else:
                print(f'No animation embedded found in the CTMD')