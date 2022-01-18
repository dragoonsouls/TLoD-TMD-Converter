"""

Standard TMD Structure Collada Exporter: This module write the Standard TMD structure data into
Collada File Format (*.dae)
Since i have no experience in this kind of files, this module it would too experimental,
expect a lot of bugs, errors, and nonsense data extracted or unused variables/values

Copyright (C) 2021 DooMMetaL

"""
from itertools import zip_longest
import os
import datetime
import standard_tmd_decoder
import standard_tmd_writer
import standard_tmd
import standard_tmd_structure


class ColladaFileWriter:
    def __init__(self, dae_conversion):
        self.self = self
        self.dae_conversion = dae_conversion
    
    def dae_from_obj(self):
        """ # this is not implemented because the Collada Format seems to be more stable and easy to trace errors on the code
        try:
            print(f'Would you like to convert the TMD into DAE file? (experimental)\n' f'yes for continue, no for finish')
            key_select = input()
            if key_select == f'yes' or f'y' or f'YES':
                print(f'TMD file: {standard_tmd_writer.file_name}, is being converted to *.dae')
            elif key_select == f'no' or f'n' or f'NO':
                print("Exiting the tool...")
                exit()
            else:
                print("Not a valid choice, exiting...")
                exit()
        except OSError:
            print("Not a valid option, exiting....")
            exit()
        """

        """ DAE FILE FORMAT (USING AS EXAMPLE THE BLENDER GENERATED FILE)
        |   
        |   LOOK INTO THE DOCUMENTATION ABOUT DAE FILE FORMAT
        |
        """
        date_conversion = datetime.datetime.now().isoformat(timespec='milliseconds')

        #-------------------------------------- PRECONVERSION OF DATA FOR COLLADA FILES --------------------------------------#
        collada_primitive_data = standard_tmd_decoder.collada_primitives
        collada_vertex_positions = standard_tmd_decoder.vertex_decoded
        ### VALUES FOR SOURCE ###
        global collada_uv
        global collada_vertex_color
        collada_uv = [] # mesh - map
        collada_vertex_color = [] # mesh - colors
        ### POLYLIST ###
        global collada_polygon
        collada_polygon = [] # polylist - vcount (this i will calculate through the total count of uv's)

        for col_prim_data in collada_primitive_data:
            denested_collada_uv = [] # mesh - map
            denested_collada_vcolor = [] # mesh - colors
            denested_polygon = [] # polylist header - v-count

            for c_prim_data in col_prim_data:

                for c_p_d in c_prim_data:
                    if c_p_d.get("v3") != None:
                        fourvertex_uv = c_p_d.get("u0"), (1 - c_p_d.get("v0")), c_p_d.get("u2"), (1 - c_p_d.get("v2")), c_p_d.get("u3"), (1 - c_p_d.get("v3")), c_p_d.get("u1"), (1 - c_p_d.get("v1"))
                        denested_collada_uv.append(fourvertex_uv)
                    elif c_p_d.get("u0") != None:
                        threevertex_uv = c_p_d.get("u2"), (1 - c_p_d.get("v2")), c_p_d.get("u1"), (1 - c_p_d.get("v1")), c_p_d.get("u0"), (1 - c_p_d.get("v0"))
                        denested_collada_uv.append(threevertex_uv)
                    elif (c_p_d.get("u0") == None) and (c_p_d.get("vertex3") != None):
                        none_uv_4v = 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01
                        denested_collada_uv.append(none_uv_4v)
                    elif (c_p_d.get("u0") == None) and (c_p_d.get("vertex2") != None):
                        none_uv_3v = 0.01, 0.01, 0.01, 0.01, 0.01, 0.01
                        denested_collada_uv.append(none_uv_3v)
                    else:
                        pass # I DO A PASS HERE, BECAUSE HERE WILL BE SHOWN ALL THE PRIMITIVES WITH COLOURS

                for vertex_color in c_prim_data:
                    if vertex_color.get("b3") != None:
                        b3_alpha_value = 1
                        fourdiff_color = (vertex_color.get("r0") / 256), (vertex_color.get("g0") / 256), (vertex_color.get("b0") / 256), b3_alpha_value, (vertex_color.get("r2") / 256), (vertex_color.get("g2") / 256), (vertex_color.get("b2") / 256), b3_alpha_value, (vertex_color.get("r3") / 256), (vertex_color.get("g3") / 256), (vertex_color.get("b3") / 256), b3_alpha_value, (vertex_color.get("r1") / 256), (vertex_color.get("g1") / 256), (vertex_color.get("b1") / 256), b3_alpha_value
                        denested_collada_vcolor.append(fourdiff_color)
                    elif vertex_color.get("r0") and vertex_color.get("b2") != None:
                        b2_alpha_value = 1
                        threediff_color = (vertex_color.get("r2") / 256), (vertex_color.get("g2") / 256), (vertex_color.get("b2") / 256), b2_alpha_value, (vertex_color.get("r1") / 256), (vertex_color.get("g1") / 256), (vertex_color.get("b1") / 256), b2_alpha_value, (vertex_color.get("r0") / 256), (vertex_color.get("g0") / 256), (vertex_color.get("b0") / 256), b2_alpha_value
                        denested_collada_vcolor.append(threediff_color)
                    elif vertex_color.get("r0") != None:
                        r0_alpha_value = 1
                        one_color_flat = (vertex_color.get("r0") / 256), (vertex_color.get("g0") / 256), (vertex_color.get("b0") / 256), r0_alpha_value
                        denested_collada_vcolor.append(one_color_flat)
                    else:
                        if c_p_d.get("lsc3vgt") or c_p_d.get("lsc3vft") or c_p_d.get("newlsc3vgt") or c_p_d.get("newlsc3vgt2") or c_p_d.get("lsc4vgt") or c_p_d.get("lsc4vft") or c_p_d.get("newlsc4vgt") or c_p_d.get("newlsc4vgt2"):
                            pass # I DO A PASS HERE, BECAUSE HERE WILL BE SHOWN ALL THE PRIMITIVES WITH UV BUT WITH NO COLOURS ON THEM
                        else:
                            print("This shouldn't happen!, look at the code at line 100 if a bug is ongoing")

                for polygon_number in c_prim_data: # counting the polygon v-count 
                    three_faces_prim = 3
                    four_faces_prim = 4
                    if polygon_number.get("vertex3") != None:
                        denested_polygon.append(four_faces_prim)
                    elif polygon_number.get("vertex2") != None:
                        denested_polygon.append(three_faces_prim)
                    else:
                        print("Something odd happen here, report this bug immediately! - No vertex Primitive ERROR")

            collada_uv.append(denested_collada_uv)
            collada_vertex_color.append(denested_collada_vcolor)
            collada_polygon.append(denested_polygon)
            #END of UV // VERTEX COLOR // V-Count loop

        # here i check if nesting for objects it's correct, this objects down here are just nested 1 level (better to say the values for the current object, but not all of them in "pairs")
        #print(len(collada_uv))
        #print(len(collada_vertex_color))
        #print(len(collada_polygon))
        #------------------------------------------START /// P-ARRAY LOOP------------------------------------------#

        collada_p_array = [] # polylist -  P ARRAY - sorting: vertex_index, normal_index, texcoord (uv), color_index
        #P-Array Constructor
        interntal_object_counter = 0
        for p_array_extraction_calc in collada_primitive_data:
            vertex_index = []
            normal_index = []
            uv_index = []
            color_index = []
            uv_num = 0
            color_num = 0
            for p_array_calc in p_array_extraction_calc:
                for polyex in p_array_calc:
                    default_value_4v = 0, 0, 0, 0
                    default_value_3v = 0, 0, 0
                    # P ARRAY - sorting: vertex_index, normal_index, texcoord (uv), color_index
                    
                    #VERTEX ARRAY
                    # VERTEX ORDER FOR 4 VERTEX IS V0 V2 V3 V1, NORMALS, UV AND OTHERS USE THE SAME ORDER
                    if polyex.get("vertex3") != None:
                        four_vertex_order = polyex.get("vertex0"), polyex.get("vertex2"), polyex.get("vertex3") ,polyex.get("vertex1")
                        vertex_index.append(four_vertex_order)
                    # VERTEX ORDER FOR 3 VERTEX IS V2 V1 V0, NORMALS, UV AND OTHERS USE THE SAME ORDER
                    elif polyex.get("vertex2") != None:
                        three_vertex_order = polyex.get("vertex2"), polyex.get("vertex1"), polyex.get("vertex0")
                        vertex_index.append(three_vertex_order)
                    else:
                        print("Something odd happen here, report this bug immediately! - No Vertex Primitive ERROR")
                    
                    #NORMAL ARRAY
                    # 4 NORMALS
                    if polyex.get("normal3") != None:
                        four_normal_order = polyex.get("normal0"), polyex.get("normal2"), polyex.get("normal3"), polyex.get("normal1")
                        normal_index.append(four_normal_order)
                    # 3 NORMALS
                    elif polyex.get("normal2") != None:
                        four_normal_order = polyex.get("normal2"), polyex.get("normal1"), polyex.get("normal0")
                        normal_index.append(four_normal_order)
                    # 1 NORMAL OR NONE NORMALS
                    elif polyex.get("normal0") != None:
                        one_normal_order_4v = polyex.get("normal0")
                        normal_index.append(one_normal_order_4v)
                    elif (polyex.get("normal0") == None) and (polyex.get("vertex3") != None):
                        normal_index.append(default_value_4v)
                    elif (polyex.get("normal0") == None) and (polyex.get("vertex2") != None):
                        normal_index.append(default_value_3v)
                    else:
                        print("Something odd happen here, report this bug immediately! - No Normal Primitive ERROR")
                    
                    #UV ARRAY
                    if polyex.get("v3") != None:
                        four_uv_order = (uv_num + 0), (uv_num + 1), (uv_num + 2), (uv_num + 3) # originally 0 1 2 3
                        uv_index.append(four_uv_order)
                        uv_num += 4
                    elif polyex.get("v2") != None:
                        three_uv_order = (uv_num + 0), (uv_num + 1), (uv_num + 2) # originally 0 1 2
                        uv_index.append(three_uv_order)
                        uv_num += 3
                    #UNTEXTURED PRIMITIVES, BUT NEED TO FILL WITH 0 VALUES
                    elif (polyex.get("v0") == None) and (polyex.get("vertex3") != None):
                        #four_uv_order_no_tex = (uv_num + 0), (uv_num + 1), (uv_num + 2), (uv_num + 3)
                        uv_index.append(default_value_4v)
                        uv_num += 4
                    elif (polyex.get("v0") == None) and (polyex.get("vertex2") != None):
                        #three_uv_order_no_tex = (uv_num + 0), (uv_num + 1), (uv_num + 2)
                        uv_index.append(default_value_3v)
                        uv_num += 3
                    else:
                        print("Something odd happen here, report this bug immediately! - No UV Primitive ERROR")
                    
                    #COLOR ARRAY
                    # 4 VERTEX COLORED
                    if polyex.get("b3") != None:
                        four_color_order = (color_num), (color_num + 1), (color_num + 2), (color_num + 3)
                        color_index.append(four_color_order)
                        color_num += 4
                    # 3 VERTEX COLORED
                    elif polyex.get("b2") != None:
                        three_color_order = (color_num), (color_num + 1), (color_num + 2), (color_num + 3)
                        color_index.append(three_color_order)
                        color_num += 3
                    # FLAT COLORED (JUST 1 COLOR)
                    elif polyex.get("b0") != None:
                        one_color_order = ((color_num), 0, 0, 0)
                        color_index.append(one_color_order)
                        color_num += 1
                    # NONE COLORS (FULLY TEXTURED)
                    elif (polyex.get("b0") == None) and (polyex.get("vertex3") != None):
                        color_index.append(default_value_4v)
                    elif (polyex.get("b0") == None) and (polyex.get("vertex2") != None):
                        color_index.append(default_value_3v)
                    else:
                        print("Something odd happen here, report this bug immediately! - No Color Primitive ERROR")
            #a print to check the data integrity, checking the length with the primitive number of each one
            #print(len(vertex_index), len(normal_index), len(uv_index), len(color_index))

            #FOR CHECKING IF FACES ARE OVERLAPPING --- FOR NOW WORKING AS INTENDED
            vertex_duplicated = vertex_index
            vertex_set = set(vertex_index)
            contains_duplicate = len(vertex_duplicated) != len(vertex_set)
            primitive_duplicate_bool = []
            if contains_duplicate == True:
                max_value_vi = max(max(vertex_duplicated)) + 2 # MAX VALUE FROM THE CURRENT OBJECT VERTEX INDEX
                print("We got a duplicate face in a Primitive, we must change some values to avoid duplicate Face automatic removing from 3D Softwares")
                primitive_duplicate_bool.append(True)

                duplicate_elements_index = []
                real_index_vertex = []
                for vertex_dup in range(0, len(vertex_duplicated)): # HERE I CALCULATE THE INDEXES OF DUPLICATE VERTEX INDEX
                    for v_dup in range(vertex_dup + 1, len(vertex_duplicated)):
                        if (vertex_duplicated[vertex_dup] == vertex_duplicated[v_dup]):
                            equal_faces = vertex_duplicated[v_dup]
                            index_in_array = vertex_duplicated.index(equal_faces)
                            duplicate_elements_index.append(index_in_array)
                            real_index_vertex.append(equal_faces)

                values_replace_final = []
                num_sum = 0
                for vertex_d in duplicate_elements_index: # HERE I CALCULATE THE NEW VERTEX INDICES TO BE USED
                    value_duplicate = vertex_duplicated[vertex_d]
                    values_for_replace = []
                    for value_change in value_duplicate:
                        value_changed = max_value_vi + num_sum
                        values_for_replace.append(value_changed)
                        num_sum += 1
                        #print(value_change, value_changed) # This is the compare between old Vertex Index Values and new ones maybe could use this as metadata in the future
                    values_replace_final.append(values_for_replace)
                #print(values_replace_final)
                start_index_pos = 0
                for vertexindex_to_change in duplicate_elements_index:
                    vertex_index.pop(vertexindex_to_change)
                    vertex_index.insert(vertexindex_to_change, tuple(values_replace_final[start_index_pos]))
                    start_index_pos += 1

                for vertex_real_index in real_index_vertex:
                    current_vertex_array = collada_vertex_positions[interntal_object_counter]
                    position_adding = len(collada_vertex_positions[interntal_object_counter])
                    slicing_value = 1
                    for vertex_pos_array in vertex_real_index:
                        duplicate_vertex_adding = current_vertex_array[vertex_pos_array]
                        add_more_index = position_adding + slicing_value
                        collada_vertex_positions[interntal_object_counter].insert(add_more_index, duplicate_vertex_adding)
                        slicing_value += 1
                        
            else:
                primitive_duplicate_bool.append(False)

            # Data compiler
            zipped_p_array = zip_longest(vertex_index, normal_index, uv_index, color_index)
            p_array_formed = []
            for vertex_arr, normal_arr, uv_arr, color_arr in zipped_p_array:
                num_count = len(vertex_arr)
                slicing_internal = 0
                while num_count > 0:
                    ver_p = vertex_arr[slicing_internal]
                    nor_p = normal_arr[slicing_internal]
                    uvs_p = uv_arr[slicing_internal]
                    col_p = color_arr[slicing_internal]
                    p_array_formed.append(ver_p)
                    p_array_formed.append(nor_p)
                    p_array_formed.append(uvs_p)
                    p_array_formed.append(col_p)
                    slicing_internal += 1
                    num_count -= 1
            collada_p_array.append(p_array_formed)
            #print(len(p_array_formed))
            interntal_object_counter += 1
        #print(len(collada_p_array))

        #-------------------------------------- ////// END ////// ==> PRECONVERSION OF DATA FOR COLLADA FILES --------------------------------------#

        # DATA WRITTER
        with open(os.path.join(standard_tmd_writer.new_folder, standard_tmd_writer.file_name) + ".dae", 'w') as dae_file_writer:
            # MOST OF THE DATA WRITE IN HERE IT'S FROM A DEFAULT EXAMPLE FROM BLENDER 2.80 i won't do something too much fancy because i don't know the half of the dae structure behave
            
            # HEADER
            technical_header = f'<?xml version="1.0" encoding="utf-8"?>\n'
            collada_header = f'<COLLADA xmlns="http://www.collada.org/2005/11/COLLADASchema" version="1.4.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n'
            
            # ASSET HEADER
            asset_header = f'  <asset>\n    <contributor>\n      <author>TLoD_TMD_Converter_User</author>\n      <authoring_tool>TLoD_TMD_Converter</authoring_tool>\n   <source_data>{standard_tmd_writer.new_folder}.bin</source_data>\n    </contributor>\n    <created>{date_conversion}</created>\n    <modified>{date_conversion}</modified>\n    <unit name="meter" meter="1"/>\n    <up_axis>Z_UP</up_axis>\n  </asset>\n'
            dae_file_writer.write(technical_header)
            dae_file_writer.write(collada_header)
            dae_file_writer.write(asset_header)

            # LYBRARY_EFFECTS PROCESSING (ALMOST ALL THE STUFF HERE IS AS BLENDER DEFAULT)
            number_of_object = range(0, standard_tmd.tmd_nobj_expected)
            library_effect_start = f'  <library_effects>\n'
            dae_file_writer.write(library_effect_start)
            for number_effects in number_of_object:
                effect_loop_1 = f'    <effect id="Object_Number_{number_effects}-effect">\n      <profile_COMMON>\n        <technique sid="common">\n          <lambert>\n            <emission>\n              <color sid="emission">0 0 0 1</color>\n            </emission>\n'
                effect_loop_2 = f'            <diffuse>\n              <color sid="diffuse">0.8 0.8 0.8 1</color>\n            </diffuse>\n            <index_of_refraction>\n              <float sid="ior">1.45</float>\n            </index_of_refraction>\n'
                effect_loop_3 = f'          </lambert>\n        </technique>\n      </profile_COMMON>\n    </effect>\n'
                dae_file_writer.write(effect_loop_1)
                dae_file_writer.write(effect_loop_2)
                dae_file_writer.write(effect_loop_3)
            library_effect_end = f'  </library_effects>\n'
            dae_file_writer.write(library_effect_end)
            
            # LIBRARY_IMAGES (NOT IMPLEMENTED, SO WILL BE BLANK!)
            library_images_blank = f'  <library_images/>\n'
            dae_file_writer.write(library_images_blank)
            
            # LIBRARY_MATERIALS PROCESSING (OBJECTS MATERIALS, YOU KNOW? JUST DEFAULT STUFF)
            library_materials_start = f'  <library_materials>\n'
            dae_file_writer.write(library_materials_start)
            for number_material in number_of_object:
                material_loop = f'    <material id="Object_Number_{number_material}-material" name="Object_Number_{number_material}">\n      <instance_effect url="#Object_Number_{number_material}-effect"/>\n    </material>\n'
                dae_file_writer.write(material_loop)
            library_materials_end = f'  </library_materials>\n'
            dae_file_writer.write(library_materials_end)

            # LIBRARY_GEOMETRIES PROCESSING (HERE IS WHERE THE FILE GET INTERESTING)
            library_geometries_start = f'  <library_geometries>\n'
            dae_file_writer.write(library_geometries_start)
            
            for number_geometry in number_of_object: # THIS WRITE THE CURRENT OBJECT ARRAYS (VERTEX, FACES, NORMALS, ETC)
                geometry_loop_1 = f'    <geometry id="Object_Number_{number_geometry}-mesh" name="Object_Number_{number_geometry}">\n      <mesh>\n'
                dae_file_writer.write(geometry_loop_1)
                # from here i have to write each mesh as source id = Object_Number_0-mesh-positions; Object_Number_0-vert-colors; Object_Number_0-mesh-normals ; Object_Number_0-mesh-map-0 ; mesh-colors-Col ; Object_Number_0-mesh-vertices // polylist
                
                # source id = Object_Number_n-mesh-positions
                mesh_positions = collada_vertex_positions[number_geometry] #CURRENT VERTEX BLOCK IN THE CURRENT NUMBER OF OBJECT
                mesh_positions_length = len(mesh_positions) * 3 # full count of vertex (so 1 vertex = 3 values [x, y, z)])
                mesh_position_source_write = f'        <source id="Object_Number_{number_geometry}-mesh-positions">\n          <float_array id="Object_Number_{number_geometry}-mesh-positions-array" count="{mesh_positions_length}">'
                dae_file_writer.write(mesh_position_source_write)
                for vertex_in_array in collada_vertex_positions[number_geometry]: # THIS WRITE THE CURRENT OBJECT VERTEX ARRAY (SOURCE ID POSITIONS)
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

                mesh_normals = standard_tmd_decoder.normal_decoded[number_geometry]
                mesh_normals_length = len(mesh_normals) * 3 # full count of normals (so 1 normal = 3 values [x, y, z)])
                mesh_normals_source_write = f'        <source id="Object_Number_{number_geometry}-mesh-normals">\n          <float_array id="Object_Number_{number_geometry}-mesh-normals-array" count="{mesh_normals_length}">'
                dae_file_writer.write(mesh_normals_source_write)
                for normal_in_array in standard_tmd_decoder.normal_decoded[number_geometry]:
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
                if mesh_maps == []:
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
                current_quantity_primitives = standard_tmd_structure.primitive_number_int[number_geometry]
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
                #print(len(list(collada_v_count)), "for object, number", number_geometry)
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
                    #print(array_ready, "for object number", number_geometry)
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

            # LIBRARY_VISUAL_SCENE (JUST DEFAULT AS BLENDER EXAMPLE)
            library_visual_scene_header = f'  <library_visual_scenes>\n    <visual_scene id="Scene" name="Scene">\n'
            dae_file_writer.write(library_visual_scene_header)
            for library_number in number_of_object:
                library_visual_scene_loop = f'      <node id="Object_Number_{library_number}" name="Object_Number_{library_number}" type="NODE">\n        <scale sid="scale">1 1 1</scale>\n        <rotate sid="rotationZ">0 0 1 0</rotate>\n        <rotate sid="rotationY">0 1 0 0</rotate>\n        <rotate sid="rotationX">1 0 0 90.00001</rotate>\n        <translate sid="location">0 0 0</translate>\n        <instance_geometry url="#Object_Number_{library_number}-mesh" name="Object_Number_{library_number}">\n          <bind_material>\n            <technique_common>\n              <instance_material symbol="Object_Number_{library_number}-material" target="#Object_Number_{library_number}-material">\n                <bind_vertex_input semantic="UVMap" input_semantic="TEXCOORD" input_set="0"/>\n              </instance_material>\n            </technique_common>\n          </bind_material>\n        </instance_geometry>\n      </node>\n'
                dae_file_writer.write(library_visual_scene_loop)
            library_visual_scene_end = f'    </visual_scene>\n  </library_visual_scenes>\n'
            dae_file_writer.write(library_visual_scene_end)


            # SCENE (JUST DEFAULT AS BLENDER EXAMPLE)
            scene_write = f'  <scene>\n    <instance_visual_scene url="#Scene"/>\n  </scene>\n'
            dae_file_writer.write(scene_write)

            # END OF THE FILE WITH </COLLADA>
            collada_end_of_file = f'</COLLADA>'
            dae_file_writer.write(collada_end_of_file)
        #print(len(collada_vertex_positions), "Total Vertices Blocks on TMD")
        print("Collada File successfully converted")