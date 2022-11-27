"""

Animation File Process Batch: This module process various files that believe to be animations,
be aware that is very buggy and experimental, the animation file has been called:
Scripted Animation File (SAF for short).

Note: This module is very buggy and experimental

Copyright (C) 2022 DooMMetaL

"""

import os
import pathlib
import standard_tmd
import struct

# SAF READER AND DECODER

class SafExtractorBatch:
    def __init__(self, readersaf, comparedata, convertsaf):
        self.self = SafExtractorBatch
        self.readersaf = readersaf
        self.comparedata = comparedata
        self.convertsaf = convertsaf
    
    def batch_saf_reader_input(self):
        try:
            print("Please, write the full path to Animation Files folder: ")
            global animation_file_paths
            global root_saf_directory
            input_folder_ani = input()
            file_paths = (os.listdir(input_folder_ani))
            root_saf_directory = input_folder_ani

            # Filtering the files paths
            animation_file_paths = []
            for filering_files in file_paths:
                if (filering_files.rfind(".bin") != -1) and (filering_files.rfind("}_35.") == -1):
                    animation_file_paths.append(filering_files)
                else:
                    pass
            
            # Checking if are files present... if not... this will be executed to stop the work
            if len(animation_file_paths) <= 0:
                print(f'No SAF (*.bin) file found... exiting...')
                exit()
        
        except OSError:
            print("Is not a valid path, exiting")
            exit()

    def batch_saf_reader(self):

        # Since i do this for joining all the animation in a single move i will put all the data out the for loop
        global keyframe_obj_block
        global anm_objs
        global anm_frames
        keyframe_obj_block = [] # HERE I GOT THE KEYFRAMES BLOCK SPLIT
        anm_objs = []
        anm_frames = []

        # iterating over the files in the file path
        for animation_file_str in animation_file_paths:
            anm_file_root_folder = root_saf_directory + f'\\' + animation_file_str
            animation_file = pathlib.Path(anm_file_root_folder)

            with open(animation_file, 'rb') as animation_saf:
                
                animation_saf.seek(12) # HERE, AVOID THE 3 RELATIVE POINTERS IN ALL THE SAFs
                head_anmfile = animation_saf.read(4) # ANIMATION HEADER, WHICH INCLUDE NOBJ AND TOTAL FRAMES?
                anm_objs_inner = int.from_bytes(head_anmfile[0:2], byteorder='little')
                anm_frames_inner = int.from_bytes(head_anmfile[2:4], byteorder='little')
                header_str = f'This Animation file contains {anm_objs_inner} Objects and {anm_frames_inner} Frames'
                anm_objs.append(anm_objs_inner)
                anm_frames.append(anm_frames_inner)
                
                print(header_str) # Printing the Animation Properties

                anm_complete_block = animation_saf.read() # Here the seek jump is done automatically
                length_each_block = anm_objs_inner * 12 # 12 == 2 Bytes for (rx,ry,rz,tx,ty,tz)

                # File size - Getting the length of the complete block, for further calculations
                anm_stat = os.path.getsize(animation_file)
                block_size = anm_stat - 16

                # Correlativity Objects/NumberFrames/Blocks
                coincidence = (block_size / length_each_block)

                if int(coincidence * 2) == anm_frames_inner:
                    pass
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
        
    def batch_compare_data(self): # HERE I COMPARE IF OBJ DATA IN TMD AND IN SAF FILE ARE EQUAL, IF NOT AN ERROR IS RAISED AND THE SOFTWARE TERMINATED
        try:
            for each_anm_objs in anm_objs:
                if each_anm_objs == standard_tmd.tmd_nobj_expected:
                    print("Objects from TMD file and Scripted Animation File are equal, so the processing will continue")
                else:
                    print("TMD file and Scripted Animation file are different, exiting")
                    exit()
        except OSError:
            print("No Data input")
    
    def batch_convert_data(self):
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