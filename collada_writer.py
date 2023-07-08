"""

Collada Writer: This module write model structure data and animations into
Collada File Format (*.dae).
Actually this is a kind of a "blueprint" obtained from a Blender 2.8
dae file.

Copyright (C) 2023 DooMMetaL

"""
import os
import datetime
from tkinter.filedialog import asksaveasfilename

class ColladaWriter:
    def __init__(self, new_folder, mod_obj_num, prim_num,
    collada_vertex, collada_normal, collada_uv, collada_vertex_color, collada_polygon, collada_p_array,
    animation_flag, collada_animation, batch_flag):
        self.self = ColladaWriter
        self.write_collada_file(new_folder=new_folder, model_obj_num=mod_obj_num, number_primitive=prim_num,
        collada_vertex=collada_vertex, collada_normal=collada_normal, collada_uv=collada_uv, collada_vertex_color=collada_vertex_color,
        collada_polygon=collada_polygon, collada_p_array=collada_p_array, collada_animation_flag=animation_flag, collada_animation=collada_animation, batch_flag=batch_flag)
    
    def write_collada_file(self, new_folder=str, model_obj_num=int, number_primitive=list, collada_vertex=list, collada_normal=list,
    collada_uv=list, collada_vertex_color=list, collada_polygon=list, collada_p_array=list,
    collada_animation_flag=list, collada_animation=list, batch_flag=bool):

        """ DAE FILE FORMAT (USING AS EXAMPLE THE BLENDER GENERATED FILE)
        |   
        |   LOOK INTO THE DOCUMENTATION ABOUT DAE FILE FORMAT
        |
        """
        date_conversion = datetime.datetime.now().isoformat(timespec='milliseconds')
        collada_vertex_positions = collada_vertex
        animation_bool = self.check_animation(animation_flag=collada_animation_flag)
        
        save_dae = f''
        if batch_flag == False:
            save_dae = asksaveasfilename(confirmoverwrite=True, defaultextension=f'dae', initialdir=new_folder)
        else:
            save_dae = new_folder + f'.dae'

        with open(save_dae, 'w') as dae_file_writer:            
            # HEADER
            technical_header = f'<?xml version="1.0" encoding="utf-8"?>\n'
            collada_header = f'<COLLADA xmlns="http://www.collada.org/2005/11/COLLADASchema" version="1.4.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n'
            # ASSET HEADER
            asset_header = f'  <asset>\n    <contributor>\n      <author>TLoD_TMD_Converter_User</author>\n      <authoring_tool>TLoD_TMD_Converter</authoring_tool>\n   <source_data>{new_folder}.bin</source_data>\n    </contributor>\n    <created>{date_conversion}</created>\n    <modified>{date_conversion}</modified>\n    <unit name="meter" meter="1"/>\n    <up_axis>Z_UP</up_axis>\n  </asset>\n'
            colladada_total_header = technical_header + collada_header + asset_header
            dae_file_writer.write(colladada_total_header)
            # LYBRARY_EFFECTS PROCESSING (ALMOST ALL THE STUFF HERE IS AS BLENDER DEFAULT)
            library_effect_start = f'  <library_effects>\n'
            dae_file_writer.write(library_effect_start)
            for number_effects in range(0, model_obj_num):
                effect_loop_1 = f'    <effect id="Object_Number_{number_effects}-effect">\n      <profile_COMMON>\n        <technique sid="common">\n          <lambert>\n            <emission>\n              <color sid="emission">0 0 0 1</color>\n            </emission>\n'
                effect_loop_2 = f'            <diffuse>\n              <color sid="diffuse">0.8 0.8 0.8 1</color>\n            </diffuse>\n            <index_of_refraction>\n              <float sid="ior">1.45</float>\n            </index_of_refraction>\n'
                effect_loop_3 = f'          </lambert>\n        </technique>\n      </profile_COMMON>\n    </effect>\n'
                effect_total = effect_loop_1 + effect_loop_2 + effect_loop_3
                dae_file_writer.write(effect_total)

            # LIBRARY_IMAGES/LIBRARY_MATERIALS PROCESSING (NOT IMPLEMENTED, SO WILL BE BLANK!)
            library_effect_end = f'  </library_effects>\n'
            library_images_blank = f'  <library_images/>\n'
            library_materials_start = f'  <library_materials>\n'
            library_default_together = library_effect_end + library_images_blank + library_materials_start
            dae_file_writer.write(library_default_together)
            for number_material in range(0, model_obj_num):
                material_loop = f'    <material id="Object_Number_{number_material}-material" name="Object_Number_{number_material}">\n      <instance_effect url="#Object_Number_{number_material}-effect"/>\n    </material>\n'
                dae_file_writer.write(material_loop)
            library_materials_end = f'  </library_materials>\n'
            dae_file_writer.write(library_materials_end)

            # LIBRARY_GEOMETRIES PROCESSING (HERE IS WHERE THE FILE GET INTERESTING)
            library_geometries_start = f'  <library_geometries>\n'
            dae_file_writer.write(library_geometries_start)

            for number_geometry in range(0, model_obj_num): # THIS WRITE THE CURRENT OBJECT ARRAYS (VERTEX, FACES, NORMALS, ETC)
                geometry_loop_1 = f'    <geometry id="Object_Number_{number_geometry}-mesh" name="Object_Number_{number_geometry}">\n      <mesh>\n'
                dae_file_writer.write(geometry_loop_1)
                """from here i have to write each mesh as source id = Object_Number_0-mesh-positions; 
                Object_Number_0-vert-colors; Object_Number_0-mesh-normals ; Object_Number_0-mesh-map-0 ; 
                mesh-colors-Col ; Object_Number_0-mesh-vertices // polylist"""

                # source id = Object_Number_n-mesh-positions
                mesh_positions = collada_vertex_positions[number_geometry] #CURRENT VERTEX BLOCK IN THE CURRENT NUMBER OF OBJECT
                mesh_positions_length = len(mesh_positions) * 3 # full count of vertex (so 1 vertex = 3 values [x, y, z)])
                mesh_position_source_write = f'        <source id="Object_Number_{number_geometry}-mesh-positions">\n          <float_array id="Object_Number_{number_geometry}-mesh-positions-array" count="{mesh_positions_length}">'
                dae_file_writer.write(mesh_position_source_write)
                for vertex_in_array in collada_vertex_positions[number_geometry]: # THIS WRITE THE CURRENT OBJECT VERTEX ARRAY (SOURCE ID POSITIONS)
                    if vertex_in_array == 0: #TODO THIS IS ONLY A SIMPLE WORKAROUND UNTIL I WRITE A PROPER PRIMITIVE INDEX FIXER
                        vertex_val_x = 0.0
                        vertex_val_y = 0.0
                        vertex_val_z = 0.0
                        vertex_array = f'{vertex_val_x} {vertex_val_y} {vertex_val_z} '
                        dae_file_writer.write(vertex_array)
                    else:
                        vertex_val_x = (vertex_in_array[0] / 1000)
                        vertex_val_y = (vertex_in_array[1] / 1000)
                        vertex_val_z = (vertex_in_array[2] / 1000)
                        vertex_array = f'{vertex_val_x} {vertex_val_y} {vertex_val_z} '
                        dae_file_writer.write(vertex_array)
                positions_float_array_end = f'</float_array>\n'
                dae_file_writer.write(positions_float_array_end)
                vertex_array_length = len(mesh_positions)
                technique_common_loop_1 = f'          <technique_common>\n            <accessor source="#Object_Number_{number_geometry}-mesh-positions-array" count="{vertex_array_length}" stride="3">\n              <param name="X" type="float"/>\n              <param name="Y" type="float"/>\n              <param name="Z" type="float"/>\n            </accessor>\n          </technique_common>\n'
                dae_file_writer.write(technique_common_loop_1)
                position_source_end = f'        </source>\n'
                dae_file_writer.write(position_source_end)

                #  source id = Object_Number_n-mesh-normals

                mesh_normals = collada_normal[number_geometry]
                mesh_normals_length = len(mesh_normals) * 3 # full count of normals (so 1 normal = 3 values [x, y, z)])
                mesh_normals_source_write = f'        <source id="Object_Number_{number_geometry}-mesh-normals">\n          <float_array id="Object_Number_{number_geometry}-mesh-normals-array" count="{mesh_normals_length}">'
                dae_file_writer.write(mesh_normals_source_write)
                for normal_in_array in collada_normal[number_geometry]:
                    normal_val_x = (normal_in_array[0] / 1000)
                    normal_val_y = (normal_in_array[1] / 1000)
                    normal_val_z = (normal_in_array[2] / 1000)
                    normal_array = f'{normal_val_x} {normal_val_y} {normal_val_z} '
                    dae_file_writer.write(normal_array)
                normals_float_array_end = f'</float_array>\n'
                dae_file_writer.write(normals_float_array_end)
                normals_array_length = len(mesh_normals)
                technique_common_loop_2 = f'          <technique_common>\n            <accessor source="#Object_Number_{number_geometry}-mesh-normals-array" count="{normals_array_length}" stride="3">\n              <param name="X" type="float"/>\n              <param name="Y" type="float"/>\n              <param name="Z" type="float"/>\n            </accessor>\n          </technique_common>\n'
                dae_file_writer.write(technique_common_loop_2)
                normals_source_end =  f'        </source>\n'
                dae_file_writer.write(normals_source_end)

                # source id = Object_Number_0-mesh-map-0 
                mesh_maps = collada_uv[number_geometry]
                mesh_maps_length = len(mesh_maps)
                mesh_maps_length_row = []
                for uv_map_number in mesh_maps:
                    number_uv = len(uv_map_number)
                    mesh_maps_length_row.append(number_uv)
                mesh_maps_row_sum = sum(mesh_maps_length_row)
                mesh_maps_source_write = f'        <source id="Object_Number_{number_geometry}-mesh-map-0">\n          <float_array id="Object_Number_{number_geometry}-mesh-map-0-array" count="{mesh_maps_row_sum}">'
                dae_file_writer.write(mesh_maps_source_write)
                if mesh_maps == []: #TODO THIS IS ALREADY FIXED?
                    uv_zero_write = f'{0.0} {0.0} '
                    dae_file_writer.write(uv_zero_write)
                else:
                    for uv_map in mesh_maps:
                            for uv_m in uv_map:
                                uv_to_write = f'{uv_m} '
                                dae_file_writer.write(uv_to_write)
                uv_float_array_end = f'</float_array>\n'
                dae_file_writer.write(uv_float_array_end)
                technique_common_loop_maps = f'          <technique_common>\n            <accessor source="#Object_Number_{number_geometry}-mesh-map-0-array" count="{int(mesh_maps_row_sum / 2)}" stride="2">\n              <param name="S" type="float"/>\n              <param name="T" type="float"/>\n            </accessor>\n          </technique_common>\n'
                dae_file_writer.write(technique_common_loop_maps)
                maps_source_end = f'        </source>\n'
                dae_file_writer.write(maps_source_end)

                #  source id = Object_Number_n-vert-colors
                mesh_colors = collada_vertex_color[number_geometry]
                mesh_colors_length = len(mesh_colors)
                mesh_colors_length_row = []
                for color_length in mesh_colors:
                    color_numeration = len(color_length)
                    mesh_colors_length_row.append(color_numeration)
                
                mesh_colors_length_row_sum = sum(mesh_colors_length_row)
                mesh_colors_source_write = f'        <source id="Object_Number_{number_geometry}-mesh-colors-Col{number_geometry}" name="Col{number_geometry}">\n          <float_array id="Object_Number_{number_geometry}-mesh-colors-Col{number_geometry}-array" count="{mesh_colors_length_row_sum}">'
                dae_file_writer.write(mesh_colors_source_write)

                for vcolor_in_array in collada_vertex_color[number_geometry]:
                    vcolor_array_write = f'{vcolor_in_array} '.replace("(","").replace(")","").replace(",","")
                    dae_file_writer.write(vcolor_array_write)

                colors_float_array_end = f'</float_array>\n'
                dae_file_writer.write(colors_float_array_end)
                technique_common_loop_colors = f'          <technique_common>\n            <accessor source="#Object_Number_{number_geometry}-mesh-colors-Col{number_geometry}-array" count="{mesh_colors_length}" stride="4">\n              <param name="R" type="float"/>\n              <param name="G" type="float"/>\n              <param name="B" type="float"/>\n              <param name="A" type="float"/>\n            </accessor>\n          </technique_common>\n'
                dae_file_writer.write(technique_common_loop_colors)
                colors_source_end = f'        </source>\n'
                dae_file_writer.write(colors_source_end)

                # Vertices ID
                vertices_id_legend = f'        <vertices id="Object_Number_{number_geometry}-mesh-vertices">\n          <input semantic="POSITION" source="#Object_Number_{number_geometry}-mesh-positions"/>\n        </vertices>\n'
                dae_file_writer.write(vertices_id_legend)

                # POLYLIST MATERIAL - header
                current_quantity_primitives = number_primitive[number_geometry]
                polylist_mat_header = f'        <polylist material="Object_Number_{number_geometry}-material" count="{current_quantity_primitives}">\n'
                polylist_mat_header_row_0 = f'          <input semantic="VERTEX" source="#Object_Number_{number_geometry}-mesh-vertices" offset="0"/>\n'
                polylist_mat_header_row_1 = f'          <input semantic="NORMAL" source="#Object_Number_{number_geometry}-mesh-normals" offset="1"/>\n'
                polylist_mat_header_row_2 = f'          <input semantic="TEXCOORD" source="#Object_Number_{number_geometry}-mesh-map-0" offset="2" set="0"/>\n'
                polylist_mat_header_row_3 = f'          <input semantic="COLOR" source="#Object_Number_{number_geometry}-mesh-colors-Col{number_geometry}" offset="3" set="0"/>\n'
                dae_file_writer.write(polylist_mat_header)
                dae_file_writer.write(polylist_mat_header_row_0)
                dae_file_writer.write(polylist_mat_header_row_1)
                dae_file_writer.write(polylist_mat_header_row_2)
                dae_file_writer.write(polylist_mat_header_row_3)

                # v-count
                v_count_start = f'          <vcount>'
                dae_file_writer.write(v_count_start)
                collada_v_count = collada_polygon[number_geometry]
                for v_count_array in collada_v_count:
                    v_count_write = f'{v_count_array} '
                    dae_file_writer.write(v_count_write)
                v_count_end = f'</vcount>\n'
                dae_file_writer.write(v_count_end)

                # p-array
                p_start = f'          <p>'
                dae_file_writer.write(p_start)
                # loop for the p-array
                for array_ready in collada_p_array[number_geometry]:
                    p_data = f'{array_ready} '
                    dae_file_writer.write(p_data)

                p_end = f'</p>\n'
                dae_file_writer.write(p_end)
                polylist_mat_end = f'        </polylist>\n'
                dae_file_writer.write(polylist_mat_end)                  

                # THIS IS THE VERY END OF THE GEOMETRY LIBRARY BEFORE END THE FILE
                geometry_loop_end = f'      </mesh>\n'
                dae_file_writer.write(geometry_loop_end)
                current_geometry_end = f'    </geometry>\n'
                dae_file_writer.write(current_geometry_end)
            
            library_geometries_end = f'  </library_geometries>\n'
            dae_file_writer.write(library_geometries_end)

            if animation_bool == True:
                # LIBRARY_ANIMATIONS - HERE GOES THE DATA FROM ANIMATION FILE PROCESS
                library_animations_header = f'  <library_animations>\n'
                dae_file_writer.write(library_animations_header)
                total_keyframes = collada_animation_flag[1] # SAF/CMB/LMB SEEMS TO BE WORKING
                time_keyframe = 3 / 60
                for obj_anm_number in range(0, model_obj_num):
                    library_animations_loop = f'    <animation id="action_container-Object_Number_{obj_anm_number}" name="Object_Number_{obj_anm_number}">\n'
                    dae_file_writer.write(library_animations_loop)

                    ######################################### LOCATION #########################################
                    ######################################### LOCATION #########################################

                    ########### Location X ###########
                    ########### Location X ###########
                    obj_rot_loc_nesting_x = f'      <animation id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_X" name="Object_Number_{obj_anm_number}">\n'
                    dae_file_writer.write(obj_rot_loc_nesting_x)

                    # Translation / Location X - input
                    obj_transx_input = f'        <source id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_X-input">\n'
                    dae_file_writer.write(obj_transx_input)
                    obj_transx_input_array = f'          <float_array id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_X-input-array" count="{total_keyframes}">'
                    dae_file_writer.write(obj_transx_input_array)
                    frame_count_num = 0
                    t_keyframes = total_keyframes
                    while t_keyframes > 0:
                        number_consecutive_frame = f'{frame_count_num} '
                        dae_file_writer.write(number_consecutive_frame)
                        frame_count_num += time_keyframe
                        t_keyframes -= 1
                    obj_transx_input_array_end = f'</float_array>\n'
                    dae_file_writer.write(obj_transx_input_array_end)

                    technique_common_transx_in_start = f'          <technique_common>\n            <accessor source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_X-input-array" count="{total_keyframes}" stride="1">\n'
                    technique_common_transx_in_end = f'              <param name="TIME" type="float"/>\n            </accessor>\n          </technique_common>\n'
                    dae_file_writer.write(technique_common_transx_in_start)
                    dae_file_writer.write(technique_common_transx_in_end)
                    obj_transx_end = f'        </source>\n'
                    dae_file_writer.write(obj_transx_end)

                    # Translation / Location X - output
                    obj_transx_output = f'        <source id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_X-output">\n'
                    obj_transx_output_array = f'          <float_array id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_X-output-array" count="{total_keyframes}">'
                    dae_file_writer.write(obj_transx_output)
                    dae_file_writer.write(obj_transx_output_array)                
                    for key_frame, rot_loc in collada_animation:
                        current_object_animation = rot_loc[obj_anm_number]
                        current_anim_noobj = current_object_animation[1:2]
                        for trans_x in current_anim_noobj:
                            translation_x = trans_x.get("Tx")
                            translation_x_str = f'{translation_x} '
                            dae_file_writer.write(translation_x_str)
                    obj_transx_output_array_end = f'</float_array>\n'
                    dae_file_writer.write(obj_transx_output_array_end)
                    technique_common_transx_out = f'          <technique_common>\n            <accessor source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_X-output-array" count="{total_keyframes}" stride="1">\n              <param name="X" type="float"/>\n            </accessor>\n          </technique_common>\n'
                    dae_file_writer.write(technique_common_transx_out)
                    obj_transx_output_end = f'        </source>\n'
                    dae_file_writer.write(obj_transx_output_end)

                    #Translation / Location X - interpolation
                    obj_transx_inter = f'        <source id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_X-interpolation">\n'
                    obj_transx_inter_na = f'          <Name_array id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_X-interpolation-array" count="{total_keyframes}">'
                    dae_file_writer.write(obj_transx_inter)
                    dae_file_writer.write(obj_transx_inter_na)
                    #linear algorithm to repeat the N number of Keyframes
                    t_k_inter = total_keyframes
                    while t_k_inter > 0:
                        lin_str = f'LINEAR '
                        dae_file_writer.write(lin_str)
                        t_k_inter -= 1
                    obj_transx_inter_na_end = f'</Name_array>\n'
                    dae_file_writer.write(obj_transx_inter_na_end)
                    technique_common_transx_interp = f'          <technique_common>\n            <accessor source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_X-interpolation-array" count="{total_keyframes}" stride="1">\n              <param name="INTERPOLATION" type="name"/>\n            </accessor>\n          </technique_common>\n        </source>\n'
                    dae_file_writer.write(technique_common_transx_interp) # also close the source opener

                    # Translation / Location X - sampler
                    obj_transx_sampler_start = f'        <sampler id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_X-sampler">\n'
                    obj_transx_sem_1 = f'          <input semantic="INPUT" source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_X-input"/>\n'
                    obj_transx_sem_2 = f'          <input semantic="OUTPUT" source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_X-output"/>\n'
                    obj_transx_sem_3 = f'          <input semantic="INTERPOLATION" source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_X-interpolation"/>\n'
                    obj_transx_sampler_end = f'        </sampler>\n'
                    dae_file_writer.write(obj_transx_sampler_start)
                    dae_file_writer.write(obj_transx_sem_1)
                    dae_file_writer.write(obj_transx_sem_2)
                    dae_file_writer.write(obj_transx_sem_3)
                    dae_file_writer.write(obj_transx_sampler_end)

                    # Translation / Location X - channel
                    obj_transx_channel = f'        <channel source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_X-sampler" target="Object_Number_{obj_anm_number}/location.X"/>\n'
                    dae_file_writer.write(obj_transx_channel)

                    obj_rot_loc_nesting_end = f'      </animation>\n' #End of nesting
                    dae_file_writer.write(obj_rot_loc_nesting_end)
                    ########### Location X ###########
                    ########### Location X ###########

                    ########### Location Y ###########
                    ########### Location Y ###########
                    obj_rot_loc_nesting_y = f'      <animation id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_Y" name="Object_Number_{obj_anm_number}">\n'
                    dae_file_writer.write(obj_rot_loc_nesting_y)

                    # Translation / Location Y - input
                    obj_transy_input = f'        <source id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_Y-input">\n'
                    dae_file_writer.write(obj_transy_input)
                    obj_transy_input_array = f'          <float_array id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_Y-input-array" count="{total_keyframes}">'
                    dae_file_writer.write(obj_transy_input_array)
                    frame_count_num = 0
                    t_keyframes = total_keyframes
                    while t_keyframes > 0:
                        number_consecutive_frame = f'{frame_count_num} '
                        dae_file_writer.write(number_consecutive_frame)
                        frame_count_num += time_keyframe
                        t_keyframes -= 1
                    obj_transy_input_array_end = f'</float_array>\n'
                    dae_file_writer.write(obj_transy_input_array_end)

                    technique_common_transy_in_start = f'          <technique_common>\n            <accessor source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_Y-input-array" count="{total_keyframes}" stride="1">\n'
                    technique_common_transy_in_end = f'              <param name="TIME" type="float"/>\n            </accessor>\n          </technique_common>\n'
                    dae_file_writer.write(technique_common_transy_in_start)
                    dae_file_writer.write(technique_common_transy_in_end)
                    obj_transy_end = f'        </source>\n'
                    dae_file_writer.write(obj_transy_end)

                    # Translation / Location Y - output
                    obj_transy_output = f'        <source id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_Y-output">\n'
                    obj_transy_output_array = f'          <float_array id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_Y-output-array" count="{total_keyframes}">'
                    dae_file_writer.write(obj_transy_output)
                    dae_file_writer.write(obj_transy_output_array)                
                    for key_frame, rot_loc in collada_animation:
                        current_object_animation = rot_loc[obj_anm_number]
                        current_anim_noobj = current_object_animation[1:2]
                        for trans_y in current_anim_noobj:
                            translation_y = trans_y.get("Ty")
                            translation_y_str = f'{translation_y} '
                            dae_file_writer.write(translation_y_str)
                    obj_transy_output_array_end = f'</float_array>\n'
                    dae_file_writer.write(obj_transy_output_array_end)
                    technique_common_transy_out = f'          <technique_common>\n            <accessor source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_Y-output-array" count="{total_keyframes}" stride="1">\n              <param name="Y" type="float"/>\n            </accessor>\n          </technique_common>\n'
                    dae_file_writer.write(technique_common_transy_out)
                    obj_transy_output_end = f'        </source>\n'
                    dae_file_writer.write(obj_transy_output_end)

                    #Translation / Location Y - interpolation
                    obj_transy_inter = f'        <source id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_Y-interpolation">\n'
                    obj_transy_inter_na = f'          <Name_array id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_Y-interpolation-array" count="{total_keyframes}">'
                    dae_file_writer.write(obj_transy_inter)
                    dae_file_writer.write(obj_transy_inter_na)
                    #linear algorithm to repeat the N number of Keyframes
                    t_k_inter = total_keyframes
                    while t_k_inter > 0:
                        lin_str = f'LINEAR '
                        dae_file_writer.write(lin_str)
                        t_k_inter -= 1
                    obj_transy_inter_na_end = f'</Name_array>\n'
                    dae_file_writer.write(obj_transy_inter_na_end)
                    technique_common_transy_interp = f'          <technique_common>\n            <accessor source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_Y-interpolation-array" count="{total_keyframes}" stride="1">\n              <param name="INTERPOLATION" type="name"/>\n            </accessor>\n          </technique_common>\n        </source>\n'
                    dae_file_writer.write(technique_common_transy_interp) # also close the source opener

                    # Translation / Location Y - sampler
                    obj_transy_sampler_start = f'        <sampler id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_Y-sampler">\n'
                    obj_transy_sem_1 = f'          <input semantic="INPUT" source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_Y-input"/>\n'
                    obj_transy_sem_2 = f'          <input semantic="OUTPUT" source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_Y-output"/>\n'
                    obj_transy_sem_3 = f'          <input semantic="INTERPOLATION" source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_Y-interpolation"/>\n'
                    obj_transy_sampler_end = f'        </sampler>\n'
                    dae_file_writer.write(obj_transy_sampler_start)
                    dae_file_writer.write(obj_transy_sem_1)
                    dae_file_writer.write(obj_transy_sem_2)
                    dae_file_writer.write(obj_transy_sem_3)
                    dae_file_writer.write(obj_transy_sampler_end)

                    # Translation / Location Y - channel
                    obj_transy_channel = f'        <channel source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_Y-sampler" target="Object_Number_{obj_anm_number}/location.Y"/>\n'
                    dae_file_writer.write(obj_transy_channel)

                    obj_rot_loc_nesting_end = f'      </animation>\n' #End of nesting
                    dae_file_writer.write(obj_rot_loc_nesting_end)
                    ########### Location Y ###########
                    ########### Location Y ###########

                    ########### Location Z ###########
                    ########### Location Z ###########
                    obj_rot_loc_nesting_z = f'      <animation id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_Z" name="Object_Number_{obj_anm_number}">\n'
                    dae_file_writer.write(obj_rot_loc_nesting_z)

                    # Translation / Location Z - input
                    obj_transz_input = f'        <source id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_Z-input">\n'
                    dae_file_writer.write(obj_transz_input)
                    obj_transz_input_array = f'          <float_array id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_Z-input-array" count="{total_keyframes}">'
                    dae_file_writer.write(obj_transz_input_array)
                    frame_count_num = 0
                    t_keyframes = total_keyframes
                    while t_keyframes > 0:
                        number_consecutive_frame = f'{frame_count_num} '
                        dae_file_writer.write(number_consecutive_frame)
                        frame_count_num += time_keyframe
                        t_keyframes -= 1
                    obj_transz_input_array_end = f'</float_array>\n'
                    dae_file_writer.write(obj_transz_input_array_end)

                    technique_common_transz_in_start = f'          <technique_common>\n            <accessor source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_Z-input-array" count="{total_keyframes}" stride="1">\n'
                    technique_common_transz_in_end = f'              <param name="TIME" type="float"/>\n            </accessor>\n          </technique_common>\n'
                    dae_file_writer.write(technique_common_transz_in_start)
                    dae_file_writer.write(technique_common_transz_in_end)
                    obj_transz_end = f'        </source>\n'
                    dae_file_writer.write(obj_transz_end)

                    # Translation / Location Z - output
                    obj_transz_output = f'        <source id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_Z-output">\n'
                    obj_transz_output_array = f'          <float_array id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_Z-output-array" count="{total_keyframes}">'
                    dae_file_writer.write(obj_transz_output)
                    dae_file_writer.write(obj_transz_output_array)                
                    for key_frame, rot_loc in collada_animation:
                        current_object_animation = rot_loc[obj_anm_number]
                        current_anim_noobj = current_object_animation[1:2]
                        for trans_z in current_anim_noobj:
                            translation_z = trans_z.get("Tz")
                            translation_z_str = f'{translation_z} '
                            dae_file_writer.write(translation_z_str)
                    obj_transz_output_array_end = f'</float_array>\n'
                    dae_file_writer.write(obj_transz_output_array_end)
                    technique_common_transz_out = f'          <technique_common>\n            <accessor source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_Z-output-array" count="{total_keyframes}" stride="1">\n              <param name="Z" type="float"/>\n            </accessor>\n          </technique_common>\n'
                    dae_file_writer.write(technique_common_transz_out)
                    obj_transz_output_end = f'        </source>\n'
                    dae_file_writer.write(obj_transz_output_end)

                    #Translation / Location Z - interpolation
                    obj_transz_inter = f'        <source id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_Z-interpolation">\n'
                    obj_transz_inter_na = f'          <Name_array id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_Z-interpolation-array" count="{total_keyframes}">'
                    dae_file_writer.write(obj_transz_inter)
                    dae_file_writer.write(obj_transz_inter_na)
                    #linear algorithm to repeat the N number of Keyframes
                    t_k_inter = total_keyframes
                    while t_k_inter > 0:
                        lin_str = f'LINEAR '
                        dae_file_writer.write(lin_str)
                        t_k_inter -= 1
                    obj_transz_inter_na_end = f'</Name_array>\n'
                    dae_file_writer.write(obj_transz_inter_na_end)
                    technique_common_transz_interp = f'          <technique_common>\n            <accessor source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_Z-interpolation-array" count="{total_keyframes}" stride="1">\n              <param name="INTERPOLATION" type="name"/>\n            </accessor>\n          </technique_common>\n        </source>\n'
                    dae_file_writer.write(technique_common_transz_interp) # also close the source opener

                    # Translation / Location Z - sampler
                    obj_transz_sampler_start = f'        <sampler id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_Z-sampler">\n'
                    obj_transz_sem_1 = f'          <input semantic="INPUT" source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_Z-input"/>\n'
                    obj_transz_sem_2 = f'          <input semantic="OUTPUT" source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_Z-output"/>\n'
                    obj_transz_sem_3 = f'          <input semantic="INTERPOLATION" source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_Z-interpolation"/>\n'
                    obj_transz_sampler_end = f'        </sampler>\n'
                    dae_file_writer.write(obj_transz_sampler_start)
                    dae_file_writer.write(obj_transz_sem_1)
                    dae_file_writer.write(obj_transz_sem_2)
                    dae_file_writer.write(obj_transz_sem_3)
                    dae_file_writer.write(obj_transz_sampler_end)

                    # Translation / Location Z - channel
                    obj_transz_channel = f'        <channel source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_location_Z-sampler" target="Object_Number_{obj_anm_number}/location.Z"/>\n'
                    dae_file_writer.write(obj_transz_channel)

                    obj_rot_loc_nesting_end = f'      </animation>\n' #End of nesting
                    dae_file_writer.write(obj_rot_loc_nesting_end)
                    ########### Location Z ###########
                    ########### Location Z ###########

                    ######################################### ROTATION #########################################
                    ######################################### ROTATION #########################################
                    #"""

                    ########### Rotation X ###########
                    ########### Rotation X ###########
                    obj_rot_loc_nesting_rx = f'      <animation id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_X" name="Object_Number_{obj_anm_number}">\n'
                    dae_file_writer.write(obj_rot_loc_nesting_rx)

                    # Rotation X - input
                    obj_rotx_input = f'        <source id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_X-input">\n'
                    dae_file_writer.write(obj_rotx_input)
                    obj_rotx_input_array = f'          <float_array id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_X-input-array" count="{total_keyframes}">'
                    dae_file_writer.write(obj_rotx_input_array)
                    frame_count_num = 0
                    t_keyframes = total_keyframes
                    while t_keyframes > 0:
                        number_consecutive_frame = f'{frame_count_num} '
                        dae_file_writer.write(number_consecutive_frame)
                        frame_count_num += time_keyframe
                        t_keyframes -= 1
                    obj_rotx_input_array_end = f'</float_array>\n'
                    dae_file_writer.write(obj_rotx_input_array_end)

                    technique_common_rotx_in_start = f'          <technique_common>\n            <accessor source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_X-input-array" count="{total_keyframes}" stride="1">\n'
                    technique_common_rotx_in_end = f'              <param name="TIME" type="float"/>\n            </accessor>\n          </technique_common>\n'
                    dae_file_writer.write(technique_common_rotx_in_start)
                    dae_file_writer.write(technique_common_rotx_in_end)
                    obj_rotx_end = f'        </source>\n'
                    dae_file_writer.write(obj_rotx_end)

                    # Rotation X - output
                    obj_rotx_output = f'        <source id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_X-output">\n'
                    obj_rotx_output_array = f'          <float_array id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_X-output-array" count="{total_keyframes}">'
                    dae_file_writer.write(obj_rotx_output)
                    dae_file_writer.write(obj_rotx_output_array)                
                    for key_frame, rot_loc in collada_animation:
                        current_object_animation = rot_loc[obj_anm_number]
                        current_anim_noobj = current_object_animation[1:2]
                        for rot_x in current_anim_noobj:
                            rotation_x = rot_x.get("Rx")
                            rotation_x_str = f'{rotation_x} '
                            dae_file_writer.write(rotation_x_str)
                    obj_rotx_output_array_end = f'</float_array>\n'
                    dae_file_writer.write(obj_rotx_output_array_end)
                    technique_common_rotx_out = f'          <technique_common>\n            <accessor source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_X-output-array" count="{total_keyframes}" stride="1">\n              <param name="ANGLE" type="float"/>\n            </accessor>\n          </technique_common>\n'
                    dae_file_writer.write(technique_common_rotx_out)
                    obj_rotx_output_end = f'        </source>\n'
                    dae_file_writer.write(obj_rotx_output_end)

                    # Rotation X - interpolation
                    obj_rotx_inter = f'        <source id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_X-interpolation">\n'
                    obj_rotx_inter_na = f'          <Name_array id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_X-interpolation-array" count="{total_keyframes}">'
                    dae_file_writer.write(obj_rotx_inter)
                    dae_file_writer.write(obj_rotx_inter_na)
                    #linear algorithm to repeat the N number of Keyframes
                    t_k_inter = total_keyframes
                    while t_k_inter > 0:
                        lin_str = f'LINEAR '
                        dae_file_writer.write(lin_str)
                        t_k_inter -= 1
                    obj_rotx_inter_na_end = f'</Name_array>\n'
                    dae_file_writer.write(obj_rotx_inter_na_end)
                    technique_common_rotx_interp = f'          <technique_common>\n            <accessor source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_X-interpolation-array" count="{total_keyframes}" stride="1">\n              <param name="INTERPOLATION" type="name"/>\n            </accessor>\n          </technique_common>\n        </source>\n'
                    dae_file_writer.write(technique_common_rotx_interp) # also close the source opener

                    # Rotation X - sampler
                    obj_rotx_sampler_start = f'        <sampler id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_X-sampler">\n'
                    obj_rotx_sem_1 = f'          <input semantic="INPUT" source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_X-input"/>\n'
                    obj_rotx_sem_2 = f'          <input semantic="OUTPUT" source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_X-output"/>\n'
                    obj_rotx_sem_3 = f'          <input semantic="INTERPOLATION" source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_X-interpolation"/>\n'
                    obj_rotx_sampler_end = f'        </sampler>\n'
                    dae_file_writer.write(obj_rotx_sampler_start)
                    dae_file_writer.write(obj_rotx_sem_1)
                    dae_file_writer.write(obj_rotx_sem_2)
                    dae_file_writer.write(obj_rotx_sem_3)
                    dae_file_writer.write(obj_rotx_sampler_end)

                    # Rotation X - channel
                    obj_rotx_channel = f'        <channel source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_X-sampler" target="Object_Number_{obj_anm_number}/rotationX.ANGLE"/>\n'
                    dae_file_writer.write(obj_rotx_channel)

                    obj_rot_loc_nesting_end = f'      </animation>\n' #End of nesting
                    dae_file_writer.write(obj_rot_loc_nesting_end)
                    ########### Rotation X ###########
                    ########### Rotation X ###########

                    ########### Rotation Y ###########
                    ########### Rotation Y ###########
                    obj_rot_loc_nesting_ry = f'      <animation id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_Y" name="Object_Number_{obj_anm_number}">\n'
                    dae_file_writer.write(obj_rot_loc_nesting_ry)

                    # Rotation Y - input
                    obj_roty_input = f'        <source id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_Y-input">\n'
                    dae_file_writer.write(obj_roty_input)
                    obj_roty_input_array = f'          <float_array id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_Y-input-array" count="{total_keyframes}">'
                    dae_file_writer.write(obj_roty_input_array)
                    frame_count_num = 0
                    t_keyframes = total_keyframes
                    while t_keyframes > 0:
                        number_consecutive_frame = f'{frame_count_num} '
                        dae_file_writer.write(number_consecutive_frame)
                        frame_count_num += time_keyframe
                        t_keyframes -= 1
                    obj_roty_input_array_end = f'</float_array>\n'
                    dae_file_writer.write(obj_roty_input_array_end)

                    technique_common_roty_in_start = f'          <technique_common>\n            <accessor source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_Y-input-array" count="{total_keyframes}" stride="1">\n'
                    technique_common_roty_in_end = f'              <param name="TIME" type="float"/>\n            </accessor>\n          </technique_common>\n'
                    dae_file_writer.write(technique_common_roty_in_start)
                    dae_file_writer.write(technique_common_roty_in_end)
                    obj_roty_end = f'        </source>\n'
                    dae_file_writer.write(obj_roty_end)

                    # Rotation Y - output
                    obj_roty_output = f'        <source id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_Y-output">\n'
                    obj_roty_output_array = f'          <float_array id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_Y-output-array" count="{total_keyframes}">'
                    dae_file_writer.write(obj_roty_output)
                    dae_file_writer.write(obj_roty_output_array)                
                    for key_frame, rot_loc in collada_animation:
                        current_object_animation = rot_loc[obj_anm_number]
                        current_anim_noobj = current_object_animation[1:2]
                        for rot_y in current_anim_noobj:
                            rotation_y = rot_y.get("Ry")
                            rotation_y_str = f'{rotation_y} '
                            dae_file_writer.write(rotation_y_str)
                    obj_roty_output_array_end = f'</float_array>\n'
                    dae_file_writer.write(obj_roty_output_array_end)
                    technique_common_roty_out = f'          <technique_common>\n            <accessor source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_Y-output-array" count="{total_keyframes}" stride="1">\n              <param name="ANGLE" type="float"/>\n            </accessor>\n          </technique_common>\n'
                    dae_file_writer.write(technique_common_roty_out)
                    obj_roty_output_end = f'        </source>\n'
                    dae_file_writer.write(obj_roty_output_end)

                    # Rotation Y - interpolation
                    obj_roty_inter = f'        <source id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_Y-interpolation">\n'
                    obj_roty_inter_na = f'          <Name_array id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_Y-interpolation-array" count="{total_keyframes}">'
                    dae_file_writer.write(obj_roty_inter)
                    dae_file_writer.write(obj_roty_inter_na)
                    #linear algorithm to repeat the N number of Keyframes
                    t_k_inter = total_keyframes
                    while t_k_inter > 0:
                        lin_str = f'LINEAR '
                        dae_file_writer.write(lin_str)
                        t_k_inter -= 1
                    obj_roty_inter_na_end = f'</Name_array>\n'
                    dae_file_writer.write(obj_roty_inter_na_end)
                    technique_common_roty_interp = f'          <technique_common>\n            <accessor source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_Y-interpolation-array" count="{total_keyframes}" stride="1">\n              <param name="INTERPOLATION" type="name"/>\n            </accessor>\n          </technique_common>\n        </source>\n'
                    dae_file_writer.write(technique_common_roty_interp) # also close the source opener

                    # Rotation Y - sampler
                    obj_roty_sampler_start = f'        <sampler id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_Y-sampler">\n'
                    obj_roty_sem_1 = f'          <input semantic="INPUT" source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_Y-input"/>\n'
                    obj_roty_sem_2 = f'          <input semantic="OUTPUT" source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_Y-output"/>\n'
                    obj_roty_sem_3 = f'          <input semantic="INTERPOLATION" source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_Y-interpolation"/>\n'
                    obj_roty_sampler_end = f'        </sampler>\n'
                    dae_file_writer.write(obj_roty_sampler_start)
                    dae_file_writer.write(obj_roty_sem_1)
                    dae_file_writer.write(obj_roty_sem_2)
                    dae_file_writer.write(obj_roty_sem_3)
                    dae_file_writer.write(obj_roty_sampler_end)

                    # Rotation Y - channel
                    obj_roty_channel = f'        <channel source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_Y-sampler" target="Object_Number_{obj_anm_number}/rotationY.ANGLE"/>\n'
                    dae_file_writer.write(obj_roty_channel)

                    obj_rot_loc_nesting_end = f'      </animation>\n' #End of nesting
                    dae_file_writer.write(obj_rot_loc_nesting_end)
                    ########### Rotation Y ###########
                    ########### Rotation Y ###########

                    ########### Rotation Z ###########
                    ########### Rotation Z ###########
                    obj_rot_loc_nesting_rz = f'      <animation id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_Z" name="Object_Number_{obj_anm_number}">\n'
                    dae_file_writer.write(obj_rot_loc_nesting_rz)

                    # Rotation Z - input
                    obj_rotz_input = f'        <source id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_Z-input">\n'
                    dae_file_writer.write(obj_rotz_input)
                    obj_rotz_input_array = f'          <float_array id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_Z-input-array" count="{total_keyframes}">'
                    dae_file_writer.write(obj_rotz_input_array)
                    frame_count_num = 0
                    t_keyframes = total_keyframes
                    while t_keyframes > 0:
                        number_consecutive_frame = f'{frame_count_num} '
                        dae_file_writer.write(number_consecutive_frame)
                        frame_count_num += time_keyframe
                        t_keyframes -= 1
                    obj_rotz_input_array_end = f'</float_array>\n'
                    dae_file_writer.write(obj_rotz_input_array_end)

                    technique_common_rotz_in_start = f'          <technique_common>\n            <accessor source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_Z-input-array" count="{total_keyframes}" stride="1">\n'
                    technique_common_rotz_in_end = f'              <param name="TIME" type="float"/>\n            </accessor>\n          </technique_common>\n'
                    dae_file_writer.write(technique_common_rotz_in_start)
                    dae_file_writer.write(technique_common_rotz_in_end)
                    obj_rotz_end = f'        </source>\n'
                    dae_file_writer.write(obj_rotz_end)

                    # Rotation Z - output
                    obj_rotz_output = f'        <source id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_Z-output">\n'
                    obj_rotz_output_array = f'          <float_array id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_Z-output-array" count="{total_keyframes}">'
                    dae_file_writer.write(obj_rotz_output)
                    dae_file_writer.write(obj_rotz_output_array)                
                    for key_frame, rot_loc in collada_animation:
                        current_object_animation = rot_loc[obj_anm_number]
                        current_anim_noobj = current_object_animation[1:2]
                        for rot_z in current_anim_noobj:
                            rotation_z = rot_z.get("Rz")
                            rotation_z_str = f'{rotation_z} '
                            dae_file_writer.write(rotation_z_str)
                    obj_rotz_output_array_end = f'</float_array>\n'
                    dae_file_writer.write(obj_rotz_output_array_end)
                    technique_common_rotz_out = f'          <technique_common>\n            <accessor source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_Z-output-array" count="{total_keyframes}" stride="1">\n              <param name="ANGLE" type="float"/>\n            </accessor>\n          </technique_common>\n'
                    dae_file_writer.write(technique_common_rotz_out)
                    obj_rotz_output_end = f'        </source>\n'
                    dae_file_writer.write(obj_rotz_output_end)

                    # Rotation Z - interpolation
                    obj_rotz_inter = f'        <source id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_Z-interpolation">\n'
                    obj_rotz_inter_na = f'          <Name_array id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_Z-interpolation-array" count="{total_keyframes}">'
                    dae_file_writer.write(obj_rotz_inter)
                    dae_file_writer.write(obj_rotz_inter_na)
                    #linear algorithm to repeat the N number of Keyframes
                    t_k_inter = total_keyframes
                    while t_k_inter > 0:
                        lin_str = f'LINEAR '
                        dae_file_writer.write(lin_str)
                        t_k_inter -= 1
                    obj_rotz_inter_na_end = f'</Name_array>\n'
                    dae_file_writer.write(obj_rotz_inter_na_end)
                    technique_common_rotz_interp = f'          <technique_common>\n            <accessor source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_Z-interpolation-array" count="{total_keyframes}" stride="1">\n              <param name="INTERPOLATION" type="name"/>\n            </accessor>\n          </technique_common>\n        </source>\n'
                    dae_file_writer.write(technique_common_rotz_interp) # also close the source opener

                    # Rotation Z - sampler
                    obj_rotz_sampler_start = f'        <sampler id="Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_Z-sampler">\n'
                    obj_rotz_sem_1 = f'          <input semantic="INPUT" source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_Z-input"/>\n'
                    obj_rotz_sem_2 = f'          <input semantic="OUTPUT" source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_Z-output"/>\n'
                    obj_rotz_sem_3 = f'          <input semantic="INTERPOLATION" source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_Z-interpolation"/>\n'
                    obj_rotz_sampler_end = f'        </sampler>\n'
                    dae_file_writer.write(obj_rotz_sampler_start)
                    dae_file_writer.write(obj_rotz_sem_1)
                    dae_file_writer.write(obj_rotz_sem_2)
                    dae_file_writer.write(obj_rotz_sem_3)
                    dae_file_writer.write(obj_rotz_sampler_end)

                    # Rotation Z - channel
                    obj_rotz_channel = f'        <channel source="#Object_Number_{obj_anm_number}_Object_Number_{obj_anm_number}Action_002_rotation_euler_Z-sampler" target="Object_Number_{obj_anm_number}/rotationZ.ANGLE"/>\n'
                    dae_file_writer.write(obj_rotz_channel)

                    obj_rot_loc_nesting_end = f'      </animation>\n' #End of nesting
                    dae_file_writer.write(obj_rot_loc_nesting_end)
                    ########### Rotation Z ###########
                    ########### Rotation Z ###########

                    obj_anm_end = f'    </animation>\n'
                    dae_file_writer.write(obj_anm_end)

                library_animations_end = f'  </library_animations>\n'
                dae_file_writer.write(library_animations_end)

            # LIBRARY_VISUAL_SCENE (JUST DEFAULT AS BLENDER EXAMPLE)
            library_visual_scene_header = f'  <library_visual_scenes>\n    <visual_scene id="Scene" name="Scene">\n'
            dae_file_writer.write(library_visual_scene_header)
            for library_number in range(0, model_obj_num):
                library_visual_scene_loop = f'      <node id="Object_Number_{library_number}" name="Object_Number_{library_number}" type="NODE">\n        <scale sid="scale">1 1 1</scale>\n        <rotate sid="rotationZ">0 0 1 0</rotate>\n        <rotate sid="rotationY">0 1 0 0</rotate>\n        <rotate sid="rotationX">1 0 0 90.00001</rotate>\n        <translate sid="location">0 0 0</translate>\n        <instance_geometry url="#Object_Number_{library_number}-mesh" name="Object_Number_{library_number}">\n          <bind_material>\n            <technique_common>\n              <instance_material symbol="Object_Number_{library_number}-material" target="#Object_Number_{library_number}-material">\n                <bind_vertex_input semantic="UVMap" input_semantic="TEXCOORD" input_set="0"/>\n              </instance_material>\n            </technique_common>\n          </bind_material>\n        </instance_geometry>\n      </node>\n'
                dae_file_writer.write(library_visual_scene_loop)
            library_visual_scene_end = f'    </visual_scene>\n  </library_visual_scenes>\n'
            dae_file_writer.write(library_visual_scene_end)


            # SCENE (JUST DEFAULT AS BLENDER EXAMPLE) // END OF THE FILE WITH </COLLADA>
            scene_write = f'  <scene>\n    <instance_visual_scene url="#Scene"/>\n  </scene>\n'
            collada_end_of_file = f'</COLLADA>'
            end_of_file = scene_write + collada_end_of_file
            dae_file_writer.write(end_of_file)
        global collada_success
        collada_success = f'Collada File successfully converted...'
    
    @staticmethod
    def check_animation(animation_flag=list):
        animation_type = animation_flag[2]
        anim_bool = False
        if (animation_type != f'NONE'):
            anim_bool = True
        return anim_bool