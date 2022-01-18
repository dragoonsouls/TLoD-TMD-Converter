"""

Standard TMD Structure Writer: This module write the Standard TMD structure data into
TMD Properties and Debug data,OBJ, PLY (support will be soon), 
because this module has to be very flexible and easy to update

Copyright (C) 2021 DooMMetaL

"""

import itertools
import os
from posixpath import basename
import standard_tmd # USING THE VARIABLES FROM HERE, DUE TO BE MORE EASY TO CATCH FROM THE GLOBAL SCOPE
import standard_tmd_structure
import datetime
import standard_tmd_decoder

class NewFolder():                      # THIS CLASS IS IN CHARGE OF CREATING A DUMP FOLDER AND TO TAKE THE FILE NAME, USED AFTER
    def __init__(self, create_folder):  # FOR NAMING FILES DUMPED
        self.self = NewFolder
        self.create_folder = create_folder
    
    def convert_folder(self):
        global file_name
        global new_folder
        #global ply_nest

        path_folder = os.path.dirname(standard_tmd.tmd_file)
        file_path_complete = (standard_tmd.tmd_file).strip()
        file_name_complete = os.path.basename(file_path_complete)
        file_name = os.path.splitext(file_name_complete)[0]
        new_folder = os.path.join(path_folder, file_name)
        #ply_nest_no_join = os.fspath(f'PLY_Conversion') ONLY USED FOR PLY CONVESION, BECAUSE I NEED TO NEST FILES
        #ply_nest = os.path.join(new_folder, ply_nest_no_join)

        try:
            os.makedirs(new_folder, exist_ok=True)
        except OSError:
            print("Can't create the folder, permission denied")


