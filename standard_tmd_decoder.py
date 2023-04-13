"""

Standard TMD Decoder: This module decode the data from Vertex, Normal and Primitives
into integers/strings for easy read/write for the Standard TMD Writer.
This module has to be very flexible and easy to update.

Copyright (C) 2023 DooMMetaL

"""
from tkinter import messagebox

class VertexInterpreter():
    def __init__(self, vertex_number_list, vertex_to_decode):
        self.self = VertexInterpreter
        self.vertex_to_decode = vertex_to_decode
        self.vertex_number_list = vertex_number_list
        self.vertex_decoder(vertex_number_list=vertex_number_list, vertex_to_decode=vertex_to_decode)
    
    def vertex_decoder(self, vertex_number_list=int, vertex_to_decode=list):
        vertex_raw_4 = []
        vertex_number_in_obj = zip(vertex_number_list, vertex_to_decode)
        for num_v, vertices_raw in vertex_number_in_obj:
            vertices_split = []
            number_vertex = num_v
            start_vertex_count = 0
            end_vertex_count = 8
            while number_vertex > 0:
                vertices_split_in_4 = vertices_raw[start_vertex_count:end_vertex_count]
                number_vertex -= 1
                start_vertex_count += 8
                end_vertex_count += 8
                vertices_split.append(vertices_split_in_4)
            vertex_raw_4.append(vertices_split)
        
        vertex_decoded = []
        for vertices_splitted in vertex_raw_4:
            vertex_in_obj = []
            for vertex_pos in vertices_splitted:
                vertex_single = []
                vertex_x = int.from_bytes(vertex_pos[0:2], 'little', signed=True)
                vertex_y = int.from_bytes(vertex_pos[2:4], 'little', signed=True)
                vertex_z = int.from_bytes(vertex_pos[4:6], 'little', signed=True)
                vertex_pad = vertex_pos[6:8] # IGNORED BUT TAKING THIS VALUE IN ACCOUNT BY ANY CASE OF A NEW FINDING
                vertex_single.append(vertex_x)
                vertex_single.append(vertex_y)
                vertex_single.append(vertex_z)

                vertex_in_obj.append(vertex_single)
            vertex_decoded.append(vertex_in_obj)

        return vertex_decoded

class NormalInterpreter():
    def __init__(self, normal_number_list, normal_to_decode):
        self.self = NormalInterpreter
        self.normal_number_list = normal_number_list
        self.normal_to_decode = normal_to_decode
        self.normal_decoder(normal_number_list=normal_number_list, normal_to_decode=normal_to_decode)
    
    def normal_decoder(self, normal_number_list=int, normal_to_decode=list):
        normal_raw_4 = []
        normal_number_in_obj = zip(normal_number_list, normal_to_decode)
        for num_n, normal_raw in normal_number_in_obj:
            normal_split = []
            number_normal = num_n
            start_normal_count = 0
            end_normal_count = 8
            while number_normal > 0:
                normal_split_in_4 = normal_raw[start_normal_count:end_normal_count]
                number_normal -= 1
                start_normal_count += 8
                end_normal_count += 8
                normal_split.append(normal_split_in_4)
            normal_raw_4.append(normal_split)
        
        normal_decoded = []
        for normal_splitted in normal_raw_4:
            normal_in_obj = []
            for normal_pos in normal_splitted:
                normal_single = []
                normal_x = int.from_bytes(normal_pos[0:2], 'little', signed=True)
                normal_y = int.from_bytes(normal_pos[2:4], 'little', signed=True)
                normal_z = int.from_bytes(normal_pos[4:6], 'little', signed=True)
                normal_pad = normal_pos[6:8] # IGNORED BUT TAKING THIS VALUE IN ACCOUNT BY ANY CASE OF A NEW FINDING
                normal_single.append(normal_x)
                normal_single.append(normal_y)
                normal_single.append(normal_z)

                normal_in_obj.append(normal_single)
            normal_decoded.append(normal_in_obj)
        
        return normal_decoded

