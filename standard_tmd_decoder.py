"""

Standard TMD Decoder: This module decode the data from Vertex, Normal and Primitive
into integers for easy read/write for the Standard TMD Writer.
This module has to be very flexible and easy to update

Copyright (C) 2022 DooMMetaL

"""
from itertools import zip_longest
from posixpath import basename, join
import struct
import standard_tmd_structure
import re


class VertexInterpreter():
    def __init__(self, vertex_decode):
        self.self = VertexInterpreter
        self.vertex_decode = vertex_decode
    
    def vertex_decoder(self): # VERTEX WILL BE PASS AS INT FOR LATER DO THE MATHS FOR THEM IN THE STANDARD_TMD_WRITER -- do this for the proper conversion to any other format
        global vertex_decoded
        vertex_decoded = []
        vertex_raw_4 = []
        vertex_number_in_obj = zip(standard_tmd_structure.vertex_number_int, standard_tmd_structure.vertex_block_byte)
        for num_v, vertices_raw in vertex_number_in_obj:
            vertices_split = []
            number_vertex = num_v
            start_vertex_count = 0
            end_vertex_count = 8
            while number_vertex > 0:
                vertices_split_in_4 = vertices_raw[start_vertex_count:end_vertex_count]
                number_vertex -= 1
                start_vertex_count += 8
                end_vertex_count += 8
                vertices_split.append(vertices_split_in_4)
            vertex_raw_4.append(vertices_split)
        
        for vertices_splitted in vertex_raw_4:
            vertex_in_obj = []
            for vertex_pos in vertices_splitted:
                vertex_single = []
                vertex_x = int(str(struct.unpack('<h', vertex_pos[0:2])).replace("(", "").replace(")", "").replace(",", ""))
                vertex_y = int(str(struct.unpack('<h', vertex_pos[2:4])).replace("(", "").replace(")", "").replace(",", ""))
                vertex_z = int(str(struct.unpack('<h', vertex_pos[4:6])).replace("(", "").replace(")", "").replace(",", ""))
                vertex_pad = vertex_pos[6:8] # IGNORED BUT TAKING THIS VALUE IN ACCOUNT BY ANY CASE OF A NEW FINDING
                vertex_single.append(vertex_x)
                vertex_single.append(vertex_y)
                vertex_single.append(vertex_z)

                vertex_in_obj.append(vertex_single)
            vertex_decoded.append(vertex_in_obj)


class NormalInterpreter():
    def __init__(self, normal_decode):
        self.self = NormalInterpreter
        self.normal_decode = normal_decode
    
    def normal_decoder(self): # NORMAL WILL BE PASS AS INT FOR LATER DO THE MATHS FOR THEM IN THE STANDARD_TMD_WRITER -- do this for the proper conversion to any other format
        global normal_decoded
        normal_decoded = []
        normal_raw_4 = []
        normal_number_in_obj = zip(standard_tmd_structure.normal_number_int, standard_tmd_structure.normal_block_byte)
        for num_n, normal_raw in normal_number_in_obj:
            normal_split = []
            number_normal = num_n
            start_normal_count = 0
            end_normal_count = 8
            while number_normal > 0:
                normal_split_in_4 = normal_raw[start_normal_count:end_normal_count]
                number_normal -= 1
                start_normal_count += 8
                end_normal_count += 8
                normal_split.append(normal_split_in_4)
            normal_raw_4.append(normal_split)
        
        for normal_splitted in normal_raw_4:
            normal_in_obj = []
            for normal_pos in normal_splitted:
                normal_single = []
                normal_x = int(str(struct.unpack('<h', normal_pos[0:2])).replace("(", "").replace(")", "").replace(",", ""))
                normal_y = int(str(struct.unpack('<h', normal_pos[2:4])).replace("(", "").replace(")", "").replace(",", ""))
                normal_z = int(str(struct.unpack('<h', normal_pos[4:6])).replace("(", "").replace(")", "").replace(",", ""))
                normal_pad = normal_pos[6:8] # IGNORED BUT TAKING THIS VALUE IN ACCOUNT BY ANY CASE OF A NEW FINDING
                normal_single.append(normal_x)
                normal_single.append(normal_y)
                normal_single.append(normal_z)

                normal_in_obj.append(normal_single)
            normal_decoded.append(normal_in_obj)




class PrimitivePacketHeader():
    def __init__(self):
        self.self = PrimitivePacketHeader
    

    # TYPES OF PRIMITIVES - DID THIS WAY, FOR SAKE OF SIMPLICITY AND EASY UPDATE (MAYBE NOT THE BEST WAY)
    # THE STRAIGHT LINE AND 3-DIMENSIONAL SPRITE IS DESCRIBED HERE, BUT NOT IMPLEMENTED RIGHT NOW
    # FOR SAKE OF SORTING THE NEW PRIMITIVES FOUND WILL BE PLACED HERE, BUT LATER IN THE CODE WILL BE AT BOTTOM OF THE LSC TEX/NOTEX OR NLSC TEX/NOTEX LIST
    
    # 3 VERTEX POLY LIGHT SOURCE CALCULATION
    # TEXTURED
    lsc_3v_g_t = b'\x09\x06\x00\x34'    # GOURAUD TEXTURED - 6 row = 24
    lsc_3v_f_t = b'\x07\x05\x00\x24'    # FLAT TEXTURED - 5 row = 20
    new_lsc_3v_gt = b'\x09\x06\x02\x34' # NEW 3 VERTEX GOURAUD TEXTURED - 6 row = 24
    new_lsc_3v_gt_2 = b'\x09\x06\x00\x36' # NEW 3 VERTEX GOURAUD TEXTURED - 6 row = 24
    # NO TEXTURED
    lsc_3v_nt_g_s = b'\x06\x04\x00\x30' # GOURAUD SOLID - 4 row = 16
    lsc_3v_nt_f_s = b'\x04\x03\x00\x20' # FLAT SOLID - 3 row = 12
    lsc_3v_nt_g_g = b'\x06\x06\x04\x30' # GOURAUD GRADATION - 6 row = 24
    lsc_3v_nt_f_g = b'\x06\x05\x04\x20' # FLAT GRADATION - 5 row = 20
    new_lsc_3v_nt_gg = b'\x06\x06\x04\x32' # NEW 3 VERTEX GOURAUD GRADATION NO TEXTURE - 6 row = 24 REAL NAME = LSC_3V_GOURAUD_GRADATION_TRANSLUCENT_SINGLE_FACE
    new_lsc_3v_nt_fg = b'\x06\x04\x00\x32' # NEW 3 VERTEX GOURAUD FLAT NO TEXTURE TRANSLUCENT - 5 row = 20, REAL NAME = LSC_3V_GOURAUD_FLAT_SINGLE_FACE_NO_TEXTURED_TRANSLUCENT //// add it!!

    # 4 VERTEX POLY LIGHT SOURCE CALCULATION
    # TEXTURED
    lsc_4v_g_t = b'\x0c\x08\x00\x3c'    # GOURAUD TEXTURED - 8 row = 32
    lsc_4v_f_t = b'\x09\x07\x00\x2c'    # FLAT TEXTURED - 7 row = 28
    new_lsc_4v_g_t = b'\x0c\x08\x00\x3e' # NEW TYPE OF PACKET a 4 VERTEX GOURAUD TEXTURED - 8 row = 32
    new_lsc_4v_g_t_2 = b'\x0c\x08\x02\x3c' # NEW TYPE OF PACKET a 4 VERTEX GOURAUD TEXTURED 2 - 8 row = 32
    # NO TEXTURED
    lsc_4v_nt_g_s = b'\x08\x05\x00\x38' # GOURAUD SOLID - 5 row = 20
    lsc_4v_nt_f_s = b'\x05\x04\x00\x28' # FLAT SOLID - 4 row = 16
    lsc_4v_nt_g_g = b'\x08\x08\x04\x38' # GOURAUD GRADATION - 8 row = 32
    lsc_4v_nt_f_g = b'\x08\x07\x04\x28' # FLAT GRADATION - 7 row = 28
    new_lsc_4v_nt_g_s = b'\x08\x05\x00\x3a' # NEW 4 VERTEX GOURAUD SOLID NO TEXTURE - 5 row = 20
    new_lsc_4v_nt_g_g = b'\x08\x08\x04\x3a' # NEW 4 VERTEX GOURAUD GRADATION NO TEXTURE - 8 row = 32 REAL NAME = LSC_4V_GOURAUD_GRADATION_TRANSLUCENT_SINGLE_FACE

    #-------------------------------------------------------#
    #-------------------------------------------------------#

    # 3 VERTEX POLY NO LIGHT SOURCE CALCULATION
    # TEXTURED
    nlsc_3v_g_t = b'\x09\x08\x01\x35'   # GRADATION - 8 row = 32
    nlsc_3v_f_t = b'\x04\x03\x01\x21'   # FLAT - 3 row = 12
    new_nlsc_3v_g_t = b'\x09\x08\x01\x37' # NEW TYPE OF PACKET a 3 VERTEX GRADATION TEXTURED - 8 row = 32
    # NO TEXTURED
    nlsc_3v_nt_g = b'\x06\x05\x01\x31'  # GRADATION - 5 row = 20
    nlsc_3v_nt_f = b'\x04\x03\x01\x21'  # FLAT - 3 row = 12

    # 4 VERTEX POLY NO LIGHT SOURCE CALCULATION
    # TEXTURED
    nlsc_4v_g_t = b'\x0c\x0a\x01\x3d'   # GRADATION - 10 row = 40
    nlsc_4v_f_t = b'\x09\x07\x01\x2d'   # FLAT - 7 row = 28
    new_nlsc_4v_g_t = b'\x0c\x0a\x01\x3f' # NEW TYPE OF PACKET a 4 VERTEX GRADATION TEXTURED - 10 row = 40
    # NO TEXTURED
    nlsc_4v_nt_g = b'\x08\x06\x01\x39'  # GRADATION - 6 row = 24
    nlsc_4v_nt_f = b'\x05\x03\x01\x29'  # FLAT - 3 row = 12

    #-------------------------------------------------------#
                    # NOT IMPLEMENTED
    #-------------------------------------------------------#

    # STRAIGHT LINE
    sl_g_on = b'\x04\x03\x01\x50'
    sl_g_off = b'\x03\x02\x01\x40'

    #-------------------------------------------------------#
                    # NOT IMPLEMENTED
    #-------------------------------------------------------#

    # 3-DIMENSIONAL SPRITES
    td_spr_freesize = b'\x05\x03\x01\x64'
    td_spr_1x1 = b'\x04\x02\x01\x6c'
    td_spr_8x8 = b'\x04\x02\x01\x74'
    td_spr_16x16 = b'\x04\x02\x01\x7c'


