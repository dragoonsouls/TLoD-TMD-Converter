"""

Custom TMD Structure Writer: This module write the Custom TMD structure data into
TMD Properties and Debug data, OBJ. As the standard version of the writer, DAE write will be in a separate *.py file
because this module has to be very flexible and easy to update

Copyright (C) 2021 DooMMetaL

"""

import os
from posixpath import basename
import custom_tmd # USING THE VARIABLES FROM HERE, DUE TO BE MORE EASY TO CATCH FROM THE GLOBAL SCOPE
import custom_tmd_structure
import datetime
import custom_tmd_decoder

class NewFolderCustom():                      # THIS CLASS IS IN CHARGE OF CREATING A DUMP FOLDER AND TO TAKE THE FILE NAME, USED AFTER
    def __init__(self, create_folder):        # FOR NAMING FILES DUMPED
        self.self = NewFolderCustom
        self.create_folder = create_folder
    
    def custom_convert_folder(self):
        global custom_file_name
        global custom_new_folder

        custom_path_folder = os.path.dirname(custom_tmd.custom_tmd_file)
        file_path_complete = (custom_tmd.custom_tmd_file).strip()
        file_name_complete = os.path.basename(file_path_complete)
        custom_file_name = os.path.splitext(file_name_complete)[0]
        custom_new_folder = os.path.join(custom_path_folder, custom_file_name)

        # FOR VNP SEPARATOR CLASS
        global custom_vnp_folder
        vnp_path = f'VNP_blocks'
        custom_vnp_folder = os.path.join(custom_new_folder, vnp_path)

        try:
            os.makedirs(custom_new_folder, exist_ok=True)
        except OSError:
            print("Can't create the folder, permission denied")

        print("Please, enter a desired name for the file converted,\nKeep in mind that the chosen name will be add to the end of the filename,\nEx: Idle, Pose, Run")
        global custom_animation_final_name
        custom_animation_final_name = input()
        if custom_animation_final_name == '':
            print("You Should enter a file name, exiting")
        else:
            pass

class CustomClutData: # THIS CLASS MUST BE REWRITED SINCE THERE IS CODE USED WHICH IS DEPRECATED
    def __init__(self, clut_writer):
        self.self = CustomClutData
        self.clut_interpreter = clut_writer
    
    def clut_write(self):
        with open(os.path.join(custom_new_folder, custom_file_name) + "_CLUT_EXTRA_DATA" + ".txt", 'w') as clut_data_writer:
            header_clut_text = f'File: {custom_tmd.custom_tmd_file}, was extracted using TLoD - TMD Converter by DooMMetaL. \n \n \n'
            clut_data_writer.write(header_clut_text)

            clut_data = custom_tmd_decoder.clut_data_decoded
            search_this_value = (0, 0, 0, 0)
            search_this_value_2 = (12, 0, 0, 0)
            clut_data_vram_index_start = clut_data.index(search_this_value) + 1
            clut_data_vram_index_end = clut_data.index(search_this_value_2)
            clut_data_vram = clut_data[clut_data_vram_index_start:clut_data_vram_index_end]
            pre_clut_data = clut_data[0:clut_data_vram_index_start]
            post_clut_data = clut_data[clut_data_vram_index_end:(clut_data_vram_index_end + 12)]
            clut_data_vram_len = len(clut_data_vram)
            post_clut_data_len = len(post_clut_data)

            header_id = pre_clut_data[0]
            header_id_data_left = pre_clut_data[1:]
            header_id_data_left_len = len(header_id_data_left)

            header_id_write = f'Custom TMD File ID: {header_id} \n \n'.replace("(", "").replace(")", "").replace(", ", "_")
            clut_data_writer.write(header_id_write)
            
            next_index = 0
            while header_id_data_left_len > 0 :
                id_data_extract = str(header_id_data_left[next_index]).replace("(", "").replace(")", "").replace(", ", "      ")
                id_data_left_write = f'The next is additional data in the pre-header: {id_data_extract} \n'
                clut_data_writer.write(id_data_left_write)
                header_id_data_left_len -= 1
                next_index += 1
            separation_space = f'\n \n \n'

            clut_data_writer.write(separation_space)
            
            clut_vram_info = f'############### HERE STARTS THE VRAM DATA IN THE CUSTOM TMD ############### \n \n'
            clut_data_writer.write(clut_vram_info)
            clut_data_index_s = 0
            clut_data_index_e = 1
            while clut_data_vram_len > 0:
                clut_vram_extracted = clut_data_vram[clut_data_index_s:clut_data_index_e]
                clut_vram_write = f'## VRAM - DATA ## {clut_vram_extracted} \n'.replace("(", "").replace(")", "").replace(", ", "       ")
                clut_data_writer.write(clut_vram_write)
                clut_data_vram_len -= 1
                clut_data_index_s += 1
                clut_data_index_e += 1
            
            separation_space_2 = f'\n \n \n'

            clut_data_writer.write(separation_space_2)
            
            start_post_clut = 0
            end_post_clut = 1
            while post_clut_data_len > 0:
                post_clut_write = f'Here is the data from the 0x 0C header: {post_clut_data[start_post_clut:end_post_clut]}\n'.replace("(", "").replace(")", "").replace(", ", "       ")
                clut_data_writer.write(post_clut_write)
                post_clut_data_len -= 1
                start_post_clut += 1
                end_post_clut += 1
            
            separation_space_3 = f'\n \n \n'
            clut_data_writer.write(separation_space_3)
            
            time_now = "\n" + "Work finished at: " + str(datetime.datetime.now())
            clut_data_writer.write(time_now)

class CustomTmdReporter:
    def __init__(self, report_file):
        self.self = CustomTmdReporter
        self.report_file = report_file
    
    def custom_tmd_reporter(self):
        with open(os.path.join(custom_new_folder, custom_file_name) + "_Custom_TMD_Report" + ".txt", 'w') as report_writer:
            reporter_file_header = f'File: {custom_tmd.custom_tmd_file}, was extracted using TLoD - TMD Converter by DooMMetaL. \n \n \n'
            report_writer.write(reporter_file_header)

            current_obj_num = 0
            all_obj_num = custom_tmd.ctmd_nobj_expected
            while all_obj_num > 0 :
                vertex_current = custom_tmd_structure.cvertex_number_int[current_obj_num]
                normal_current = custom_tmd_structure.cnormal_number_int[current_obj_num]
                primitive_current = custom_tmd_structure.cprimitive_number_int[current_obj_num]
                
                obj_current_text = f'Object N° {current_obj_num} have: \n'
                vnp_current_text = f'Vertices: {vertex_current} - Normals: {normal_current} - Primitives: {primitive_current} \n \n'
                report_writer.write(obj_current_text)
                report_writer.write(vnp_current_text)
                
                current_obj_num += 1
                all_obj_num -= 1
            
            space_pad = "\n \n \n"
            report_writer.write(space_pad)
            
            total_vertices = custom_tmd_structure.cvertex_number_total
            total_normals = custom_tmd_structure.cnormal_number_total
            total_primitives = custom_tmd_structure.cprimitive_number_total

            total_obj_vnp = f'Total N° of: Objects: {custom_tmd.ctmd_nobj_expected} - Vertices: {custom_tmd_structure.cvertex_number_total} - Normals: {custom_tmd_structure.cnormal_number_total} - Primitives: {custom_tmd_structure.cprimitive_number_total} \n \n'
            report_writer.write(total_obj_vnp)

            time_now = "\n" + "Work finished at: " + str(datetime.datetime.now())
            report_writer.write(time_now)




