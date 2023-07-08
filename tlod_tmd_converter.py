"""

TLoD TMD Converter Tool, was written for the Standard and Custom TMD from The Legend of Dragoon,
this simple tool will take the objects data, vertex data, CLUT/Palette data and Primitive data,
to export it into DAE format, and import to 3D Softwares such Blender.

Note: Custom TMD are under research so Primitives and CLUT is not fully supported

Copyright (C) 2023 DooMMetaL

"""
import filter_model_anim as fma
import split_model_data as smd
import model_decoder as md
import animation_file_process as afp
import properties_writer as pr
import collada_compiler as colcomp
import collada_writer as cw

def main(input_file):
    try:
        fma.FilterFile(input_file)
        smd.SplitStructure(model_data=fma.model_data, model_nobjects=fma.model_data_objects, model_type=fma.file_type)
        
        md.ModelDecoder(model_type=fma.file_type, obj_num=fma.model_data_objects, v_block=smd.vertex_block_byte, n_block=smd.normal_block_byte, 
        p_block=smd.primitive_block_byte, v_num=smd.vertex_number_int, n_num=smd.normal_number_int, p_num=smd.primitives_number_int)

        afp.AnimationInterpreter(animation_file=fma.animation_data, animation_type=fma.animation_data_info)

        pr.NewFolder(model_path=input_file)
        pr.DebugWriter(file_path=input_file, num_obj_model=fma.model_data_objects, num_vertex_model=smd.vertex_number_int, num_normal_model=smd.normal_number_int,
        num_primitive_model=smd.primitives_number_int, prim_decoded=md.primitive_decoded)

        colcomp.ColladaCompiler(collada_primitives=md.primitive_decoded, collada_vertex=md.vertex_decoded)
        cw.ColladaWriter(new_folder=pr.new_folder, mod_obj_num=fma.model_data_objects, prim_num=smd.primitives_number_int, 
        collada_vertex=md.vertex_decoded, collada_normal=md.normal_decoded, collada_uv=colcomp.collada_uv, collada_vertex_color=colcomp.collada_vertex_color,
        collada_polygon=colcomp.collada_polygon, collada_p_array=colcomp.collada_p_array,
        animation_flag=fma.animation_data_info, collada_animation=afp.animation_decoded, batch_flag=False)

    except KeyboardInterrupt:
        exit()