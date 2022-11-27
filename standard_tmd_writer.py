"""

Standard TMD Structure Writer: This module write the Standard TMD structure data into
TMD Properties and Debug data, DAE data write is done by tlod_tmd_saf_collada.py 
because this module has to be very flexible and easy to update

Copyright (C) 2022 DooMMetaL

"""
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

        try:
            os.makedirs(new_folder, exist_ok=True)
        except OSError:
            print("Can't create the folder, permission denied")
        
        print("Please, enter a desired name for the file converted,\nKeep in mind that the chosen name will be add to the end of the filename,\nEx: Idle, Pose, Run")
        global animation_final_name
        animation_final_name = input()
        if animation_final_name == '':
            print("You Should enter a file name, exiting")
        else:
            pass 


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
        tmd_object_primitives = standard_tmd_decoder.collada_primitives
        
        global primitives_per_object
        primitives_per_object = []
        primitives_types_per_object_precalc = []
        for object_primitives in tmd_object_primitives:
            primitives_inside_obj = []
            primitives_type_inside_obj = []
            prim_nested_len = len(object_primitives)
            primitives_inside_obj.append(prim_nested_len)
            for obj_prim in object_primitives:
                
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
                # NEW PRIMITIVES FOUND AFTER RELEASE 0.1 GO HERE
                elif obj_prim.get('newlsc4vntgg') != None:
                    primitives_type_inside_obj.append('newlsc4vntgg')
                elif obj_prim.get('newlsc3vntgg') != None:
                    primitives_type_inside_obj.append('newlsc3vntgg')
                elif obj_prim.get('newlsc3vntfg') != None:
                    primitives_type_inside_obj.append('newlsc3vntfg')
                
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
            # NEW PRIMITIVES FOUND AFTER RELEASE 0.1 GO HERE
            ptc_newlsc4vntgg = counted_by_type.count('newlsc4vntgg')
            ptc_newlsc3vntgg = counted_by_type.count('newlsc3vntgg')
            ptc_newlsc3vntfg = counted_by_type.count('newlsc3vntfg')
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
            # NEW PRIMITIVES FOUND AFTER RELEASE 0.1 GO HERE
            if ptc_newlsc4vntgg > 0:
                primitives_types_per_object.append(f'new_lsc_4vntgg {ptc_newlsc4vntgg}')
            if ptc_newlsc3vntgg > 0:
                primitives_types_per_object.append(f'new_lsc_3vntgg {ptc_newlsc3vntgg}')
            if ptc_newlsc3vntfg > 0:
                primitives_types_per_object.append(f'new_lsc_3vntfg {ptc_newlsc3vntfg}')
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
            time_now = f'Work finished at: ' + str(datetime.datetime.now())
            primitive_report.write(time_now)