class PropertiesWriter():               # THIS IS THE TMD FILE REPORTER, JUST COMPILING THE NUMBERS OF OBJECTS, VERTEX, NORMALS AND PRIMITIVES 
    def __init__(self, tmd_information, primitive_information):
        self.self = PropertiesWriter
        self.tmd_information = tmd_information
        self.primitive_information = primitive_information
    
    def tmd_informer(self):
        number_of_objects_int = standard_tmd.tmd_nobj_expected
        number_of_vertices = standard_tmd_structure.vertex_number_str
        number_of_normals = standard_tmd_structure.normal_number_str
        number_of_primitives = standard_tmd_structure.primitive_number_str
        object_range_number = range(number_of_objects_int)
        values_merged = zip(object_range_number, number_of_vertices, number_of_normals, number_of_primitives)
        with open(os.path.join(new_folder, file_name) + "_TMD_report" + ".txt", 'w') as file_report:
            header_text = "File: " + standard_tmd.tmd_file + ", was extracted with TLoD - TMD Converter by DooMMetaL." + "\n" + "\n" + "\n"
            file_report.write(header_text)
            for items in values_merged:
                number_objects = str(items[0:1]).replace("(", "").replace("'", "").replace(")", "").replace(",", "")
                number_vertices = str(items[1:2]).replace("(", "").replace("'", "").replace(")", "").replace(",", "")
                number_normals = str(items[2:3]).replace("(", "").replace("'", "").replace(")", "").replace(",", "")
                number_primitives = str(items[3:4]).replace("(", "").replace("'", "").replace(")", "").replace(",", "")
                subtitle_obj = "Object N° " + number_objects + " " + "have:" + "\n"
                elements_sorted = "Vertices: " + number_vertices + " " + "-" + " " + "Normals: " + number_normals + " " + "-" + " " + "Primitives: " + number_primitives + "\n" + "\n"
                file_report.write(subtitle_obj)
                file_report.write(elements_sorted)
            total_number_vnp = "\n" + "Total number of: " + " " + "Vertices: " + str(standard_tmd_structure.vertex_number_total) + " " + "-" + " " + "Normals: " + str(standard_tmd_structure.normal_number_total) + " " + "-" + " " + "Primitives: " + str(standard_tmd_structure.primitive_number_total) + "\n" + "\n"
            time_now = "\n" + "Work finished at: " + str(datetime.datetime.now())
            file_report.write(total_number_vnp)
            file_report.write(time_now)
            total_number_vnp_print = "Total number of: " + " " + "Vertices: " + str(standard_tmd_structure.vertex_number_total) + " " + "-" + " " + "Normals: " + str(standard_tmd_structure.normal_number_total) + " " + "-" + " " + "Primitives: " + str(standard_tmd_structure.primitive_number_total)
            print(total_number_vnp_print)
    
    def primitives_for_object(self): # A method to calculate the amount of primitives extracted from the original byte block
        primitives_counter = 0
        tmd_object_primitives = standard_tmd_decoder.primobj_primitives
        
        global primitives_per_object
        primitives_per_object = []
        primitives_types_per_object_precalc = []
        for object_primitives in tmd_object_primitives:
            primitives_inside_obj = []
            primitives_type_inside_obj = []
            for obj_primitives in object_primitives:
                prim_nested_len = len(obj_primitives)
                primitives_inside_obj.append(prim_nested_len)
                for obj_prim in obj_primitives:
                    if obj_prim.get('lsc3vgt') != None:
                        primitives_type_inside_obj.append('lsc3vgt')
                    elif obj_prim.get('lsc3vft') != None:
                        primitives_type_inside_obj.append('lsc3vft')                    
                    elif obj_prim.get('newlsc3vgt') != None:
                        primitives_type_inside_obj.append('newlsc3vgt')
                    elif obj_prim.get('newlsc3vgt2') != None:
                        primitives_type_inside_obj.append('newlsc3vgt2')
                    elif obj_prim.get('lsc3vntgs') != None:
                        primitives_type_inside_obj.append('lsc3vntgs')
                    elif obj_prim.get('lsc3vntfs') != None:
                        primitives_type_inside_obj.append('lsc3vntfs')
                    elif obj_prim.get('lsc3vntgg') != None:
                        primitives_type_inside_obj.append('lsc3vntgg')
                    elif obj_prim.get('lsc3vntfg') != None:
                        primitives_type_inside_obj.append('lsc3vntfg')
                    elif obj_prim.get('lsc4vgt') != None:
                        primitives_type_inside_obj.append('lsc4vgt')
                    elif obj_prim.get('lsc4vft') != None:
                        primitives_type_inside_obj.append('lsc4vft')
                    elif obj_prim.get('newlsc4vgt') != None:
                        primitives_type_inside_obj.append('newlsc4vgt')
                    elif obj_prim.get('newlsc4vgt2') != None:
                        primitives_type_inside_obj.append('newlsc4vgt2')
                    elif obj_prim.get('lsc4vntgs') != None:
                        primitives_type_inside_obj.append('lsc4vntgs')
                    elif obj_prim.get('lsc4vntfs') != None:
                        primitives_type_inside_obj.append('lsc4vntfs')
                    elif obj_prim.get('lsc4vntgg') != None:
                        primitives_type_inside_obj.append('lsc4vntgg')
                    elif obj_prim.get('lsc4vntfg') != None:
                        primitives_type_inside_obj.append('lsc4vntfg')
                    elif obj_prim.get('newlsc4vntgs') != None:
                        primitives_type_inside_obj.append('newlsc4vntgs')
                    elif obj_prim.get('nlsc3vgt') != None:
                        primitives_type_inside_obj.append('nlsc3vgt')
                    elif obj_prim.get('nlsc3vft') != None:
                        primitives_type_inside_obj.append('nlsc3vft')
                    elif obj_prim.get('newnlsc3vgt') != None:
                        primitives_type_inside_obj.append('newnlsc3vgt')
                    elif obj_prim.get('nlsc3vntg') != None:
                        primitives_type_inside_obj.append('nlsc3vntg')
                    elif obj_prim.get('nlsc3vntf') != None:
                        primitives_type_inside_obj.append('nlsc3vntf')
                    elif obj_prim.get('nlsc4vgt') != None:
                        primitives_type_inside_obj.append('nlsc4vgt')
                    elif obj_prim.get('nlsc4vft') != None:
                        primitives_type_inside_obj.append('nlsc4vft')
                    elif obj_prim.get('newnlsc4vgt') != None:
                        primitives_type_inside_obj.append('newnlsc4vgt')
                    elif obj_prim.get('nlsc4vntg') != None:
                        primitives_type_inside_obj.append('nlsc4vntg')
                    elif obj_prim.get('nlsc4vntf') != None:
                        primitives_type_inside_obj.append('nlsc4vntf')
                    
                    else:
                        primitives_type_inside_obj.append("UNKNOWN_PRIMITIVE_TYPE")

            primitives_summatory = sum(primitives_inside_obj)
            primitives_per_object.append(primitives_summatory)
            primitives_types_per_object_precalc.append(primitives_type_inside_obj)
            primitives_counter += 1

        global primitives_in_obj
        primitives_in_obj = [] # Here will append the type of primitive and amount, present in each object inside the TMD /// need it nested lol
        for counted_by_type in primitives_types_per_object_precalc: # Primitive Type Counter
            primitives_types_per_object = []

            ptc_lsc3vgt = counted_by_type.count('lsc3vgt')
            ptc_lsc3vft = counted_by_type.count('lsc3vft')
            ptc_newlsc3vgt = counted_by_type.count('newlsc3vgt')
            ptc_newlsc3vgt2 = counted_by_type.count('newlsc3vgt2')
            ptc_lsc3vntgs = counted_by_type.count('lsc3vntgs')
            ptc_lsc3vntfs = counted_by_type.count('lsc3vntfs')
            ptc_lsc3vntgg = counted_by_type.count('lsc3vntgg')
            ptc_lsc3vntfg = counted_by_type.count('lsc3vntfg')
            ptc_lsc4vgt = counted_by_type.count('lsc4vgt')
            ptc_lsc4vft = counted_by_type.count('lsc4vft')
            ptc_newlsc4vgt = counted_by_type.count('newlsc4vgt')
            ptc_newlsc4vgt2 = counted_by_type.count('newlsc4vgt2')
            ptc_lsc4vntgs = counted_by_type.count('lsc4vntgs')
            ptc_lsc4vntfs = counted_by_type.count('lsc4vntfs')
            ptc_lsc4vntgg = counted_by_type.count('lsc4vntgg')
            ptc_lsc4vntfg = counted_by_type.count('lsc4vntfg')
            ptc_newlsc4vntgs = counted_by_type.count('newlsc4vntgs')
            ptc_nlsc3vgt = counted_by_type.count('nlsc3vgt')
            ptc_nlsc3vft = counted_by_type.count('nlsc3vft')
            ptc_newnlsc3vgt = counted_by_type.count('newnlsc3vgt')
            ptc_nlsc3vntg = counted_by_type.count('nlsc3vntg')
            ptc_nlsc3vntf = counted_by_type.count('nlsc3vntf')
            ptc_nlsc4vgt = counted_by_type.count('nlsc4vgt')
            ptc_nlsc4vft = counted_by_type.count('nlsc4vft')
            ptc_newnlsc4vgt = counted_by_type.count('newnlsc4vgt')
            ptc_nlsc4vntg = counted_by_type.count('nlsc4vntg')
            ptc_nlsc4vntf = counted_by_type.count('nlsc4vntf')
            ptc_unk_prim_type = counted_by_type.count('UNKNOWN_PRIMITIVE_TYPE')

            if ptc_lsc3vgt > 0:
                primitives_types_per_object.append(f'lsc_3vgt {ptc_lsc3vgt}')
            if ptc_lsc3vft > 0:
                primitives_types_per_object.append(f'lsc_3vft {ptc_lsc3vft}')
            if ptc_newlsc3vgt > 0:
                primitives_types_per_object.append(f'new_lsc_3vgt {ptc_newlsc3vgt}')
            if ptc_newlsc3vgt2 > 0:
                primitives_types_per_object.append(f'new_lsc_3vgt_2 {ptc_newlsc3vgt2}')
            if ptc_lsc3vntgs > 0:
                primitives_types_per_object.append(f'lsc_3vntgs {ptc_lsc3vntgs}')
            if ptc_lsc3vntfs > 0:
                primitives_types_per_object.append(f'lsc_3vntfs {ptc_lsc3vntfs}')
            if ptc_lsc3vntgg > 0:
                primitives_types_per_object.append(f'lsc_3vntgg {ptc_lsc3vntgg}')
            if ptc_lsc3vntfg > 0:
                primitives_types_per_object.append(f'lsc_3vntfg {ptc_lsc3vntfg}')
            if ptc_lsc4vgt > 0:
                primitives_types_per_object.append(f'lsc_4vgt {ptc_lsc4vgt}')
            if ptc_lsc4vft > 0:
                primitives_types_per_object.append(f'lsc_4vft {ptc_lsc4vft}')
            if ptc_newlsc4vgt > 0:
                primitives_types_per_object.append(f'new_lsc_4vgt {ptc_newlsc4vgt}')
            if ptc_newlsc4vgt2 > 0:
                primitives_types_per_object.append(f'new_lsc_4vgt_2 {ptc_newlsc4vgt2}')
            if ptc_lsc4vntgs > 0:
                primitives_types_per_object.append(f'lsc_4vntgs {ptc_lsc4vntgs}')
            if ptc_lsc4vntfs > 0:
                primitives_types_per_object.append(f'lsc_4vntfs {ptc_lsc4vntfs}')
            if ptc_lsc4vntgg > 0:
                primitives_types_per_object.append(f'lsc_4vntgg {ptc_lsc4vntgg}')
            if ptc_lsc4vntfg > 0:
                primitives_types_per_object.append(f'lsc_4vntfg {ptc_lsc4vntfg}')
            if ptc_newlsc4vntgs > 0:
                primitives_types_per_object.append(f'new_lsc_4vntgs {ptc_newlsc4vntgs}')
            if ptc_nlsc3vgt > 0:
                primitives_types_per_object.append(f'nlsc_3vgt {ptc_nlsc3vgt}')
            if ptc_nlsc3vft > 0:
                primitives_types_per_object.append(f'nlsc_3vgt {ptc_nlsc3vft}')
            if ptc_nlsc3vntf > 0:
                primitives_types_per_object.append(f'nlsc_3vntf {ptc_nlsc3vntf}')
            if ptc_newnlsc3vgt > 0:
                primitives_types_per_object.append(f'new_nlsc_3vgt {ptc_newnlsc3vgt}')
            if ptc_nlsc3vntg > 0:
                primitives_types_per_object.append(f'nlsc_3vntg {ptc_nlsc3vntg}')
            if ptc_nlsc3vntf > 0:
                primitives_types_per_object.append(f'nlsc_3vntf {ptc_nlsc3vntf}')
            if ptc_nlsc4vgt > 0:
                primitives_types_per_object.append(f'nlsc_4vgt {ptc_nlsc4vgt}')
            if ptc_nlsc4vft > 0:
                primitives_types_per_object.append(f'nlsc_4vft {ptc_nlsc4vft}')
            if ptc_newnlsc4vgt > 0:
                primitives_types_per_object.append(f'new_nlsc_4vgt {ptc_newnlsc4vgt}')
            if ptc_nlsc4vntg > 0:
                primitives_types_per_object.append(f'nlsc_4vntg {ptc_nlsc4vntg}')
            if ptc_nlsc4vntf > 0:
                primitives_types_per_object.append(f'nlsc_4vntf {ptc_nlsc4vntf}')
            if ptc_unk_prim_type > 0:
                primitives_types_per_object.append(f'Unknown_Primitive_Type {ptc_unk_prim_type}')
            
            else:
                pass

            primitives_in_obj.append(primitives_types_per_object)


    def primitives_per_obj_write(self):
        tmd_object_number = range(0, standard_tmd.tmd_nobj_expected)
        tmd_object_counter = 0
        prim_count = 0
        with open(os.path.join(new_folder, file_name) + "_Primitive_per_Object" + ".txt", 'w') as primitive_report:
            primitive_reporter_superheader = f'PRIMITIVE INSIGHT REPORT\n\n\n'
            primitive_reporter_header = f'File: {standard_tmd.tmd_file}, was extracted using TLoD - TMD Converter by DooMMetaL. \n \n \n'
            primitive_reporter_warning = f'This report file is used to debug and/or add New primitive types found. \nAlso helps to compare Obj Table Calculation and final extracted primitives. \nIf you are not sure what are you doing, please ignore this file.\n \n'
            primitive_reporter_advice = f'The current file contains the amount of primitives split per object in the TMD file: {file_name} \n \n \n'
            primitive_report.write(primitive_reporter_superheader)
            primitive_report.write(primitive_reporter_header)
            primitive_report.write(primitive_reporter_warning)
            primitive_report.write(primitive_reporter_advice)
            for prim_objects in tmd_object_number:
                obj_number_current = f'PRIMITIVES PRESENT IN OBJECT NUMBER: {tmd_object_counter}\n'
                primitive_sum_in_obj = f'Total extracted by the tool: {primitives_per_object[tmd_object_counter]}\nTotal calculated in Obj Table: {standard_tmd_structure.primitive_number_int[tmd_object_counter]}\n\n'
                primitive_report.write(obj_number_current)
                primitive_report.write(primitive_sum_in_obj)
                for prim_c in primitives_in_obj[prim_count]:
                    prim_type_num_write = f'{prim_c}\n'
                    primitive_report.write(prim_type_num_write)
                spacing = "\n\n"
                primitive_report.write(spacing)
                tmd_object_counter += 1
                prim_count += 1


