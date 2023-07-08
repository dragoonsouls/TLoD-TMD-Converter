"""

Database to Listbox(Dict):
This Algorithm will create a dict from the database,
to be sure that the content loaded to the Sub List
and the Object List is the correct

Copyright (C) 2023 DooMMetaL

"""

import os

class DatabaseDict:
    """Database to Listbox(Dict):
    This Algorithm will create a dict from the database,
    to be sure that the content loaded to the Sub List
    and the Object List is the correct"""
    def __init__(self, database_path) -> dict:
        self.self = DatabaseDict
        self.database_path = database_path
        self.process_database(database_path_str=database_path)
    
    def process_database(self, database_path_str=str) -> dict:
        get_path = database_path_str

        database_files = []
        if os.path.isdir(get_path):
            total_files = os.walk(get_path)
            for root, dirs, files in total_files:
                for single_file in files:
                    new_path = os.path.join(root, single_file)
                    database_files.append(new_path)
        else:
            error_string = f'{get_path} is not a correct path, exiting...'
            print(error_string)
            exit()
        
        # First declare the full dictionary to avoid adding more code lines
        database_dict = {'Battle_Stages': {}, 'Bosses': {}, 'Characters': {}, 'CutScenes': {}, 'Enemies': {}, 'Logo': {}, 'Tutorial': {}, 'World_Map': {}}
        for db_file in database_files:
            if f'Battle_Stages' in db_file:
                reading_text_bs = self.process_text_file(text_file=db_file)
                reading_db_bs = self.process_database_from_text(text_file=reading_text_bs)
                for load_to_dict_bs in reading_db_bs:
                    database_dict['Battle_Stages'][f'{load_to_dict_bs[0]}'] = [load_to_dict_bs[1], load_to_dict_bs[2]]
            elif f'Bosses' in db_file:
                reading_text_bosses = self.process_text_file(text_file=db_file)
                reading_db_bosses = self.process_database_from_text(text_file=reading_text_bosses)
                for load_to_dict_bosses in reading_db_bosses:
                    database_dict['Bosses'][f'{load_to_dict_bosses[0]}'] = [load_to_dict_bosses[1], load_to_dict_bosses[2]]
            elif f'Characters' in db_file:
                reading_text_characters = self.process_text_file(text_file=db_file)
                reading_db_characters = self.process_database_from_text(text_file=reading_text_characters)
                for load_to_dict_char in reading_db_characters:
                    character_name = load_to_dict_char[0]
                    character_model = load_to_dict_char[1]
                    character_saf_addition = load_to_dict_char[2]
                    find_comma = character_saf_addition.find(f', ')
                    addition_name = character_saf_addition[find_comma + 1: ].strip()
                    additon_saf = f''
                    if f'Dragoon' in character_name:
                        char_name_and_addition = f'{character_name}'
                        additon_saf = f'None'
                    else:
                        char_name_and_addition = f'{character_name} - {addition_name}'
                        additon_saf = character_saf_addition[:find_comma]
                    database_dict['Characters'][f'{char_name_and_addition}'] = [character_model, additon_saf]
            elif f'CutScenes' in db_file:
                reading_text_cutscenes = self.process_text_file(text_file=db_file)
                reading_db_cutscenes = self.process_database_from_text_cu(text_file=reading_text_cutscenes)
                for load_to_dict_cutscenes in reading_db_cutscenes:
                    database_dict['CutScenes'][f'{load_to_dict_cutscenes[0]}'] = [load_to_dict_cutscenes[1]]
            elif f'Enemies' in db_file:
                reading_text_enemies = self.process_text_file(text_file=db_file)
                reading_db_enemies = self.process_database_from_text(text_file=reading_text_enemies)
                for load_to_dict_enemies in reading_db_enemies:
                    database_dict['Enemies'][f'{load_to_dict_enemies[0]}'] = [load_to_dict_enemies[1], load_to_dict_enemies[2]]
            elif f'Logo' in db_file:
                reading_text_logo = self.process_text_file(text_file=db_file)
                reading_db_logo = self.process_database_from_text(text_file=reading_text_logo)
                for load_to_dict_logo in reading_db_logo:
                    database_dict['Logo'][f'{load_to_dict_logo[0]}'] = [load_to_dict_logo[1], load_to_dict_logo[2]]
            elif f'Tutorial' in db_file:
                reading_text_tutorial = self.process_text_file(text_file=db_file)
                reading_db_tutorial = self.process_database_from_text(text_file=reading_text_tutorial)
                for load_to_dict_tutorial in reading_db_tutorial:
                    database_dict['Tutorial'][f'{load_to_dict_tutorial[0]}'] = [load_to_dict_tutorial[1], load_to_dict_tutorial[2]]
            elif f'World_Map' in db_file:
                reading_text_worldmap = self.process_text_file(text_file=db_file)
                reading_db_worldmap = self.process_database_from_text(text_file=reading_text_worldmap)
                for load_to_dict_worldmap in reading_db_worldmap:
                    database_dict['World_Map'][f'{load_to_dict_worldmap[0]}'] = [load_to_dict_worldmap[1], load_to_dict_worldmap[2]]
        return database_dict

    def process_text_file(self, text_file=str) -> str:
        text_read = None
        with open(text_file, 'r') as text_to_read:
            text_read = text_to_read.readlines()
        
        return text_read

    def process_database_from_text(self, text_file=str) -> list:
        name_objects = []
        for text in text_file:
            cleaning_text = text.strip()
            find_colon = cleaning_text.find(f':')
            find_dash = cleaning_text.find(f' - ')
            name_object = cleaning_text[:find_colon].strip()
            model_loc = cleaning_text[find_colon + 1: find_dash].strip()
            saf_loc = cleaning_text[find_dash + 3: ].strip()
            objects_complete = name_object, model_loc, saf_loc
            name_objects.append(objects_complete)
        return name_objects

    def process_database_from_text_cu(self, text_file=str) -> list:
        name_scene = []
        name_objects = []
        index_insert = []
        index_place = 0
        for text in text_file:
            if f'[/' in text:
                name_scene_original = text.strip()
                find_start = name_scene_original.find(f'[')
                find_end = name_scene_original.find(f']')
                name_scene_for_listbox = name_scene_original[find_start + 2: find_end]
                name_scene.append(name_scene_for_listbox)
                index_insert.append(index_place)
                name_objects.append(f'index_placeholder')
            else:
                cleaning_text = text.strip()
                find_colon = cleaning_text.find(f':')
                find_dash = cleaning_text.find(f' - ')
                name_object_cu = cleaning_text[:find_colon].strip()
                model_loc = cleaning_text[find_colon + 1: find_dash].strip()
                saf_loc = cleaning_text[find_dash + 3: ].strip()
                objects_complete = name_object_cu, model_loc, saf_loc
                name_objects.append(objects_complete)
            index_place += 1
        
        combined_index = []
        for index_combine in range(0, len(index_insert)):
            if index_combine == 0:
                pass
            else:
                start_index = index_insert[index_combine - 1]
                end_index = index_insert[index_combine]
                comb_ind = start_index, end_index
                combined_index.append(comb_ind)
        
        final_cutscene_list = []
        slice_name_scene = 0
        for get_segments in combined_index:
            start_segment = get_segments[0]
            end_segment = get_segments[1]
            segment = name_objects[start_segment + 1 :end_segment]
            name_scene_current = name_scene[slice_name_scene]
            final_current_scene = name_scene_current, segment
            final_cutscene_list.append(final_current_scene)
            slice_name_scene += 1

        return final_cutscene_list