class PrimitiveTmd:
    """ The very first idea was using the bit reading of each packet header... doing that will need a LOT of refactor"""
    def __init__(self, primitive_number_list, primitive_to_decode, number_of_primitives):
        self.self = PrimitiveTmd
        self.primitive_number_list = primitive_number_list
        self.primitive_to_decode = primitive_to_decode
        self.number_of_primitives = number_of_primitives
    
    def decode_primitive(self, primitive_number_list=int, primitive_to_decode=list, number_of_primitives=list):

        primitive_block_complete = primitive_to_decode
        primitive_number = primitive_number_list
        length_prim_block = len(primitive_block_complete)
        number_primitives_complete = number_of_primitives

        collada_primitives = []

        for current_prim_block_num in range(0, length_prim_block):
            current_prim_block = primitive_block_complete[current_prim_block_num]
            current_number_primitives = number_primitives_complete[current_prim_block_num]
            
            primitives_in_object = []
            next_primitive_start = 0
            for current_primitive_num in range(0, current_number_primitives):
                decoded_primitive = {'Prim_Name': f''}
                current_primitive = current_prim_block[next_primitive_start:]
                primitive_packet_header = current_primitive[0:4]
                olen = primitive_packet_header[0] # Currently not used
                ilen = primitive_packet_header[1]
                flag = primitive_packet_header[2]
                mode = primitive_packet_header[3]

                # FLAG
                key_light_name = f''
                face_var = f'' # Calculated but not used at the moment
                grad_var = f''
                # MODE
                brigth_var = f'' # Calculated but not used at the moment
                translucency_var = f'' # Calculated but not used at the moment ||| i will soon
                texture_var = f''
                vertex_var = f''
                shading_var = f''
                
                # FLAG Calcs
                if (flag & (1 << 0)): # NLSC (the bits 3 to 7 are ignored in this case)
                    key_light_name = f'NLSC_'
                else: # LSC
                    key_light_name = f'LSC_'
                
                if (flag & (1 << 1)):
                    face_var = f'double_face'
                else:
                    face_var = f'single_face'
                
                if (flag & (1 << 2)):
                    grad_var = f'Gradation_'
                else:
                    grad_var = f'Solid_'
                
                # MODE Calcs (the bits 5 to 7 are ignored in this case)
                if (mode & (1 << 0)):
                    brigth_var = f'BRIGHT OFF'
                else:
                    brigth_var = f' BRIGHT ON'
                
                if (mode & (1 << 1)):
                    translucency_var = f'Translucent'
                else:
                    translucency_var = f'No-Translucent'
                
                if (mode & (1 << 2)):
                    texture_var = f'Texture_'
                else:
                    texture_var = f'No-Texture_'
                
                if (mode & (1 << 3)):
                    vertex_var = f'4Vertex_'
                else:
                    vertex_var = f'3Vertex_'
                
                if (mode & (1 << 4)):
                    shading_var = f'Gouraud_'
                else:
                    shading_var = f'Flat_'
                
                # Setting Primitive Name
                prim_name_key = f'{key_light_name}{vertex_var}{shading_var}{texture_var}{grad_var}{translucency_var}'
                decoded_primitive['Prim_Name'] = prim_name_key

                if key_light_name == f'LSC_':
                    if vertex_var == f'3Vertex_':
                        if (texture_var == 'No-Texture_') and (shading_var == f'Gouraud_') and (grad_var == f'Solid_'):
                            decoded_primitive.update({
                            f'r0': int.from_bytes(current_primitive[4:5], byteorder='little'), f'g0': int.from_bytes(current_primitive[5:6], byteorder='little'), f'b0': int.from_bytes(current_primitive[6:7], byteorder='little'), f'mode_val': current_primitive[7:8], 
                            f'normal0': int.from_bytes(current_primitive[8:10], byteorder='little'), f'vertex0': int.from_bytes(current_primitive[10:12], byteorder='little'), 
                            f'normal1': int.from_bytes(current_primitive[12:14], byteorder='little'), f'vertex1': int.from_bytes(current_primitive[14:16], byteorder='little'), 
                            f'normal2': int.from_bytes(current_primitive[16:18], byteorder='little'), f'vertex2': int.from_bytes(current_primitive[18:20], byteorder='little')})
                        
                        elif (texture_var == 'No-Texture_') and (shading_var == f'Flat_') and (grad_var == f'Solid_'):
                            decoded_primitive.update({
                            f'r0': int.from_bytes(current_primitive[4:5], byteorder='little'), f'g0': int.from_bytes(current_primitive[5:6], byteorder='little'), f'b0': int.from_bytes(current_primitive[6:7], byteorder='little'), f'mode_val': current_primitive[7:8], 
                            f'normal0': int.from_bytes(current_primitive[8:10], byteorder='little'), f'vertex0': int.from_bytes(current_primitive[10:12], byteorder='little'), 
                            f'vertex1': int.from_bytes(current_primitive[12:14], byteorder='little'), f'vertex2': int.from_bytes(current_primitive[14:16], byteorder='little')})
                       
                        elif (texture_var == 'No-Texture_') and (shading_var == f'Gouraud_') and (grad_var == f'Gradation_'):
                            decoded_primitive.update({
                            f'r0': int.from_bytes(current_primitive[4:5], byteorder='little'), f'g0': int.from_bytes(current_primitive[5:6], byteorder='little'), f'b0': int.from_bytes(current_primitive[6:7], byteorder='little'), f'mode_val': current_primitive[7:8], 
                            f'r1': int.from_bytes(current_primitive[8:9], byteorder='little'), f'g1': int.from_bytes(current_primitive[9:10], byteorder='little'), f'b1': int.from_bytes(current_primitive[10:11], byteorder='little'), f'pad_val0': current_primitive[11:12], 
                            f'r2': int.from_bytes(current_primitive[12:13], byteorder='little'), f'g2': int.from_bytes(current_primitive[13:14], byteorder='little'), f'b2': int.from_bytes(current_primitive[14:15], byteorder='little'), f'pad_val1': current_primitive[15:16], 
                            f'normal0': int.from_bytes(current_primitive[16:18], byteorder='little'), f'vertex0': int.from_bytes(current_primitive[18:20], byteorder='little'), 
                            f'normal1': int.from_bytes(current_primitive[20:22], byteorder='little'), f'vertex1': int.from_bytes(current_primitive[22:24], byteorder='little'), 
                            f'normal2': int.from_bytes(current_primitive[24:26], byteorder='little'), f'vertex2': int.from_bytes(current_primitive[26:28], byteorder='little')})
                        
                        elif (texture_var == 'No-Texture_') and (shading_var == f'Flat_') and (grad_var == f'Gradation_'):
                            decoded_primitive.update({
                            f'r0': int.from_bytes(current_primitive[4:5], byteorder='little'), f'g0': int.from_bytes(current_primitive[5:6], byteorder='little'), f'b0': int.from_bytes(current_primitive[6:7], byteorder='little'), f'mode_val': current_primitive[7:8], 
                            f'r1': int.from_bytes(current_primitive[8:9], byteorder='little'), f'g1': int.from_bytes(current_primitive[9:10], byteorder='little'), f'b1': int.from_bytes(current_primitive[10:11], byteorder='little'), f'pad_val0': current_primitive[11:12], 
                            f'r2': int.from_bytes(current_primitive[12:13], byteorder='little'), f'g2': int.from_bytes(current_primitive[13:14], byteorder='little'), f'b2': int.from_bytes(current_primitive[14:15], byteorder='little'), f'pad_val1': current_primitive[15:16], 
                            f'normal0': int.from_bytes(current_primitive[16:18], byteorder='little'), f'vertex0': int.from_bytes(current_primitive[18:20], byteorder='little'),
                            f'vertex1': int.from_bytes(current_primitive[20:22], byteorder='little'), f'vertex2': int.from_bytes(current_primitive[22:24], byteorder='little')})
                        
                        elif (texture_var == 'Texture_') and (shading_var == f'Gouraud_'):
                            decoded_primitive.update({
                            f'u0': (int.from_bytes(current_primitive[4:5], byteorder='little') / 256), f'v0': (int.from_bytes(current_primitive[5:6], byteorder='little') / 256), f'cba': current_primitive[6:8], 
                            f'u1': (int.from_bytes(current_primitive[8:9], byteorder='little') / 256), f'v1': (int.from_bytes(current_primitive[9:10], byteorder='little') / 256), f'tsb': current_primitive[10:12], 
                            f'u2': (int.from_bytes(current_primitive[12:13], byteorder='little') / 256), f'v2': (int.from_bytes(current_primitive[13:14], byteorder='little') / 256), f'pad_value0': current_primitive[14:16], 
                            f'normal0': int.from_bytes(current_primitive[16:18], byteorder='little'), f'vertex0': int.from_bytes(current_primitive[18:20], byteorder='little'), 
                            f'normal1': int.from_bytes(current_primitive[20:22], byteorder='little'), f'vertex1': int.from_bytes(current_primitive[22:24], byteorder='little'), 
                            f'normal2': int.from_bytes(current_primitive[24:26], byteorder='little'), f'vertex2': int.from_bytes(current_primitive[26:28], byteorder='little')})
                        
                        elif (texture_var == 'Texture_') and (shading_var == f'Flat_'):
                            decoded_primitive.update({
                            f'u0': (int.from_bytes(current_primitive[4:5], byteorder='little') / 256), f'v0': (int.from_bytes(current_primitive[5:6], byteorder='little') / 256), f'cba': current_primitive[6:8], 
                            f'u1': (int.from_bytes(current_primitive[8:9], byteorder='little') / 256), f'v1': (int.from_bytes(current_primitive[9:10], byteorder='little') / 256), f'tsb': current_primitive[10:12], 
                            f'u2': (int.from_bytes(current_primitive[12:13], byteorder='little') / 256), f'v2': (int.from_bytes(current_primitive[13:14], byteorder='little') / 256), f'pad_value0': current_primitive[14:16], 
                            f'normal0': int.from_bytes(current_primitive[16:18], byteorder='little'), f'vertex0': int.from_bytes(current_primitive[18:20], byteorder='little'), 
                            f'vertex1': int.from_bytes(current_primitive[20:22], byteorder='little'), f'vertex2': int.from_bytes(current_primitive[22:24], byteorder='little')})
                        
                    elif vertex_var == f'4Vertex_':
                        if (texture_var == 'No-Texture_') and (shading_var == f'Gouraud_') and (grad_var == f'Solid_'):
                            decoded_primitive.update({
                            f'r0': int.from_bytes(current_primitive[4:5], byteorder='little'), f'g0': int.from_bytes(current_primitive[5:6], byteorder='little'), f'b0': int.from_bytes(current_primitive[6:7], byteorder='little'), f'mode_val': current_primitive[7:8], 
                            f'normal0': int.from_bytes(current_primitive[8:10], byteorder='little'), f'vertex0': int.from_bytes(current_primitive[10:12], byteorder='little'), 
                            f'normal1': int.from_bytes(current_primitive[12:14], byteorder='little'), f'vertex1': int.from_bytes(current_primitive[14:16], byteorder='little'), 
                            f'normal2': int.from_bytes(current_primitive[16:18], byteorder='little'), f'vertex2': int.from_bytes(current_primitive[18:20], byteorder='little'),
                            f'normal3': int.from_bytes(current_primitive[20:22], byteorder='little'), f'vertex3': int.from_bytes(current_primitive[22:24], byteorder='little')})

                        elif (texture_var == 'No-Texture_') and (shading_var == f'Flat_') and (grad_var == f'Solid_'):
                            decoded_primitive.update({
                            f'r0': int.from_bytes(current_primitive[4:5], byteorder='little'), f'g0': int.from_bytes(current_primitive[5:6], byteorder='little'), f'b0': int.from_bytes(current_primitive[6:7], byteorder='little'), f'mode_val': current_primitive[7:8], 
                            f'normal0': int.from_bytes(current_primitive[8:10], byteorder='little'), f'vertex0': int.from_bytes(current_primitive[10:12], byteorder='little'), 
                            f'vertex1': int.from_bytes(current_primitive[12:14], byteorder='little'), f'vertex2': int.from_bytes(current_primitive[14:16], byteorder='little'),
                            f'vertex3': int.from_bytes(current_primitive[16:18], byteorder='little'), f'pad_value0': int.from_bytes(current_primitive[18:20], byteorder='little')})
                        
                        elif (texture_var == 'No-Texture_') and (shading_var == f'Gouraud_') and (grad_var == f'Gradation_'):
                            decoded_primitive.update({
                            f'r0': int.from_bytes(current_primitive[4:5], byteorder='little'), f'g0': int.from_bytes(current_primitive[5:6], byteorder='little'), f'b0': int.from_bytes(current_primitive[6:7], byteorder='little'), f'mode_val': current_primitive[7:8], 
                            f'r1': int.from_bytes(current_primitive[8:9], byteorder='little'), f'g1': int.from_bytes(current_primitive[9:10], byteorder='little'), f'b1': int.from_bytes(current_primitive[10:11], byteorder='little'), f'pad_val0': current_primitive[11:12], 
                            f'r2': int.from_bytes(current_primitive[12:13], byteorder='little'), f'g2': int.from_bytes(current_primitive[13:14], byteorder='little'), f'b2': int.from_bytes(current_primitive[14:15], byteorder='little'), f'pad_val1': current_primitive[15:16], 
                            f'r3': int.from_bytes(current_primitive[16:17], byteorder='little'), f'g3': int.from_bytes(current_primitive[17:18], byteorder='little'), f'b3': int.from_bytes(current_primitive[18:19], byteorder='little'), f'pad_val2': current_primitive[19:20], 
                            f'normal0': int.from_bytes(current_primitive[20:22], byteorder='little'), f'vertex0': int.from_bytes(current_primitive[22:24], byteorder='little'), 
                            f'normal1': int.from_bytes(current_primitive[24:26], byteorder='little'), f'vertex1': int.from_bytes(current_primitive[26:28], byteorder='little'), 
                            f'normal2': int.from_bytes(current_primitive[28:30], byteorder='little'), f'vertex2': int.from_bytes(current_primitive[30:32], byteorder='little'),
                            f'normal3': int.from_bytes(current_primitive[32:34], byteorder='little'), f'vertex3': int.from_bytes(current_primitive[34:36], byteorder='little')})

                        elif (texture_var == 'No-Texture_') and (shading_var == f'Flat_') and (grad_var == f'Gradation_'):
                            decoded_primitive.update({
                            f'r0': int.from_bytes(current_primitive[4:5], byteorder='little'), f'g0': int.from_bytes(current_primitive[5:6], byteorder='little'), f'b0': int.from_bytes(current_primitive[6:7], byteorder='little'), f'mode_val': current_primitive[7:8], 
                            f'r1': int.from_bytes(current_primitive[8:9], byteorder='little'), f'g1': int.from_bytes(current_primitive[9:10], byteorder='little'), f'b1': int.from_bytes(current_primitive[10:11], byteorder='little'), f'pad_val0': current_primitive[11:12], 
                            f'r2': int.from_bytes(current_primitive[12:13], byteorder='little'), f'g2': int.from_bytes(current_primitive[13:14], byteorder='little'), f'b2': int.from_bytes(current_primitive[14:15], byteorder='little'), f'pad_val1': current_primitive[15:16], 
                            f'r3': int.from_bytes(current_primitive[16:17], byteorder='little'), f'g3': int.from_bytes(current_primitive[17:18], byteorder='little'), f'b3': int.from_bytes(current_primitive[18:19], byteorder='little'), f'pad_val2': current_primitive[19:20], 
                            f'normal0': int.from_bytes(current_primitive[20:22], byteorder='little'), f'vertex0': int.from_bytes(current_primitive[22:24], byteorder='little'),
                            f'vertex1': int.from_bytes(current_primitive[24:26], byteorder='little'), f'vertex2': int.from_bytes(current_primitive[26:28], byteorder='little'), 
                            f'vertex3': int.from_bytes(current_primitive[28:30], byteorder='little'), f'pad_val3': int.from_bytes(current_primitive[30:32], byteorder='little')})
                            
                        elif (texture_var == 'Texture_') and (shading_var == f'Gouraud_'):
                            decoded_primitive.update({
                            f'u0': (int.from_bytes(current_primitive[4:5], byteorder='little') / 256), f'v0': (int.from_bytes(current_primitive[5:6], byteorder='little') / 256), f'cba': current_primitive[6:8], 
                            f'u1': (int.from_bytes(current_primitive[8:9], byteorder='little') / 256), f'v1': (int.from_bytes(current_primitive[9:10], byteorder='little') / 256), f'tsb': current_primitive[10:12], 
                            f'u2': (int.from_bytes(current_primitive[12:13], byteorder='little') / 256), f'v2': (int.from_bytes(current_primitive[13:14], byteorder='little') / 256), f'pad_value0': current_primitive[14:16], 
                            f'u3': (int.from_bytes(current_primitive[16:17], byteorder='little') / 256), f'v3': (int.from_bytes(current_primitive[17:18], byteorder='little') / 256), f'pad_value1': current_primitive[18:20], 
                            f'normal0': int.from_bytes(current_primitive[20:22], byteorder='little'), f'vertex0': int.from_bytes(current_primitive[22:24], byteorder='little'), 
                            f'normal1': int.from_bytes(current_primitive[24:26], byteorder='little'), f'vertex1': int.from_bytes(current_primitive[26:28], byteorder='little'), 
                            f'normal2': int.from_bytes(current_primitive[28:30], byteorder='little'), f'vertex2': int.from_bytes(current_primitive[30:32], byteorder='little'), 
                            f'normal3': int.from_bytes(current_primitive[32:34], byteorder='little'), f'vertex3': int.from_bytes(current_primitive[34:36], byteorder='little')})
                        
                        elif (texture_var == 'Texture_') and (shading_var == f'Flat_'):
                            decoded_primitive.update({
                            f'u0': (int.from_bytes(current_primitive[4:5], byteorder='little') / 256), f'v0': (int.from_bytes(current_primitive[5:6], byteorder='little') / 256), f'cba': current_primitive[6:8], 
                            f'u1': (int.from_bytes(current_primitive[8:9], byteorder='little') / 256), f'v1': (int.from_bytes(current_primitive[9:10], byteorder='little') / 256), f'tsb': current_primitive[10:12], 
                            f'u2': (int.from_bytes(current_primitive[12:13], byteorder='little') / 256), f'v2': (int.from_bytes(current_primitive[13:14], byteorder='little') / 256), f'pad_value0': current_primitive[14:16], 
                            f'u3': (int.from_bytes(current_primitive[16:17], byteorder='little') / 256), f'v3': (int.from_bytes(current_primitive[17:18], byteorder='little') / 256), f'pad_value1': current_primitive[18:20], 
                            f'normal0': int.from_bytes(current_primitive[20:22], byteorder='little'), f'vertex0': int.from_bytes(current_primitive[22:24], byteorder='little'), 
                            f'vertex1': int.from_bytes(current_primitive[24:26], byteorder='little'), f'vertex2': int.from_bytes(current_primitive[26:28], byteorder='little'), 
                            f'vertex3': int.from_bytes(current_primitive[28:30], byteorder='little'), f'pad_value2': int.from_bytes(current_primitive[30:32], byteorder='little')})
                    
                    else:
                        no_vertex_primitive_lsc = f'Not reading Vertex Primitive Data (LSC)... exiting...'
                        no_vertex_primitive_error = messagebox.showerror(title='FATAL CRASH!!!...', message=no_vertex_primitive_lsc)
                        exit()

                elif key_light_name == f'NLSC_':
                    if vertex_var == f'3Vertex_':
                        if (texture_var == 'No-Texture_') and (shading_var == f'Gouraud_'):
                            decoded_primitive.update({
                            f'r0': int.from_bytes(current_primitive[4:5], byteorder='little'), f'g0': int.from_bytes(current_primitive[5:6], byteorder='little'), f'b0': int.from_bytes(current_primitive[6:7], byteorder='little'), f'mode_val': current_primitive[7:8], 
                            f'r1': int.from_bytes(current_primitive[8:9], byteorder='little'), f'g1': int.from_bytes(current_primitive[9:10], byteorder='little'), f'b1': int.from_bytes(current_primitive[10:11], byteorder='little'), f'pad_val0': current_primitive[11:12], 
                            f'r2': int.from_bytes(current_primitive[12:13], byteorder='little'), f'g2': int.from_bytes(current_primitive[13:14], byteorder='little'), f'b2': int.from_bytes(current_primitive[14:15], byteorder='little'), f'pad_val1': current_primitive[15:16], 
                            f'vertex0': int.from_bytes(current_primitive[16:18], byteorder='little'), f'vertex1': int.from_bytes(current_primitive[18:20], byteorder='little'), 
                            f'vertex2': int.from_bytes(current_primitive[20:22], byteorder='little'), f'pad_value1': current_primitive[22:24]})
                        
                        elif (texture_var == 'No-Texture_') and (shading_var == f'Flat_'):
                            decoded_primitive.update({
                            f'r0': int.from_bytes(current_primitive[4:5], byteorder='little'), f'g0': int.from_bytes(current_primitive[5:6], byteorder='little'), f'b0': int.from_bytes(current_primitive[6:7], byteorder='little'), f'mode_val': current_primitive[7:8], 
                            f'vertex0': int.from_bytes(current_primitive[8:10], byteorder='little'), f'vertex1': int.from_bytes(current_primitive[10:12], byteorder='little'), 
                            f'vertex2': int.from_bytes(current_primitive[12:14], byteorder='little'), f'pad_val0': int.from_bytes(current_primitive[14:16], byteorder='little')})
                        
                        elif (texture_var == 'Texture_') and (shading_var == f'Gouraud_'):
                            decoded_primitive.update({
                            f'u0': (int.from_bytes(current_primitive[4:5], byteorder='little') / 256), f'v0': (int.from_bytes(current_primitive[5:6], byteorder='little') / 256), f'cba': current_primitive[6:8], 
                            f'u1': (int.from_bytes(current_primitive[8:9], byteorder='little') / 256), f'v1': (int.from_bytes(current_primitive[9:10], byteorder='little') / 256), f'tsb': current_primitive[10:12], 
                            f'u2': (int.from_bytes(current_primitive[12:13], byteorder='little') / 256), f'v2': (int.from_bytes(current_primitive[13:14], byteorder='little') / 256), f'pad_value0': current_primitive[14:16], 
                            f'r0': int.from_bytes(current_primitive[16:17], byteorder='little'), f'g0': int.from_bytes(current_primitive[17:18], byteorder='little'), f'b0': int.from_bytes(current_primitive[18:19], byteorder='little'), f'pad_val1': current_primitive[19:20], 
                            f'r1': int.from_bytes(current_primitive[20:21], byteorder='little'), f'g1': int.from_bytes(current_primitive[21:22], byteorder='little'), f'b1': int.from_bytes(current_primitive[22:23], byteorder='little'), f'pad_val2': current_primitive[23:24], 
                            f'r2': int.from_bytes(current_primitive[24:25], byteorder='little'), f'g2': int.from_bytes(current_primitive[25:26], byteorder='little'), f'b2': int.from_bytes(current_primitive[26:27], byteorder='little'), f'pad_val3': current_primitive[27:28],
                            f'vertex0': int.from_bytes(current_primitive[28:30], byteorder='little'), f'vertex1': int.from_bytes(current_primitive[30:32], byteorder='little'), 
                            f'vertex2': int.from_bytes(current_primitive[32:34], byteorder='little'), f'pad_val4': int.from_bytes(current_primitive[34:36], byteorder='little')})
                        
                        elif (texture_var == 'Texture_') and (shading_var == f'Flat_'):
                            decoded_primitive.update({
                            f'u0': (int.from_bytes(current_primitive[4:5], byteorder='little') / 256), f'v0': (int.from_bytes(current_primitive[5:6], byteorder='little') / 256), f'cba': current_primitive[6:8], 
                            f'u1': (int.from_bytes(current_primitive[8:9], byteorder='little') / 256), f'v1': (int.from_bytes(current_primitive[9:10], byteorder='little') / 256), f'tsb': current_primitive[10:12], 
                            f'u2': (int.from_bytes(current_primitive[12:13], byteorder='little') / 256), f'v2': (int.from_bytes(current_primitive[13:14], byteorder='little') / 256), f'pad_value0': current_primitive[14:16], 
                            f'r0': int.from_bytes(current_primitive[16:17], byteorder='little'), f'g0': int.from_bytes(current_primitive[17:18], byteorder='little'), f'b0': int.from_bytes(current_primitive[18:19], byteorder='little'), f'pad_val1': current_primitive[19:20], 
                            f'vertex0': int.from_bytes(current_primitive[20:22], byteorder='little'), f'vertex1': int.from_bytes(current_primitive[22:24], byteorder='little'), 
                            f'vertex2': int.from_bytes(current_primitive[24:26], byteorder='little'), f'pad_value2': int.from_bytes(current_primitive[26:28], byteorder='little')})
                    
                    elif vertex_var == f'4Vertex_':
                        if (texture_var == 'No-Texture_') and (shading_var == f'Gouraud_'):
                            decoded_primitive.update({
                            f'r0': int.from_bytes(current_primitive[4:5], byteorder='little'), f'g0': int.from_bytes(current_primitive[5:6], byteorder='little'), f'b0': int.from_bytes(current_primitive[6:7], byteorder='little'), f'mode_val': current_primitive[7:8], 
                            f'r1': int.from_bytes(current_primitive[8:9], byteorder='little'), f'g1': int.from_bytes(current_primitive[9:10], byteorder='little'), f'b1': int.from_bytes(current_primitive[10:11], byteorder='little'), f'pad_val0': current_primitive[11:12], 
                            f'r2': int.from_bytes(current_primitive[12:13], byteorder='little'), f'g2': int.from_bytes(current_primitive[13:14], byteorder='little'), f'b2': int.from_bytes(current_primitive[14:15], byteorder='little'), f'pad_val1': current_primitive[15:16], 
                            f'r3': int.from_bytes(current_primitive[16:17], byteorder='little'), f'g3': int.from_bytes(current_primitive[17:18], byteorder='little'), f'b3': int.from_bytes(current_primitive[18:19], byteorder='little'), f'pad_val2': current_primitive[19:20], 
                            f'vertex0': int.from_bytes(current_primitive[20:22], byteorder='little'), f'vertex1': int.from_bytes(current_primitive[22:24], byteorder='little'), 
                            f'vertex2': int.from_bytes(current_primitive[24:26], byteorder='little'), f'vertex3': current_primitive[26:28]})
                        
                        elif (texture_var == 'No-Texture_') and (shading_var == f'Flat_'):
                            decoded_primitive.update({
                            f'r0': int.from_bytes(current_primitive[4:5], byteorder='little'), f'g0': int.from_bytes(current_primitive[5:6], byteorder='little'), f'b0': int.from_bytes(current_primitive[6:7], byteorder='little'), f'mode_val': current_primitive[7:8], 
                            f'vertex0': int.from_bytes(current_primitive[8:10], byteorder='little'), f'vertex1': int.from_bytes(current_primitive[10:12], byteorder='little'), 
                            f'vertex2': int.from_bytes(current_primitive[12:14], byteorder='little'), f'vertex3': int.from_bytes(current_primitive[14:16], byteorder='little')})
                        
                        elif (texture_var == 'Texture_') and (shading_var == f'Gouraud_'):
                            decoded_primitive.update({
                            f'u0': (int.from_bytes(current_primitive[4:5], byteorder='little') / 256), f'v0': (int.from_bytes(current_primitive[5:6], byteorder='little') / 256), f'cba': current_primitive[6:8], 
                            f'u1': (int.from_bytes(current_primitive[8:9], byteorder='little') / 256), f'v1': (int.from_bytes(current_primitive[9:10], byteorder='little') / 256), f'tsb': current_primitive[10:12], 
                            f'u2': (int.from_bytes(current_primitive[12:13], byteorder='little') / 256), f'v2': (int.from_bytes(current_primitive[13:14], byteorder='little') / 256), f'pad_value0': current_primitive[14:16], 
                            f'u3': (int.from_bytes(current_primitive[16:17], byteorder='little') / 256), f'v3': (int.from_bytes(current_primitive[17:18], byteorder='little') / 256), f'pad_value1': current_primitive[18:20], 
                            f'r0': int.from_bytes(current_primitive[20:21], byteorder='little'), f'g0': int.from_bytes(current_primitive[21:22], byteorder='little'), f'b0': int.from_bytes(current_primitive[22:23], byteorder='little'), f'pad_val2': current_primitive[23:24], 
                            f'r1': int.from_bytes(current_primitive[24:25], byteorder='little'), f'g1': int.from_bytes(current_primitive[25:26], byteorder='little'), f'b1': int.from_bytes(current_primitive[26:27], byteorder='little'), f'pad_val3': current_primitive[27:28], 
                            f'r2': int.from_bytes(current_primitive[28:29], byteorder='little'), f'g2': int.from_bytes(current_primitive[29:30], byteorder='little'), f'b2': int.from_bytes(current_primitive[30:31], byteorder='little'), f'pad_val4': current_primitive[31:32], 
                            f'r3': int.from_bytes(current_primitive[32:33], byteorder='little'), f'g3': int.from_bytes(current_primitive[33:34], byteorder='little'), f'b3': int.from_bytes(current_primitive[34:35], byteorder='little'), f'pad_val5': current_primitive[35:36], 
                            f'vertex0': int.from_bytes(current_primitive[36:38], byteorder='little'), f'vertex1': int.from_bytes(current_primitive[38:40], byteorder='little'), 
                            f'vertex2': int.from_bytes(current_primitive[40:42], byteorder='little'), f'vertex3': int.from_bytes(current_primitive[42:44], byteorder='little')})
                        
                        elif (texture_var == 'Texture_') and (shading_var == f'Flat_'):
                            decoded_primitive.update({
                            f'u0': (int.from_bytes(current_primitive[4:5], byteorder='little') / 256), f'v0': (int.from_bytes(current_primitive[5:6], byteorder='little') / 256), f'cba': current_primitive[6:8], 
                            f'u1': (int.from_bytes(current_primitive[8:9], byteorder='little') / 256), f'v1': (int.from_bytes(current_primitive[9:10], byteorder='little') / 256), f'tsb': current_primitive[10:12], 
                            f'u2': (int.from_bytes(current_primitive[12:13], byteorder='little') / 256), f'v2': (int.from_bytes(current_primitive[13:14], byteorder='little') / 256), f'pad_value0': current_primitive[14:16], 
                            f'u3': (int.from_bytes(current_primitive[16:17], byteorder='little') / 256), f'v3': (int.from_bytes(current_primitive[17:18], byteorder='little') / 256), f'pad_value1': current_primitive[18:20], 
                            f'r0': int.from_bytes(current_primitive[20:21], byteorder='little'), f'g0': int.from_bytes(current_primitive[21:22], byteorder='little'), f'b0': int.from_bytes(current_primitive[22:23], byteorder='little'), f'pad_val2': current_primitive[23:24], 
                            f'vertex0': int.from_bytes(current_primitive[24:26], byteorder='little'), f'vertex1': int.from_bytes(current_primitive[26:28], byteorder='little'), 
                            f'vertex2': int.from_bytes(current_primitive[28:30], byteorder='little'), f'vertex3': int.from_bytes(current_primitive[30:32], byteorder='little')})
                    
                    else:
                        no_vertex_primitive_nlsc = f'Not reading Vertex Primitive Data (NLSC)... exiting...'
                        no_vertex_primitive_error = messagebox.showerror(title='FATAL CRASH!!!...', message=no_vertex_primitive_nlsc)
                        exit()
                
                else:
                    no_light_primitive= f'Not reading Light Primitive Data...\nObject Number: {current_prim_block_num}, Primitive Number: {current_primitive_num}, Current Packet Header: {primitive_packet_header}\nexiting...'
                    no_light_primitive_error = messagebox.showerror(title='FATAL CRASH!!!...', message=no_light_primitive)
                    exit()

                primitives_in_object.append(decoded_primitive)
                ilen_calc = (ilen * 4) + 4
                next_primitive_start += ilen_calc
        
            collada_primitives.append(primitives_in_object)
    
        return collada_primitives