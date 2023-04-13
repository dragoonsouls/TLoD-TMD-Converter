"""

DECODER MODEL DATA: this module is in charge of decoding the data of
model files, in here is where the TMD and CTMD are different.
since the complexity of each one is pretty much 
this will work with several modules.

Copyright (C) 2023 DooMMetaL

"""

import standard_tmd_decoder as std
import custom_tmd_decoder as ctd
from tkinter import messagebox


class ModelDecoder:
    def __init__(self, model_type, obj_num, v_block, n_block, p_block, v_num, n_num, p_num):
        self.self = ModelDecoder
        self.select_model_type(model_type=model_type, obj_num=obj_num, v_block=v_block, n_block=n_block, p_block=p_block, v_num=v_num, n_num=n_num, p_num=p_num)
    
    def select_model_type(self, model_type=str, obj_num=int, v_block=list, n_block=list, p_block=list, v_num=list, n_num=list, p_num=list):
        """v_block == Block of Vertices per Object, n_block == Block of Normals per Object, p_block == Block of Primitives per Object"""
        """v_num == Number of Vertices per Object, n_num == Number of Normals per Object, p_num == Number of Primitives per Object"""
        global vertex_decoded
        global normal_decoded
        global primitive_decoded
        vertex_decoded = []
        normal_decoded = []
        primitive_decoded = []

        if (model_type == f'TMD') or (model_type == f'TMD_CCONTAINER') or (model_type == f'TMD_DEFF'):
            vertex_decoded = self.standard_tmd_vertex_decoder(vertex_int=v_num, vertex_block_in=v_block)
            normal_decoded = self.standard_tmd_normal_decoder(normal_int=n_num, normal_block_in=n_block)
            primitive_decoded = self.standard_tmd_primitive_decoder(primitive_int=p_num, primitive_block_in=p_block, number_of_prims=p_num)

        elif (model_type == f'CTMD'):
            normal_decoded = self.custom_tmd_normal_decoder(num_obj=obj_num, normal_int=n_num, normal_block_in=n_block)
            primitive_decoded = self.custom_tmd_primitive_decoder(num_obj=obj_num, primitive_int=p_num, primitive_block_in=p_block)
            vertex_decoded = self.custom_tmd_vertex_decoder(vertex_int=v_num, vertex_block_in=v_block)

        else:
            error_model_type = f'File type: {model_type}, is not a Model file... exiting tool...'
            error_model = messagebox.showerror(title=f'FATAL CRASH!!!...', message=error_model)
            exit()
    
    @staticmethod
    def standard_tmd_vertex_decoder(vertex_int=int, vertex_block_in=list):
        vertex_dec = std.VertexInterpreter.vertex_decoder(self=std.VertexInterpreter, vertex_number_list=vertex_int, vertex_to_decode=vertex_block_in)
        return vertex_dec

    @staticmethod
    def standard_tmd_normal_decoder(normal_int=int, normal_block_in=list):
        normal_dec = std.NormalInterpreter.normal_decoder(self=std.NormalInterpreter, normal_number_list=normal_int, normal_to_decode=normal_block_in)
        return normal_dec

    @staticmethod
    def standard_tmd_primitive_decoder(primitive_int=int, primitive_block_in=list, number_of_prims=list):
        primitive_dec = std.PrimitiveTmd.decode_primitive(self=std.PrimitiveTmd, primitive_number_list=primitive_int, primitive_to_decode=primitive_block_in, number_of_primitives=number_of_prims)
        return primitive_dec

    @staticmethod
    def custom_tmd_normal_decoder(num_obj, normal_int, normal_block_in):
        normal_dec = ctd.CustomTmdNormal.normal_decoder(ctd.CustomTmdNormal.normal_decoder, nobj_expected=num_obj, normal_obj_int=normal_int, normal_block_byte=normal_block_in)
        return normal_dec

    @staticmethod
    def custom_tmd_primitive_decoder(num_obj, primitive_int, primitive_block_in):
        #print(f'Select the Desired Attribute:\n1 = 0x14 00 00 40;\n2 = 0x14 00 00 00;\n3 = 0x50 00 00 00;\n4 = 0x64 00 00 40;\n5 = 0x54 00 00 00;\nAny other value will be set as 0x14 00 00 00')
        attribute_select = int(1)
        primitive_dec = ctd.CustomTmdPrimitive.cprimitive_types_depacker(ctd.CustomTmdPrimitive.cprimitive_types_depacker, object_num=num_obj, prim_num=primitive_int, prim_block_byte=primitive_block_in, tmd_attribute=attribute_select)
        return primitive_dec

    @staticmethod
    def custom_tmd_vertex_decoder(vertex_int, vertex_block_in):
        vertex_dec = ctd.CustomTmdVertex.vertex_decoder(ctd.CustomTmdVertex.vertex_decoder, vertex_number=vertex_int, vertex_block=vertex_block_in)
        return vertex_dec