class PrimitiveTmd:
    def __init__(self, prim_type):
        self.prim_type = prim_type
    
    #----------------------------------------------------- 3 Vertex (LSC - TEXTURED - NO TEXTURED) -----------------------------------------------------#

    def decoded_lsc3vgt(self):
        global lsc3vgt_obj
        lsc3vgt_obj = []
        lsc3vgt_index_block = []
        for lsc3vgt_match in standard_tmd_structure.primitive_block_byte:
            lsc3vgt_m = [m.start() for m in re.finditer(PrimitivePacketHeader.lsc_3v_g_t, lsc3vgt_match)]
            lsc3vgt_index_block.append(lsc3vgt_m)
        lsc3vgt_extraction = zip(lsc3vgt_index_block, standard_tmd_structure.primitive_block_byte)
            
        for index_num, lsc3vgt_block in lsc3vgt_extraction:
            lsc3vgt_in_obj = []
            for i_num in index_num:
                start_read = i_num
                end_read = i_num + 28
                lsc3vgt_extracted = lsc3vgt_block[start_read:end_read]
                # CONVERSION IN A SINGLE MOVE
                lsc3vgt = {"lsc3vgt":lsc3vgt_extracted[0:4], 
                           "u0":(int.from_bytes(lsc3vgt_extracted[4:5], byteorder='little') / 256), "v0":(int.from_bytes(lsc3vgt_extracted[5:6], byteorder='little') / 256), "cba":lsc3vgt_extracted[6:8], 
                           "u1":(int.from_bytes(lsc3vgt_extracted[8:9], byteorder='little') / 256), "v1":(int.from_bytes(lsc3vgt_extracted[9:10], byteorder='little') / 256), "tsb":lsc3vgt_extracted[10:12], 
                           "u2":(int.from_bytes(lsc3vgt_extracted[12:13], byteorder='little') / 256), "v2":(int.from_bytes(lsc3vgt_extracted[13:14], byteorder='little') / 256), "pad0":lsc3vgt_extracted[14:16], 
                           "normal0":int.from_bytes(lsc3vgt_extracted[16:18], byteorder='little'), "vertex0":int.from_bytes(lsc3vgt_extracted[18:20], byteorder='little'), 
                           "normal1":int.from_bytes(lsc3vgt_extracted[20:22], byteorder='little'), "vertex1":int.from_bytes(lsc3vgt_extracted[22:24], byteorder='little'), 
                           "normal2":int.from_bytes(lsc3vgt_extracted[24:26], byteorder='little'), "vertex2":int.from_bytes(lsc3vgt_extracted[26:28], byteorder='little')}
                lsc3vgt_in_obj.append(lsc3vgt)
            lsc3vgt_obj.append(lsc3vgt_in_obj)
    
    def decoded_lsc3vft(self):
        global lsc3vft_obj
        lsc3vft_obj = []
        lsc3vft_index_block = []
        for lsc3vft_match in standard_tmd_structure.primitive_block_byte:
            lsc3vft_m = [m.start() for m in re.finditer(PrimitivePacketHeader.lsc_3v_f_t, lsc3vft_match)]
            lsc3vft_index_block.append(lsc3vft_m)
        lsc3vft_extraction = zip(lsc3vft_index_block, standard_tmd_structure.primitive_block_byte)
        
        for index_num, lsc3vft_block in lsc3vft_extraction:
            lsc3vft_in_obj = []
            for i_num in index_num:
                start_read = i_num
                end_read = i_num + 24
                lsc3vft_extracted = lsc3vft_block[start_read:end_read]
                # CONVERSION IN A SINGLE MOVE
                lsc3vft = {"lsc3vft":lsc3vft_extracted[0:4], 
                           "u0":(int.from_bytes(lsc3vft_extracted[4:5], byteorder='little') / 256), "v0":(int.from_bytes(lsc3vft_extracted[5:6], byteorder='little') / 256), "cba":lsc3vft_extracted[6:8], 
                           "u1":(int.from_bytes(lsc3vft_extracted[8:9], byteorder='little') / 256), "v1":(int.from_bytes(lsc3vft_extracted[9:10], byteorder='little') / 256), "tsb":lsc3vft_extracted[10:12], 
                           "u2":(int.from_bytes(lsc3vft_extracted[12:13], byteorder='little') / 256), "v2":(int.from_bytes(lsc3vft_extracted[13:14], byteorder='little') / 256), "pad":lsc3vft_extracted[14:16], 
                           "normal0":int.from_bytes(lsc3vft_extracted[16:18], byteorder='little'), "vertex0":int.from_bytes(lsc3vft_extracted[18:20], byteorder='little'), 
                           "vertex1":int.from_bytes(lsc3vft_extracted[20:22], byteorder='little'), "vertex2":int.from_bytes(lsc3vft_extracted[22:24], byteorder='little')}
                lsc3vft_in_obj.append(lsc3vft)
            lsc3vft_obj.append(lsc3vft_in_obj)
    
    def decoded_new_lsc_3v_gt(self):
        global newlsc3vgt_obj
        newlsc3vgt_obj = []
        newlsc3vgt_index_block = []
        for newlsc3vgt_match in standard_tmd_structure.primitive_block_byte:
            newlsc3vgt_m = [m.start() for m in re.finditer(PrimitivePacketHeader.new_lsc_3v_gt, newlsc3vgt_match)]
            newlsc3vgt_index_block.append(newlsc3vgt_m)
        newlsc3vgt_extraction = zip(newlsc3vgt_index_block, standard_tmd_structure.primitive_block_byte)

        for index_num, newlsc3vgt_block in newlsc3vgt_extraction:
            newlsc3vgt_in_obj = []
            for i_num in index_num:
                start_read = i_num
                end_read = i_num + 28
                newlsc3vgt_extracted = newlsc3vgt_block[start_read:end_read]
                # CONVERSION IN A SINGLE MOVE
                newlsc3vgt = {"newlsc3vgt":newlsc3vgt_extracted[0:4], 
                           "u0":(int.from_bytes(newlsc3vgt_extracted[4:5], byteorder='little') / 256), "v0":(int.from_bytes(newlsc3vgt_extracted[5:6], byteorder='little') / 256), "cba":newlsc3vgt_extracted[6:8], 
                           "u1":(int.from_bytes(newlsc3vgt_extracted[8:9], byteorder='little') / 256), "v1":(int.from_bytes(newlsc3vgt_extracted[9:10], byteorder='little') / 256), "tsb":newlsc3vgt_extracted[10:12], 
                           "u2":(int.from_bytes(newlsc3vgt_extracted[12:13], byteorder='little') / 256), "v2":(int.from_bytes(newlsc3vgt_extracted[13:14], byteorder='little') / 256), "pad0":newlsc3vgt_extracted[14:16], 
                           "normal0":int.from_bytes(newlsc3vgt_extracted[16:18], byteorder='little'), "vertex0":int.from_bytes(newlsc3vgt_extracted[18:20], byteorder='little'), 
                           "normal1":int.from_bytes(newlsc3vgt_extracted[20:22], byteorder='little'), "vertex1":int.from_bytes(newlsc3vgt_extracted[22:24], byteorder='little'), 
                           "normal2":int.from_bytes(newlsc3vgt_extracted[24:26], byteorder='little'), "vertex2":int.from_bytes(newlsc3vgt_extracted[26:28], byteorder='little')}
                newlsc3vgt_in_obj.append(newlsc3vgt)
            newlsc3vgt_obj.append(newlsc3vgt_in_obj)
    
    def decoded_new_lsc_3v_gt_2(self):
        global newlsc3vgt2_obj
        newlsc3vgt2_obj = []
        newlsc3vgt2_index_block = []
        for newlsc3vgt2_match in standard_tmd_structure.primitive_block_byte:
            newlsc3vgt2_m = [m.start() for m in re.finditer(PrimitivePacketHeader.new_lsc_3v_gt_2, newlsc3vgt2_match)]
            newlsc3vgt2_index_block.append(newlsc3vgt2_m)
        newlsc3vgt2_extraction = zip(newlsc3vgt2_index_block, standard_tmd_structure.primitive_block_byte)

        for index_num, newlsc3vgt2_block in newlsc3vgt2_extraction:
            newlsc3vgt2_in_obj = []
            for i_num in index_num:
                start_read = i_num
                end_read = i_num + 28
                newlsc3vgt2_extracted = newlsc3vgt2_block[start_read:end_read]
                # CONVERSION IN A SINGLE MOVE
                newlsc3vgt2 = {"newlsc3vgt2":newlsc3vgt2_extracted[0:4], 
                           "u0":(int.from_bytes(newlsc3vgt2_extracted[4:5], byteorder='little') / 256), "v0":(int.from_bytes(newlsc3vgt2_extracted[5:6], byteorder='little') / 256), "cba":newlsc3vgt2_extracted[6:8], 
                           "u1":(int.from_bytes(newlsc3vgt2_extracted[8:9], byteorder='little') / 256), "v1":(int.from_bytes(newlsc3vgt2_extracted[9:10], byteorder='little') / 256), "tsb":newlsc3vgt2_extracted[10:12], 
                           "u2":(int.from_bytes(newlsc3vgt2_extracted[12:13], byteorder='little') / 256), "v2":(int.from_bytes(newlsc3vgt2_extracted[13:14], byteorder='little') / 256), "pad0":newlsc3vgt2_extracted[14:16], 
                           "normal0":int.from_bytes(newlsc3vgt2_extracted[16:18], byteorder='little'), "vertex0":int.from_bytes(newlsc3vgt2_extracted[18:20], byteorder='little'), 
                           "normal1":int.from_bytes(newlsc3vgt2_extracted[20:22], byteorder='little'), "vertex1":int.from_bytes(newlsc3vgt2_extracted[22:24], byteorder='little'), 
                           "normal2":int.from_bytes(newlsc3vgt2_extracted[24:26], byteorder='little'), "vertex2":int.from_bytes(newlsc3vgt2_extracted[26:28], byteorder='little')}
                newlsc3vgt2_in_obj.append(newlsc3vgt2)
            newlsc3vgt2_obj.append(newlsc3vgt2_in_obj)
    
    def decoded_lsc3vntgs(self):
        global lsc3vntgs_obj
        lsc3vntgs_obj = []
        lsc3vntgs_index_block = []
        for lsc3vntgs_match in standard_tmd_structure.primitive_block_byte:
            lsc3vntgs_m = [m.start() for m in re.finditer(PrimitivePacketHeader.lsc_3v_nt_g_s, lsc3vntgs_match)]
            lsc3vntgs_index_block.append(lsc3vntgs_m)
        lsc3vntgs_extraction = zip(lsc3vntgs_index_block, standard_tmd_structure.primitive_block_byte)

        for index_num, lsc3vntgs_block in lsc3vntgs_extraction:
            lsc3vntgs_in_obj = []
            for i_num in index_num:
                start_read = i_num
                end_read = i_num + 20
                lsc3vntgs_extracted = lsc3vntgs_block[start_read:end_read]
                # CONVERSION IN A SINGLE MOVE
                lsc3vntgs = {"lsc3vntgs":lsc3vntgs_extracted[0:4], 
                             "r0":int.from_bytes(lsc3vntgs_extracted[4:5], byteorder='little'), "g0":int.from_bytes(lsc3vntgs_extracted[5:6], byteorder='little'), "b0":int.from_bytes(lsc3vntgs_extracted[6:7], byteorder='little'), "pad0":lsc3vntgs_extracted[7:8], 
                             "normal0":int.from_bytes(lsc3vntgs_extracted[8:10], byteorder='little'), "vertex0":int.from_bytes(lsc3vntgs_extracted[10:12], byteorder='little'), 
                             "normal1":int.from_bytes(lsc3vntgs_extracted[12:14], byteorder='little'), "vertex1":int.from_bytes(lsc3vntgs_extracted[14:16], byteorder='little'), 
                             "normal2":int.from_bytes(lsc3vntgs_extracted[16:18], byteorder='little'), "vertex2":int.from_bytes(lsc3vntgs_extracted[18:20], byteorder='little')}
                lsc3vntgs_in_obj.append(lsc3vntgs)
            lsc3vntgs_obj.append(lsc3vntgs_in_obj)
    
    def decoded_lsc3vntfs(self):
        global lsc3vntfs_obj
        lsc3vntfs_obj = []
        lsc3vntfs_index_block = []
        for lsc3vntfs_match in standard_tmd_structure.primitive_block_byte:
            lsc3vntfs_m = [m.start() for m in re.finditer(PrimitivePacketHeader.lsc_3v_nt_f_s, lsc3vntfs_match)]
            lsc3vntfs_index_block.append(lsc3vntfs_m)
        lsc3vntfs_extraction = zip(lsc3vntfs_index_block, standard_tmd_structure.primitive_block_byte)

        for index_num, lsc3vntfs_block in lsc3vntfs_extraction:
            lsc3vntfs_in_obj = []
            for i_num in index_num:
                start_read = i_num
                end_read = i_num + 16
                lsc3vntfs_extracted = lsc3vntfs_block[start_read:end_read]
                # CONVERSION IN A SINGLE MOVE
                lsc3vntfs = {"lsc3vntfs":lsc3vntfs_extracted[0:4], 
                             "r0":int.from_bytes(lsc3vntfs_extracted[4:5], byteorder='little'), "g0":int.from_bytes(lsc3vntfs_extracted[5:6], byteorder='little'), "b0":int.from_bytes(lsc3vntfs_extracted[6:7], byteorder='little'), "pad0":lsc3vntfs_extracted[7:8], 
                             "normal0":int.from_bytes(lsc3vntfs_extracted[8:10], byteorder='little'), "vertex0":int.from_bytes(lsc3vntfs_extracted[10:12], byteorder='little'), 
                             "vertex1":int.from_bytes(lsc3vntfs_extracted[12:14], byteorder='little'), "vertex2":int.from_bytes(lsc3vntfs_extracted[14:16], byteorder='little')}
                lsc3vntfs_in_obj.append(lsc3vntfs)
            lsc3vntfs_obj.append(lsc3vntfs_in_obj)
    
    def decoded_lsc3vntgg(self):
        global lsc3vntgg_obj
        lsc3vntgg_obj = []
        lsc3vntgg_index_block = []
        for lsc3vntgg_match in standard_tmd_structure.primitive_block_byte:
            lsc3vntgg_m = [m.start() for m in re.finditer(PrimitivePacketHeader.lsc_3v_nt_g_g, lsc3vntgg_match)]
            lsc3vntgg_index_block.append(lsc3vntgg_m)
        lsc3vntgg_extraction = zip(lsc3vntgg_index_block, standard_tmd_structure.primitive_block_byte)

        for index_num, lsc3vntgg_block in lsc3vntgg_extraction:
            lsc3vntgg_in_obj = []
            for i_num in index_num:
                start_read = i_num
                end_read = i_num + 28
                lsc3vntgg_extracted = lsc3vntgg_block[start_read:end_read]
                # CONVERSION IN A SINGLE MOVE
                lsc3vntgg = {"lsc3vntgg":lsc3vntgg_extracted[0:4], 
                             "r0":int.from_bytes(lsc3vntgg_extracted[4:5], byteorder='little'), "g0":int.from_bytes(lsc3vntgg_extracted[5:6], byteorder='little'), "b0":int.from_bytes(lsc3vntgg_extracted[6:7], byteorder='little'), "pad0":lsc3vntgg_extracted[7:8], 
                             "r1":int.from_bytes(lsc3vntgg_extracted[8:9], byteorder='little'), "g1":int.from_bytes(lsc3vntgg_extracted[9:10], byteorder='little'), "b1":int.from_bytes(lsc3vntgg_extracted[10:11], byteorder='little'), "pad1":lsc3vntgg_extracted[11:12], 
                             "r2":int.from_bytes(lsc3vntgg_extracted[12:13], byteorder='little'), "g2":int.from_bytes(lsc3vntgg_extracted[13:14], byteorder='little'), "b2":int.from_bytes(lsc3vntgg_extracted[14:15], byteorder='little'), "pad2":lsc3vntgg_extracted[15:16], 
                             "normal0":int.from_bytes(lsc3vntgg_extracted[16:18], byteorder='little'), "vertex0":int.from_bytes(lsc3vntgg_extracted[18:20], byteorder='little'), 
                             "normal1":int.from_bytes(lsc3vntgg_extracted[20:22], byteorder='little'), "vertex1":int.from_bytes(lsc3vntgg_extracted[22:24], byteorder='little'), 
                             "normal2":int.from_bytes(lsc3vntgg_extracted[24:26], byteorder='little'), "vertex2":int.from_bytes(lsc3vntgg_extracted[26:28], byteorder='little')}
                lsc3vntgg_in_obj.append(lsc3vntgg)
            lsc3vntgg_obj.append(lsc3vntgg_in_obj)

    def decoded_lsc3vntfg(self):
        global lsc3vntfg_obj
        lsc3vntfg_obj = []
        lsc3vntfg_index_block = []
        for lsc3vntfg_match in standard_tmd_structure.primitive_block_byte:
            lsc3vntfg_m = [m.start() for m in re.finditer(PrimitivePacketHeader.lsc_3v_nt_f_g, lsc3vntfg_match)]
            lsc3vntfg_index_block.append(lsc3vntfg_m)
        lsc3vntfg_extraction = zip(lsc3vntfg_index_block, standard_tmd_structure.primitive_block_byte)

        for index_num, lsc3vntfg_block in lsc3vntfg_extraction:
            lsc3vntfg_in_obj = []
            for i_num in index_num:
                start_read = i_num
                end_read = i_num + 24
                lsc3vntfg_extracted = lsc3vntfg_block[start_read:end_read]
                # CONVERSION IN A SINGLE MOVE
                lsc3vntfg = {"lsc3vntfg":lsc3vntfg_extracted[0:4], 
                             "r0":int.from_bytes(lsc3vntfg_extracted[4:5], byteorder='little'), "g0":int.from_bytes(lsc3vntfg_extracted[5:6], byteorder='little'), "b0":int.from_bytes(lsc3vntfg_extracted[6:7], byteorder='little'), "pad0":lsc3vntfg_extracted[7:8], 
                             "r1":int.from_bytes(lsc3vntfg_extracted[8:9], byteorder='little'), "g1":int.from_bytes(lsc3vntfg_extracted[9:10], byteorder='little'), "b1":int.from_bytes(lsc3vntfg_extracted[10:11], byteorder='little'), "pad1":lsc3vntfg_extracted[11:12], 
                             "r2":int.from_bytes(lsc3vntfg_extracted[12:13], byteorder='little'), "g2":int.from_bytes(lsc3vntfg_extracted[13:14], byteorder='little'), "b1":int.from_bytes(lsc3vntfg_extracted[14:15], byteorder='little'), "pad2":lsc3vntfg_extracted[15:16], 
                             "normal0":int.from_bytes(lsc3vntfg_extracted[16:18], byteorder='little'), "vertex0":int.from_bytes(lsc3vntfg_extracted[18:20], byteorder='little'), 
                             "vertex1":int.from_bytes(lsc3vntfg_extracted[20:22], byteorder='little'), "vertex2":int.from_bytes(lsc3vntfg_extracted[22:24], byteorder='little')}
                lsc3vntfg_in_obj.append(lsc3vntfg)
            lsc3vntfg_obj.append(lsc3vntfg_in_obj)
    
    def decoded_new_lsc_3v_nt_gg(self):
        global newlsc3vntgg_obj
        newlsc3vntgg_obj = []
        newlsc3vntgg_index_block = []
        for newlsc3vntgg_match in standard_tmd_structure.primitive_block_byte:
            newlsc3vntgg_m = [m.start() for m in re.finditer(PrimitivePacketHeader.new_lsc_3v_nt_gg, newlsc3vntgg_match)]
            newlsc3vntgg_index_block.append(newlsc3vntgg_m)
        newlsc3vntgg_extraction = zip(newlsc3vntgg_index_block, standard_tmd_structure.primitive_block_byte)

        for index_num, newlsc3vntgg_block in newlsc3vntgg_extraction:
            newlsc3vntgg_in_obj = []
            for i_num in index_num:
                start_read = i_num
                end_read = i_num + 28
                newlsc3vntgg_extracted = newlsc3vntgg_block[start_read:end_read]
                # CONVERSION IN A SINGLE MOVE
                newlsc3vntgg = {"newlsc3vntgg":newlsc3vntgg_extracted[0:4], 
                             "r0":int.from_bytes(newlsc3vntgg_extracted[4:5], byteorder='little'), "g0":int.from_bytes(newlsc3vntgg_extracted[5:6], byteorder='little'), "b0":int.from_bytes(newlsc3vntgg_extracted[6:7], byteorder='little'), "pad0":newlsc3vntgg_extracted[7:8], 
                             "r1":int.from_bytes(newlsc3vntgg_extracted[8:9], byteorder='little'), "g1":int.from_bytes(newlsc3vntgg_extracted[9:10], byteorder='little'), "b1":int.from_bytes(newlsc3vntgg_extracted[10:11], byteorder='little'), "pad1":newlsc3vntgg_extracted[11:12], 
                             "r2":int.from_bytes(newlsc3vntgg_extracted[12:13], byteorder='little'), "g2":int.from_bytes(newlsc3vntgg_extracted[13:14], byteorder='little'), "b2":int.from_bytes(newlsc3vntgg_extracted[14:15], byteorder='little'), "pad2":newlsc3vntgg_extracted[15:16], 
                             "normal0":int.from_bytes(newlsc3vntgg_extracted[16:18], byteorder='little'), "vertex0":int.from_bytes(newlsc3vntgg_extracted[18:20], byteorder='little'), 
                             "normal1":int.from_bytes(newlsc3vntgg_extracted[20:22], byteorder='little'), "vertex1":int.from_bytes(newlsc3vntgg_extracted[22:24], byteorder='little'), 
                             "normal2":int.from_bytes(newlsc3vntgg_extracted[24:26], byteorder='little'), "vertex2":int.from_bytes(newlsc3vntgg_extracted[26:28], byteorder='little')}
                newlsc3vntgg_in_obj.append(newlsc3vntgg)
            newlsc3vntgg_obj.append(newlsc3vntgg_in_obj)
    
    def decoded_new_lsc_3v_nt_fg(self):
        global newlsc3vntfg_obj
        newlsc3vntfg_obj = []
        newlsc3vntfg_index_block = []
        for newlsc3vntfg_match in standard_tmd_structure.primitive_block_byte:
            newlsc3vntfg_m = [m.start() for m in re.finditer(PrimitivePacketHeader.new_lsc_3v_nt_fg, newlsc3vntfg_match)]
            newlsc3vntfg_index_block.append(newlsc3vntfg_m)
        newlsc3vntfg_extraction = zip(newlsc3vntfg_index_block, standard_tmd_structure.primitive_block_byte)

        for index_num, newlsc3vntfg_block in newlsc3vntfg_extraction:
            newlsc3vntfg_in_obj = []
            for i_num in index_num:
                start_read = i_num
                end_read = i_num + 20
                newlsc3vntfg_extracted = newlsc3vntfg_block[start_read:end_read]
                # CONVERSION IN A SINGLE MOVE
                newlsc3vntfg = {"newlsc3vntfg":newlsc3vntfg_extracted[0:4], 
                             "r0":int.from_bytes(newlsc3vntfg_extracted[4:5], byteorder='little'), "g0":int.from_bytes(newlsc3vntfg_extracted[5:6], byteorder='little'), "b0":int.from_bytes(newlsc3vntfg_extracted[6:7], byteorder='little'), "pad0":newlsc3vntfg_extracted[7:8], 
                             "normal0":int.from_bytes(newlsc3vntfg_extracted[8:10], byteorder='little'), "vertex0":int.from_bytes(newlsc3vntfg_extracted[10:12], byteorder='little'), 
                             "normal1":int.from_bytes(newlsc3vntfg_extracted[12:14], byteorder='little'), "vertex1":int.from_bytes(newlsc3vntfg_extracted[14:16], byteorder='little'),
                             "normal2":int.from_bytes(newlsc3vntfg_extracted[16:18], byteorder='little'), "vertex2":int.from_bytes(newlsc3vntfg_extracted[18:20], byteorder='little')}
                newlsc3vntfg_in_obj.append(newlsc3vntfg)
            newlsc3vntfg_obj.append(newlsc3vntfg_in_obj)

    #----------------------------------------------------- 4 Vertex (LSC - TEXTURED - NO TEXTURED) -----------------------------------------------------#

    def decoded_lsc4vgt(self):
        global lsc4vgt_obj
        lsc4vgt_obj = []
        lsc4vgt_index_block = []
        for lsc4vgt_match in standard_tmd_structure.primitive_block_byte:
            lsc4vgt_m = [m.start() for m in re.finditer(PrimitivePacketHeader.lsc_4v_g_t, lsc4vgt_match)]
            lsc4vgt_index_block.append(lsc4vgt_m)
        lsc4vgt_extraction = zip(lsc4vgt_index_block, standard_tmd_structure.primitive_block_byte)

        for index_num, lsc4vgt_block in lsc4vgt_extraction:
            lsc4vgt_in_obj = []
            for i_num in index_num:
                start_read = i_num
                end_read = i_num + 36
                lsc4vgt_extracted = lsc4vgt_block[start_read:end_read]
                # CONVERSION IN A SINGLE MOVE
                lsc4vgt = {"lsc4vgt":lsc4vgt_extracted[0:4], 
                           "u0":(int.from_bytes(lsc4vgt_extracted[4:5], byteorder='little') / 256), "v0":(int.from_bytes(lsc4vgt_extracted[5:6], byteorder='little') / 256), "cba":lsc4vgt_extracted[6:8], 
                           "u1":(int.from_bytes(lsc4vgt_extracted[8:9], byteorder='little') / 256), "v1":(int.from_bytes(lsc4vgt_extracted[9:10], byteorder='little') / 256), "tsb":lsc4vgt_extracted[10:12], 
                           "u2":(int.from_bytes(lsc4vgt_extracted[12:13], byteorder='little') / 256), "v2":(int.from_bytes(lsc4vgt_extracted[13:14], byteorder='little') / 256), "pad0":lsc4vgt_extracted[14:16], 
                           "u3":(int.from_bytes(lsc4vgt_extracted[16:17], byteorder='little') / 256), "v3":(int.from_bytes(lsc4vgt_extracted[17:18], byteorder='little') / 256), "pad1":lsc4vgt_extracted[18:20], 
                           "normal0":int.from_bytes(lsc4vgt_extracted[20:22], byteorder='little'), "vertex0":int.from_bytes(lsc4vgt_extracted[22:24], byteorder='little'), 
                           "normal1":int.from_bytes(lsc4vgt_extracted[24:26], byteorder='little'), "vertex1":int.from_bytes(lsc4vgt_extracted[26:28], byteorder='little'), 
                           "normal2":int.from_bytes(lsc4vgt_extracted[28:30], byteorder='little'), "vertex2":int.from_bytes(lsc4vgt_extracted[30:32], byteorder='little'), 
                           "normal3":int.from_bytes(lsc4vgt_extracted[32:34], byteorder='little'), "vertex3":int.from_bytes(lsc4vgt_extracted[34:36], byteorder='little')}
                lsc4vgt_in_obj.append(lsc4vgt)
            lsc4vgt_obj.append(lsc4vgt_in_obj)
    
    def decoded_lsc4vft(self):
        global lsc4vft_obj
        lsc4vft_obj = []
        lsc4vft_index_block = []
        for lsc4vft_match in standard_tmd_structure.primitive_block_byte:
            lsc4vft_m = [m.start() for m in re.finditer(PrimitivePacketHeader.lsc_4v_f_t, lsc4vft_match)]
            lsc4vft_index_block.append(lsc4vft_m)
        lsc4vft_extraction = zip(lsc4vft_index_block, standard_tmd_structure.primitive_block_byte)

        for index_num, lsc4vft_block in lsc4vft_extraction:
            lsc4vft_in_obj = []
            for i_num in index_num:
                start_read = i_num
                end_read = i_num + 32
                lsc4vft_extracted = lsc4vft_block[start_read:end_read]
                # CONVERSION IN A SINGLE MOVE
                lsc4vft = {"lsc4vft":lsc4vft_extracted[0:4], 
                           "u0":(int.from_bytes(lsc4vft_extracted[4:5], byteorder='little') / 256), "v0":(int.from_bytes(lsc4vft_extracted[5:6], byteorder='little') / 256), "cba":lsc4vft_extracted[6:8],
                           "u1":(int.from_bytes(lsc4vft_extracted[8:9], byteorder='little') / 256), "v1":(int.from_bytes(lsc4vft_extracted[9:10], byteorder='little') / 256), "tsb":lsc4vft_extracted[10:12],
                           "u2":(int.from_bytes(lsc4vft_extracted[12:13], byteorder='little') / 256), "v2":(int.from_bytes(lsc4vft_extracted[13:14], byteorder='little') / 256), "pad0":lsc4vft_extracted[14:16], 
                           "u3":(int.from_bytes(lsc4vft_extracted[16:17], byteorder='little') / 256), "v3":(int.from_bytes(lsc4vft_extracted[17:18], byteorder='little') / 256), "pad1":lsc4vft_extracted[18:20],
                           "normal0":int.from_bytes(lsc4vft_extracted[20:22], byteorder='little'), "vertex0":int.from_bytes(lsc4vft_extracted[22:24], byteorder='little'), 
                           "vertex1":int.from_bytes(lsc4vft_extracted[24:26], byteorder='little'), "vertex2":int.from_bytes(lsc4vft_extracted[26:28], byteorder='little'), 
                           "vertex3":int.from_bytes(lsc4vft_extracted[28:30], byteorder='little'), "pad2":lsc4vft_extracted[30:32]}
                lsc4vft_in_obj.append(lsc4vft)
            lsc4vft_obj.append(lsc4vft_in_obj)
    
    def decoded_new_lsc_4v_g_t(self):
        global newlsc4vgt_obj
        newlsc4vgt_obj = []
        newlsc4vgt_index_block = []
        for newlsc4vgt_match in standard_tmd_structure.primitive_block_byte:
            newlsc4vgt_m = [m.start() for m in re.finditer(PrimitivePacketHeader.new_lsc_4v_g_t, newlsc4vgt_match)]
            newlsc4vgt_index_block.append(newlsc4vgt_m)
        newlsc4vgt_extraction = zip(newlsc4vgt_index_block, standard_tmd_structure.primitive_block_byte)

        for index_num, newlsc4vgt_block in newlsc4vgt_extraction:
            newlsc4vgt_in_obj = []
            for i_num in index_num:
                start_read = i_num
                end_read = i_num + 36
                newlsc4vgt_extracted = newlsc4vgt_block[start_read:end_read]
                # CONVERSION IN A SINGLE MOVE
                newlsc4vgt = {"newlsc4vgt":newlsc4vgt_extracted[0:4], 
                           "u0":(int.from_bytes(newlsc4vgt_extracted[4:5], byteorder='little') / 256), "v0":(int.from_bytes(newlsc4vgt_extracted[5:6], byteorder='little') / 256), "cba":newlsc4vgt_extracted[6:8], 
                           "u1":(int.from_bytes(newlsc4vgt_extracted[8:9], byteorder='little') / 256), "v1":(int.from_bytes(newlsc4vgt_extracted[9:10], byteorder='little') / 256), "tsb":newlsc4vgt_extracted[10:12], 
                           "u2":(int.from_bytes(newlsc4vgt_extracted[12:13], byteorder='little') / 256), "v2":(int.from_bytes(newlsc4vgt_extracted[13:14], byteorder='little') / 256), "pad0":newlsc4vgt_extracted[14:16], 
                           "u3":(int.from_bytes(newlsc4vgt_extracted[16:17], byteorder='little') / 256), "v3":(int.from_bytes(newlsc4vgt_extracted[17:18], byteorder='little') / 256), "pad1":newlsc4vgt_extracted[18:20], 
                           "normal0":int.from_bytes(newlsc4vgt_extracted[20:22], byteorder='little'), "vertex0":int.from_bytes(newlsc4vgt_extracted[22:24], byteorder='little'), 
                           "normal1":int.from_bytes(newlsc4vgt_extracted[24:26], byteorder='little'), "vertex1":int.from_bytes(newlsc4vgt_extracted[26:28], byteorder='little'), 
                           "normal2":int.from_bytes(newlsc4vgt_extracted[28:30], byteorder='little'), "vertex2":int.from_bytes(newlsc4vgt_extracted[30:32], byteorder='little'), 
                           "normal3":int.from_bytes(newlsc4vgt_extracted[32:34], byteorder='little'), "vertex3":int.from_bytes(newlsc4vgt_extracted[34:36], byteorder='little')}
                newlsc4vgt_in_obj.append(newlsc4vgt)
            newlsc4vgt_obj.append(newlsc4vgt_in_obj)
    
    def decoded_new_lsc_4v_g_t_2(self):
        global newlsc4vgt2_obj
        newlsc4vgt2_obj = []
        newlsc4vgt2_index_block = []
        for newlsc4vgt2_match in standard_tmd_structure.primitive_block_byte:
            newlsc4vgt2_m = [m.start() for m in re.finditer(PrimitivePacketHeader.new_lsc_4v_g_t_2, newlsc4vgt2_match)]
            newlsc4vgt2_index_block.append(newlsc4vgt2_m)
        newlsc4vgt2_extraction = zip(newlsc4vgt2_index_block, standard_tmd_structure.primitive_block_byte)

        for index_num, newlsc4vgt2_block in newlsc4vgt2_extraction:
            newlsc4vgt2_in_obj = []
            for i_num in index_num:
                start_read = i_num
                end_read = i_num + 36
                newlsc4vgt2_extracted = newlsc4vgt2_block[start_read:end_read]
                # CONVERSION IN A SINGLE MOVE
                newlsc4vgt2 = {"newlsc4vgt2":newlsc4vgt2_extracted[0:4], 
                           "u0":(int.from_bytes(newlsc4vgt2_extracted[4:5], byteorder='little') / 256), "v0":(int.from_bytes(newlsc4vgt2_extracted[5:6], byteorder='little') / 256), "cba":newlsc4vgt2_extracted[6:8], 
                           "u1":(int.from_bytes(newlsc4vgt2_extracted[8:9], byteorder='little') / 256), "v1":(int.from_bytes(newlsc4vgt2_extracted[9:10], byteorder='little') / 256), "tsb":newlsc4vgt2_extracted[10:12], 
                           "u2":(int.from_bytes(newlsc4vgt2_extracted[12:13], byteorder='little') / 256), "v2":(int.from_bytes(newlsc4vgt2_extracted[13:14], byteorder='little') / 256), "pad0":newlsc4vgt2_extracted[14:16], 
                           "u3":(int.from_bytes(newlsc4vgt2_extracted[16:17], byteorder='little') / 256), "v3":(int.from_bytes(newlsc4vgt2_extracted[17:18], byteorder='little') / 256), "pad1":newlsc4vgt2_extracted[18:20], 
                           "normal0":int.from_bytes(newlsc4vgt2_extracted[20:22], byteorder='little'), "vertex0":int.from_bytes(newlsc4vgt2_extracted[22:24], byteorder='little'), 
                           "normal1":int.from_bytes(newlsc4vgt2_extracted[24:26], byteorder='little'), "vertex1":int.from_bytes(newlsc4vgt2_extracted[26:28], byteorder='little'), 
                           "normal2":int.from_bytes(newlsc4vgt2_extracted[28:30], byteorder='little'), "vertex2":int.from_bytes(newlsc4vgt2_extracted[30:32], byteorder='little'), 
                           "normal3":int.from_bytes(newlsc4vgt2_extracted[32:34], byteorder='little'), "vertex3":int.from_bytes(newlsc4vgt2_extracted[34:36], byteorder='little')}
                newlsc4vgt2_in_obj.append(newlsc4vgt2)
            newlsc4vgt2_obj.append(newlsc4vgt2_in_obj)
    
    def decoded_lsc4vntgs(self):
        global lsc4vntgs_obj
        lsc4vntgs_obj = []
        lsc4vntgs_index_block = []
        for lsc4vntgs_match in standard_tmd_structure.primitive_block_byte:
            lsc4vntgs_m = [m.start() for m in re.finditer(PrimitivePacketHeader.lsc_4v_nt_g_s, lsc4vntgs_match)]
            lsc4vntgs_index_block.append(lsc4vntgs_m)
        lsc4vntgs_extraction = zip(lsc4vntgs_index_block, standard_tmd_structure.primitive_block_byte)

        for index_num, lsc4vntgs_block in lsc4vntgs_extraction:
            lsc4vntgs_in_object = []
            for i_num in index_num:
                start_read = i_num
                end_read = i_num + 24
                lsc4vntgs_extracted = lsc4vntgs_block[start_read:end_read]
                # CONVERSION IN A SINGLE MOVE
                lsc4vntgs = {"lsc4vntgs":lsc4vntgs_extracted[0:4], 
                             "r0":int.from_bytes(lsc4vntgs_extracted[4:5], byteorder='little'), "g0":int.from_bytes(lsc4vntgs_extracted[5:6], byteorder='little'), "b0":int.from_bytes(lsc4vntgs_extracted[6:7], byteorder='little'), "pad0":int.from_bytes(lsc4vntgs_extracted[7:8], byteorder='little'), 
                             "normal0":int.from_bytes(lsc4vntgs_extracted[8:10], byteorder='little'), "vertex0":int.from_bytes(lsc4vntgs_extracted[10:12], byteorder='little'), 
                             "normal1":int.from_bytes(lsc4vntgs_extracted[12:14], byteorder='little'), "vertex1":int.from_bytes(lsc4vntgs_extracted[14:16], byteorder='little'), 
                             "normal2":int.from_bytes(lsc4vntgs_extracted[16:18], byteorder='little'), "vertex2":int.from_bytes(lsc4vntgs_extracted[18:20], byteorder='little'), 
                             "normal3":int.from_bytes(lsc4vntgs_extracted[20:22], byteorder='little'), "vertex3":int.from_bytes(lsc4vntgs_extracted[22:24], byteorder='little')}
                lsc4vntgs_in_object.append(lsc4vntgs)
            lsc4vntgs_obj.append(lsc4vntgs_in_object)
    
    def decoded_lsc4vntfs(self):
        global lsc4vntfs_obj
        lsc4vntfs_obj = []
        lsc4vntfs_index_block = []
        for lsc4vntfs_match in standard_tmd_structure.primitive_block_byte:
            lsc4vntfs_m = [m.start() for m in re.finditer(re.escape(PrimitivePacketHeader.lsc_4v_nt_f_s), lsc4vntfs_match)]
            lsc4vntfs_index_block.append(lsc4vntfs_m)
        lsc4vntfs_extraction = zip(lsc4vntfs_index_block, standard_tmd_structure.primitive_block_byte)

        for index_num, lsc4vntfs_block in lsc4vntfs_extraction:
            lsc4vntfs_in_obj = []
            for i_num in index_num:
                start_read = i_num
                end_read = i_num + 20
                lsc4vntfs_extracted = lsc4vntfs_block[start_read:end_read]
                # CONVERSION IN A SINGLE MOVE
                lsc4vntfs = {"lsc4vntfs":lsc4vntfs_extracted[0:4], 
                             "r0":int.from_bytes(lsc4vntfs_extracted[4:5], byteorder='little'), "g0":int.from_bytes(lsc4vntfs_extracted[5:6], byteorder='little'), "b0":int.from_bytes(lsc4vntfs_extracted[6:7], byteorder='little'), "pad0":lsc4vntfs_extracted[7:8], 
                             "normal0":int.from_bytes(lsc4vntfs_extracted[8:10], byteorder='little'), "vertex0":int.from_bytes(lsc4vntfs_extracted[10:12], byteorder='little'), 
                             "vertex1":int.from_bytes(lsc4vntfs_extracted[12:14], byteorder='little'), "vertex2":int.from_bytes(lsc4vntfs_extracted[14:16], byteorder='little'), 
                             "vertex3":int.from_bytes(lsc4vntfs_extracted[16:18], byteorder='little'), "pad1":lsc4vntfs_extracted[18:20]}
                lsc4vntfs_in_obj.append(lsc4vntfs)
            lsc4vntfs_obj.append(lsc4vntfs_in_obj)
    
    def decoded_lsc4vntgg(self):
        global lsc4vntgg_obj
        lsc4vntgg_obj = []
        lsc4vntgg_index_block = []
        for lsc4vntgg_match in standard_tmd_structure.primitive_block_byte:
            lsc4vntgg_m = [m.start() for m in re.finditer(PrimitivePacketHeader.lsc_4v_nt_g_g, lsc4vntgg_match)]
            lsc4vntgg_index_block.append(lsc4vntgg_m)
        lsc4vntgg_extraction = zip(lsc4vntgg_index_block, standard_tmd_structure.primitive_block_byte)

        for index_num, lsc4vntgg_block in lsc4vntgg_extraction:
            lsc4vntgg_in_obj = []
            for i_num in index_num:
                start_read = i_num
                end_read = i_num + 36
                lsc4vntgg_extracted = lsc4vntgg_block[start_read:end_read]
                # CONVERSION IN A SINGLE MOVE
                lsc4vntgg = {"lsc4vntgg":lsc4vntgg_extracted[0:4], 
                             "r0":int.from_bytes(lsc4vntgg_extracted[4:5], byteorder='little'), "g0":int.from_bytes(lsc4vntgg_extracted[5:6], byteorder='little'), "b0":int.from_bytes(lsc4vntgg_extracted[6:7], byteorder='little'), "pad0":lsc4vntgg_extracted[7:8], 
                             "r1":int.from_bytes(lsc4vntgg_extracted[8:9], byteorder='little'), "g1":int.from_bytes(lsc4vntgg_extracted[9:10], byteorder='little'), "b1":int.from_bytes(lsc4vntgg_extracted[10:11], byteorder='little'), "pad1":lsc4vntgg_extracted[11:12], 
                             "r2":int.from_bytes(lsc4vntgg_extracted[12:13], byteorder='little'), "g2":int.from_bytes(lsc4vntgg_extracted[13:14], byteorder='little'), "b2":int.from_bytes(lsc4vntgg_extracted[14:15], byteorder='little'), "pad2":lsc4vntgg_extracted[15:16], 
                             "r3":int.from_bytes(lsc4vntgg_extracted[16:17], byteorder='little'), "g3":int.from_bytes(lsc4vntgg_extracted[17:18], byteorder='little'), "b3":int.from_bytes(lsc4vntgg_extracted[18:19], byteorder='little'), "pad3":lsc4vntgg_extracted[19:20], 
                             "normal0":int.from_bytes(lsc4vntgg_extracted[20:22], byteorder='little'), "vertex0":int.from_bytes(lsc4vntgg_extracted[22:24], byteorder='little'), 
                             "normal1":int.from_bytes(lsc4vntgg_extracted[24:26], byteorder='little'), "vertex1":int.from_bytes(lsc4vntgg_extracted[26:28], byteorder='little'), 
                             "normal2":int.from_bytes(lsc4vntgg_extracted[28:30], byteorder='little'), "vertex2":int.from_bytes(lsc4vntgg_extracted[30:32], byteorder='little'), 
                             "normal3":int.from_bytes(lsc4vntgg_extracted[32:34], byteorder='little'), "vertex3":int.from_bytes(lsc4vntgg_extracted[34:36], byteorder='little')}
                lsc4vntgg_in_obj.append(lsc4vntgg)
            lsc4vntgg_obj.append(lsc4vntgg_in_obj)
    
    def decoded_lsc4vntfg(self):
        global lsc4vntfg_obj
        lsc4vntfg_obj = []
        lsc4vntfg_index_block = []
        for lsc4vntfg_match in standard_tmd_structure.primitive_block_byte:
            lsc4vntfg_m = [m.start() for m in re.finditer(re.escape(PrimitivePacketHeader.lsc_4v_nt_f_g), lsc4vntfg_match)]
            lsc4vntfg_index_block.append(lsc4vntfg_m)
        lsc4vntfg_extraction = zip(lsc4vntfg_index_block, standard_tmd_structure.primitive_block_byte)

        for index_num, lsc4vntfg_block in lsc4vntfg_extraction:
            lsc4vntfg_in_obj = []
            for i_num in index_num:
                start_read = i_num
                end_read = i_num + 32
                lsc4vntfg_extracted = lsc4vntfg_block[start_read:end_read]
                # CONVERSION IN A SINGLE MOVE
                lsc4vntfg = {"lsc4vntfg":lsc4vntfg_extracted[0:4], 
                             "r0":int.from_bytes(lsc4vntfg_extracted[4:5]), "g0":int.from_bytes(lsc4vntfg_extracted[5:6]), "b0":int.from_bytes(lsc4vntfg_extracted[6:7]), "pad0":lsc4vntfg_extracted[7:8], 
                             "r1":int.from_bytes(lsc4vntfg_extracted[8:9]), "g1":int.from_bytes(lsc4vntfg_extracted[9:10]), "b1":int.from_bytes(lsc4vntfg_extracted[10:11]), "pad1":lsc4vntfg_extracted[11:12], 
                             "r2":int.from_bytes(lsc4vntfg_extracted[12:13]), "g2":int.from_bytes(lsc4vntfg_extracted[13:14]), "b2":int.from_bytes(lsc4vntfg_extracted[14:15]), "pad2":lsc4vntfg_extracted[15:16], 
                             "r3":int.from_bytes(lsc4vntfg_extracted[16:17]), "g3":int.from_bytes(lsc4vntfg_extracted[17:18]), "b3":int.from_bytes(lsc4vntfg_extracted[18:19]), "pad3":lsc4vntfg_extracted[19:20], 
                             "normal0":int.from_bytes(lsc4vntfg_extracted[20:22]), "vertex0":int.from_bytes(lsc4vntfg_extracted[22:24]),
                             "vertex1":int.from_bytes(lsc4vntfg_extracted[24:26]), "vertex2":int.from_bytes(lsc4vntfg_extracted[26:28]), 
                             "vertex3":int.from_bytes(lsc4vntfg_extracted[28:30]), "pad4":lsc4vntfg_extracted[30:32]}
                lsc4vntfg_in_obj.append(lsc4vntfg)
            lsc4vntfg_obj.append(lsc4vntfg_in_obj)
    
    def decoded_new_lsc_4v_nt_g_s(self):
        global newlsc4vntgs_obj
        newlsc4vntgs_obj = []
        newlsc4vntgs_index_block = []
        for newlsc4vntgs_match in standard_tmd_structure.primitive_block_byte:
            newlsc4vntgs_m = [m.start() for m in re.finditer(PrimitivePacketHeader.new_lsc_4v_nt_g_s, newlsc4vntgs_match)]
            newlsc4vntgs_index_block.append(newlsc4vntgs_m)
        newlsc4vntgs_extraction = zip(newlsc4vntgs_index_block, standard_tmd_structure.primitive_block_byte)

        for index_num, newlsc4vntgs_block in newlsc4vntgs_extraction:
            newlsc4vntgs_in_object = []
            for i_num in index_num:
                start_read = i_num
                end_read = i_num + 24
                newlsc4vntgs_extracted = newlsc4vntgs_block[start_read:end_read]
                # CONVERSION IN A SINGLE MOVE
                newlsc4vntgs = {"newlsc4vntgs":newlsc4vntgs_extracted[0:4], 
                             "r0":int.from_bytes(newlsc4vntgs_extracted[4:5], byteorder='little'), "g0":int.from_bytes(newlsc4vntgs_extracted[5:6], byteorder='little'), "b0":int.from_bytes(newlsc4vntgs_extracted[6:7], byteorder='little'), "pad0":int.from_bytes(newlsc4vntgs_extracted[7:8], byteorder='little'), 
                             "normal0":int.from_bytes(newlsc4vntgs_extracted[8:10], byteorder='little'), "vertex0":int.from_bytes(newlsc4vntgs_extracted[10:12], byteorder='little'), 
                             "normal1":int.from_bytes(newlsc4vntgs_extracted[12:14], byteorder='little'), "vertex1":int.from_bytes(newlsc4vntgs_extracted[14:16], byteorder='little'), 
                             "normal2":int.from_bytes(newlsc4vntgs_extracted[16:18], byteorder='little'), "vertex2":int.from_bytes(newlsc4vntgs_extracted[18:20], byteorder='little'), 
                             "normal3":int.from_bytes(newlsc4vntgs_extracted[20:22], byteorder='little'), "vertex3":int.from_bytes(newlsc4vntgs_extracted[22:24], byteorder='little')}
                newlsc4vntgs_in_object.append(newlsc4vntgs)
            newlsc4vntgs_obj.append(newlsc4vntgs_in_object)
    
    def decoded_new_lsc_4v_nt_gg(self):
        global newlsc4vntgg_obj
        newlsc4vntgg_obj = []
        newlsc4vntgg_index_block = []
        for newlsc4vntgg_match in standard_tmd_structure.primitive_block_byte:
            newlsc4vntgg_m = [m.start() for m in re.finditer(PrimitivePacketHeader.new_lsc_4v_nt_g_g, newlsc4vntgg_match)]
            newlsc4vntgg_index_block.append(newlsc4vntgg_m)
        newlsc4vntgg_extraction = zip(newlsc4vntgg_index_block, standard_tmd_structure.primitive_block_byte)

        for index_num, newlsc4vntgg_block in newlsc4vntgg_extraction:
            newlsc4vntgg_in_obj = []
            for i_num in index_num:
                start_read = i_num
                end_read = i_num + 36
                newlsc4vntgg_extracted = newlsc4vntgg_block[start_read:end_read]
                # CONVERSION IN A SINGLE MOVE
                newlsc4vntgg = {"newlsc4vntgg":newlsc4vntgg_extracted[0:4], 
                             "r0":int.from_bytes(newlsc4vntgg_extracted[4:5], byteorder='little'), "g0":int.from_bytes(newlsc4vntgg_extracted[5:6], byteorder='little'), "b0":int.from_bytes(newlsc4vntgg_extracted[6:7], byteorder='little'), "pad0":newlsc4vntgg_extracted[7:8], 
                             "r1":int.from_bytes(newlsc4vntgg_extracted[8:9], byteorder='little'), "g1":int.from_bytes(newlsc4vntgg_extracted[9:10], byteorder='little'), "b1":int.from_bytes(newlsc4vntgg_extracted[10:11], byteorder='little'), "pad1":newlsc4vntgg_extracted[11:12], 
                             "r2":int.from_bytes(newlsc4vntgg_extracted[12:13], byteorder='little'), "g2":int.from_bytes(newlsc4vntgg_extracted[13:14], byteorder='little'), "b2":int.from_bytes(newlsc4vntgg_extracted[14:15], byteorder='little'), "pad2":newlsc4vntgg_extracted[15:16], 
                             "r3":int.from_bytes(newlsc4vntgg_extracted[16:17], byteorder='little'), "g3":int.from_bytes(newlsc4vntgg_extracted[17:18], byteorder='little'), "b3":int.from_bytes(newlsc4vntgg_extracted[18:19], byteorder='little'), "pad3":newlsc4vntgg_extracted[19:20], 
                             "normal0":int.from_bytes(newlsc4vntgg_extracted[20:22], byteorder='little'), "vertex0":int.from_bytes(newlsc4vntgg_extracted[22:24], byteorder='little'), 
                             "normal1":int.from_bytes(newlsc4vntgg_extracted[24:26], byteorder='little'), "vertex1":int.from_bytes(newlsc4vntgg_extracted[26:28], byteorder='little'), 
                             "normal2":int.from_bytes(newlsc4vntgg_extracted[28:30], byteorder='little'), "vertex2":int.from_bytes(newlsc4vntgg_extracted[30:32], byteorder='little'), 
                             "normal3":int.from_bytes(newlsc4vntgg_extracted[32:34], byteorder='little'), "vertex3":int.from_bytes(newlsc4vntgg_extracted[34:36], byteorder='little')}
                newlsc4vntgg_in_obj.append(newlsc4vntgg)
            newlsc4vntgg_obj.append(newlsc4vntgg_in_obj)
    
    #----------------------------------------------------- 3 Vertex (NLSC - TEXTURED - NO TEXTURED) -----------------------------------------------------#

    def decoded_nlsc3vgt(self):
        global nlsc3vgt_obj
        nlsc3vgt_obj = []
        nlsc3vgt_index_block = []
        for nlsc3vgt_match in standard_tmd_structure.primitive_block_byte:
            nlsc3vgt_m = [m.start() for m in re.finditer(PrimitivePacketHeader.nlsc_3v_g_t, nlsc3vgt_match)]
            nlsc3vgt_index_block.append(nlsc3vgt_m)
        nlsc3vgt_extraction = zip(nlsc3vgt_index_block, standard_tmd_structure.primitive_block_byte)

        for index_num, nlsc3vgt_block in nlsc3vgt_extraction:
            nlsc3vgt_in_obj = []
            for i_num in index_num:
                start_read = i_num
                end_read = i_num + 36
                nlsc3vgt_extracted = nlsc3vgt_block[start_read:end_read]
                # CONVERSION IN A SINGLE MOVE
                nlsc3vgt = {"nlsc3vgt":nlsc3vgt_extracted[0:4], 
                            "u0":(int.from_bytes(nlsc3vgt_extracted[4:5], byteorder='little') / 256), "v0":(int.from_bytes(nlsc3vgt_extracted[5:6], byteorder='little') / 256), "cba":nlsc3vgt_extracted[6:8], 
                            "u1":(int.from_bytes(nlsc3vgt_extracted[8:9], byteorder='little') / 256), "v1":(int.from_bytes(nlsc3vgt_extracted[9:10], byteorder='little') / 256), "tsb":nlsc3vgt_extracted[10:12], 
                            "u2":(int.from_bytes(nlsc3vgt_extracted[12:13], byteorder='little') / 256), "v2":(int.from_bytes(nlsc3vgt_extracted[13:14], byteorder='little') / 256), "pad0":nlsc3vgt_extracted[14:16], 
                            "r0":int.from_bytes(nlsc3vgt_extracted[16:17], byteorder='little'), "g0":int.from_bytes(nlsc3vgt_extracted[17:18], byteorder='little'), "b0":int.from_bytes(nlsc3vgt_extracted[18:19], byteorder='little'), "pad1":nlsc3vgt_extracted[19:20], 
                            "r1":int.from_bytes(nlsc3vgt_extracted[20:21], byteorder='little'), "g1":int.from_bytes(nlsc3vgt_extracted[21:22], byteorder='little'), "b1":int.from_bytes(nlsc3vgt_extracted[22:23], byteorder='little'), "pad2":nlsc3vgt_extracted[23:24], 
                            "r2":int.from_bytes(nlsc3vgt_extracted[24:25], byteorder='little'), "g2":int.from_bytes(nlsc3vgt_extracted[25:26], byteorder='little'), "b2":int.from_bytes(nlsc3vgt_extracted[26:27], byteorder='little'), "pad3":nlsc3vgt_extracted[27:28], 
                            "vertex0":int.from_bytes(nlsc3vgt_extracted[28:30], byteorder='little'), "vertex1":int.from_bytes(nlsc3vgt_extracted[30:32], byteorder='little'), 
                            "vertex2":int.from_bytes(nlsc3vgt_extracted[32:34], byteorder='little'), "pad4":nlsc3vgt_extracted[34:36]}
                nlsc3vgt_in_obj.append(nlsc3vgt)
            nlsc3vgt_obj.append(nlsc3vgt_in_obj)
    
    def decoded_nlsc3vft(self):
        global nlsc3vft_obj
        nlsc3vft_obj = []
        nlsc3vft_index_block = []
        for nlsc3vft_match in standard_tmd_structure.primitive_block_byte:
            nlsc3vft_m = [m.start() for m in re.finditer(PrimitivePacketHeader.nlsc_3v_f_t, nlsc3vft_match)]
            nlsc3vft_index_block.append(nlsc3vft_m)
        nlsc3vft_extraction = zip(nlsc3vft_index_block, standard_tmd_structure.primitive_block_byte)

        for index_num, nlsc3vft_block in nlsc3vft_extraction:
            nlsc3vft_in_obj = []
            for i_num in index_num:
                start_read = i_num
                end_read = i_num + 28
                nlsc3vft_extracted = nlsc3vft_block[start_read:end_read]
                # CONVERSION IN A SINGLE MOVE
                nlsc3vft = {"nlsc3vft":nlsc3vft_extracted[0:4], 
                            "u0":(int.from_bytes(nlsc3vft_extracted[4:5], byteorder='little') / 256), "v0":(int.from_bytes(nlsc3vft_extracted[5:6], byteorder='little') / 256), "cba":nlsc3vft_extracted[6:8], 
                            "u1":(int.from_bytes(nlsc3vft_extracted[8:9], byteorder='little') / 256), "v1":(int.from_bytes(nlsc3vft_extracted[9:10], byteorder='little') / 256), "tsb":nlsc3vft_extracted[10:12], 
                            "u2":(int.from_bytes(nlsc3vft_extracted[12:13], byteorder='little') / 256), "v2":(int.from_bytes(nlsc3vft_extracted[13:14], byteorder='little') / 256), "pad0":nlsc3vft_extracted[14:16], 
                            "r0":int.from_bytes(nlsc3vft_extracted[16:17], byteorder='little'), "g0":int.from_bytes(nlsc3vft_extracted[17:18], byteorder='little'), "b0":int.from_bytes(nlsc3vft_extracted[18:19], byteorder='little'), "pad1":nlsc3vft_extracted[19:20], 
                            "vertex0":int.from_bytes(nlsc3vft_extracted[20:22], byteorder='little'), "vertex1":int.from_bytes(nlsc3vft_extracted[22:24], byteorder='little'), 
                            "vertex2":int.from_bytes(nlsc3vft_extracted[24:26], byteorder='little'), "pad2":nlsc3vft_extracted[26:28]}
                nlsc3vft_in_obj.append(nlsc3vft)
            nlsc3vft_obj.append(nlsc3vft_in_obj)
    
    def decoded_new_nlsc_3v_g_t(self):
        global newnlsc3vgt_obj
        newnlsc3vgt_obj = []
        newnlsc3vgt_index_block = []
        for newnlsc3vgt_match in standard_tmd_structure.primitive_block_byte:
            newnlsc3vgt_m = [m.start() for m in re.finditer(PrimitivePacketHeader.new_nlsc_3v_g_t, newnlsc3vgt_match)]
            newnlsc3vgt_index_block.append(newnlsc3vgt_m)
        newnlsc3vgt_extraction = zip(newnlsc3vgt_index_block, standard_tmd_structure.primitive_block_byte)

        for index_num, newnlsc3vgt_block in newnlsc3vgt_extraction:
            newnlsc3vgt_in_obj = []
            for i_num in index_num:
                start_read = i_num
                end_read = i_num + 36
                newnlsc3vgt_extracted = newnlsc3vgt_block[start_read:end_read]
                # CONVERSION IN A SINGLE MOVE
                newnlsc3vgt = {"newnlsc3vgt":newnlsc3vgt_extracted[0:4], 
                            "u0":(int.from_bytes(newnlsc3vgt_extracted[4:5], byteorder='little') / 256), "v0":(int.from_bytes(newnlsc3vgt_extracted[5:6], byteorder='little') / 256), "cba":newnlsc3vgt_extracted[6:8], 
                            "u1":(int.from_bytes(newnlsc3vgt_extracted[8:9], byteorder='little') / 256), "v1":(int.from_bytes(newnlsc3vgt_extracted[9:10], byteorder='little') / 256), "tsb":newnlsc3vgt_extracted[10:12], 
                            "u2":(int.from_bytes(newnlsc3vgt_extracted[12:13], byteorder='little') / 256), "v2":(int.from_bytes(newnlsc3vgt_extracted[13:14], byteorder='little') / 256), "pad0":newnlsc3vgt_extracted[14:16], 
                            "r0":int.from_bytes(newnlsc3vgt_extracted[16:17], byteorder='little'), "g0":int.from_bytes(newnlsc3vgt_extracted[17:18], byteorder='little'), "b0":int.from_bytes(newnlsc3vgt_extracted[18:19], byteorder='little'), "pad1":newnlsc3vgt_extracted[19:20], 
                            "r1":int.from_bytes(newnlsc3vgt_extracted[20:21], byteorder='little'), "g1":int.from_bytes(newnlsc3vgt_extracted[21:22], byteorder='little'), "b1":int.from_bytes(newnlsc3vgt_extracted[22:23], byteorder='little'), "pad2":newnlsc3vgt_extracted[23:24], 
                            "r2":int.from_bytes(newnlsc3vgt_extracted[24:25], byteorder='little'), "g2":int.from_bytes(newnlsc3vgt_extracted[25:26], byteorder='little'), "b2":int.from_bytes(newnlsc3vgt_extracted[26:27], byteorder='little'), "pad3":newnlsc3vgt_extracted[27:28], 
                            "vertex0":int.from_bytes(newnlsc3vgt_extracted[28:30], byteorder='little'), "vertex1":int.from_bytes(newnlsc3vgt_extracted[30:32], byteorder='little'), 
                            "vertex2":int.from_bytes(newnlsc3vgt_extracted[32:34], byteorder='little'), "pad4":newnlsc3vgt_extracted[34:36]}
                newnlsc3vgt_in_obj.append(newnlsc3vgt)
            newnlsc3vgt_obj.append(newnlsc3vgt_in_obj)
    
    def decoded_nlsc3vntg(self):
        global nlsc3vntg_obj
        nlsc3vntg_obj = []
        nlsc3vntg_index_block = []
        for nlsc3vntg_match in standard_tmd_structure.primitive_block_byte:
            nlsc3vntg_m = [m.start() for m in re.finditer(PrimitivePacketHeader.nlsc_3v_nt_g, nlsc3vntg_match)]
            nlsc3vntg_index_block.append(nlsc3vntg_m)
        nlsc3vntg_extraction = zip(nlsc3vntg_index_block, standard_tmd_structure.primitive_block_byte)

        for index_num, nlsc3vntg_block in nlsc3vntg_extraction:
            nlsc3vntg_in_obj = []
            for i_num in index_num:
                start_read = i_num
                end_read = i_num + 24
                nlsc3vntg_extracted = nlsc3vntg_block[start_read:end_read]
                # CONVERSION IN A SINGLE MOVE
                nlsc3vntg = {"nlsc3vntg":nlsc3vntg_extracted[0:4], 
                             "r0":int.from_bytes(nlsc3vntg_extracted[4:5], byteorder='little'), "g0":int.from_bytes(nlsc3vntg_extracted[5:6], byteorder='little'), "b0":int.from_bytes(nlsc3vntg_extracted[6:7], byteorder='little'), "pad0":nlsc3vntg_extracted[7:8], 
                             "r1":int.from_bytes(nlsc3vntg_extracted[8:9], byteorder='little'), "g1":int.from_bytes(nlsc3vntg_extracted[9:10], byteorder='little'), "b1":int.from_bytes(nlsc3vntg_extracted[10:11], byteorder='little'), "pad1":nlsc3vntg_extracted[11:12], 
                             "r2":int.from_bytes(nlsc3vntg_extracted[12:13], byteorder='little'), "g2":int.from_bytes(nlsc3vntg_extracted[13:14], byteorder='little'), "b1":int.from_bytes(nlsc3vntg_extracted[14:15], byteorder='little'), "pad2":nlsc3vntg_extracted[15:16], 
                             "vertex0":int.from_bytes(nlsc3vntg_extracted[16:18], byteorder='little'), "vertex1":int.from_bytes(nlsc3vntg_extracted[18:20], byteorder='little'), 
                             "vertex2":int.from_bytes(nlsc3vntg_extracted[20:22], byteorder='little'), "pad3":nlsc3vntg_extracted[22:24]}
                nlsc3vntg_in_obj.append(nlsc3vntg)
            nlsc3vntg_obj.append(nlsc3vntg_in_obj)
    
    def decoded_nlsc3vntf(self):
        global nlsc3vntf_obj
        nlsc3vntf_obj = []
        nlsc3vntf_index_block = []
        for nlsc3vntf_match in standard_tmd_structure.primitive_block_byte:
            nlsc3vntf_m = [m.start() for m in re.finditer(PrimitivePacketHeader.nlsc_3v_nt_f, nlsc3vntf_match)]
            nlsc3vntf_index_block.append(nlsc3vntf_m)
        nlsc3vntf_extraction = zip(nlsc3vntf_index_block, standard_tmd_structure.primitive_block_byte)

        for index_num, nlsc3vntf_block in nlsc3vntf_extraction:
            nlsc3vntf_in_obj = []
            for i_num in index_num:
                start_read = i_num
                end_read = i_num + 16
                nlsc3vntf_extracted = nlsc3vntf_block[start_read:end_read]
                # CONVERSION IN A SINGLE MOVE
                nlsc3vntf = {"nlsc3vntf":nlsc3vntf_extracted[0:4], 
                             "r0":int.from_bytes(nlsc3vntf_extracted[4:5], byteorder='little'), "g0":int.from_bytes(nlsc3vntf_extracted[5:6], byteorder='little'), "b0":int.from_bytes(nlsc3vntf_extracted[6:7], byteorder='little'), "pad0":nlsc3vntf_extracted[7:8], 
                             "vertex0":int.from_bytes(nlsc3vntf_extracted[8:10], byteorder='little'), "vertex1":int.from_bytes(nlsc3vntf_extracted[10:12], byteorder='little'), 
                             "vertex2":int.from_bytes(nlsc3vntf_extracted[12:14], byteorder='little'), "pad1":nlsc3vntf_extracted[14:16]}
                nlsc3vntf_in_obj.append(nlsc3vntf)
            nlsc3vntf_obj.append(nlsc3vntf_in_obj)
    
    def decoded_nlsc4vgt(self):
        global nlsc4vgt_obj
        nlsc4vgt_obj = []
        nlsc4vgt_index_block = []
        for nlsc4vgt_match in standard_tmd_structure.primitive_block_byte:
            nlsc4vgt_m = [m.start() for m in re.finditer(PrimitivePacketHeader.nlsc_4v_g_t, nlsc4vgt_match)]
            nlsc4vgt_index_block.append(nlsc4vgt_m)
        nlsc4vgt_extraction = zip(nlsc4vgt_index_block, standard_tmd_structure.primitive_block_byte)

        for index_num, nlsc4vgt_block in nlsc4vgt_extraction:
            nlsc4vgt_in_obj = []
            for i_num in index_num:
                start_read = i_num
                end_read = i_num + 44
                nlsc4vgt_extracted = nlsc4vgt_block[start_read:end_read]
                # CONVERSION IN A SINGLE MOVE
                nlsc4vgt = {"nlsc4vgt":nlsc4vgt_extracted[0:4], 
                            "u0":(int.from_bytes(nlsc4vgt_extracted[4:5], byteorder='little') / 256), "v0":(int.from_bytes(nlsc4vgt_extracted[5:6], byteorder='little') / 256), "cba":nlsc4vgt_extracted[6:8], 
                            "u1":(int.from_bytes(nlsc4vgt_extracted[8:9], byteorder='little') / 256), "v1":(int.from_bytes(nlsc4vgt_extracted[9:10], byteorder='little') / 256), "tsb":nlsc4vgt_extracted[10:12], 
                            "u2":(int.from_bytes(nlsc4vgt_extracted[12:13], byteorder='little') / 256), "v2":(int.from_bytes(nlsc4vgt_extracted[13:14], byteorder='little') / 256), "pad0":nlsc4vgt_extracted[14:16], 
                            "u3":(int.from_bytes(nlsc4vgt_extracted[16:17], byteorder='little') / 256), "v3":(int.from_bytes(nlsc4vgt_extracted[17:18], byteorder='little') / 256), "pad1":nlsc4vgt_extracted[18:20], 
                            "r0":int.from_bytes(nlsc4vgt_extracted[20:21], byteorder='little'), "g0":int.from_bytes(nlsc4vgt_extracted[21:22], byteorder='little'), "b0":int.from_bytes(nlsc4vgt_extracted[22:23], byteorder='little'), "pad2":nlsc4vgt_extracted[23:24], 
                            "r1":int.from_bytes(nlsc4vgt_extracted[24:25], byteorder='little'), "g1":int.from_bytes(nlsc4vgt_extracted[25:26], byteorder='little'), "b1":int.from_bytes(nlsc4vgt_extracted[26:27], byteorder='little'), "pad3":nlsc4vgt_extracted[27:28], 
                            "r2":int.from_bytes(nlsc4vgt_extracted[28:29], byteorder='little'), "g2":int.from_bytes(nlsc4vgt_extracted[29:30], byteorder='little'), "b2":int.from_bytes(nlsc4vgt_extracted[30:31], byteorder='little'), "pad4":nlsc4vgt_extracted[31:32], 
                            "r3":int.from_bytes(nlsc4vgt_extracted[32:33], byteorder='little'), "g3":int.from_bytes(nlsc4vgt_extracted[33:34], byteorder='little'), "b3":int.from_bytes(nlsc4vgt_extracted[34:35], byteorder='little'), "pad5":nlsc4vgt_extracted[35:36], 
                            "vertex0":int.from_bytes(nlsc4vgt_extracted[36:38], byteorder='little'), "vertex1":int.from_bytes(nlsc4vgt_extracted[38:40], byteorder='little'), 
                            "vertex2":int.from_bytes(nlsc4vgt_extracted[40:42], byteorder='little'), "vertex3":int.from_bytes(nlsc4vgt_extracted[42:44], byteorder='little')}
                nlsc4vgt_in_obj.append(nlsc4vgt)
            nlsc4vgt_obj.append(nlsc4vgt_in_obj)
    
    def decoded_nlsc4vft(self):
        global nlsc4vft_obj
        nlsc4vft_obj = []
        nlsc4vft_index_block = []
        for nlsc4vft_match in standard_tmd_structure.primitive_block_byte:
            nlsc4vft_m = [m.start() for m in re.finditer(PrimitivePacketHeader.nlsc_4v_f_t, nlsc4vft_match)]
            nlsc4vft_index_block.append(nlsc4vft_m)
        nlsc4vft_extraction = zip(nlsc4vft_index_block, standard_tmd_structure.primitive_block_byte)

        for index_num, nlsc4vft_block in nlsc4vft_extraction:
            nlsc4vft_in_obj = []
            for i_num in index_num:
                start_read = i_num
                end_read = i_num + 32
                nlsc4vft_extracted = nlsc4vft_block[start_read:end_read]
                # CONVERSION IN A SINGLE MOVE
                nlsc4vft = {"nlsc4vft":nlsc4vft_extracted[0:4], 
                            "u0":(int.from_bytes(nlsc4vft_extracted[4:5], byteorder='little') / 256), "v0":(int.from_bytes(nlsc4vft_extracted[5:6], byteorder='little') / 256), "pad0":nlsc4vft_extracted[6:8], 
                            "u1":(int.from_bytes(nlsc4vft_extracted[8:9], byteorder='little') / 256), "v1":(int.from_bytes(nlsc4vft_extracted[9:10], byteorder='little') / 256), "pad1":nlsc4vft_extracted[10:12], 
                            "u2":(int.from_bytes(nlsc4vft_extracted[12:13], byteorder='little') / 256), "v2":(int.from_bytes(nlsc4vft_extracted[13:14], byteorder='little') / 256), "pad2":nlsc4vft_extracted[14:16], 
                            "u3":(int.from_bytes(nlsc4vft_extracted[16:17], byteorder='little') / 256), "v3":(int.from_bytes(nlsc4vft_extracted[17:18], byteorder='little') / 256), "pad3":nlsc4vft_extracted[18:20], 
                            "r0":int.from_bytes(nlsc4vft_extracted[20:21], byteorder='little'), "g0":int.from_bytes(nlsc4vft_extracted[21:22], byteorder='little'), "b0":int.from_bytes(nlsc4vft_extracted[22:23], byteorder='little'), "pad4":nlsc4vft_extracted[23:24], 
                            "vertex0":int.from_bytes(nlsc4vft_extracted[24:26], byteorder='little'), "vertex1":int.from_bytes(nlsc4vft_extracted[26:28], byteorder='little'), 
                            "vertex2":int.from_bytes(nlsc4vft_extracted[28:30], byteorder='little'), "vertex3":int.from_bytes(nlsc4vft_extracted[30:32], byteorder='little')}
                nlsc4vft_in_obj.append(nlsc4vft)
            nlsc4vft_obj.append(nlsc4vft_in_obj)
    
    def decoded_new_nlsc_4v_g_t(self):
        global newnlsc4vgt_obj
        newnlsc4vgt_obj = []
        newnlsc4vgt_index_block = []
        for newnlsc4vgt_match in standard_tmd_structure.primitive_block_byte:
            newnlsc4vgt_m = [m.start() for m in re.finditer(re.escape(PrimitivePacketHeader.new_nlsc_4v_g_t), newnlsc4vgt_match)]
            newnlsc4vgt_index_block.append(newnlsc4vgt_m)
        newnlsc4vgt_extraction = zip(newnlsc4vgt_index_block, standard_tmd_structure.primitive_block_byte)

        for index_num, newnlsc4vgt_block in newnlsc4vgt_extraction:
            newnlsc4vgt_in_obj = []
            for i_num in index_num:
                start_read = i_num
                end_read = i_num + 44
                newnlsc4vgt_extracted = newnlsc4vgt_block[start_read:end_read]
                # CONVERSION IN A SINGLE MOVE
                newnlsc4vgt = {"newnlsc4vgt":newnlsc4vgt_extracted[0:4], 
                            "u0":(int.from_bytes(newnlsc4vgt_extracted[4:5], byteorder='little') / 256), "v0":(int.from_bytes(newnlsc4vgt_extracted[5:6], byteorder='little') / 256), "cba":newnlsc4vgt_extracted[6:8], 
                            "u1":(int.from_bytes(newnlsc4vgt_extracted[8:9], byteorder='little') / 256), "v1":(int.from_bytes(newnlsc4vgt_extracted[9:10], byteorder='little') / 256), "tsb":newnlsc4vgt_extracted[10:12], 
                            "u2":(int.from_bytes(newnlsc4vgt_extracted[12:13], byteorder='little') / 256), "v2":(int.from_bytes(newnlsc4vgt_extracted[13:14], byteorder='little') / 256), "pad0":newnlsc4vgt_extracted[14:16], 
                            "u3":(int.from_bytes(newnlsc4vgt_extracted[16:17], byteorder='little') / 256), "v3":(int.from_bytes(newnlsc4vgt_extracted[17:18], byteorder='little') / 256), "pad1":newnlsc4vgt_extracted[18:20], 
                            "r0":int.from_bytes(newnlsc4vgt_extracted[20:21], byteorder='little'), "g0":int.from_bytes(newnlsc4vgt_extracted[21:22], byteorder='little'), "b0":int.from_bytes(newnlsc4vgt_extracted[22:23], byteorder='little'), "pad2":newnlsc4vgt_extracted[23:24], 
                            "r1":int.from_bytes(newnlsc4vgt_extracted[24:25], byteorder='little'), "g1":int.from_bytes(newnlsc4vgt_extracted[25:26], byteorder='little'), "b1":int.from_bytes(newnlsc4vgt_extracted[26:27], byteorder='little'), "pad3":newnlsc4vgt_extracted[27:28], 
                            "r2":int.from_bytes(newnlsc4vgt_extracted[28:29], byteorder='little'), "g2":int.from_bytes(newnlsc4vgt_extracted[29:30], byteorder='little'), "b2":int.from_bytes(newnlsc4vgt_extracted[30:31], byteorder='little'), "pad4":newnlsc4vgt_extracted[31:32], 
                            "r3":int.from_bytes(newnlsc4vgt_extracted[32:33], byteorder='little'), "g3":int.from_bytes(newnlsc4vgt_extracted[33:34], byteorder='little'), "b3":int.from_bytes(newnlsc4vgt_extracted[34:35], byteorder='little'), "pad5":newnlsc4vgt_extracted[35:36], 
                            "vertex0":int.from_bytes(newnlsc4vgt_extracted[36:38], byteorder='little'), "vertex1":int.from_bytes(newnlsc4vgt_extracted[38:40], byteorder='little'), 
                            "vertex2":int.from_bytes(newnlsc4vgt_extracted[40:42], byteorder='little'), "vertex3":int.from_bytes(newnlsc4vgt_extracted[42:44], byteorder='little')}
                newnlsc4vgt_in_obj.append(newnlsc4vgt)
            newnlsc4vgt_obj.append(newnlsc4vgt_in_obj)
    
    def decoded_nlsc4vntg(self):
        global nlsc4vntg_obj
        nlsc4vntg_obj = []
        nlsc4vntg_index_block = []
        for nlsc4vntg_match in standard_tmd_structure.primitive_block_byte:
            nlsc4vntg_m = [m.start() for m in re.finditer(PrimitivePacketHeader.nlsc_4v_nt_g, nlsc4vntg_match)]
            nlsc4vntg_index_block.append(nlsc4vntg_m)
        nlsc4vntg_extraction = zip(nlsc4vntg_index_block, standard_tmd_structure.primitive_block_byte)

        for index_num, nlsc4vntg_block in nlsc4vntg_extraction:
            nlsc4vntg_in_obj = []
            for i_num in index_num:
                start_read = i_num
                end_read = i_num + 28
                nlsc4vntg_extracted = nlsc4vntg_block[start_read:end_read]
                # CONVERSION IN A SINGLE MOVE
                nlsc4vntg = {"nlsc4vntg":nlsc4vntg_extracted[0:4], 
                             "r0":int.from_bytes(nlsc4vntg_extracted[4:5], byteorder='little'), "g0":int.from_bytes(nlsc4vntg_extracted[5:6], byteorder='little'), "b0":int.from_bytes(nlsc4vntg_extracted[6:7], byteorder='little'), "pad0":nlsc4vntg_extracted[7:8], 
                             "r1":int.from_bytes(nlsc4vntg_extracted[8:9], byteorder='little'), "g1":int.from_bytes(nlsc4vntg_extracted[9:10], byteorder='little'), "b1":int.from_bytes(nlsc4vntg_extracted[10:11], byteorder='little'), "pad1":nlsc4vntg_extracted[11:12], 
                             "r2":int.from_bytes(nlsc4vntg_extracted[12:13], byteorder='little'), "g2":int.from_bytes(nlsc4vntg_extracted[13:14], byteorder='little'), "b2":int.from_bytes(nlsc4vntg_extracted[14:15], byteorder='little'), "pad2":nlsc4vntg_extracted[15:16], 
                             "r3":int.from_bytes(nlsc4vntg_extracted[16:17], byteorder='little'), "g3":int.from_bytes(nlsc4vntg_extracted[17:18], byteorder='little'), "b3":int.from_bytes(nlsc4vntg_extracted[18:19], byteorder='little'), "pad3":nlsc4vntg_extracted[19:20], 
                             "vertex0":int.from_bytes(nlsc4vntg_extracted[20:22], byteorder='little'), "vertex1":int.from_bytes(nlsc4vntg_extracted[22:24], byteorder='little'), 
                             "vertex2":int.from_bytes(nlsc4vntg_extracted[24:26], byteorder='little'), "vertex3":int.from_bytes(nlsc4vntg_extracted[26:28], byteorder='little')}
                nlsc4vntg_in_obj.append(nlsc4vntg)
            nlsc4vntg_obj.append(nlsc4vntg_in_obj)
    
    def decoded_nlsc4vntf(self):
        global nlsc4vntf_obj
        nlsc4vntf_obj = []
        nlsc4vntf_index_block = []
        for nlsc4vntf_match in standard_tmd_structure.primitive_block_byte:
            nlsc4vntf_m = [m.start() for m in re.finditer(re.escape(PrimitivePacketHeader.nlsc_4v_nt_f), nlsc4vntf_match)]
            nlsc4vntf_index_block.append(nlsc4vntf_m)
        nlsc4vntf_extraction = zip(nlsc4vntf_index_block, standard_tmd_structure.primitive_block_byte)

        for index_num, nlsc4vntf_block in nlsc4vntf_extraction:
            nlsc4vntf_in_obj = []
            for i_num in index_num:
                start_read = i_num
                end_read = i_num + 16
                nlsc4vntf_extracted = nlsc4vntf_block[start_read:end_read]
                # CONVERSION IN A SINGLE MOVE
                nlsc4vntf = {"nlsc4vntf":nlsc4vntf_extracted[0:4], 
                             "r0":int.from_bytes(nlsc4vntf_extracted[4:5], byteorder='little'), "g0":int.from_bytes(nlsc4vntf_extracted[5:6], byteorder='little'), "b0":int.from_bytes(nlsc4vntf_extracted[6:7], byteorder='little'), "pad0":nlsc4vntf_extracted[7:8], 
                             "vertex0":int.from_bytes(nlsc4vntf_extracted[8:10], byteorder='little'), "vertex1":int.from_bytes(nlsc4vntf_extracted[10:12], byteorder='little'), 
                             "vertex2":int.from_bytes(nlsc4vntf_extracted[12:14], byteorder='little'), "vertex3":int.from_bytes(nlsc4vntf_extracted[14:16], byteorder='little')}
                nlsc4vntf_in_obj.append(nlsc4vntf)
            nlsc4vntf_obj.append(nlsc4vntf_in_obj)
    
    #--------------------------------------------- HERE ENDS THE DECODERS FOR PRIMITIVES ---------------------------------------------#

