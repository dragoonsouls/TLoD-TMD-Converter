"""

Convert SAF: This module process SAF files
Scripted Animation File (SAF for short).

Copyright (C) 2023 DooMMetaL

"""

class SafConverter:
    def __init__(self, animation_byte_block, saf_transform_info, merge_flag):
        self.self = SafConverter
        self.saf_convert(animation_byte_block=animation_byte_block, saf_transform_info=saf_transform_info ,merge_flag=merge_flag)

    def saf_convert(self, animation_byte_block, saf_transform_info, merge_flag=bool):
        anm_block = animation_byte_block
        saf_trans_info = saf_transform_info
        #global saf_animation_decoded i don't think this is needed at all
        saf_animation_decoded = []
        if merge_flag == False:
            saf_animation_split = self.saf_single_split(animation_block=anm_block, saf_transform_info=saf_trans_info)
            saf_animation_decoded = self.decode_saf(keyframe_split=saf_animation_split)

        elif merge_flag == True:
            pass
        else:
            print(f'FATAL ERROR - MERGING FLAG UNSET!!')
            exit()

        return saf_animation_decoded

    @staticmethod
    def saf_single_split(animation_block=bytes, saf_transform_info=list):
        nobjs_tmd = saf_transform_info[0]
        anm_frames = saf_transform_info[1]
        anm_complete_block = animation_block # Here the seek jump is done automatically
        length_each_block = nobjs_tmd * 12 # 12 == 2 Bytes for (rx,ry,rz,tx,ty,tz)
        # File size - Getting the length of the complete block, for further calculations
        block_size = len(animation_block)
        # Correlativity Objects/NumberFrames/Blocks
        coincidence = (block_size // length_each_block)

        if int(coincidence * 2) == (anm_frames * 2): # Multiply this anm frames because in SAF are split in ROT/LOC
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
        
        return keyframe_obj_block
    
    @staticmethod
    def decode_saf(keyframe_split=list):
        keyframes_converted = [] # HERE I GET THE KEYFRAMES CONVERTED FROM BYTES TO SIGNED INTS
        for keyf_byte in keyframe_split:
            single_obj_transformations = []
            for keyfb in keyf_byte:
                object_rot_trans = {"Rx": float(int.from_bytes(keyfb[0:2], 'little', signed=True) / round((4096/360), 12)),
                "Ry": float(int.from_bytes(keyfb[2:4], 'little', signed=True) / round((4096/360), 12)),
                "Rz": float(int.from_bytes(keyfb[4:6], 'little', signed=True) / round((4096/360), 12)), 
                "Tx": float(int.from_bytes(keyfb[6:8], 'little', signed=True) / 1000), 
                "Ty": float(int.from_bytes(keyfb[8:10], 'little', signed=True) / 1000), 
                "Tz": float(int.from_bytes(keyfb[10:12], 'little', signed=True) / 1000)}
                single_obj_transformations.append(object_rot_trans)
            obj_transformations = list(enumerate(single_obj_transformations))
            keyframes_converted.append(obj_transformations)
        keyframes_converted_enum = list(enumerate(keyframes_converted)) # HERE I GET THE CORRECT NESTING USING THE KEYFRAME ENUMERATED
        print("Conversion of Keyframes successful")

        return keyframes_converted_enum