"""

Force Animation Loading:
This Algorithm will help to users find out animation structure,
using Squares for objects, replacing the original objects

Copyright (C) 2023 DooMMetaL

"""

import load_animation_type as lat
import animation_file_process as afp
import default_model as df
import collada_compiler as colcomp
import collada_writer as cw

def force_animation_loading(input_file):
    try:

        lat.LoadAnimation(animation_file_path=input_file)
        afp.AnimationInterpreter(animation_file=lat.animation_data, animation_type=lat.animation_type)
        df.DefaultModel(number_objects=lat.animation_type)

        colcomp.ColladaCompiler(collada_primitives=df.primitives_created, collada_vertex=df.vertices_created)

        cw.ColladaWriter(new_folder=lat.new_folder, mod_obj_num=df.number_of_objects, prim_num=df.number_of_primitives, 
        collada_vertex=df.vertices_created, collada_normal=df.normals_created, collada_uv=colcomp.collada_uv, collada_vertex_color=colcomp.collada_vertex_color,
        collada_polygon=colcomp.collada_polygon, collada_p_array=colcomp.collada_p_array,
        animation_flag=lat.animation_type, collada_animation=afp.animation_decoded, batch_flag=False)

    except KeyboardInterrupt:
        exit()