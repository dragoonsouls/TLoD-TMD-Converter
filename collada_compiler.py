"""

Model Collada Compiler: This module will compile the data from previous
processing to get into shape for the Collada Writer.
Formerly this code was at the top of the Collada Converter
in alpha 0.5 and lower.

Copyright (C) 2023 DooMMetaL

"""

from collections import Counter
import itertools

class ColladaCompiler:
    def __init__(self, collada_primitives, collada_vertex):
        self.self = ColladaCompiler
        self.collada_compiler(collada_primitives=collada_primitives, collada_vertex=collada_vertex)
    
    def collada_compiler(self, collada_primitives=list, collada_vertex=list):
        collada_primitive_data = collada_primitives
        collada_vertex_positions = collada_vertex

        ### VALUES FOR SOURCE ###
        global collada_uv
        global collada_vertex_color
        collada_uv = [] # mesh - map
        collada_vertex_color = [] # mesh - colors
        ### POLYLIST ###
        global collada_polygon
        collada_polygon = [] # polylist - vcount (this i will calculate through the total count of uv's)

        counter_0 = 0
        for prim_data in collada_primitive_data:
            denested_collada_uv = [] # mesh - map
            denested_collada_vcolor = [] # mesh - colors
            denested_polygon = [] # polylist header - v-count.

            for c_p_d in prim_data: #KEEP AN EYE ON IT!!
                uv_obtain = self.collada_uv_get(c_p_d=c_p_d)
                color_obtain = self.collada_vertex_color_get(c_p_d=c_p_d)
                polygon_obtain = self.collada_polygon_get(c_p_d=c_p_d)
                denested_collada_uv.append(uv_obtain)
                denested_collada_vcolor.append(color_obtain)
                denested_polygon.append(polygon_obtain)

            collada_uv.append(denested_collada_uv)
            collada_vertex_color.append(denested_collada_vcolor)
            collada_polygon.append(denested_polygon)
            counter_0 += 1
        #END of UV // VERTEX COLOR // V-Count loop

        #------------------------------------------START /// P-ARRAY LOOP------------------------------------------#

        global collada_p_array
        collada_p_array = [] # polylist -  P ARRAY - sorting: vertex_index, normal_index, texcoord (uv), color_index
        #P-Array Constructor
        internal_object_counter = 0
        for p_array_extraction_calc in collada_primitive_data:
            vertex_index = []
            normal_index = []
            uv_index = []
            color_index = []
            uv_num = 0
            color_num = 0
            for polyex in p_array_extraction_calc:
                #for polyex in p_array_calc:
                default_value_4v = 0, 0, 0, 0
                default_value_3v = 0, 0, 0
                # P ARRAY - sorting: vertex_index, normal_index, texcoord (uv), color_index

                #VERTEX ARRAY
                """Vertex Index is the only that all values are present or at least have to be that way"""
                # VERTEX ORDER FOR 4 VERTEX IS V1 V3 V2 V0, NORMALS, UV AND OTHERS USE THE SAME ORDER
                if (polyex.get("vertex3") != None) and (polyex.get("vertex2") != None):
                    four_vertex_order = polyex.get("vertex1"), polyex.get("vertex3"), polyex.get("vertex2") ,polyex.get("vertex0")
                    vertex_index.append(four_vertex_order)
                # VERTEX ORDER FOR 3 VERTEX IS V0 V1 V2, NORMALS, UV AND OTHERS USE THE SAME ORDER
                elif (polyex.get("vertex2") != None) and (polyex.get("vertex1") != None):
                    three_vertex_order = polyex.get("vertex0"), polyex.get("vertex1"), polyex.get("vertex2")
                    vertex_index.append(three_vertex_order)
                else:
                    print("Something odd happen here, report this bug immediately! - No Vertex Index Primitive ERROR")
                    print(f'Primitive Vertex Index error: {polyex}')
                    exit()

                #NORMAL ARRAY
                """If Normals don't exist, the tool will fill it with 0 values
                just to maintain the same number in data, anyway in PSX this happens the same way"""
                # 4 NORMALS
                if polyex.get("normal3") != None:
                    four_normal_order = polyex.get("normal1"), polyex.get("normal3"), polyex.get("normal2"), polyex.get("normal0")
                    normal_index.append(four_normal_order)

                # 3 NORMALS
                elif polyex.get("normal2") != None:
                    three_normal_order = polyex.get("normal0"), polyex.get("normal1"), polyex.get("normal2")
                    normal_index.append(three_normal_order)

                # 1 NORMAL OR NONE NORMALS
                elif (polyex.get("normal0") != None) and (polyex.get("vertex3") != None):
                    one_normal_order_4v = polyex.get("normal0")
                    normal_index.append(one_normal_order_4v)

                elif (polyex.get("normal0") != None) and (polyex.get("vertex2") != None):
                    one_normal_order_3v = polyex.get("normal0")
                    normal_index.append(one_normal_order_3v)

                elif (polyex.get("normal0") == None) and (polyex.get("vertex3") != None):
                    normal_index.append(default_value_4v)

                elif (polyex.get("normal0") == None) and (polyex.get("vertex2") != None):
                    normal_index.append(default_value_3v)

                else:
                    print("Something odd happen here, report this bug immediately! - No Normal Index Primitive ERROR")
                    print(f'Primitive Normal Index error: {polyex}')
                    exit()

                #UV ARRAY
                """This Indices are generated using the same UV data, simply sum values, if an untextured
                face is happening, will fill with 0 data to match the numbers for the compiler"""
                # TEXTURED 4 VERTEX
                if polyex.get("v3") != None:
                    four_uv_order = (uv_num + 0), (uv_num + 1), (uv_num + 2), (uv_num + 3) # originally 0 1 2 3
                    uv_index.append(four_uv_order)
                    uv_num += 4

                # TEXTURED 3 VERTEX
                elif polyex.get("v2") != None:
                    three_uv_order = (uv_num + 0), (uv_num + 1), (uv_num + 2) # originally 0 1 2
                    uv_index.append(three_uv_order)
                    uv_num += 3

                #UNTEXTURED PRIMITIVES, BUT NEED TO FILL WITH 0 VALUES
                elif (polyex.get("v0") == None) and (polyex.get("vertex3") != None):
                    uv_index.append(default_value_4v)
                    uv_num += 4

                elif (polyex.get("v0") == None) and (polyex.get("vertex2") != None):
                    uv_index.append(default_value_3v)
                    uv_num += 3

                else:
                    print("Something odd happen here, report this bug immediately! - No UV Primitive ERROR")
                    print(f'Primitive UV error: {polyex}')
                    exit()

                #COLOR ARRAY // new algorithm
                """Colors are an special case here, as the UV the index it's generated using the same values
                at the moment seems to be working just fine"""
                # 4 VERTEX COLORED
                if (polyex.get("r0") != None) and (polyex.get("r1") != None) and (polyex.get("r2") != None) and (polyex.get("r3") != None):
                    four_color_order = (color_num + 3), (color_num + 2), (color_num + 1), (color_num)
                    color_index.append(four_color_order)
                    color_num += 4

                # 3 VERTEX COLORED
                elif (polyex.get("r0") != None) and (polyex.get("r1") != None) and (polyex.get("r2") != None):
                    three_color_order = (color_num + 2), (color_num + 1), (color_num)
                    color_index.append(three_color_order)
                    color_num += 3

                # FLAT COLORED (JUST 1 COLOR)
                elif (polyex.get("r0") != None) and (polyex.get("vertex3") != None):
                    one_color_order_4v = ((color_num + 3), (color_num + 2), (color_num + 1), (color_num)) # THIS VALUES ORIGINALLY WERE COLOR_NUM, 0, 0, 0.
                    color_index.append(one_color_order_4v)
                    color_num += 4

                elif (polyex.get("r0") != None) and (polyex.get("vertex2") != None):
                    one_color_order_3v = ((color_num + 2), (color_num + 1), (color_num)) # THIS VALUES ORIGINALLY WERE COLOR_NUM, 0, 0.
                    color_index.append(one_color_order_3v)
                    color_num += 3

                # NONE COLORS (FULLY TEXTURED) |||| ONLY LSC CAN BE THIS WAY, BECAUSE NLSC HAVE COLOURS
                elif (polyex.get("r0") == None) and (polyex.get("vertex3") != None):
                    color_index.append(default_value_4v)
                    color_num += 4

                elif (polyex.get("r0") == None) and (polyex.get("vertex2") != None):
                    color_index.append(default_value_3v)
                    color_num += 3

                else:
                    print("Something odd happen here, report this bug immediately! - No Color Primitive ERROR")
                    print(f'Primitive Colour error: {polyex}')
                    exit()

            ##############################################################################################################################
            ############################ FOR CHECKING IF FACES ARE OVERLAPPING --- FOR NOW WORKING AS INTENDED ###########################
            ##############################################################################################################################
            vertex_duplicated = vertex_index
            vertex_set = set(vertex_index)
            contains_duplicate = len(vertex_duplicated) != len(vertex_set)

            checking_overlap = self.check_face_overlapping(contains_duplicate=contains_duplicate, vertex_duplicated=vertex_duplicated,
            internal_object_counter=internal_object_counter,vertex_index=vertex_index,collada_vertex_positions=collada_vertex_positions)
            
            vertex_index = checking_overlap[0]
            collada_vertex_positions = checking_overlap[1]

            calculate_max_vi = []
            for vertex_max in vertex_index:
                for vertex_m in vertex_max:
                    calculate_max_vi.append(vertex_m)
            
            vertex_index_max = max(calculate_max_vi)

            same_vertex_index_data = []
            check_index = 0
            for index_sorted in vertex_index:
                working_data_none = False, None
                sort_this = sorted(index_sorted)
                if tuple(sort_this) in vertex_index:
                    index_sort_this = vertex_index.index(tuple(sort_this))
                    if (index_sort_this != check_index):
                        working_data = True, check_index
                        same_vertex_index_data.append(working_data)
                    else:
                        same_vertex_index_data.append(working_data_none)
                else:
                    same_vertex_index_data.append(working_data_none)
                check_index += 1
            
            same_vertex_index = self.check_same_vertex_index(collada_vertex_positions=collada_vertex_positions, vertex_index=vertex_index, current_object=internal_object_counter, same_vi_flags=same_vertex_index_data, max_index_number=vertex_index_max)
            vertex_index = same_vertex_index[0]
            collada_vertex_positions = same_vertex_index[1]

            ##############################################################################################################################
            ############################################ FACE OVERLAPPING CHECK ALGORITHM END ############################################
            ##############################################################################################################################

            # Data compiler and sent to Collada P-Array - HERE I CREATE THE P-ARRAY FOR THE OBJECTS
            zipped_p_array = itertools.zip_longest(vertex_index, normal_index, uv_index, color_index)
            p_array_formed = []
            for vertex_arr, normal_arr, uv_arr, color_arr in zipped_p_array:
                slicing_internal = 0
                for num in range(0, len(vertex_arr)):
                    ver_p = vertex_arr[slicing_internal]
                    nor_p = normal_arr[slicing_internal]
                    uvs_p = uv_arr[slicing_internal]
                    col_p = color_arr[slicing_internal]
                    p_array_formed.append(ver_p)
                    p_array_formed.append(nor_p)
                    p_array_formed.append(uvs_p)
                    p_array_formed.append(col_p)
                    slicing_internal += 1
            collada_p_array.append(p_array_formed)
            internal_object_counter += 1

    @staticmethod
    def collada_uv_get(c_p_d=dict):
        # Getting the UV data and if not exist just fill with a default value |||| DAE format don't allow non UV if a single face in all the model is already textured
        uv_get = ()
        if (c_p_d.get("u3") != None) and (c_p_d.get("v3") != None): # uv1-uv3-uv2-uv0
            fourvertex_uv = c_p_d.get("u1"), (1 - c_p_d.get("v1")), c_p_d.get("u3"), (1 - c_p_d.get("v3")), c_p_d.get("u2"), (1 - c_p_d.get("v2")), c_p_d.get("u0"), (1 - c_p_d.get("v0"))
            uv_get = fourvertex_uv
        elif c_p_d.get("u0") != None:
            threevertex_uv = c_p_d.get("u0"), (1 - c_p_d.get("v0")), c_p_d.get("u1"), (1 - c_p_d.get("v1")), c_p_d.get("u2"), (1 - c_p_d.get("v2"))
            uv_get = threevertex_uv
        elif (c_p_d.get("u0") == None) and (c_p_d.get("v0") == None) and (c_p_d.get("vertex3") != None):
            none_uv_4v = 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01
            uv_get = none_uv_4v
        elif (c_p_d.get("u0") == None) and (c_p_d.get("v0") == None) and (c_p_d.get("vertex3") == None):
            none_uv_3v = 0.01, 0.01, 0.01, 0.01, 0.01, 0.01
            uv_get = none_uv_3v
        else:
            print(f'FATAL ERROR - UV DATA NOT RECOGNISED!!... Exiting...')
            print(f'Primitive: {c_p_d}')
            exit()
        
        return uv_get
    
    @staticmethod
    def collada_vertex_color_get(c_p_d=dict):
        # Getting Colours in the Primitive
        vertex_colour = ()
        if (c_p_d.get("r3") != None) and (c_p_d.get("b3") != None): # 4 VERTEX COLOUR Gradation
            b3_alpha_value = 1
            fourdiff_color = (c_p_d.get("r0") / 256), (c_p_d.get("g0") / 256), (c_p_d.get("b0") / 256), b3_alpha_value, (c_p_d.get("r2") / 256), (c_p_d.get("g2") / 256), (c_p_d.get("b2") / 256), b3_alpha_value, (c_p_d.get("r3") / 256), (c_p_d.get("g3") / 256), (c_p_d.get("b3") / 256), b3_alpha_value, (c_p_d.get("r1") / 256), (c_p_d.get("g1") / 256), (c_p_d.get("b1") / 256), b3_alpha_value
            vertex_colour = fourdiff_color

        elif (c_p_d.get("r2") != None) and (c_p_d.get("b2") != None): # 3 VERTEX COLOUR Gradation
            b2_alpha_value = 1
            threediff_color = (c_p_d.get("r2") / 256), (c_p_d.get("g2") / 256), (c_p_d.get("b2") / 256), b2_alpha_value, (c_p_d.get("r1") / 256), (c_p_d.get("g1") / 256), (c_p_d.get("b1") / 256), b2_alpha_value, (c_p_d.get("r0") / 256), (c_p_d.get("g0") / 256), (c_p_d.get("b0") / 256), b2_alpha_value
            vertex_colour = threediff_color

        elif (c_p_d.get("r0") != None) and (c_p_d.get("b0") != None) and (c_p_d.get("vertex3") != None): # 4 Vertex FLAT COLOUR
            r0_alpha_value = 1
            one_color_flat_4v = (c_p_d.get("r0") / 256), (c_p_d.get("g0") / 256), (c_p_d.get("b0") / 256), r0_alpha_value, (c_p_d.get("r0") / 256), (c_p_d.get("g0") / 256), (c_p_d.get("b0") / 256), r0_alpha_value, (c_p_d.get("r0") / 256), (c_p_d.get("g0") / 256), (c_p_d.get("b0") / 256), r0_alpha_value, (c_p_d.get("r0") / 256), (c_p_d.get("g0") / 256), (c_p_d.get("b0") / 256), r0_alpha_value
            vertex_colour = one_color_flat_4v

        elif (c_p_d.get("r0") != None) and (c_p_d.get("b0") != None) and (c_p_d.get("vertex2") != None): # 3 Vertex FLAT COLOUR
            r0_alpha_value = 1
            one_color_flat_3v = (c_p_d.get("r0") / 256), (c_p_d.get("g0") / 256), (c_p_d.get("b0") / 256), r0_alpha_value, (c_p_d.get("r0") / 256), (c_p_d.get("g0") / 256), (c_p_d.get("b0") / 256), r0_alpha_value, (c_p_d.get("r0") / 256), (c_p_d.get("g0") / 256), (c_p_d.get("b0") / 256), r0_alpha_value
            vertex_colour = one_color_flat_3v

        else: # FULLY TEXTURED PRIMITIVES
            if (c_p_d.get("r0") == None) and (c_p_d.get("vertex3") != None):
                none_colour_4v = (0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1)
                vertex_colour = none_colour_4v
            elif (c_p_d.get("r0") == None) and (c_p_d.get("vertex2") != None):
                none_colour_3v = (0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1)
                vertex_colour = none_colour_3v
            else:
                print(f'WARNING: VERTEX COLOR ERROR, Value not possible, Report as Vertex Color Conversion packer - not in dict... exiting')
                print(f'Primitive: {c_p_d}')
                exit()
        
        return vertex_colour

    @staticmethod
    def collada_polygon_get(c_p_d=dict):
        # Getting how many Vertices are in the Primitive
        four_faces_prim = 4
        three_faces_prim = 3
        face_type = 0
        if c_p_d.get("vertex3") != None:
            face_type = four_faces_prim
        elif c_p_d.get("vertex2") != None:
            face_type = three_faces_prim
        else:
            print("Something odd happen here, report this bug immediately! - No vertex Primitive ERROR... Exiting")
            print(f'Primitive: {c_p_d}')
            exit()
        return face_type
    
    @staticmethod
    def check_face_overlapping(contains_duplicate=bool, vertex_duplicated=list, internal_object_counter=int, vertex_index=list, collada_vertex_positions=list):
        if contains_duplicate == True:
            print("We got a duplicate face in a Primitive, we must change some values to avoid duplicate Face automatic removing from 3D Softwares, Object number:", f'{internal_object_counter}')
            vertex_dup_maxvalue_list = []
            for ver_2_list in vertex_duplicated:
                vertex_to_list = list(ver_2_list)
                vertex_dup_maxvalue_list.append(vertex_to_list)
            
            maxval_vi_list = [max(map(int, i)) for i in vertex_dup_maxvalue_list]

            max_value_vi = max(maxval_vi_list) + 1 # MAX VALUE FROM THE CURRENT OBJECT VERTEX INDEX = will be max_index + 1
            """max_value_vi means Max Value Vertex Index and it's used for know the first highest Vertex Index to be use in the duplicator"""
            
            """ HERE I MUST CHECK THE OCURRENCES OF VERTEX INDEX IF THIS IS MORE THAN 3, TOOL WILL CRASH BECAUSE I EXPECT ONLY DUPLICATED
            NOT MULTIPLICATED VERTEX INDEX..."""
            vertex_index_dup_count = Counter(map(tuple,vertex_dup_maxvalue_list))

            counted_duplicates = [] # LIST OF DUPLICATED VERTEX INDEX
            for vi_dup_count in vertex_index_dup_count.items():
                if vi_dup_count[1] == 2:
                    changing_stuff = list(vi_dup_count[0])
                    counted_duplicates.append(changing_stuff)
                elif vi_dup_count[1] == 3:
                    print(f'FATAL CRASH - Unexpected quantity of Vertex Index are not duplicated, are Multiplicated... exiting...')
                    exit()
            
            duplicated_vi_indices = [] # LIST OF VERTEX INDEX NUMERATED BY LIST INDEX
            for vertex_index_pos in enumerate(vertex_dup_maxvalue_list): 
                duplicated_vi_indices.append(vertex_index_pos)
            
            this_are_second_duplicated = []
            for loop_dup_values in counted_duplicates:
                get_values_dup_index = []
                for vertexindex_indice in duplicated_vi_indices:
                    if vertexindex_indice[1] == loop_dup_values:
                        get_values_dup_index.append(vertexindex_indice)
                get_values_dup_index.sort()
                
                second_duplicated = get_values_dup_index[1]
                this_are_second_duplicated.append(second_duplicated)
            
            """FIRST I NEED TO ADD THE NEW VERTICES, for that i will take the confirmed duplicated vertex index and get the vertices that it use,
            also will recalculate the new index in the list of vertices and that new index will be the new vertex index to replace them"""

            vertices_value_to_duplicate = []
            for get_vertices in this_are_second_duplicated:
                actual_vertexindex_data = get_vertices[1]
                for get_vertex in actual_vertexindex_data:
                    vertices_value_to_duplicate.append(get_vertex)
            
            unique_vertices_to_duplicate = set(vertices_value_to_duplicate)
            unique_vertices_no_set = []
            for vi_noset in unique_vertices_to_duplicate:
                unique_vertices_no_set.append(vi_noset)
            
            # Duplicating the Vertices
            vertex_in_current_object = collada_vertex_positions[internal_object_counter]

            add_this_vertex = [] # THIS VERTEX MUST BE RETURNED BY THE ALGORITHM AND SEND INTO THE COLLADA VERTEX POSITIONS
            for vertex_index_get in unique_vertices_to_duplicate:
                new_vertex = vertex_in_current_object[vertex_index_get]
                add_this_vertex.append(new_vertex)
            
            collada_vertex_positions[internal_object_counter] = vertex_in_current_object + add_this_vertex
            
            """NOW IT'S TIME TO CONTINUE WITH THE VERTEX INDEX, BUT THE NEW VERTEX INDEX MUST USE THE SAME AS USED IN THE NEW VERTEX BLOCK BUILD"""

            new_old_vertex_index = []
            for new_vertex_index in range(0, len(unique_vertices_no_set)):
                new_vi = new_vertex_index + max_value_vi
                old_vi = unique_vertices_no_set[new_vertex_index]
                both_vi = new_vi, old_vi
                new_old_vertex_index.append(both_vi)
            
            new_vertex_index_values = []
            for replacing_vi in this_are_second_duplicated:
                replacing_vi_list_index = replacing_vi[0]
                replacing_vi_values = replacing_vi[1]
                for no_vi in new_old_vertex_index:
                    new_rep_vi = no_vi[0]
                    old_rep_vi = no_vi[1]
                    if old_rep_vi in replacing_vi_values:
                        index_replace = replacing_vi_values.index(old_rep_vi)
                        replacing_vi_values[index_replace] = new_rep_vi
                
                replace_vi_values = replacing_vi_list_index, replacing_vi_values
                new_vertex_index_values.append(replace_vi_values)
            
            for replace_this_values in new_vertex_index_values:
                index_list = replace_this_values[0]
                values_list = tuple(replace_this_values[1])
                vertex_index[index_list] = values_list

        else:
            print(f'This Model, Object number: {internal_object_counter}, do not have overlapped faces, processing will continue...')
        
        return vertex_index, collada_vertex_positions

    @staticmethod
    def check_same_vertex_index(collada_vertex_positions=list, vertex_index=list, current_object=int, same_vi_flags=list, max_index_number=int):
        """THIS ALGORITHM WILL FIND IF A SAME VERTEX INDEX DIFFERENT WINDING IT'S GOING ON"""

        check_bool = False
        check_index = []

        for flags in same_vi_flags:
            if flags[0] == True:
                check_bool = True
                check_index.append(flags[1])
            else:
                pass
        
        if check_bool == True:
            check_index_str = str(check_index).replace("[", "").replace("]", "")
            print(f'In Object Number {current_object}, Primitives Number: {check_index_str} have Faces with different Vertex Index Winding')
            print(f'We are going to do some calculations to fix this...')

            all_involved_vertex_index = []

            for index_involved in check_index:
                append_this_index = vertex_index[index_involved]
                for append_index in append_this_index:
                    all_involved_vertex_index.append(append_index)
            
            set_involved_vi = set(all_involved_vertex_index)

            """"FIRST WE MUST GET THE NEW VERTICES ADDED INTO THE BLOCK"""
            vertices_current_object = collada_vertex_positions[current_object]
            new_vertices_add = []
            involved_vi = []
            for index_find_vertex in set_involved_vi:
                new_vertex = vertices_current_object[index_find_vertex]
                new_vertices_add.append(new_vertex)
                involved_vi.append(index_find_vertex)
            
            collada_vertex_positions[current_object] = vertices_current_object + new_vertices_add

            """NOW I CALCULATE THE NEW VERTEX INDEX"""

            old_new_vertex_index = []
            old_index_slice = 0
            for index_new_val in range(0, len(involved_vi)):
                new_vertex_index_value = index_new_val + max_index_number + 1
                old_vertex_index_value = involved_vi[old_index_slice]
                old_new_vals = old_vertex_index_value, new_vertex_index_value
                old_new_vertex_index.append(old_new_vals)
                old_index_slice += 1
            
            new_build = []
            for check_this in check_index:
                vertex_new_build = list(vertex_index[check_this])
                for new_old_vals in old_new_vertex_index:
                    old_val = new_old_vals[0]
                    new_val = new_old_vals[1]
                    if old_val in vertex_new_build:
                        look_index = vertex_new_build.index(old_val)
                        vertex_new_build[look_index] = new_val
                vertex_last_adjust = tuple(vertex_new_build)
                new_build.append(vertex_last_adjust)
            
            slicing_change = 0
            for replace in check_index:
                vertex_index[replace] = new_build[slicing_change]
                slicing_change += 1
        return vertex_index, collada_vertex_positions