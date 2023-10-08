"""

Properties Writer: This module write the model structure data into
Properties and Debug data.
This data will be dumped as Plain Text file (*.txt).
Also this module will create the folders and subfolders to place
the converted model

Copyright (C) 2023 DooMMetaL

"""
import os
import datetime
import collections as coll

from tkinter import messagebox

class NewFolder:
    def __init__(self, model_path):
        self.self = NewFolder
        self.create_new_folder(model_path=model_path)

    def create_new_folder(self, model_path=str):
        global new_folder
        global file_name
        path_folder = os.path.dirname(model_path)
        file_path_complete = (model_path).strip()
        file_name_complete = os.path.basename(file_path_complete)
        file_name = os.path.splitext(file_name_complete)[0]
        check_model_path = os.path.isdir(model_path) # If not a directory... will continue
        if check_model_path == False:
            file_name = file_name + f'_converted'
        new_folder = os.path.join(path_folder, file_name)

        try:
            os.makedirs(new_folder, exist_ok=True)
        except OSError:
            error_folder = f'Can\'t create the folder, permission denied'
            error_folder_window = messagebox.showerror(title='System Error...', message=error_folder)
            exit()

class DebugWriter:
    def __init__(self, file_path, num_obj_model, num_vertex_model, num_normal_model, num_primitive_model, prim_decoded):
        self.self = DebugWriter
        self.model_informer(file_path=file_path, num_obj_mod=num_obj_model, num_vertex_mod=num_vertex_model, num_normal_mod=num_normal_model, num_primitive_mod=num_primitive_model)
        self.primitives_per_object_write(file_path=file_path, number_objs=num_obj_model, primitive_numbers=num_primitive_model, prim_decoded=prim_decoded)
        self.primdata_write(file_path=file_path, number_objs=num_obj_model, prim_numb=num_primitive_model, primitive_decoded=prim_decoded)
    
    def model_informer(self, file_path=str, num_obj_mod=int, num_vertex_mod=list, num_normal_mod=list, num_primitive_mod=list):
        number_of_objects_int = num_obj_mod
        with open(file_path + "_TMD_report" + ".txt", 'w') as file_report:
            header_text = f'File: {file_path}, was converted with TLoD - TMD Converter by DooMMetaL.\n\n\n'
            file_report.write(header_text)
            for object_number in range(0, number_of_objects_int):
                number_vertices = num_vertex_mod[object_number]
                number_normals = num_normal_mod[object_number]
                number_primitives = num_primitive_mod[object_number]
                subtitle_obj = f'Object N° {object_number} have:\n'
                elements_sorted = f'Vertices: {number_vertices} - Normals: {number_normals} - Primitives: {number_primitives}\n\n'
                file_report.write(subtitle_obj)
                file_report.write(elements_sorted)
            global total_number_vnp
            total_number_vnp = f'\nTotal number of ==> Vertices: {sum(num_vertex_mod)} - Normals: {sum(num_normal_mod)} - Primitives: {sum(num_primitive_mod)}\n\n'
            time_now = f'\nWork finished at: {datetime.datetime.now()}'
            file_report.write(total_number_vnp)
            file_report.write(time_now)
    
    def primitives_per_object_write(self, file_path=str, number_objs=int, primitive_numbers=list, prim_decoded=list):
        prim_count = 0
        with open(file_path + "_Primitive_per_Object" + ".txt", 'w') as primitive_report:
            primitive_reporter_superheader = f'PRIMITIVE INSIGHT REPORT\n'
            primitive_reporter_header = f'File: {file_path}, was extracted using TLoD - TMD Converter by DooMMetaL.\n\n\n'
            primitive_reporter_warning = f'This report file is used to debug and/or add New primitive types found. \nAlso helps to compare Obj Table Calculation and final extracted primitives.\nIf you are not sure what are you doing, please ignore this file.\n\n'
            primitive_reporter_advice = f'The current file contains the amount of primitives split per object in the TMD file: {file_path}\n\n\n'
            all_text = primitive_reporter_superheader + primitive_reporter_header + primitive_reporter_warning + primitive_reporter_advice
            primitive_report.write(all_text)
            calc_primitives_obtained = self.count_decoded_prims(primitives_decoded=prim_decoded)
            primitives_obtained = calc_primitives_obtained[0]
            quantity_primitives = calc_primitives_obtained[1]
            for current_object in range(0, number_objs):
                obj_number_current = f'PRIMITIVES PRESENT IN OBJECT NUMBER: {current_object}\n'
                primitive_report.write(obj_number_current)
                current_primitives = primitives_obtained[current_object]
                primitive_sum_in_obj = f'Total extracted by the tool: {quantity_primitives[current_object]}\nTotal calculated in Obj Table: {primitive_numbers[current_object]}\n\n'
                primitive_report.write(primitive_sum_in_obj)
                for prim_c in current_primitives:
                    prim_new_str = str(prim_c).replace("'", "").replace("(", "").replace(")", "").replace(",", "")
                    prim_type_num_write = f'{prim_new_str}\n'
                    primitive_report.write(prim_type_num_write)
                spacing = "\n\n"
                primitive_report.write(spacing)
                prim_count += 1
            time_now = f'Work finished at: ' + str(datetime.datetime.now())
            primitive_report.write(time_now)
    
    def primdata_write(self, file_path=str, number_objs=int, prim_numb=int, primitive_decoded=list):
        texture_data_in_object = []
        for current_object in range(0, number_objs):
            number_of_current_primitives = prim_numb[current_object]
            current_primitive_set = primitive_decoded[current_object]
            texture_data_in_primitive = []
            for current_primitive_number in range(0, number_of_current_primitives):
                this_primitive = current_primitive_set[current_primitive_number]
                if this_primitive.get('u0') != None:
                    start_magic_string_primitive = b'\x50\x52\x49\x4D'
                    primitive_number = int.to_bytes(current_primitive_number, 4, 'little', signed=False)
                    get_cba = this_primitive.get('cba')
                    get_tsb = this_primitive.get('tsb')
                    array_bytes_complete = start_magic_string_primitive + primitive_number + get_cba + get_tsb
                    texture_data_in_primitive.append(array_bytes_complete)
            joined_texture_data = b''.join(texture_data_in_primitive)
            current_object_bytes = int.to_bytes(current_object, 4, 'little', signed=False)
            start_magic_string_object = b'\x4F\x42\x4A\x5F'
            end_magic_string_object = b'\x5F\x45\x4E\x44'
            final_texture_process = start_magic_string_object + current_object_bytes + joined_texture_data + current_object_bytes + end_magic_string_object
            texture_data_in_object.append(final_texture_process)
        
        finished_texture_data = b''.join(texture_data_in_object)
        number_objects_bytes = int.to_bytes(number_objs, length=4, byteorder='little', signed=False)
        header_magic = b'\x50\x52\x49\x4D\x44\x41\x54\x41'

        final_package = header_magic + number_objects_bytes + finished_texture_data

        with open(file_path + ".primdata", 'wb') as write_data:
            write_data.write(final_package)


    @staticmethod
    def count_decoded_prims(primitives_decoded=list):
        model_object_level = []
        number_primitives_decoded = []

        for object_level in primitives_decoded:
            primitive_level_obtained = []
            for primitive_level in object_level:
                key_primitive = list(primitive_level.values())
                prim_type = key_primitive[0]
                primitive_level_obtained.append(prim_type)
            
            counting_prims = list(coll.Counter(primitive_level_obtained).items())
            prim_quantity = len(primitive_level_obtained)
            model_object_level.append(counting_prims)
            number_primitives_decoded.append(prim_quantity)
        return model_object_level, number_primitives_decoded