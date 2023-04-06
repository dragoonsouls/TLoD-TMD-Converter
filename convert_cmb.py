"""

Convert CMB: This module process CMB files
CMB Files use Fibonnaci Sequence as "base".
there is a Base pose and the animation is applied to
that base pose

At the moment are fully supported only Embedded CMBs

Copyright (C) 2023 DooMMetaL

"""

class CmbConverter:
    def __init__(self):
        self.self = CmbConverter

    def cmb_convert(self, cmb_anim=bytes, cmb_trans_info=list):
        cmb_anm_objs = cmb_trans_info[0]
        cmb_data = cmb_anim

        split_blocks = self.cmb_split_blocks(cmb_data_block=cmb_data, cmb_objs_info=cmb_anm_objs)
        static_anm_block = split_blocks[0]
        add_accumulative_anm_block = split_blocks[1]
        cmb_decoded_animation = self.cmb_decode(first_anm_block=static_anm_block, cmb_anm_block=add_accumulative_anm_block)

        return cmb_decoded_animation
    
    @staticmethod
    def cmb_split_blocks(cmb_data_block=bytes, cmb_objs_info=int):
        first_animation_block = []
        static_block_len = cmb_objs_info * 12
        static_block = cmb_data_block[0:static_block_len]

        static_value = static_block_len
        s_static = 0
        e_static = 12
        while static_value > 0:
            static_extract = static_block[s_static:e_static]
            first_animation_block.append(static_extract)
            s_static += 12
            e_static += 12
            static_value -= 12
        
        subtransform_block = cmb_data_block[static_block_len:]
        each_block_size = cmb_objs_info * 8
        subtransform_animation = []
        s_subanm = 0
        e_subanm = each_block_size
        length_sub_anm = len(subtransform_block)
        while length_sub_anm > 0:
            sub_extract = subtransform_block[s_subanm:e_subanm]
            subtransform_animation.append(sub_extract)
            s_subanm += each_block_size
            e_subanm += each_block_size
            length_sub_anm -= each_block_size
        
        cmb_anm_block = []
        for unique_subtransform_obj in subtransform_animation:
            obj_sub_keyframe = []
            len_obj_uni = len(unique_subtransform_obj)
            s_unkey = 0
            e_unkey = 8
            while len_obj_uni > 0:
                u_key_get = unique_subtransform_obj[s_unkey:e_unkey]
                obj_sub_keyframe.append(u_key_get)
                s_unkey += 8
                e_unkey += 8
                len_obj_uni -= 8
            cmb_anm_block.append(obj_sub_keyframe)
        
        return first_animation_block, cmb_anm_block
    
    @staticmethod
    def cmb_decode(first_anm_block=list, cmb_anm_block=list):

        static_rot_trans_cmb = [] # HERE I GET THE STATIC POSE
        object_number_cmb = 0
        for cmb_static in first_anm_block:
            rottrans_static_dict = {"Rx": float(int.from_bytes(cmb_static[0:2], 'little', signed=True) / round((4096/360), 12)),
                    "Ry": float(int.from_bytes(cmb_static[2:4], 'little', signed=True) / round((4096/360), 12)),
                    "Rz": float(int.from_bytes(cmb_static[4:6], 'little', signed=True) / round((4096/360), 12)), 
                    "Tx": float(int.from_bytes(cmb_static[6:8], 'little', signed=True) / 1000), 
                    "Ty": float(int.from_bytes(cmb_static[8:10], 'little', signed=True) / 1000), 
                    "Tz": float(int.from_bytes(cmb_static[10:12], 'little', signed=True) / 1000)}
            rot_trans_static = object_number_cmb, rottrans_static_dict
            static_rot_trans_cmb.append(rot_trans_static)
            object_number_cmb += 1

        cmb_keyframes_converted = []
        internal_keyframe_count = 0
        length_init = len(cmb_anm_block) + 1
        for current_frame in range(0, length_init):
            number_obj = 0
            if internal_keyframe_count == 0:
                ctmd_first_anm = []
                for static_anm_1st in static_rot_trans_cmb:
                    change_a_little = static_anm_1st[1]
                    ctmd_first_anm.append(change_a_little)
                cmb_keyframes_converted.append(ctmd_first_anm)
            else:
                ctmd_obj_transformations = []
                next_sum = []
                for keyfb_cmb in cmb_anm_block[current_frame - 1]:
                    # GETTING STATIC VALUES
                    sum_static_val = static_rot_trans_cmb[number_obj]
                    non_enum_static_value = sum_static_val[1]

                    static_value_rotx = non_enum_static_value.get("Rx")
                    static_value_roty = non_enum_static_value.get("Ry")
                    static_value_rotz = non_enum_static_value.get("Rz")
                    static_value_transx = non_enum_static_value.get("Tx")
                    static_value_transy = non_enum_static_value.get("Ty")
                    static_value_transz = non_enum_static_value.get("Tz")

                    # GETTING THE ACTIVE VALUES
                    rot_scalar_uint = int.from_bytes(keyfb_cmb[0:1], 'little', signed=True)
                    trans_scalar_uint = int.from_bytes(keyfb_cmb[4:5], 'little', signed=True)

                    rot_x_int = int.from_bytes(keyfb_cmb[1:2], 'little', signed=True)
                    rot_y_int = int.from_bytes(keyfb_cmb[2:3], 'little', signed=True)
                    rot_z_int = int.from_bytes(keyfb_cmb[3:4], 'little', signed=True)
                    trans_x_int = int.from_bytes(keyfb_cmb[5:6], 'little', signed=True)
                    trans_y_int = int.from_bytes(keyfb_cmb[6:7], 'little', signed=True)
                    trans_z_int = int.from_bytes(keyfb_cmb[7:8], 'little', signed=True)

                    rot_x_calc = rot_x_int << rot_scalar_uint
                    rot_y_calc = rot_y_int << rot_scalar_uint
                    rot_z_calc = rot_z_int << rot_scalar_uint
                    trans_x_calc = trans_x_int << trans_scalar_uint
                    trans_y_calc = trans_y_int << trans_scalar_uint
                    trans_z_calc = trans_z_int << trans_scalar_uint

                    end_calc_rotx = static_value_rotx + float(rot_x_calc / round((4096/360), 12))
                    end_calc_roty = static_value_roty + float(rot_y_calc / round((4096/360), 12))
                    end_calc_rotz = static_value_rotz + float(rot_z_calc / round((4096/360), 12))
                    end_calc_locx = static_value_transx + float(trans_x_calc / 1000)
                    end_calc_locy = static_value_transy + float(trans_y_calc / 1000)
                    end_calc_locz = static_value_transz + float(trans_z_calc / 1000)

                    #New Static Value
                    non_enum_static_value.update({"Rx": end_calc_rotx})
                    non_enum_static_value.update({"Ry": end_calc_roty})
                    non_enum_static_value.update({"Rz": end_calc_rotz})
                    non_enum_static_value.update({"Tx": end_calc_locx})
                    non_enum_static_value.update({"Ty": end_calc_locy})
                    non_enum_static_value.update({"Tz": end_calc_locz})

                    ctmd_rot_trans = {"Rx": float(end_calc_rotx), "Ry": float(end_calc_roty), "Rz": float(end_calc_rotz), "Tx": float(end_calc_locx), "Ty": float(end_calc_locy), "Tz": float(end_calc_locz)}
                    ctmd_obj_transformations.append(ctmd_rot_trans)
                    next_sum.append(ctmd_rot_trans)
                    number_obj += 1
                cmb_keyframes_converted.append(ctmd_obj_transformations)
            internal_keyframe_count += 1

        enumerating_keyframe_final = []
        for enumerating in cmb_keyframes_converted:
            enumerating_keyframe_obj = []
            for enum in enumerating:
                enum_inside = enum
                enumerating_keyframe_obj.append(enum_inside)
            getting_enum = list(enumerate(enumerating_keyframe_obj))
            enumerating_keyframe_final.append(getting_enum)

        cmb_keyframes_converted_enum = list(enumerate(enumerating_keyframe_final)) # HERE I GET THE CORRECT NESTING USING THE KEYFRAME ENUMERATED
        print("Conversion of Keyframes successful")
        return cmb_keyframes_converted_enum