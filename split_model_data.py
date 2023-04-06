"""

SPLIT MODEL DATA: this module is in charge of split the data of
model files, since TMD and CTMD share some similitudes this gone to be
a generic one.

Copyright (C) 2023 DooMMetaL

"""


class SplitStructure:
    def __init__(self, model_data, model_nobjects, model_type):
        self.self = SplitStructure
        self.split_blocks(model_data=model_data, model_nobjects=model_nobjects, model_type=model_type)
    
    def split_blocks(self, model_data=bytes, model_nobjects=int, model_type=str):
        """In here will need to input the information data obtained to match
        the lengths of data, specially for CTMD Blocks"""
        object_table_calc = model_nobjects * 28 # 28 ===> 4 bytes * 7 rows of data in the Object table in TMDs
        object_table = model_data[0:object_table_calc]
        
        split_object_table = []
        start_data_block = 0
        end_data_block = 28
        number_objects = model_nobjects
        while number_objects > 0:
            single_obj_table = object_table[start_data_block:end_data_block]
            split_object_table.append(single_obj_table)
            number_objects -= 1
            start_data_block += 28
            end_data_block += 28
        
        # Split table into single read values
        global vertex_number_int
        global normal_number_int
        global primitives_number_int
        vertex_address_int = []
        vertex_number_int = []
        normal_address_int = []
        normal_number_int = []
        primitives_address_int = []
        primitives_number_int = []
        scale_value_int = []
        
        for block_values in split_object_table:
            values_vertex_add = int.from_bytes(block_values[0:4], 'little', signed=False)
            values_vertex_num = int.from_bytes(block_values[4:8], 'little', signed=False)
            values_normal_add = int.from_bytes(block_values[8:12], 'little', signed=False)
            values_normal_num = int.from_bytes(block_values[12:16], 'little', signed=False)
            values_primitives_add = int.from_bytes(block_values[16:20], 'little', signed=False)
            values_primitives_num = int.from_bytes(block_values[20:24], 'little', signed=False)
            values_scale = int.from_bytes(block_values[24:28], 'little', signed=False)
            # Appending the previous values
            vertex_address_int.append(values_vertex_add)
            vertex_number_int.append(values_vertex_num)
            normal_address_int.append(values_normal_add)
            normal_number_int.append(values_normal_num)
            primitives_address_int.append(values_primitives_add)
            primitives_number_int.append(values_primitives_num)
            scale_value_int.append(values_scale)
        
        primitive_address_copy = primitives_address_int.copy()
        primitive_next_address = primitive_address_copy[1:]
        # getting the first value of Vertex array which would be the end of the Primitive block
        end_primitive_block = vertex_address_int[0]
        primitive_next_address.append(end_primitive_block)

        vertex_data_zip = zip(vertex_address_int, vertex_number_int)
        normal_data_zip = zip(normal_address_int, normal_number_int)
        primitives_data_zip = zip(primitives_address_int, primitive_next_address)

        global vertex_block_byte
        global normal_block_byte
        global primitive_block_byte
        vertex_block_byte = self.vertex_block_split(vertex_block_address=vertex_data_zip, type_of_model=model_type, model_data_byte=model_data)
        normal_block_byte = self.normal_block_split(normal_block_address=normal_data_zip, type_of_model=model_type, model_data_byte=model_data)
        primitive_block_byte = self.primitive_block_split(primitive_block_address=primitives_data_zip, type_of_model=model_type, model_data_byte=model_data)
    
    @staticmethod
    def vertex_block_split(vertex_block_address=zip, type_of_model=str, model_data_byte=bytes):
        multiplier_byte = 0
        if (type_of_model == f'TMD') or (type_of_model == f'TMD_CCONTAINER') or (type_of_model == f'TMD_DEFF'):
            multiplier_byte = 8
        elif type_of_model == f'CTMD':
            multiplier_byte = 4
        vertex_block_bytes = []
        for v_block in vertex_block_address:
            start_v_address = v_block[0]
            end_v_block = start_v_address + (v_block[1] * multiplier_byte)
            current_vertex_block = model_data_byte[start_v_address:end_v_block]
            vertex_block_bytes.append(current_vertex_block)
        
        return vertex_block_bytes

    @staticmethod
    def normal_block_split(normal_block_address=zip, type_of_model=str, model_data_byte=bytes):
        multiplier_byte = 0
        if (type_of_model == f'TMD') or (type_of_model == f'TMD_CCONTAINER') or (type_of_model == f'TMD_DEFF'):
            multiplier_byte = 8
        elif type_of_model == f'CTMD':
            multiplier_byte = 4
        normal_block_bytes = []
        for n_block in normal_block_address:
            start_n_address = n_block[0]
            end_n_block = start_n_address + (n_block[1] * multiplier_byte)
            current_normal_block = model_data_byte[start_n_address:end_n_block]
            normal_block_bytes.append(current_normal_block)
        
        return normal_block_bytes

    @staticmethod
    def primitive_block_split(primitive_block_address=zip, type_of_model=str, model_data_byte=bytes):
        primitives_block_bytes = []
        for p_block in primitive_block_address:
            start_p_address = p_block[0]
            end_p_block = p_block[1]
            current_primitive_block = model_data_byte[start_p_address:end_p_block]
            primitives_block_bytes.append(current_primitive_block)
        
        return primitives_block_bytes