"""

Converting Batch Module: This Module will handle the conversions
for each model.
This will work as TLoD TMD Converter module, the ony difference it's i pass the
Model and the Animation/s as parameters to simplify the work

Copyright (C) 2023 DooMMetaL

"""

from tkinter import messagebox
import model_batch_filter as mbf
import split_model_data as smd
import model_decoder as md
import animation_file_process as afp
import properties_writer as pr
import collada_compiler as colcomp
import collada_writer as cw

def main(model_file, animation_file, animation_type, new_folder) -> bool:
    try:
        mbf.ModelFilterFile(model_file=model_file, animation_file=animation_file, animation_type=animation_type)
        smd.SplitStructure(model_data=mbf.model_data, model_nobjects=mbf.model_data_objects, model_type=mbf.file_type)
        
        md.ModelDecoder(model_type=mbf.file_type, obj_num=mbf.model_data_objects, v_block=smd.vertex_block_byte, n_block=smd.normal_block_byte, 
        p_block=smd.primitive_block_byte, v_num=smd.vertex_number_int, n_num=smd.normal_number_int, p_num=smd.primitives_number_int)

        afp.AnimationInterpreter(animation_file=mbf.animation_data, animation_type=mbf.animation_data_info)

        pr.DebugWriter(file_path=new_folder, num_obj_model=mbf.model_data_objects, num_vertex_model=smd.vertex_number_int, num_normal_model=smd.normal_number_int,
        num_primitive_model=smd.primitives_number_int, prim_decoded=md.primitive_decoded)

        colcomp.ColladaCompiler(collada_primitives=md.primitive_decoded, collada_vertex=md.vertex_decoded)
        cw.ColladaWriter(new_folder=new_folder, mod_obj_num=mbf.model_data_objects, prim_num=smd.primitives_number_int, 
        collada_vertex=md.vertex_decoded, collada_normal=md.normal_decoded, collada_uv=colcomp.collada_uv, collada_vertex_color=colcomp.collada_vertex_color,
        collada_polygon=colcomp.collada_polygon, collada_p_array=colcomp.collada_p_array,
        animation_flag=mbf.animation_data_info, collada_animation=afp.animation_decoded, batch_flag=True)
        
        if cw.collada_success == f'Collada File successfully converted...':
            return True
        else:
            return False
            
    except RuntimeError:
        messagebox.showerror(title=f'FATAL ERROR', message=f'file {model_file} cannot be converted')
        exit()