class TmdConverter():
    def __init__(self, obj_conversion):
        self.self = TmdConverter
        self.obj_conversion = obj_conversion
    
    def object_converter(self):
        with open(os.path.join(new_folder, file_name) + ".obj", 'w') as object_3d:
            header_obj = "#File: " + standard_tmd.tmd_file + ", was converted using TLoD - TMD Converter by DooMMetaL." + "\n" + "\n" + "\n"
            mat_path = "mtllib " + standard_tmd.tmd_file.rstrip('.bin') + ".mtl" + "\n" + "\n"
            
            object_3d.write(header_obj)
            object_3d.write(mat_path)


            # VERTEX CONVERTER
            vertex_obj_header = "# Here start the Vertex Block of the model" + "\n" + "\n"
            object_3d.write(vertex_obj_header)

            for vertex_all_obj in standard_tmd_decoder.vertex_decoded: # NEED A PRE-SCALE FOR FITTING GOOD IN ANY 3D SOFTWARE
                for vertex_each in vertex_all_obj:                      # if i don't do this, the model can't be visible because of being super big
                    vertex_obj_scale = 1000
                    divide_vertex = [v / vertex_obj_scale for v in vertex_each]
                    vertex_x_l = divide_vertex[0:1]
                    vertex_y_l = divide_vertex[1:2]
                    vertex_z_l = divide_vertex[2:3]
                    vertex_x_str = "".join(str(vertex_x_l)).replace("[", "").replace("]", "")
                    vertex_y_str = "".join(str(vertex_y_l)).replace("[", "").replace("]", "")
                    vertex_z_str = "".join(str(vertex_z_l)).replace("[", "").replace("]", "")
                    
                    vertex_write_block = "v" + " " + vertex_x_str + " " + vertex_y_str + " " + vertex_z_str + " " + "1.0" + "\n"

                    object_3d.write(vertex_write_block)
            vertex_finish_write = "#" + " " + str(standard_tmd_structure.vertex_number_total) + " " + "Vertices" + "\n" + "\n"
            object_3d.write(vertex_finish_write)

            # PRIMITIVE CONVERTER (TEXTURE COORDINATE + FACES) - For this i will split the primitives into classifications LSC, NLSC, NEW PRIMITIVES
            
            #----------------------------------------------- TEXTURE COORDINATE WRITER -----------------------------------------------#
            texture_coordinate_header = "# Here start the Texture Coordinates Block of the model, if exist an object with no data, means that object have no textures" + "\n" + "\n"
            object_3d.write(texture_coordinate_header)
            obj_number_start = 0
            total_texture_coordinate = []
            for uv_conversion in standard_tmd_decoder.obj_primitives_uv:
                number_obj = [number for number in range(0, standard_tmd.tmd_nobj_expected)]
                uv_position = f'# This is Texture coordinate from Object Number: {number_obj[obj_number_start]}' + "\n" + "\n"
                obj_number_start += 1
                object_3d.write(uv_position)
                for uv_conv in uv_conversion:
                    for uv in uv_conv:
                        if uv.get("v3") != None:
                            u4_0 = uv.get("u0")
                            v4_0 = uv.get("v0")
                            u4_1 = uv.get("u1")
                            v4_1 = uv.get("v1")
                            u4_2 = uv.get("u2")
                            v4_2 = uv.get("v2")
                            u4_3 = uv.get("u3")
                            v4_3 = uv.get("v3")
                            converted_uv_4v = f'vt {u4_0} {(1 - v4_0)}' + "\n" + f'vt {u4_2} {(1 - v4_2)}' + "\n" + f'vt {u4_3} {(1 - v4_3)}' + "\n" + f'vt {u4_1} {(1 - v4_1)}' + "\n"
                            object_3d.write(converted_uv_4v)
                            total_texture_coordinate.append(4)
                        elif uv.get("u0") != None:
                            u3_0 = uv.get("u0")
                            v3_0 = uv.get("v0")
                            u3_1 = uv.get("u1")
                            v3_1 = uv.get("v1")
                            u3_2 = uv.get("u2")
                            v3_2 = uv.get("v2")
                            converted_uv_3v = f'vt {u3_2} {(1 - v3_2)}' + "\n" + f'vt {u3_1} {(1 - v3_1)}' + "\n" + f'vt {u3_0} {(1 - v3_0)}' + "\n"
                            object_3d.write(converted_uv_3v)
                            total_texture_coordinate.append(3)
                        else:
                            pass
                backslash_for_sep = "\n"
                object_3d.write(backslash_for_sep)
            total_tc = sum(total_texture_coordinate)
            total_number_coord = f'# {total_tc} Textures Coordinates' + "\n" + "\n"
            object_3d.write(total_number_coord)

            #-------------------------------------------------------------------------------------------------------------------------#

            # NORMAL CONVERTER

            normal_obj_header = "# Here start the Normal Block of the model" + "\n" + "\n"

            with open(os.path.join(new_folder, file_name) + ".mtl", 'w') as mat_obj:
                pass

            #-------------------------------------------------------------------------------------------------------------------------#
            # PRIMITIVE WRITER
            #-------------------------------------------------------------------------------------------------------------------------#
            face_header = f'# Here start the Faces Block of the model' + "\n" + "\n"
            object_3d.write(face_header)
            primitive_obj_number_start = 0
            vertex_index_init = 1
            vertex_numeration_first = standard_tmd_structure.vertex_number_int.copy()
            vertex_numeration_first.insert(0, vertex_index_init)
            vertex_numeration_second = list(itertools.accumulate(vertex_numeration_first))
            vertex_numeration = vertex_numeration_second
            primitive_count = []
            number_in_obj = [number for number in range(0, standard_tmd.tmd_nobj_expected)]
            tc_number = 0
            for face_conversion in standard_tmd_decoder.obj_primitives_vertexindex:
                object_face_number = f'# Primitives for Object Number: {number_in_obj[primitive_obj_number_start]}' + "\n" + "\n"
                object_face_group = f'g Object_Number_{number_in_obj[primitive_obj_number_start]}' + "\n" + f'usemtl Object_Number_{number_in_obj[primitive_obj_number_start]}' + "\n"
                object_3d.write(object_face_number)
                object_3d.write(object_face_group)
                vertex_index_num = vertex_numeration[number_in_obj[primitive_obj_number_start]]
                for faces in face_conversion:
                    for f in faces:
                        # TEXTURED OBJECTS
                        if f.get("v3") != None:
                            face4v_v0 = f.get("vertex0")
                            face4v_v1 = f.get("vertex1")
                            face4v_v2 = f.get("vertex2")
                            face4v_v3 = f.get("vertex3")
                            converted_4v_faces_textured = f'f {face4v_v0 + vertex_index_num}/{tc_number + 1} {face4v_v2 + vertex_index_num}/{tc_number + 2} {face4v_v3 + vertex_index_num}/{tc_number + 3} {face4v_v1 + vertex_index_num}/{tc_number + 4}' + "\n"
                            object_3d.write(converted_4v_faces_textured)
                            primitive_count.append(1)
                            tc_number += 4
                        elif f.get("u0") != None:
                            face3v_v0 = f.get("vertex0")
                            face3v_v1 = f.get("vertex1")
                            face3v_v2 = f.get("vertex2")
                            converted_3v_faces_textured = f'f {face3v_v2 + vertex_index_num}/{tc_number + 1} {face3v_v1 + vertex_index_num}/{tc_number + 2} {face3v_v0 + vertex_index_num}/{tc_number + 3}' + "\n"
                            object_3d.write(converted_3v_faces_textured)
                            primitive_count.append(1)
                            tc_number += 3
                        # NO TEXTURE OBJECTS
                        elif f.get("vertex3") != None:
                            face4v_vi0 = f.get("vertex0")
                            face4v_vi1 = f.get("vertex1")
                            face4v_vi2 = f.get("vertex2")
                            face4v_vi3 = f.get("vertex3")
                            converted_4v_faces_notextured = f'f {face4v_vi0 + vertex_index_num} {face4v_vi2 + vertex_index_num} {face4v_vi3 + vertex_index_num} {face4v_vi1 + vertex_index_num}' + "\n"
                            object_3d.write(converted_4v_faces_notextured)
                            primitive_count.append(1)
                        elif f.get("vertex0") != None:
                            face3v_vi0 = f.get("vertex0")
                            face3v_vi1 = f.get("vertex1")
                            face3v_vi2 = f.get("vertex2")
                            converted_3v_faces_notextured = f'f {face3v_vi2 + vertex_index_num} {face3v_vi1 + vertex_index_num} {face3v_vi0 + vertex_index_num}' + "\n"
                            object_3d.write(converted_3v_faces_notextured)
                            primitive_count.append(1)
                        else:
                            print("This message it's a warning to re-check the code for the writer, if you see this, be sure of report this bug!")
                face_backslash = "\n"
                object_3d.write(face_backslash)
                primitive_obj_number_start += 1
            total_primitive_count = sum(primitive_count)
            if total_primitive_count == standard_tmd_structure.primitive_number_total:
                print("The Primitive Count and Conversion count are equal, so everything is fine")
            else:
                print("WARNING: The primitive Count and Conversion count are different, this could mean a bug in the tool or a New Primitive Type found")
