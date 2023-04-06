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
import model_fixer as mf
import collada_compiler as colcomp
import collada_writer as cw

print(f'||||---> TLoD TMD CONVERTER <---||||')
print(f'IMPORTANT NOTE: For TMD and CTMD Files from DEFF packages, tool will try to find embedded CMB/LMB/SAF animations')

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

        mf.ModelFix(primitive_block=md.primitive_decoded, vertex_block=md.vertex_decoded)

        colcomp.ColladaCompiler(collada_primitives=mf.primitive_decoded_fix, collada_vertex=mf.vertex_decoded_fix)
        cw.ColladaWriter(new_folder=pr.new_folder, file_name=pr.file_name, anim_name=pr.animation_final_name, 
        mod_obj_num=fma.model_data_objects, prim_num=smd.primitives_number_int, 
        collada_vertex=mf.vertex_decoded_fix, collada_normal=md.normal_decoded, collada_uv=colcomp.collada_uv, collada_vertex_color=colcomp.collada_vertex_color,
        collada_polygon=colcomp.collada_polygon, collada_p_array=colcomp.collada_p_array,
        animation_flag=fma.animation_data_info, collada_animation=afp.animation_decoded)

    except KeyboardInterrupt:
        exit()

print(f'Enter the full path of the Model:')
model_input = input()

if __name__ == "__main__":
    main(model_input)