"""

Standard TMD Decoder: This module decode the data from Vertex, Normal and Primitive
into integers for easy read/write for the Standard TMD Writer.
This module has to be very flexible and easy to update

Copyright (C) 2022 DooMMetaL

"""
import struct
import standard_tmd_structure

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




class PrimPacketHeader():
    def __init__(self):
        self.self = PrimPacketHeader
    
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
    new_lsc_3v_nt_fg = b'\x06\x04\x00\x32' # NEW 3 VERTEX GOURAUD FLAT NO TEXTURE TRANSLUCENT - 4 row = 16, REAL NAME = LSC_3V_GOURAUD_FLAT_SINGLE_FACE_NO_TEXTURED_TRANSLUCENT //// add it!!

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
    """The Primitive Packet Header is\n 
        [OLEN - ILEN - FLAG - MODE] ||| Packet Header\n
        Olen = Length of the primitive packet in intermediate processing\n
        Ilen = Length of the packet (reading a raw of 4 bytes or 32bits)\n
        Flag = Contains information at the moment of rendering\n 
        Mode = Indicate Type of Primitive and added attributes"""
    def __init__(self, primitive_decode):
        self.self = PrimitiveTmd
        self.primitive_decode = primitive_decode
    
    def decode_primitive(self):

        primitive_block_complete = standard_tmd_structure.primitive_block_byte
        primitive_number = standard_tmd_structure.primitive_number_int
        length_prim_block = len(primitive_block_complete)

        global collada_primitives
        collada_primitives = []
        for obj_num in range(0, length_prim_block):
            cur_prim_block_inmut = primitive_block_complete[obj_num]
            cur_prim_block = bytearray(cur_prim_block_inmut) # HERE I CONVERT THE ELEMENTS INTO A BYTE ARRAY BECAUSE BYTEARRAYS ARE MUTABLE
            current_number_primitives = primitive_number[obj_num]
            
            """First i need to split the primitives into their blocks, here i say Object->Primitive Block->Primitive"""
            primitives_split = []
            for actual_prim_number in range(0, current_number_primitives):
                """Rows are the Data below the primitive packet, so i need to add the primitive packet too"""
                # 3 Rows
                if (PrimPacketHeader.lsc_3v_nt_f_s == cur_prim_block[0:4]) or (PrimPacketHeader.nlsc_3v_f_t == cur_prim_block[0:4]) or (PrimPacketHeader.nlsc_3v_nt_f == cur_prim_block[0:4]) or (PrimPacketHeader.nlsc_4v_nt_f == cur_prim_block[0:4]):
                    prim_ext_3r = cur_prim_block[0:16]
                    primitives_split.append(prim_ext_3r)
                    del cur_prim_block[0:16]
                
                # 4 Rows
                elif (PrimPacketHeader.lsc_3v_nt_g_s == cur_prim_block[0:4]) or (PrimPacketHeader.new_lsc_3v_nt_fg == cur_prim_block[0:4]) or (PrimPacketHeader.lsc_4v_nt_f_s == cur_prim_block[0:4]):
                    prim_ext_4r = cur_prim_block[0:20]
                    primitives_split.append(prim_ext_4r)
                    del cur_prim_block[0:20]
                
                # 5 Rows
                elif (PrimPacketHeader.lsc_3v_f_t == cur_prim_block[0:4]) or (PrimPacketHeader.lsc_3v_nt_f_g == cur_prim_block[0:4]) or (PrimPacketHeader.lsc_4v_nt_g_s == cur_prim_block[0:4]) or (PrimPacketHeader.new_lsc_4v_nt_g_s == cur_prim_block[0:4]) or (PrimPacketHeader.nlsc_3v_nt_g == cur_prim_block[0:4]):
                    prim_ext_5r = cur_prim_block[0:24]
                    primitives_split.append(prim_ext_5r)
                    del cur_prim_block[0:24]
                
                # 6 Rows
                elif (PrimPacketHeader.lsc_3v_g_t == cur_prim_block[0:4]) or (PrimPacketHeader.new_lsc_3v_gt == cur_prim_block[0:4]) or (PrimPacketHeader.new_lsc_3v_gt_2 == cur_prim_block[0:4]) or (PrimPacketHeader.lsc_3v_nt_g_g == cur_prim_block[0:4]) or (PrimPacketHeader.new_lsc_3v_nt_gg == cur_prim_block[0:4]) or (PrimPacketHeader.nlsc_4v_nt_g == cur_prim_block[0:4]):
                    prim_ext_6r = cur_prim_block[0:28]
                    primitives_split.append(prim_ext_6r)
                    del cur_prim_block[0:28]
                
                # 7 Rows
                elif (PrimPacketHeader.lsc_4v_f_t == cur_prim_block[0:4]) or (PrimPacketHeader.lsc_4v_nt_f_g == cur_prim_block[0:4]) or (PrimPacketHeader.nlsc_4v_f_t == cur_prim_block[0:4]):
                    prim_ext_7r = cur_prim_block[0:32]
                    primitives_split.append(prim_ext_7r)
                    del cur_prim_block[0:32]
                
                # 8 Rows
                elif (PrimPacketHeader.lsc_4v_g_t == cur_prim_block[0:4]) or (PrimPacketHeader.new_lsc_4v_g_t == cur_prim_block[0:4]) or (PrimPacketHeader.new_lsc_4v_g_t_2 == cur_prim_block[0:4]) or (PrimPacketHeader.lsc_4v_nt_g_g == cur_prim_block[0:4]) or (PrimPacketHeader.new_lsc_4v_nt_g_g == cur_prim_block[0:4]) or (PrimPacketHeader.nlsc_3v_g_t == cur_prim_block[0:4]) or (PrimPacketHeader.new_nlsc_3v_g_t == cur_prim_block[0:4]):
                    prim_ext_8r = cur_prim_block[0:36]
                    primitives_split.append(prim_ext_8r)
                    del cur_prim_block[0:36]
                
                # 9 Rows
                # Do not exist (at least i didn't find any of them)

                # 10 Rows
                elif (PrimPacketHeader.nlsc_4v_g_t == cur_prim_block[0:4]) or (PrimPacketHeader.new_nlsc_4v_g_t == cur_prim_block[0:4]):
                    prim_ext_10r = cur_prim_block[0:44]
                    primitives_split.append(prim_ext_10r)
                    del cur_prim_block[0:44]
                
                else:
                    print(f'New Primitive Type Found, \nInterrupting Conversion to avoid future errors...')
                    print(f'This is found in the Object Number: {obj_num},\nPrimitive Number: {actual_prim_number}')
                    exit()
 
            # DECODING THE PRIMITIVES

            primitive_decoded = []
            for primitive_to_decode in primitives_split:
                # 3 Vertex LSC
                if primitive_to_decode[0:4] == PrimPacketHeader.lsc_3v_g_t:
                    lsc3vgt = {"lsc3vgt":primitive_to_decode[0:4], 
                           "u0":(int.from_bytes(primitive_to_decode[4:5], byteorder='little') / 256), "v0":(int.from_bytes(primitive_to_decode[5:6], byteorder='little') / 256), "cba":primitive_to_decode[6:8], 
                           "u1":(int.from_bytes(primitive_to_decode[8:9], byteorder='little') / 256), "v1":(int.from_bytes(primitive_to_decode[9:10], byteorder='little') / 256), "tsb":primitive_to_decode[10:12], 
                           "u2":(int.from_bytes(primitive_to_decode[12:13], byteorder='little') / 256), "v2":(int.from_bytes(primitive_to_decode[13:14], byteorder='little') / 256), "pad0":primitive_to_decode[14:16], 
                           "normal0":int.from_bytes(primitive_to_decode[16:18], byteorder='little'), "vertex0":int.from_bytes(primitive_to_decode[18:20], byteorder='little'), 
                           "normal1":int.from_bytes(primitive_to_decode[20:22], byteorder='little'), "vertex1":int.from_bytes(primitive_to_decode[22:24], byteorder='little'), 
                           "normal2":int.from_bytes(primitive_to_decode[24:26], byteorder='little'), "vertex2":int.from_bytes(primitive_to_decode[26:28], byteorder='little')}
                    primitive_decoded.append(lsc3vgt)

                elif primitive_to_decode[0:4] == PrimPacketHeader.lsc_3v_f_t:
                    lsc3vft = {"lsc3vft":primitive_to_decode[0:4], 
                           "u0":(int.from_bytes(primitive_to_decode[4:5], byteorder='little') / 256), "v0":(int.from_bytes(primitive_to_decode[5:6], byteorder='little') / 256), "cba":primitive_to_decode[6:8], 
                           "u1":(int.from_bytes(primitive_to_decode[8:9], byteorder='little') / 256), "v1":(int.from_bytes(primitive_to_decode[9:10], byteorder='little') / 256), "tsb":primitive_to_decode[10:12], 
                           "u2":(int.from_bytes(primitive_to_decode[12:13], byteorder='little') / 256), "v2":(int.from_bytes(primitive_to_decode[13:14], byteorder='little') / 256), "pad":primitive_to_decode[14:16], 
                           "normal0":int.from_bytes(primitive_to_decode[16:18], byteorder='little'), "vertex0":int.from_bytes(primitive_to_decode[18:20], byteorder='little'), 
                           "vertex1":int.from_bytes(primitive_to_decode[20:22], byteorder='little'), "vertex2":int.from_bytes(primitive_to_decode[22:24], byteorder='little')}
                    primitive_decoded.append(lsc3vft)
                
                elif primitive_to_decode[0:4] == PrimPacketHeader.new_lsc_3v_gt:
                    newlsc3vgt = {"newlsc3vgt":primitive_to_decode[0:4], 
                           "u0":(int.from_bytes(primitive_to_decode[4:5], byteorder='little') / 256), "v0":(int.from_bytes(primitive_to_decode[5:6], byteorder='little') / 256), "cba":primitive_to_decode[6:8], 
                           "u1":(int.from_bytes(primitive_to_decode[8:9], byteorder='little') / 256), "v1":(int.from_bytes(primitive_to_decode[9:10], byteorder='little') / 256), "tsb":primitive_to_decode[10:12], 
                           "u2":(int.from_bytes(primitive_to_decode[12:13], byteorder='little') / 256), "v2":(int.from_bytes(primitive_to_decode[13:14], byteorder='little') / 256), "pad0":primitive_to_decode[14:16], 
                           "normal0":int.from_bytes(primitive_to_decode[16:18], byteorder='little'), "vertex0":int.from_bytes(primitive_to_decode[18:20], byteorder='little'), 
                           "normal1":int.from_bytes(primitive_to_decode[20:22], byteorder='little'), "vertex1":int.from_bytes(primitive_to_decode[22:24], byteorder='little'), 
                           "normal2":int.from_bytes(primitive_to_decode[24:26], byteorder='little'), "vertex2":int.from_bytes(primitive_to_decode[26:28], byteorder='little')}
                    primitive_decoded.append(newlsc3vgt)
                
                elif primitive_to_decode[0:4] == PrimPacketHeader.new_lsc_3v_gt_2:
                    newlsc3vgt2 = {"newlsc3vgt2":primitive_to_decode[0:4], 
                           "u0":(int.from_bytes(primitive_to_decode[4:5], byteorder='little') / 256), "v0":(int.from_bytes(primitive_to_decode[5:6], byteorder='little') / 256), "cba":primitive_to_decode[6:8], 
                           "u1":(int.from_bytes(primitive_to_decode[8:9], byteorder='little') / 256), "v1":(int.from_bytes(primitive_to_decode[9:10], byteorder='little') / 256), "tsb":primitive_to_decode[10:12], 
                           "u2":(int.from_bytes(primitive_to_decode[12:13], byteorder='little') / 256), "v2":(int.from_bytes(primitive_to_decode[13:14], byteorder='little') / 256), "pad0":primitive_to_decode[14:16], 
                           "normal0":int.from_bytes(primitive_to_decode[16:18], byteorder='little'), "vertex0":int.from_bytes(primitive_to_decode[18:20], byteorder='little'), 
                           "normal1":int.from_bytes(primitive_to_decode[20:22], byteorder='little'), "vertex1":int.from_bytes(primitive_to_decode[22:24], byteorder='little'), 
                           "normal2":int.from_bytes(primitive_to_decode[24:26], byteorder='little'), "vertex2":int.from_bytes(primitive_to_decode[26:28], byteorder='little')}
                    primitive_decoded.append(newlsc3vgt2)
                
                elif primitive_to_decode[0:4] == PrimPacketHeader.lsc_3v_nt_g_s:
                    lsc3vntgs = {"lsc3vntgs":primitive_to_decode[0:4], 
                             "r0":int.from_bytes(primitive_to_decode[4:5], byteorder='little'), "g0":int.from_bytes(primitive_to_decode[5:6], byteorder='little'), "b0":int.from_bytes(primitive_to_decode[6:7], byteorder='little'), "pad0":primitive_to_decode[7:8], 
                             "normal0":int.from_bytes(primitive_to_decode[8:10], byteorder='little'), "vertex0":int.from_bytes(primitive_to_decode[10:12], byteorder='little'), 
                             "normal1":int.from_bytes(primitive_to_decode[12:14], byteorder='little'), "vertex1":int.from_bytes(primitive_to_decode[14:16], byteorder='little'), 
                             "normal2":int.from_bytes(primitive_to_decode[16:18], byteorder='little'), "vertex2":int.from_bytes(primitive_to_decode[18:20], byteorder='little')}
                    primitive_decoded.append(lsc3vntgs)
                
                elif primitive_to_decode[0:4] == PrimPacketHeader.lsc_3v_nt_f_s:
                    lsc3vntfs = {"lsc3vntfs":primitive_to_decode[0:4], 
                             "r0":int.from_bytes(primitive_to_decode[4:5], byteorder='little'), "g0":int.from_bytes(primitive_to_decode[5:6], byteorder='little'), "b0":int.from_bytes(primitive_to_decode[6:7], byteorder='little'), "pad0":primitive_to_decode[7:8], 
                             "normal0":int.from_bytes(primitive_to_decode[8:10], byteorder='little'), "vertex0":int.from_bytes(primitive_to_decode[10:12], byteorder='little'), 
                             "vertex1":int.from_bytes(primitive_to_decode[12:14], byteorder='little'), "vertex2":int.from_bytes(primitive_to_decode[14:16], byteorder='little')}
                    primitive_decoded.append(lsc3vntfs)
                
                elif primitive_to_decode[0:4] == PrimPacketHeader.lsc_3v_nt_g_g:
                    lsc3vntgg = {"lsc3vntgg":primitive_to_decode[0:4], 
                             "r0":int.from_bytes(primitive_to_decode[4:5], byteorder='little'), "g0":int.from_bytes(primitive_to_decode[5:6], byteorder='little'), "b0":int.from_bytes(primitive_to_decode[6:7], byteorder='little'), "pad0":primitive_to_decode[7:8], 
                             "r1":int.from_bytes(primitive_to_decode[8:9], byteorder='little'), "g1":int.from_bytes(primitive_to_decode[9:10], byteorder='little'), "b1":int.from_bytes(primitive_to_decode[10:11], byteorder='little'), "pad1":primitive_to_decode[11:12], 
                             "r2":int.from_bytes(primitive_to_decode[12:13], byteorder='little'), "g2":int.from_bytes(primitive_to_decode[13:14], byteorder='little'), "b2":int.from_bytes(primitive_to_decode[14:15], byteorder='little'), "pad2":primitive_to_decode[15:16], 
                             "normal0":int.from_bytes(primitive_to_decode[16:18], byteorder='little'), "vertex0":int.from_bytes(primitive_to_decode[18:20], byteorder='little'), 
                             "normal1":int.from_bytes(primitive_to_decode[20:22], byteorder='little'), "vertex1":int.from_bytes(primitive_to_decode[22:24], byteorder='little'), 
                             "normal2":int.from_bytes(primitive_to_decode[24:26], byteorder='little'), "vertex2":int.from_bytes(primitive_to_decode[26:28], byteorder='little')}
                    primitive_decoded.append(lsc3vntgg)
                
                elif primitive_to_decode[0:4] == PrimPacketHeader.lsc_3v_nt_f_g:
                    lsc3vntfg = {"lsc3vntfg":primitive_to_decode[0:4], 
                             "r0":int.from_bytes(primitive_to_decode[4:5], byteorder='little'), "g0":int.from_bytes(primitive_to_decode[5:6], byteorder='little'), "b0":int.from_bytes(primitive_to_decode[6:7], byteorder='little'), "pad0":primitive_to_decode[7:8], 
                             "r1":int.from_bytes(primitive_to_decode[8:9], byteorder='little'), "g1":int.from_bytes(primitive_to_decode[9:10], byteorder='little'), "b1":int.from_bytes(primitive_to_decode[10:11], byteorder='little'), "pad1":primitive_to_decode[11:12], 
                             "r2":int.from_bytes(primitive_to_decode[12:13], byteorder='little'), "g2":int.from_bytes(primitive_to_decode[13:14], byteorder='little'), "b1":int.from_bytes(primitive_to_decode[14:15], byteorder='little'), "pad2":primitive_to_decode[15:16], 
                             "normal0":int.from_bytes(primitive_to_decode[16:18], byteorder='little'), "vertex0":int.from_bytes(primitive_to_decode[18:20], byteorder='little'), 
                             "vertex1":int.from_bytes(primitive_to_decode[20:22], byteorder='little'), "vertex2":int.from_bytes(primitive_to_decode[22:24], byteorder='little')}
                    primitive_decoded.append(lsc3vntfg)
                
                elif primitive_to_decode[0:4] == PrimPacketHeader.new_lsc_3v_nt_gg:
                    newlsc3vntgg = {"newlsc3vntgg":primitive_to_decode[0:4], 
                             "r0":int.from_bytes(primitive_to_decode[4:5], byteorder='little'), "g0":int.from_bytes(primitive_to_decode[5:6], byteorder='little'), "b0":int.from_bytes(primitive_to_decode[6:7], byteorder='little'), "pad0":primitive_to_decode[7:8], 
                             "r1":int.from_bytes(primitive_to_decode[8:9], byteorder='little'), "g1":int.from_bytes(primitive_to_decode[9:10], byteorder='little'), "b1":int.from_bytes(primitive_to_decode[10:11], byteorder='little'), "pad1":primitive_to_decode[11:12], 
                             "r2":int.from_bytes(primitive_to_decode[12:13], byteorder='little'), "g2":int.from_bytes(primitive_to_decode[13:14], byteorder='little'), "b2":int.from_bytes(primitive_to_decode[14:15], byteorder='little'), "pad2":primitive_to_decode[15:16], 
                             "normal0":int.from_bytes(primitive_to_decode[16:18], byteorder='little'), "vertex0":int.from_bytes(primitive_to_decode[18:20], byteorder='little'), 
                             "normal1":int.from_bytes(primitive_to_decode[20:22], byteorder='little'), "vertex1":int.from_bytes(primitive_to_decode[22:24], byteorder='little'), 
                             "normal2":int.from_bytes(primitive_to_decode[24:26], byteorder='little'), "vertex2":int.from_bytes(primitive_to_decode[26:28], byteorder='little')}
                    primitive_decoded.append(newlsc3vntgg)
                
                elif primitive_to_decode[0:4] == PrimPacketHeader.new_lsc_3v_nt_fg:
                    newlsc3vntfg = {"newlsc3vntfg":primitive_to_decode[0:4], 
                             "r0":int.from_bytes(primitive_to_decode[4:5], byteorder='little'), "g0":int.from_bytes(primitive_to_decode[5:6], byteorder='little'), "b0":int.from_bytes(primitive_to_decode[6:7], byteorder='little'), "pad0":primitive_to_decode[7:8], 
                             "normal0":int.from_bytes(primitive_to_decode[8:10], byteorder='little'), "vertex0":int.from_bytes(primitive_to_decode[10:12], byteorder='little'), 
                             "normal1":int.from_bytes(primitive_to_decode[12:14], byteorder='little'), "vertex1":int.from_bytes(primitive_to_decode[14:16], byteorder='little'),
                             "normal2":int.from_bytes(primitive_to_decode[16:18], byteorder='little'), "vertex2":int.from_bytes(primitive_to_decode[18:20], byteorder='little')}
                    primitive_decoded.append(newlsc3vntfg)
                
                # 4 Vertex LSC
                elif primitive_to_decode[0:4] == PrimPacketHeader.lsc_4v_g_t:
                    lsc4vgt = {"lsc4vgt":primitive_to_decode[0:4], 
                           "u0":(int.from_bytes(primitive_to_decode[4:5], byteorder='little') / 256), "v0":(int.from_bytes(primitive_to_decode[5:6], byteorder='little') / 256), "cba":primitive_to_decode[6:8], 
                           "u1":(int.from_bytes(primitive_to_decode[8:9], byteorder='little') / 256), "v1":(int.from_bytes(primitive_to_decode[9:10], byteorder='little') / 256), "tsb":primitive_to_decode[10:12], 
                           "u2":(int.from_bytes(primitive_to_decode[12:13], byteorder='little') / 256), "v2":(int.from_bytes(primitive_to_decode[13:14], byteorder='little') / 256), "pad0":primitive_to_decode[14:16], 
                           "u3":(int.from_bytes(primitive_to_decode[16:17], byteorder='little') / 256), "v3":(int.from_bytes(primitive_to_decode[17:18], byteorder='little') / 256), "pad1":primitive_to_decode[18:20], 
                           "normal0":int.from_bytes(primitive_to_decode[20:22], byteorder='little'), "vertex0":int.from_bytes(primitive_to_decode[22:24], byteorder='little'), 
                           "normal1":int.from_bytes(primitive_to_decode[24:26], byteorder='little'), "vertex1":int.from_bytes(primitive_to_decode[26:28], byteorder='little'), 
                           "normal2":int.from_bytes(primitive_to_decode[28:30], byteorder='little'), "vertex2":int.from_bytes(primitive_to_decode[30:32], byteorder='little'), 
                           "normal3":int.from_bytes(primitive_to_decode[32:34], byteorder='little'), "vertex3":int.from_bytes(primitive_to_decode[34:36], byteorder='little')}
                    primitive_decoded.append(lsc4vgt)
                
                elif primitive_to_decode[0:4] == PrimPacketHeader.lsc_4v_f_t:
                    lsc4vft = {"lsc4vft":primitive_to_decode[0:4], 
                           "u0":(int.from_bytes(primitive_to_decode[4:5], byteorder='little') / 256), "v0":(int.from_bytes(primitive_to_decode[5:6], byteorder='little') / 256), "cba":primitive_to_decode[6:8],
                           "u1":(int.from_bytes(primitive_to_decode[8:9], byteorder='little') / 256), "v1":(int.from_bytes(primitive_to_decode[9:10], byteorder='little') / 256), "tsb":primitive_to_decode[10:12],
                           "u2":(int.from_bytes(primitive_to_decode[12:13], byteorder='little') / 256), "v2":(int.from_bytes(primitive_to_decode[13:14], byteorder='little') / 256), "pad0":primitive_to_decode[14:16], 
                           "u3":(int.from_bytes(primitive_to_decode[16:17], byteorder='little') / 256), "v3":(int.from_bytes(primitive_to_decode[17:18], byteorder='little') / 256), "pad1":primitive_to_decode[18:20],
                           "normal0":int.from_bytes(primitive_to_decode[20:22], byteorder='little'), "vertex0":int.from_bytes(primitive_to_decode[22:24], byteorder='little'), 
                           "vertex1":int.from_bytes(primitive_to_decode[24:26], byteorder='little'), "vertex2":int.from_bytes(primitive_to_decode[26:28], byteorder='little'), 
                           "vertex3":int.from_bytes(primitive_to_decode[28:30], byteorder='little'), "pad2":primitive_to_decode[30:32]}
                    primitive_decoded.append(lsc4vft)
                
                elif primitive_to_decode[0:4] == PrimPacketHeader.new_lsc_4v_g_t:
                    newlsc4vgt = {"newlsc4vgt":primitive_to_decode[0:4], 
                           "u0":(int.from_bytes(primitive_to_decode[4:5], byteorder='little') / 256), "v0":(int.from_bytes(primitive_to_decode[5:6], byteorder='little') / 256), "cba":primitive_to_decode[6:8], 
                           "u1":(int.from_bytes(primitive_to_decode[8:9], byteorder='little') / 256), "v1":(int.from_bytes(primitive_to_decode[9:10], byteorder='little') / 256), "tsb":primitive_to_decode[10:12], 
                           "u2":(int.from_bytes(primitive_to_decode[12:13], byteorder='little') / 256), "v2":(int.from_bytes(primitive_to_decode[13:14], byteorder='little') / 256), "pad0":primitive_to_decode[14:16], 
                           "u3":(int.from_bytes(primitive_to_decode[16:17], byteorder='little') / 256), "v3":(int.from_bytes(primitive_to_decode[17:18], byteorder='little') / 256), "pad1":primitive_to_decode[18:20], 
                           "normal0":int.from_bytes(primitive_to_decode[20:22], byteorder='little'), "vertex0":int.from_bytes(primitive_to_decode[22:24], byteorder='little'), 
                           "normal1":int.from_bytes(primitive_to_decode[24:26], byteorder='little'), "vertex1":int.from_bytes(primitive_to_decode[26:28], byteorder='little'), 
                           "normal2":int.from_bytes(primitive_to_decode[28:30], byteorder='little'), "vertex2":int.from_bytes(primitive_to_decode[30:32], byteorder='little'), 
                           "normal3":int.from_bytes(primitive_to_decode[32:34], byteorder='little'), "vertex3":int.from_bytes(primitive_to_decode[34:36], byteorder='little')}
                    primitive_decoded.append(newlsc4vgt)
                
                elif primitive_to_decode[0:4] == PrimPacketHeader.new_lsc_4v_g_t_2:
                    newlsc4vgt2 = {"newlsc4vgt2":primitive_to_decode[0:4], 
                           "u0":(int.from_bytes(primitive_to_decode[4:5], byteorder='little') / 256), "v0":(int.from_bytes(primitive_to_decode[5:6], byteorder='little') / 256), "cba":primitive_to_decode[6:8], 
                           "u1":(int.from_bytes(primitive_to_decode[8:9], byteorder='little') / 256), "v1":(int.from_bytes(primitive_to_decode[9:10], byteorder='little') / 256), "tsb":primitive_to_decode[10:12], 
                           "u2":(int.from_bytes(primitive_to_decode[12:13], byteorder='little') / 256), "v2":(int.from_bytes(primitive_to_decode[13:14], byteorder='little') / 256), "pad0":primitive_to_decode[14:16], 
                           "u3":(int.from_bytes(primitive_to_decode[16:17], byteorder='little') / 256), "v3":(int.from_bytes(primitive_to_decode[17:18], byteorder='little') / 256), "pad1":primitive_to_decode[18:20], 
                           "normal0":int.from_bytes(primitive_to_decode[20:22], byteorder='little'), "vertex0":int.from_bytes(primitive_to_decode[22:24], byteorder='little'), 
                           "normal1":int.from_bytes(primitive_to_decode[24:26], byteorder='little'), "vertex1":int.from_bytes(primitive_to_decode[26:28], byteorder='little'), 
                           "normal2":int.from_bytes(primitive_to_decode[28:30], byteorder='little'), "vertex2":int.from_bytes(primitive_to_decode[30:32], byteorder='little'), 
                           "normal3":int.from_bytes(primitive_to_decode[32:34], byteorder='little'), "vertex3":int.from_bytes(primitive_to_decode[34:36], byteorder='little')}
                    primitive_decoded.append(newlsc4vgt2)
                
                elif primitive_to_decode[0:4] == PrimPacketHeader.lsc_4v_nt_g_s:
                    lsc4vntgs = {"lsc4vntgs":primitive_to_decode[0:4], 
                             "r0":int.from_bytes(primitive_to_decode[4:5], byteorder='little'), "g0":int.from_bytes(primitive_to_decode[5:6], byteorder='little'), "b0":int.from_bytes(primitive_to_decode[6:7], byteorder='little'), "pad0":int.from_bytes(primitive_to_decode[7:8], byteorder='little'), 
                             "normal0":int.from_bytes(primitive_to_decode[8:10], byteorder='little'), "vertex0":int.from_bytes(primitive_to_decode[10:12], byteorder='little'), 
                             "normal1":int.from_bytes(primitive_to_decode[12:14], byteorder='little'), "vertex1":int.from_bytes(primitive_to_decode[14:16], byteorder='little'), 
                             "normal2":int.from_bytes(primitive_to_decode[16:18], byteorder='little'), "vertex2":int.from_bytes(primitive_to_decode[18:20], byteorder='little'), 
                             "normal3":int.from_bytes(primitive_to_decode[20:22], byteorder='little'), "vertex3":int.from_bytes(primitive_to_decode[22:24], byteorder='little')}
                    primitive_decoded.append(lsc4vntgs)
                
                elif primitive_to_decode[0:4] == PrimPacketHeader.lsc_4v_nt_f_s:
                    lsc4vntfs = {"lsc4vntfs":primitive_to_decode[0:4], 
                             "r0":int.from_bytes(primitive_to_decode[4:5], byteorder='little'), "g0":int.from_bytes(primitive_to_decode[5:6], byteorder='little'), "b0":int.from_bytes(primitive_to_decode[6:7], byteorder='little'), "pad0":primitive_to_decode[7:8], 
                             "normal0":int.from_bytes(primitive_to_decode[8:10], byteorder='little'), "vertex0":int.from_bytes(primitive_to_decode[10:12], byteorder='little'), 
                             "vertex1":int.from_bytes(primitive_to_decode[12:14], byteorder='little'), "vertex2":int.from_bytes(primitive_to_decode[14:16], byteorder='little'), 
                             "vertex3":int.from_bytes(primitive_to_decode[16:18], byteorder='little'), "pad1":primitive_to_decode[18:20]}
                    primitive_decoded.append(lsc4vntfs)
                
                elif primitive_to_decode[0:4] == PrimPacketHeader.lsc_4v_nt_g_g:
                    lsc4vntgg = {"lsc4vntgg":primitive_to_decode[0:4], 
                             "r0":int.from_bytes(primitive_to_decode[4:5], byteorder='little'), "g0":int.from_bytes(primitive_to_decode[5:6], byteorder='little'), "b0":int.from_bytes(primitive_to_decode[6:7], byteorder='little'), "pad0":primitive_to_decode[7:8], 
                             "r1":int.from_bytes(primitive_to_decode[8:9], byteorder='little'), "g1":int.from_bytes(primitive_to_decode[9:10], byteorder='little'), "b1":int.from_bytes(primitive_to_decode[10:11], byteorder='little'), "pad1":primitive_to_decode[11:12], 
                             "r2":int.from_bytes(primitive_to_decode[12:13], byteorder='little'), "g2":int.from_bytes(primitive_to_decode[13:14], byteorder='little'), "b2":int.from_bytes(primitive_to_decode[14:15], byteorder='little'), "pad2":primitive_to_decode[15:16], 
                             "r3":int.from_bytes(primitive_to_decode[16:17], byteorder='little'), "g3":int.from_bytes(primitive_to_decode[17:18], byteorder='little'), "b3":int.from_bytes(primitive_to_decode[18:19], byteorder='little'), "pad3":primitive_to_decode[19:20], 
                             "normal0":int.from_bytes(primitive_to_decode[20:22], byteorder='little'), "vertex0":int.from_bytes(primitive_to_decode[22:24], byteorder='little'), 
                             "normal1":int.from_bytes(primitive_to_decode[24:26], byteorder='little'), "vertex1":int.from_bytes(primitive_to_decode[26:28], byteorder='little'), 
                             "normal2":int.from_bytes(primitive_to_decode[28:30], byteorder='little'), "vertex2":int.from_bytes(primitive_to_decode[30:32], byteorder='little'), 
                             "normal3":int.from_bytes(primitive_to_decode[32:34], byteorder='little'), "vertex3":int.from_bytes(primitive_to_decode[34:36], byteorder='little')}
                    primitive_decoded.append(lsc4vntgg)
                
                elif primitive_to_decode[0:4] == PrimPacketHeader.lsc_4v_nt_f_g:
                    lsc4vntfg = {"lsc4vntfg":primitive_to_decode[0:4], 
                             "r0":int.from_bytes(primitive_to_decode[4:5]), "g0":int.from_bytes(primitive_to_decode[5:6]), "b0":int.from_bytes(primitive_to_decode[6:7]), "pad0":primitive_to_decode[7:8], 
                             "r1":int.from_bytes(primitive_to_decode[8:9]), "g1":int.from_bytes(primitive_to_decode[9:10]), "b1":int.from_bytes(primitive_to_decode[10:11]), "pad1":primitive_to_decode[11:12], 
                             "r2":int.from_bytes(primitive_to_decode[12:13]), "g2":int.from_bytes(primitive_to_decode[13:14]), "b2":int.from_bytes(primitive_to_decode[14:15]), "pad2":primitive_to_decode[15:16], 
                             "r3":int.from_bytes(primitive_to_decode[16:17]), "g3":int.from_bytes(primitive_to_decode[17:18]), "b3":int.from_bytes(primitive_to_decode[18:19]), "pad3":primitive_to_decode[19:20], 
                             "normal0":int.from_bytes(primitive_to_decode[20:22]), "vertex0":int.from_bytes(primitive_to_decode[22:24]),
                             "vertex1":int.from_bytes(primitive_to_decode[24:26]), "vertex2":int.from_bytes(primitive_to_decode[26:28]), 
                             "vertex3":int.from_bytes(primitive_to_decode[28:30]), "pad4":primitive_to_decode[30:32]}
                    primitive_decoded.append(lsc4vntfg)
                
                elif primitive_to_decode[0:4] == PrimPacketHeader.new_lsc_4v_nt_g_s:
                    newlsc4vntgs = {"newlsc4vntgs":primitive_to_decode[0:4], 
                             "r0":int.from_bytes(primitive_to_decode[4:5], byteorder='little'), "g0":int.from_bytes(primitive_to_decode[5:6], byteorder='little'), "b0":int.from_bytes(primitive_to_decode[6:7], byteorder='little'), "pad0":int.from_bytes(primitive_to_decode[7:8], byteorder='little'), 
                             "normal0":int.from_bytes(primitive_to_decode[8:10], byteorder='little'), "vertex0":int.from_bytes(primitive_to_decode[10:12], byteorder='little'), 
                             "normal1":int.from_bytes(primitive_to_decode[12:14], byteorder='little'), "vertex1":int.from_bytes(primitive_to_decode[14:16], byteorder='little'), 
                             "normal2":int.from_bytes(primitive_to_decode[16:18], byteorder='little'), "vertex2":int.from_bytes(primitive_to_decode[18:20], byteorder='little'), 
                             "normal3":int.from_bytes(primitive_to_decode[20:22], byteorder='little'), "vertex3":int.from_bytes(primitive_to_decode[22:24], byteorder='little')}
                    primitive_decoded.append(newlsc4vntgs)

                elif primitive_to_decode[0:4] == PrimPacketHeader.new_lsc_4v_nt_g_g:
                    newlsc4vntgg = {"newlsc4vntgg":primitive_to_decode[0:4], 
                             "r0":int.from_bytes(primitive_to_decode[4:5], byteorder='little'), "g0":int.from_bytes(primitive_to_decode[5:6], byteorder='little'), "b0":int.from_bytes(primitive_to_decode[6:7], byteorder='little'), "pad0":primitive_to_decode[7:8], 
                             "r1":int.from_bytes(primitive_to_decode[8:9], byteorder='little'), "g1":int.from_bytes(primitive_to_decode[9:10], byteorder='little'), "b1":int.from_bytes(primitive_to_decode[10:11], byteorder='little'), "pad1":primitive_to_decode[11:12], 
                             "r2":int.from_bytes(primitive_to_decode[12:13], byteorder='little'), "g2":int.from_bytes(primitive_to_decode[13:14], byteorder='little'), "b2":int.from_bytes(primitive_to_decode[14:15], byteorder='little'), "pad2":primitive_to_decode[15:16], 
                             "r3":int.from_bytes(primitive_to_decode[16:17], byteorder='little'), "g3":int.from_bytes(primitive_to_decode[17:18], byteorder='little'), "b3":int.from_bytes(primitive_to_decode[18:19], byteorder='little'), "pad3":primitive_to_decode[19:20], 
                             "normal0":int.from_bytes(primitive_to_decode[20:22], byteorder='little'), "vertex0":int.from_bytes(primitive_to_decode[22:24], byteorder='little'), 
                             "normal1":int.from_bytes(primitive_to_decode[24:26], byteorder='little'), "vertex1":int.from_bytes(primitive_to_decode[26:28], byteorder='little'), 
                             "normal2":int.from_bytes(primitive_to_decode[28:30], byteorder='little'), "vertex2":int.from_bytes(primitive_to_decode[30:32], byteorder='little'), 
                             "normal3":int.from_bytes(primitive_to_decode[32:34], byteorder='little'), "vertex3":int.from_bytes(primitive_to_decode[34:36], byteorder='little')}
                    primitive_decoded.append(newlsc4vntgg)
                
                # 3 Vertex NLSC
                elif primitive_to_decode[0:4] == PrimPacketHeader.nlsc_3v_g_t:
                    nlsc3vgt = {"nlsc3vgt":primitive_to_decode[0:4], 
                            "u0":(int.from_bytes(primitive_to_decode[4:5], byteorder='little') / 256), "v0":(int.from_bytes(primitive_to_decode[5:6], byteorder='little') / 256), "cba":primitive_to_decode[6:8], 
                            "u1":(int.from_bytes(primitive_to_decode[8:9], byteorder='little') / 256), "v1":(int.from_bytes(primitive_to_decode[9:10], byteorder='little') / 256), "tsb":primitive_to_decode[10:12], 
                            "u2":(int.from_bytes(primitive_to_decode[12:13], byteorder='little') / 256), "v2":(int.from_bytes(primitive_to_decode[13:14], byteorder='little') / 256), "pad0":primitive_to_decode[14:16], 
                            "r0":int.from_bytes(primitive_to_decode[16:17], byteorder='little'), "g0":int.from_bytes(primitive_to_decode[17:18], byteorder='little'), "b0":int.from_bytes(primitive_to_decode[18:19], byteorder='little'), "pad1":primitive_to_decode[19:20], 
                            "r1":int.from_bytes(primitive_to_decode[20:21], byteorder='little'), "g1":int.from_bytes(primitive_to_decode[21:22], byteorder='little'), "b1":int.from_bytes(primitive_to_decode[22:23], byteorder='little'), "pad2":primitive_to_decode[23:24], 
                            "r2":int.from_bytes(primitive_to_decode[24:25], byteorder='little'), "g2":int.from_bytes(primitive_to_decode[25:26], byteorder='little'), "b2":int.from_bytes(primitive_to_decode[26:27], byteorder='little'), "pad3":primitive_to_decode[27:28], 
                            "vertex0":int.from_bytes(primitive_to_decode[28:30], byteorder='little'), "vertex1":int.from_bytes(primitive_to_decode[30:32], byteorder='little'), 
                            "vertex2":int.from_bytes(primitive_to_decode[32:34], byteorder='little'), "pad4":primitive_to_decode[34:36]}
                    primitive_decoded.append(nlsc3vgt)
                
                elif primitive_to_decode[0:4] == PrimPacketHeader.nlsc_3v_f_t:
                    nlsc3vft = {"nlsc3vft":primitive_to_decode[0:4], 
                            "u0":(int.from_bytes(primitive_to_decode[4:5], byteorder='little') / 256), "v0":(int.from_bytes(primitive_to_decode[5:6], byteorder='little') / 256), "cba":primitive_to_decode[6:8], 
                            "u1":(int.from_bytes(primitive_to_decode[8:9], byteorder='little') / 256), "v1":(int.from_bytes(primitive_to_decode[9:10], byteorder='little') / 256), "tsb":primitive_to_decode[10:12], 
                            "u2":(int.from_bytes(primitive_to_decode[12:13], byteorder='little') / 256), "v2":(int.from_bytes(primitive_to_decode[13:14], byteorder='little') / 256), "pad0":primitive_to_decode[14:16], 
                            "r0":int.from_bytes(primitive_to_decode[16:17], byteorder='little'), "g0":int.from_bytes(primitive_to_decode[17:18], byteorder='little'), "b0":int.from_bytes(primitive_to_decode[18:19], byteorder='little'), "pad1":primitive_to_decode[19:20], 
                            "vertex0":int.from_bytes(primitive_to_decode[20:22], byteorder='little'), "vertex1":int.from_bytes(primitive_to_decode[22:24], byteorder='little'), 
                            "vertex2":int.from_bytes(primitive_to_decode[24:26], byteorder='little'), "pad2":primitive_to_decode[26:28]}
                    primitive_decoded.append(nlsc3vft)
                
                elif primitive_to_decode[0:4] == PrimPacketHeader.new_nlsc_3v_g_t:
                    newnlsc3vgt = {"newnlsc3vgt":primitive_to_decode[0:4], 
                            "u0":(int.from_bytes(primitive_to_decode[4:5], byteorder='little') / 256), "v0":(int.from_bytes(primitive_to_decode[5:6], byteorder='little') / 256), "cba":primitive_to_decode[6:8], 
                            "u1":(int.from_bytes(primitive_to_decode[8:9], byteorder='little') / 256), "v1":(int.from_bytes(primitive_to_decode[9:10], byteorder='little') / 256), "tsb":primitive_to_decode[10:12], 
                            "u2":(int.from_bytes(primitive_to_decode[12:13], byteorder='little') / 256), "v2":(int.from_bytes(primitive_to_decode[13:14], byteorder='little') / 256), "pad0":primitive_to_decode[14:16], 
                            "r0":int.from_bytes(primitive_to_decode[16:17], byteorder='little'), "g0":int.from_bytes(primitive_to_decode[17:18], byteorder='little'), "b0":int.from_bytes(primitive_to_decode[18:19], byteorder='little'), "pad1":primitive_to_decode[19:20], 
                            "r1":int.from_bytes(primitive_to_decode[20:21], byteorder='little'), "g1":int.from_bytes(primitive_to_decode[21:22], byteorder='little'), "b1":int.from_bytes(primitive_to_decode[22:23], byteorder='little'), "pad2":primitive_to_decode[23:24], 
                            "r2":int.from_bytes(primitive_to_decode[24:25], byteorder='little'), "g2":int.from_bytes(primitive_to_decode[25:26], byteorder='little'), "b2":int.from_bytes(primitive_to_decode[26:27], byteorder='little'), "pad3":primitive_to_decode[27:28], 
                            "vertex0":int.from_bytes(primitive_to_decode[28:30], byteorder='little'), "vertex1":int.from_bytes(primitive_to_decode[30:32], byteorder='little'), 
                            "vertex2":int.from_bytes(primitive_to_decode[32:34], byteorder='little'), "pad4":primitive_to_decode[34:36]}
                    primitive_decoded.append(newnlsc3vgt)
                
                elif primitive_to_decode[0:4] == PrimPacketHeader.nlsc_3v_nt_g:
                    nlsc3vntg = {"nlsc3vntg":primitive_to_decode[0:4], 
                             "r0":int.from_bytes(primitive_to_decode[4:5], byteorder='little'), "g0":int.from_bytes(primitive_to_decode[5:6], byteorder='little'), "b0":int.from_bytes(primitive_to_decode[6:7], byteorder='little'), "pad0":primitive_to_decode[7:8], 
                             "r1":int.from_bytes(primitive_to_decode[8:9], byteorder='little'), "g1":int.from_bytes(primitive_to_decode[9:10], byteorder='little'), "b1":int.from_bytes(primitive_to_decode[10:11], byteorder='little'), "pad1":primitive_to_decode[11:12], 
                             "r2":int.from_bytes(primitive_to_decode[12:13], byteorder='little'), "g2":int.from_bytes(primitive_to_decode[13:14], byteorder='little'), "b2":int.from_bytes(primitive_to_decode[14:15], byteorder='little'), "pad2":primitive_to_decode[15:16], 
                             "vertex0":int.from_bytes(primitive_to_decode[16:18], byteorder='little'), "vertex1":int.from_bytes(primitive_to_decode[18:20], byteorder='little'), 
                             "vertex2":int.from_bytes(primitive_to_decode[20:22], byteorder='little'), "pad3":primitive_to_decode[22:24]}
                    primitive_decoded.append(nlsc3vntg)
                
                elif primitive_to_decode[0:4] == PrimPacketHeader.nlsc_3v_nt_f:
                    nlsc3vntf = {"nlsc3vntf":primitive_to_decode[0:4], 
                             "r0":int.from_bytes(primitive_to_decode[4:5], byteorder='little'), "g0":int.from_bytes(primitive_to_decode[5:6], byteorder='little'), "b0":int.from_bytes(primitive_to_decode[6:7], byteorder='little'), "pad0":primitive_to_decode[7:8], 
                             "vertex0":int.from_bytes(primitive_to_decode[8:10], byteorder='little'), "vertex1":int.from_bytes(primitive_to_decode[10:12], byteorder='little'), 
                             "vertex2":int.from_bytes(primitive_to_decode[12:14], byteorder='little'), "pad1":primitive_to_decode[14:16]}
                    primitive_decoded.append(nlsc3vntf)
                
                # 4 Vertex NLSC
                elif primitive_to_decode[0:4] == PrimPacketHeader.nlsc_4v_g_t:
                    nlsc4vgt = {"nlsc4vgt":primitive_to_decode[0:4], 
                            "u0":(int.from_bytes(primitive_to_decode[4:5], byteorder='little') / 256), "v0":(int.from_bytes(primitive_to_decode[5:6], byteorder='little') / 256), "cba":primitive_to_decode[6:8], 
                            "u1":(int.from_bytes(primitive_to_decode[8:9], byteorder='little') / 256), "v1":(int.from_bytes(primitive_to_decode[9:10], byteorder='little') / 256), "tsb":primitive_to_decode[10:12], 
                            "u2":(int.from_bytes(primitive_to_decode[12:13], byteorder='little') / 256), "v2":(int.from_bytes(primitive_to_decode[13:14], byteorder='little') / 256), "pad0":primitive_to_decode[14:16], 
                            "u3":(int.from_bytes(primitive_to_decode[16:17], byteorder='little') / 256), "v3":(int.from_bytes(primitive_to_decode[17:18], byteorder='little') / 256), "pad1":primitive_to_decode[18:20], 
                            "r0":int.from_bytes(primitive_to_decode[20:21], byteorder='little'), "g0":int.from_bytes(primitive_to_decode[21:22], byteorder='little'), "b0":int.from_bytes(primitive_to_decode[22:23], byteorder='little'), "pad2":primitive_to_decode[23:24], 
                            "r1":int.from_bytes(primitive_to_decode[24:25], byteorder='little'), "g1":int.from_bytes(primitive_to_decode[25:26], byteorder='little'), "b1":int.from_bytes(primitive_to_decode[26:27], byteorder='little'), "pad3":primitive_to_decode[27:28], 
                            "r2":int.from_bytes(primitive_to_decode[28:29], byteorder='little'), "g2":int.from_bytes(primitive_to_decode[29:30], byteorder='little'), "b2":int.from_bytes(primitive_to_decode[30:31], byteorder='little'), "pad4":primitive_to_decode[31:32], 
                            "r3":int.from_bytes(primitive_to_decode[32:33], byteorder='little'), "g3":int.from_bytes(primitive_to_decode[33:34], byteorder='little'), "b3":int.from_bytes(primitive_to_decode[34:35], byteorder='little'), "pad5":primitive_to_decode[35:36], 
                            "vertex0":int.from_bytes(primitive_to_decode[36:38], byteorder='little'), "vertex1":int.from_bytes(primitive_to_decode[38:40], byteorder='little'), 
                            "vertex2":int.from_bytes(primitive_to_decode[40:42], byteorder='little'), "vertex3":int.from_bytes(primitive_to_decode[42:44], byteorder='little')}
                    primitive_decoded.append(nlsc4vgt)
                
                elif primitive_to_decode[0:4] == PrimPacketHeader.nlsc_4v_f_t:
                    nlsc4vft = {"nlsc4vft":primitive_to_decode[0:4], 
                            "u0":(int.from_bytes(primitive_to_decode[4:5], byteorder='little') / 256), "v0":(int.from_bytes(primitive_to_decode[5:6], byteorder='little') / 256), "pad0":primitive_to_decode[6:8], 
                            "u1":(int.from_bytes(primitive_to_decode[8:9], byteorder='little') / 256), "v1":(int.from_bytes(primitive_to_decode[9:10], byteorder='little') / 256), "pad1":primitive_to_decode[10:12], 
                            "u2":(int.from_bytes(primitive_to_decode[12:13], byteorder='little') / 256), "v2":(int.from_bytes(primitive_to_decode[13:14], byteorder='little') / 256), "pad2":primitive_to_decode[14:16], 
                            "u3":(int.from_bytes(primitive_to_decode[16:17], byteorder='little') / 256), "v3":(int.from_bytes(primitive_to_decode[17:18], byteorder='little') / 256), "pad3":primitive_to_decode[18:20], 
                            "r0":int.from_bytes(primitive_to_decode[20:21], byteorder='little'), "g0":int.from_bytes(primitive_to_decode[21:22], byteorder='little'), "b0":int.from_bytes(primitive_to_decode[22:23], byteorder='little'), "pad4":primitive_to_decode[23:24], 
                            "vertex0":int.from_bytes(primitive_to_decode[24:26], byteorder='little'), "vertex1":int.from_bytes(primitive_to_decode[26:28], byteorder='little'), 
                            "vertex2":int.from_bytes(primitive_to_decode[28:30], byteorder='little'), "vertex3":int.from_bytes(primitive_to_decode[30:32], byteorder='little')}
                    primitive_decoded.append(nlsc4vft)
                
                elif primitive_to_decode[0:4] == PrimPacketHeader.new_nlsc_4v_g_t:
                    newnlsc4vgt = {"newnlsc4vgt":primitive_to_decode[0:4], 
                            "u0":(int.from_bytes(primitive_to_decode[4:5], byteorder='little') / 256), "v0":(int.from_bytes(primitive_to_decode[5:6], byteorder='little') / 256), "cba":primitive_to_decode[6:8], 
                            "u1":(int.from_bytes(primitive_to_decode[8:9], byteorder='little') / 256), "v1":(int.from_bytes(primitive_to_decode[9:10], byteorder='little') / 256), "tsb":primitive_to_decode[10:12], 
                            "u2":(int.from_bytes(primitive_to_decode[12:13], byteorder='little') / 256), "v2":(int.from_bytes(primitive_to_decode[13:14], byteorder='little') / 256), "pad0":primitive_to_decode[14:16], 
                            "u3":(int.from_bytes(primitive_to_decode[16:17], byteorder='little') / 256), "v3":(int.from_bytes(primitive_to_decode[17:18], byteorder='little') / 256), "pad1":primitive_to_decode[18:20], 
                            "r0":int.from_bytes(primitive_to_decode[20:21], byteorder='little'), "g0":int.from_bytes(primitive_to_decode[21:22], byteorder='little'), "b0":int.from_bytes(primitive_to_decode[22:23], byteorder='little'), "pad2":primitive_to_decode[23:24], 
                            "r1":int.from_bytes(primitive_to_decode[24:25], byteorder='little'), "g1":int.from_bytes(primitive_to_decode[25:26], byteorder='little'), "b1":int.from_bytes(primitive_to_decode[26:27], byteorder='little'), "pad3":primitive_to_decode[27:28], 
                            "r2":int.from_bytes(primitive_to_decode[28:29], byteorder='little'), "g2":int.from_bytes(primitive_to_decode[29:30], byteorder='little'), "b2":int.from_bytes(primitive_to_decode[30:31], byteorder='little'), "pad4":primitive_to_decode[31:32], 
                            "r3":int.from_bytes(primitive_to_decode[32:33], byteorder='little'), "g3":int.from_bytes(primitive_to_decode[33:34], byteorder='little'), "b3":int.from_bytes(primitive_to_decode[34:35], byteorder='little'), "pad5":primitive_to_decode[35:36], 
                            "vertex0":int.from_bytes(primitive_to_decode[36:38], byteorder='little'), "vertex1":int.from_bytes(primitive_to_decode[38:40], byteorder='little'), 
                            "vertex2":int.from_bytes(primitive_to_decode[40:42], byteorder='little'), "vertex3":int.from_bytes(primitive_to_decode[42:44], byteorder='little')}
                    primitive_decoded.append(newnlsc4vgt)
                
                elif primitive_to_decode[0:4] == PrimPacketHeader.nlsc_4v_nt_g:
                    nlsc4vntg = {"nlsc4vntg":primitive_to_decode[0:4], 
                             "r0":int.from_bytes(primitive_to_decode[4:5], byteorder='little'), "g0":int.from_bytes(primitive_to_decode[5:6], byteorder='little'), "b0":int.from_bytes(primitive_to_decode[6:7], byteorder='little'), "pad0":primitive_to_decode[7:8], 
                             "r1":int.from_bytes(primitive_to_decode[8:9], byteorder='little'), "g1":int.from_bytes(primitive_to_decode[9:10], byteorder='little'), "b1":int.from_bytes(primitive_to_decode[10:11], byteorder='little'), "pad1":primitive_to_decode[11:12], 
                             "r2":int.from_bytes(primitive_to_decode[12:13], byteorder='little'), "g2":int.from_bytes(primitive_to_decode[13:14], byteorder='little'), "b2":int.from_bytes(primitive_to_decode[14:15], byteorder='little'), "pad2":primitive_to_decode[15:16], 
                             "r3":int.from_bytes(primitive_to_decode[16:17], byteorder='little'), "g3":int.from_bytes(primitive_to_decode[17:18], byteorder='little'), "b3":int.from_bytes(primitive_to_decode[18:19], byteorder='little'), "pad3":primitive_to_decode[19:20], 
                             "vertex0":int.from_bytes(primitive_to_decode[20:22], byteorder='little'), "vertex1":int.from_bytes(primitive_to_decode[22:24], byteorder='little'), 
                             "vertex2":int.from_bytes(primitive_to_decode[24:26], byteorder='little'), "vertex3":int.from_bytes(primitive_to_decode[26:28], byteorder='little')}
                    primitive_decoded.append(nlsc4vntg)
                
                elif primitive_to_decode[0:4] == PrimPacketHeader.nlsc_4v_nt_f:
                    nlsc4vntf = {"nlsc4vntf":primitive_to_decode[0:4], 
                             "r0":int.from_bytes(primitive_to_decode[4:5], byteorder='little'), "g0":int.from_bytes(primitive_to_decode[5:6], byteorder='little'), "b0":int.from_bytes(primitive_to_decode[6:7], byteorder='little'), "pad0":primitive_to_decode[7:8], 
                             "vertex0":int.from_bytes(primitive_to_decode[8:10], byteorder='little'), "vertex1":int.from_bytes(primitive_to_decode[10:12], byteorder='little'), 
                             "vertex2":int.from_bytes(primitive_to_decode[12:14], byteorder='little'), "vertex3":int.from_bytes(primitive_to_decode[14:16], byteorder='little')}
                    primitive_decoded.append(nlsc4vntf)
                
                else:
                    print(f'Unknown Primitive Type - Object Number {obj_num} - DECODER ERROR...\nExiting to avoid future errors...')
                    exit()
            
            collada_primitives.append(primitive_decoded)