class ObjectCleaner: # POST DECODING PROCESS TO CLEAN THE NONE VALUES ALONG THE PRIMITIVE OBJECT DICTS TO SEND IT TO STANDARD TMD WRITER
    def __init__(self):
        self.self = self

    def primitive_cleaner(self): 

        primitives_for_prim_calc = zip_longest(lsc3vgt_obj, lsc3vft_obj, newlsc3vgt_obj, newlsc3vgt2_obj, lsc3vntgs_obj, lsc3vntfs_obj, lsc3vntgg_obj, lsc3vntfg_obj, lsc4vgt_obj, lsc4vft_obj, newlsc4vgt_obj, newlsc4vgt2_obj, lsc4vntgs_obj, lsc4vntfs_obj, lsc4vntgg_obj, lsc4vntfg_obj, newlsc4vntgs_obj, nlsc3vgt_obj, nlsc3vft_obj, newnlsc3vgt_obj, nlsc3vntg_obj, nlsc3vntf_obj, nlsc4vgt_obj, nlsc4vft_obj, newnlsc4vgt_obj, nlsc4vntg_obj, nlsc4vntf_obj, newlsc4vntgg_obj, newlsc3vntgg_obj, newlsc3vntfg_obj)# I DO THIS TO AVOID THE EXHAUSTING FROM THE FIRST LIST COMPREHENSION OF THE ZIP, BECAUSE ZIP OBJECT GET EXHAUSTED
        primitives_uv_preclean = zip_longest(lsc3vgt_obj, lsc3vft_obj, newlsc3vgt_obj, newlsc3vgt2_obj, lsc3vntgs_obj, lsc3vntfs_obj, lsc3vntgg_obj, lsc3vntfg_obj, lsc4vgt_obj, lsc4vft_obj, newlsc4vgt_obj, newlsc4vgt2_obj, lsc4vntgs_obj, lsc4vntfs_obj, lsc4vntgg_obj, lsc4vntfg_obj, newlsc4vntgs_obj, nlsc3vgt_obj, nlsc3vft_obj, newnlsc3vgt_obj, nlsc3vntg_obj, nlsc3vntf_obj, nlsc4vgt_obj, nlsc4vft_obj, newnlsc4vgt_obj, nlsc4vntg_obj, nlsc4vntf_obj, newlsc4vntgg_obj, newlsc3vntgg_obj, newlsc3vntfg_obj) # I DO THIS TO AVOID THE EXHAUSTING FROM THE FIRST LIST COMPREHENSION OF THE ZIP, BECAUSE ZIP OBJECT GET EXHAUSTED
        primitives_vertex_index_preclean = zip_longest(lsc3vgt_obj, lsc3vft_obj, newlsc3vgt_obj, newlsc3vgt2_obj, lsc3vntgs_obj, lsc3vntfs_obj, lsc3vntgg_obj, lsc3vntfg_obj, lsc4vgt_obj, lsc4vft_obj, newlsc4vgt_obj, newlsc4vgt2_obj, lsc4vntgs_obj, lsc4vntfs_obj, lsc4vntgg_obj, lsc4vntfg_obj, newlsc4vntgs_obj, nlsc3vgt_obj, nlsc3vft_obj, newnlsc3vgt_obj, nlsc3vntg_obj, nlsc3vntf_obj, nlsc4vgt_obj, nlsc4vft_obj, newnlsc4vgt_obj, nlsc4vntg_obj, nlsc4vntf_obj, newlsc4vntgg_obj, newlsc3vntgg_obj, newlsc3vntfg_obj) # I DO THIS TO AVOID THE EXHAUSTING FROM THE FIRST LIST COMPREHENSION OF THE ZIP, BECAUSE ZIP OBJECT GET EXHAUSTED
        number_of_prims = [] # I DO THIS CALCULATION TO KNOW IF EVERYTHING GOES CORRECT AND IF I NEED TO ADD A NEW PRIMITIVE TYPE OR CHANGE SOMETHING FROM THE DECODERS CODE
        # THIS ZIP WOULD BE USED FOR COLLADA FILE CONVERSION (TOO EXPERIMENTAL)
        # I DO THIS TO AVOID THE EXHAUSTING FROM THE FIRST LIST COMPREHENSION OF THE ZIP, BECAUSE ZIP OBJECT GET EXHAUSTED
        preclean_primitives_collada = zip_longest(lsc3vgt_obj, lsc3vft_obj, newlsc3vgt_obj, newlsc3vgt2_obj, lsc3vntgs_obj, lsc3vntfs_obj, lsc3vntgg_obj, lsc3vntfg_obj, lsc4vgt_obj, lsc4vft_obj, newlsc4vgt_obj, newlsc4vgt2_obj, lsc4vntgs_obj, lsc4vntfs_obj, lsc4vntgg_obj, lsc4vntfg_obj, newlsc4vntgs_obj, nlsc3vgt_obj, nlsc3vft_obj, newnlsc3vgt_obj, nlsc3vntg_obj, nlsc3vntf_obj, nlsc4vgt_obj, nlsc4vft_obj, newnlsc4vgt_obj, nlsc4vntg_obj, nlsc4vntf_obj, newlsc4vntgg_obj, newlsc3vntgg_obj, newlsc3vntfg_obj)
        preclean_primitives_primobj = zip_longest(lsc3vgt_obj, lsc3vft_obj, newlsc3vgt_obj, newlsc3vgt2_obj, lsc3vntgs_obj, lsc3vntfs_obj, lsc3vntgg_obj, lsc3vntfg_obj, lsc4vgt_obj, lsc4vft_obj, newlsc4vgt_obj, newlsc4vgt2_obj, lsc4vntgs_obj, lsc4vntfs_obj, lsc4vntgg_obj, lsc4vntfg_obj, newlsc4vntgs_obj, nlsc3vgt_obj, nlsc3vft_obj, newnlsc3vgt_obj, nlsc3vntg_obj, nlsc3vntf_obj, nlsc4vgt_obj, nlsc4vft_obj, newnlsc4vgt_obj, nlsc4vntg_obj, nlsc4vntf_obj, newlsc4vntgg_obj, newlsc3vntgg_obj, newlsc3vntfg_obj)
        
        for num_prims in primitives_for_prim_calc:
            for n_prim in num_prims:
                if n_prim != []:
                    number_final = len(n_prim)
                    number_of_prims.append(number_final)
        final_number_of_prims = sum(number_of_prims)
        primitive_number_calc = sum(standard_tmd_structure.primitive_number_int)
        if final_number_of_prims == primitive_number_calc:
            print("The primitives calculated and the extracted are equal, so no problems here...")
        else:
            print("WARNING: Check the primitive decoder code you may find for bugs or there is a new primitive type present")

        # PRIMITIVE FOR OBJECT CLEANER
        global primobj_primitives
        primobj_primitives = []
        for primobj_clean_first_step in preclean_primitives_primobj:
            cleanedprimobj_primitives_inner = []
            for primobj_clean_second_step in primobj_clean_first_step:
                if primobj_clean_second_step != []:
                    cleanedprimobj_primitives_inner.append(primobj_clean_second_step)
                else:
                    pass
            primobj_primitives.append(cleanedprimobj_primitives_inner)
        
        # UV CLEANER
        global obj_primitives_uv
        obj_primitives_uv = [] # THIS IS THE FINAL CLEAN, USING THE NUMBER OBJECT AS EXPECTED
        for uv_clean_first_step in primitives_uv_preclean: # NUMBER OF PROCESSED PRIMITIVES, 27
            cleaneduv_primitives_inner = [] # THIS WILL STORE THE REAL NUMBER OF PRIMITIVES INSTEAD OF THE 27 TYPES
            for uv_clean_second_step in uv_clean_first_step:
                if uv_clean_second_step != []: # THIS CHANGE TO THE REAL NUMBER OF EACH PROCESSED PRIMITIVE
                    cleaneduv_primitives_inner.append(uv_clean_second_step)
                else:
                    pass
            obj_primitives_uv.append(cleaneduv_primitives_inner)
        
        # VERTEX INDEX CLEANER
        global obj_primitives_vertexindex
        obj_primitives_vertexindex = []
        for vi_clean_first_step in primitives_vertex_index_preclean:
            cleanedvi_primitives_inner = []
            for vi_clean_second_step in vi_clean_first_step:
                if vi_clean_second_step != []:
                    cleanedvi_primitives_inner.append(vi_clean_second_step)
                else:
                    pass
            obj_primitives_vertexindex.append(cleanedvi_primitives_inner)

        # COLLADA CLEANER
        global collada_primitives
        collada_primitives = []
        for col_clean_first_step in preclean_primitives_collada:
            cleanedcol_primitives_inner = []
            for col_clean_second_step in col_clean_first_step:
                if col_clean_second_step != []:
                    cleanedcol_primitives_inner.append(col_clean_second_step)
                else:
                    pass
            collada_primitives.append(cleanedcol_primitives_inner)
