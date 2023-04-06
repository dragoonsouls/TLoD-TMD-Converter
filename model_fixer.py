"""

Model Fixer: This module will process the model
before the Collada compiler, to check if there are
unused vertices or weird stuff going on an fix them
before the conversion

Copyright (C) 2023 DooMMetaL

"""

class ModelFix:
    def __init__(self, primitive_block, vertex_block):
        self.self = ModelFix
        self.find_bug_vertex(primitive_block=primitive_block, vertex_block=vertex_block)
    
    def find_bug_vertex(self, primitive_block=list, vertex_block=list): # SEEMS TO BE WORKING SMOOTHLY
        global vertex_decoded_fix
        global primitive_decoded_fix
        counter_obj = 0
        new_vertex_block = []
        new_primitive_block = []
        for primitive_in in primitive_block:
            vertex_index_compendium = []
            for vertex_index in primitive_in:
                if (vertex_index.get('vertex3') !=None):
                    get_vertex_index_1 = vertex_index.get('vertex0')
                    get_vertex_index_2 = vertex_index.get('vertex1')
                    get_vertex_index_3 = vertex_index.get('vertex2')
                    get_vertex_index_4 = vertex_index.get('vertex3')
                    vertex_index_compendium.append(get_vertex_index_1)
                    vertex_index_compendium.append(get_vertex_index_2)
                    vertex_index_compendium.append(get_vertex_index_3)
                    vertex_index_compendium.append(get_vertex_index_4)
                else:
                    get_vertex_index_1_1 = vertex_index.get('vertex0')
                    get_vertex_index_2_1 = vertex_index.get('vertex1')
                    get_vertex_index_3_1 = vertex_index.get('vertex2')
                    vertex_index_compendium.append(get_vertex_index_1_1)
                    vertex_index_compendium.append(get_vertex_index_2_1)
                    vertex_index_compendium.append(get_vertex_index_3_1)
            
            set_vertex_index = set(vertex_index_compendium)
            current_vertex_block = vertex_block[counter_obj]
            if (len(set_vertex_index)) != len(vertex_block[counter_obj]):
                print(f'Original model seems to have retail bugged Vertex Block and Vertex Index, we will try a fix for it!...')
                new_vertex_block_calc = self.vertex_block_fixer(vertex_index_set=set_vertex_index, original_vertex_block=current_vertex_block)
                print(f'||||>>>>>>>>>>WORKING WITH PRIMITIVE BLOCK NUM {counter_obj}<<<<<<<<<<||||')
                new_primitive_block_get = self.primitive_block_fixer(old_vi=set_vertex_index, orig_prim_block=primitive_in)
                new_vertex_block.append(new_vertex_block_calc)
                new_primitive_block.append(new_primitive_block_get)
            counter_obj += 1
        if (len(new_vertex_block) == 0) or (len(new_primitive_block) == 0):
            vertex_decoded_fix = vertex_block
            primitive_decoded_fix = primitive_block
        else:
            vertex_decoded_fix = new_vertex_block
            primitive_decoded_fix = new_primitive_block

    @staticmethod
    def vertex_block_fixer(vertex_index_set=set, original_vertex_block=list):
        vertex_extracted = []
        vertex_index_count = 0
        for vertex_index_old in vertex_index_set:
            vertex_position = original_vertex_block[vertex_index_old]
            vertex_extracted.append(vertex_position)
            vertex_index_count += 1
        return vertex_extracted
    
    @staticmethod
    def primitive_block_fixer(old_vi=list, orig_prim_block=list):
        old_vi_list = list(sorted(old_vi))
        new_prim_get = []
        new_vi_list = []
        for num in old_vi_list:
            max_old_list = max(old_vi_list)
            len_old_list = len(old_vi_list)
            new_index = num - max_old_list + (len_old_list - 1)
            new_vi_list.append(new_index)

        for current_prim in orig_prim_block:
            if current_prim.get('vertex3') != None:
                if current_prim.get('vertex0') in old_vi_list:
                    list_index_v0 = old_vi_list.index(current_prim.get('vertex0'))
                    new_vertex_index = new_vi_list[list_index_v0]
                    current_prim.update({'vertex0': new_vertex_index})
                
                if current_prim.get('vertex1') in old_vi_list:
                    list_index_v0 = old_vi_list.index(current_prim.get('vertex1'))
                    new_vertex_index = new_vi_list[list_index_v0]
                    current_prim.update({'vertex1': new_vertex_index})
                
                if current_prim.get('vertex2') in old_vi_list:
                    list_index_v0 = old_vi_list.index(current_prim.get('vertex2'))
                    new_vertex_index = new_vi_list[list_index_v0]
                    current_prim.update({'vertex2': new_vertex_index})
                
                if current_prim.get('vertex3') in old_vi_list:
                    list_index_v0 = old_vi_list.index(current_prim.get('vertex3'))
                    new_vertex_index = new_vi_list[list_index_v0]
                    current_prim.update({'vertex3': new_vertex_index})
                new_prim_get.append(current_prim)

            elif current_prim.get('vertex2') != None:
                if current_prim.get('vertex0') in old_vi_list:
                    list_index_v0 = old_vi_list.index(current_prim.get('vertex0'))
                    new_vertex_index = new_vi_list[list_index_v0]
                    current_prim.update({'vertex0': new_vertex_index})
                
                if current_prim.get('vertex1') in old_vi_list:
                    list_index_v0 = old_vi_list.index(current_prim.get('vertex1'))
                    new_vertex_index = new_vi_list[list_index_v0]
                    current_prim.update({'vertex1': new_vertex_index})
                
                if current_prim.get('vertex2') in old_vi_list:
                    list_index_v0 = old_vi_list.index(current_prim.get('vertex2'))
                    new_vertex_index = new_vi_list[list_index_v0]
                    current_prim.update({'vertex2': new_vertex_index})
                new_prim_get.append(current_prim)
            
            else:
                print(f'FATAL ERROR - Impossible to set new Vertex Index... exiting')
                exit()

        return new_prim_get