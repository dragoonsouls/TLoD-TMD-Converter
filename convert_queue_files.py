"""

Convert Queue Files: This code will take care of 
converting the files from the Queue List on the Convert Model from GUI

Copyright (C) 2023 DooMMetaL

"""
from tkinter import messagebox, Label
from tkinter import ttk
import os
import convert_batch
import decompress_bpe
import shutil

class ConvertGuiFiles:
    def __init__(self, files_to_convert, all_files_list, merge_flag, masterbar):
        """Convert Queue Files: This code will convert the files from the Queue List on the Convert Model from GUI"""
        self.self = ConvertGuiFiles
        self.files_to_convert = files_to_convert
        self.all_files_list = all_files_list
        self.merge_flag = merge_flag
        self.master = masterbar
        self.convert_files()
    
    def convert_files(self) -> bool:
        # Folder creation
        merge_flag = self.merge_flag
        path_to_dump = self.get_dump_path()
        path_sc_get = self.get_sc_folder()
        create_folder = []
        for folder_parent in self.files_to_convert:
            find_arrow_folder = folder_parent.find(f'==>')
            this_parent_folder = folder_parent[:find_arrow_folder] # Base Folder Name
            create_folder.append(this_parent_folder)
        create_folder_set = [set(create_folder)]
        paths_to_dump_files_base = self.create_folders(folder_list=create_folder_set, dump_path=path_to_dump)
        length_bar = 100 / len(self.files_to_convert)
        self.new_bar = ttk.Progressbar(master=self.master, length=100, maximum=100, mode='determinate', orient='horizontal')
        self.new_bar.place(relx=0.01, rely=0.2, relwidth= 0.98, relheight= 0.2)
        percent = float(length_bar)
        percent_string = "%.2f" % percent
        self.percentage_label = Label(master=self.master, text=f'{percent_string}%')
        self.percentage_label.place(relx=0.45, rely=0.5, relwidth= 0.1, relheight= 0.1)
        
        """Creating the conversion list and Conversion itself
        Handling the conversion from the same condition of Parent List, this make more easy to work with models without doing too much stuff"""
        for f_to_convert in self.files_to_convert:
            """WILL USING THREE FLAGS FOR CONVERSION
            PASSIVE MEANS THAT ONLY HAVE ANIMATIONS IN THE SAME FOLDER
            ATTACK MEANS THAT HAVE PASSIVE AND ATTACK ANIMATIONS IN DIFFERENT FOLDERS"""
            """LIST CONVERSION STRUCTURE:
            this_parent == Name of the Parent for doing some stuff later
            path_model_file == Path to the model and animations
            path_saf_file == Path to the additional animations if needed
            path_type == FLAG to indicate if have passive and attack animations
            dae_file_name == default name for the converted file, if more than one file it's conversion will be numbered"""
            
            find_arrow = f_to_convert.find(f'==>')
            this_parent = f_to_convert[:find_arrow] # Parent Name
            this_object = f_to_convert[find_arrow + 3:] # Object Name
            create_folder.append(this_parent)
            dict_key_parent = self.all_files_list[f'{this_parent}']
            for name_sub in dict_key_parent:
                if this_object == name_sub:
                    name_sub_changed = name_sub
                    objects_mod_saf = dict_key_parent[f'{name_sub}']
                    if f'?' in name_sub: # IF some weird symbols appears i can handle it from here
                            name_sub_changed = name_sub.replace(f'?', '')
                    
                    if this_parent == f'Battle_Stages':
                        append_battle_stages = self.create_filter_non_entities(name_sub_changed=name_sub_changed, paths_to_dump_files_base=paths_to_dump_files_base, this_parent=this_parent, objects_mod_saf=objects_mod_saf, path_sc_get=path_sc_get)
                        path_model = append_battle_stages[1]
                        complete_path = self.look_for_files(path_to_files=path_model, this_parent=this_parent)
                        model_complete_path = complete_path[0]
                        saf_complete_path = complete_path[1]
                        animation_type = complete_path[2]
                        dae_file = append_battle_stages[4]
                        convert_batch.main(model_file=model_complete_path, animation_file=saf_complete_path, animation_type=animation_type, new_folder=dae_file)
                                
                    elif this_parent == f'Bosses':
                        append_bosses = self.create_filter_entities(name_sub_changed=name_sub_changed, paths_to_dump_files_base=paths_to_dump_files_base, this_parent=this_parent, objects_mod_saf=objects_mod_saf, path_sc_get=path_sc_get)
                        path_model_and_passive = append_bosses[1]
                        path_attack_anims = append_bosses[2]
                        path_flag = append_bosses[3]
                        path_to_dump_data = append_bosses[4]
                        path_base_model_anim = self.look_for_files_entities(path_to_files=path_model_and_passive, this_parent=this_parent)
                        model_path = path_base_model_anim[0]
                        passive_path = path_base_model_anim[1]
                        
                        if path_flag == f'PASSIVE':
                            self.convert_passive(passive_path=passive_path, path_to_dump_data=path_to_dump_data, name_sub_changed=name_sub_changed, model_path=model_path, path_flag=path_flag)
                        else:
                            self.convert_passive_and_attack(passive_path=passive_path, path_to_dump_data=path_to_dump_data, name_sub_changed=name_sub_changed, model_path=model_path, path_flag=path_flag, path_attack_anims=path_attack_anims, this_parent=this_parent)

                    elif this_parent == f'Characters': # TODO FOR THIS I NEED A SPECIAL HANDLER, SINCE SC HAVE THE ADDITIONS BPE'D
                        append_characters = self.create_filter_entities(name_sub_changed=name_sub_changed, paths_to_dump_files_base=paths_to_dump_files_base, this_parent=this_parent, objects_mod_saf=objects_mod_saf, path_sc_get=path_sc_get)
                        self.convert_additions(merge_flag=merge_flag, models_specs=append_characters, name_sub_changed=name_sub_changed)

                    elif this_parent == f'CutScenes': # TODO FOR THIS ONE I WILL NEED A SPECIAL HANDLER, SINCE THE MODELS and ANIMATIONS ARE IN THE ROOT OF DRGN0.BIN
                        self.convert_cutscenes(name_sub_changed=name_sub_changed, paths_to_dump_files_base=paths_to_dump_files_base, objects_mod_saf=objects_mod_saf, path_sc_get=path_sc_get)
                    
                    elif this_parent == f'Enemies':
                        append_enemies = self.create_filter_entities(name_sub_changed=name_sub_changed, paths_to_dump_files_base=paths_to_dump_files_base, this_parent=this_parent, objects_mod_saf=objects_mod_saf, path_sc_get=path_sc_get)
                        path_model_and_passive = append_enemies[1]
                        path_attack_anims = append_enemies[2]
                        path_flag = append_enemies[3]
                        path_to_dump_data = append_enemies[4]
                        path_base_model_anim = self.look_for_files_entities(path_to_files=path_model_and_passive, this_parent=this_parent)
                        model_path = path_base_model_anim[0]
                        passive_path = path_base_model_anim[1]
                        self.convert_passive_and_attack(passive_path=passive_path, path_to_dump_data=path_to_dump_data, name_sub_changed=name_sub_changed, model_path=model_path, path_flag=path_flag, path_attack_anims=path_attack_anims, this_parent=this_parent)
                    
                    elif this_parent == f'Logo':
                        append_logo = self.create_filter_non_entities(name_sub_changed=name_sub_changed, paths_to_dump_files_base=paths_to_dump_files_base, this_parent=this_parent, objects_mod_saf=objects_mod_saf, path_sc_get=path_sc_get)
                        path_model = append_logo[1]
                        complete_path = self.look_for_files(path_to_files=path_model, this_parent=this_parent)
                        model_complete_path = complete_path[0]
                        saf_complete_path = complete_path[1]
                        animation_type = complete_path[2]
                        dae_file = append_logo[4]
                        convert_batch.main(model_file=model_complete_path, animation_file=saf_complete_path, animation_type=animation_type, new_folder=dae_file)
                    
                    elif this_parent == f'Tutorial':
                        append_tutorial = self.create_filter_entities(name_sub_changed=name_sub_changed, paths_to_dump_files_base=paths_to_dump_files_base, this_parent=this_parent, objects_mod_saf=objects_mod_saf, path_sc_get=path_sc_get)
                        path_model_and_passive = append_tutorial[1]
                        path_attack_anims = append_tutorial[2]
                        path_flag = append_tutorial[3]
                        path_to_dump_data = append_tutorial[4]
                        path_base_model_anim = self.look_for_files_entities(path_to_files=path_model_and_passive, this_parent=this_parent)
                        model_path = path_base_model_anim[0]
                        passive_path = path_base_model_anim[1]
                        
                        if path_flag == f'PASSIVE':
                            self.convert_passive(passive_path=passive_path, path_to_dump_data=path_to_dump_data, name_sub_changed=name_sub_changed, model_path=model_path, path_flag=path_flag)
                        else:
                            self.convert_passive_and_attack(passive_path=passive_path, path_to_dump_data=path_to_dump_data, name_sub_changed=name_sub_changed, model_path=model_path, path_flag=path_flag, path_attack_anims=path_attack_anims, this_parent=this_parent)
                    
                    elif this_parent == f'World_Map':
                        append_world_maps = self.create_filter_non_entities(name_sub_changed=name_sub_changed, paths_to_dump_files_base=paths_to_dump_files_base, this_parent=this_parent, objects_mod_saf=objects_mod_saf, path_sc_get=path_sc_get)
                        path_model = append_world_maps[1]
                        complete_path = self.look_for_files(path_to_files=path_model, this_parent=this_parent)
                        model_complete_path = complete_path[0]
                        saf_complete_path = complete_path[1]
                        animation_type = complete_path[2]
                        dae_file = append_world_maps[4]
                        if (f'Coloon' in name_sub) or (f'Mini Dart' in name_sub) or (f'Queen Fury' in name_sub) or (f'Teleportation Glow' in name_sub):
                            number_to_add = 0
                            for saf_convert in saf_complete_path:
                                model_new_name = f'{dae_file}_{number_to_add}'
                                convert_batch.main(model_file=model_complete_path, animation_file=saf_convert, animation_type=animation_type, new_folder=model_new_name)
                                number_to_add +=1
                        else:
                            convert_batch.main(model_file=model_complete_path, animation_file=saf_complete_path, animation_type=animation_type, new_folder=dae_file)
                    
                    else:
                        messagebox.showerror(title='FATAL CRASH', message=f'Parent: {this_parent}, not in Database, exiting program...')
                        exit()

            self.update_percent_label(number_add=percent)
            self.update_bar_progression(model_processed=percent)
            percent += length_bar
        
    def create_folders(self, folder_list=list, dump_path=str) -> list:
        """Create a list of paths to create folders, returning a list if necessary to get files or other folders into it"""
        complete_path_base = []
        for create_folder_path in folder_list:
            for c_folder_path in create_folder_path:
                path_base = f'{dump_path}{c_folder_path}'
                complete_path_base.append(path_base)
                try:
                    os.makedirs(path_base, exist_ok=True)
                except OSError:
                    error_folder = f'Can\'t create the folder, permission denied'
                    error_folder_window = messagebox.showerror(title='System Error...', message=error_folder)
                    exit()
        return complete_path_base

    def get_dump_path(self) -> str:
        try:
            config_file = f'Resources/converter_config.config'
            with open(config_file, 'r') as configuration_file:
                configuration_file_all = configuration_file.readlines()
                for cnf_file in configuration_file_all:
                    if f'DUMP_FOLDER' in cnf_file:
                        find_equal = cnf_file.find(f' = ')
                        path_dump_raw = cnf_file[find_equal + 3:].strip()
                        path_dump = f'{path_dump_raw}/'
                        return path_dump
        except OSError:
            messagebox.showerror(title='FATAL CRASH', message='Configuration File must be in Resources Folder, exiting...')
            exit()

    def get_sc_folder(self) -> str:
        try:
            config_file = f'Resources/converter_config.config'
            with open(config_file, 'r') as configuration_file:
                configuration_file_all = configuration_file.readlines()
                for cnf_file in configuration_file_all:
                    if f'SC_FOLDER' in cnf_file:
                        find_equal = cnf_file.find(f' = ')
                        path_sc_raw = cnf_file[find_equal + 3:].strip()
                        path_sc = f'{path_sc_raw}/'
                        return path_sc
        except OSError:
            messagebox.showerror(title='FATAL CRASH', message='Configuration File must be in Resources Folder, exiting...')
            exit()

    def create_single_folder(self, folder_creation=str):
        try:
            os.makedirs(folder_creation, exist_ok=True)
        except OSError:
            error_folder = f'Can\'t create the folder, permission denied'
            error_folder_window = messagebox.showerror(title='System Error...', message=error_folder)
            exit()

    def create_filter_entities(self, name_sub_changed=str, paths_to_dump_files_base=list, this_parent=str, objects_mod_saf=list, path_sc_get=str):
        append_this_data = ()
        add_name_to_path = name_sub_changed
        dae_file_name = f''
        for path_convert in paths_to_dump_files_base:
            if this_parent in path_convert:
                new_folder = f'{path_convert}/{add_name_to_path}/'
                self.create_single_folder(folder_creation=new_folder)
                dae_file_name = f'{new_folder}{add_name_to_path}'
        split_model = objects_mod_saf[0]
        split_saf = objects_mod_saf[1]
        path_model_file = f'{path_sc_get}SECT/DRGN0.BIN/{split_model}'
        path_saf_file = f'{path_sc_get}SECT/DRGN0.BIN/{split_saf}'
        if f'None' not in path_saf_file:
            path_type = f'ATTACK'
            append_enemies_attack = this_parent, path_model_file, path_saf_file, path_type, dae_file_name
            append_this_data = append_enemies_attack
        else:
            path_type = f'PASSIVE'
            append_enemies_passive = this_parent, path_model_file, path_saf_file, path_type, dae_file_name
            append_this_data = append_enemies_passive
        return append_this_data
    
    def create_filter_non_entities(self, name_sub_changed=str, paths_to_dump_files_base=list, this_parent=str, objects_mod_saf=list, path_sc_get=str):
        add_name_to_path = name_sub_changed
        dae_file_name = f''
        for path_convert in paths_to_dump_files_base:
            if this_parent in path_convert:
                new_folder = f'{path_convert}/{add_name_to_path}/'
                self.create_single_folder(folder_creation=new_folder)
                dae_file_name = f'{new_folder}{add_name_to_path}'
        split_model = objects_mod_saf[0]
        split_saf = objects_mod_saf[1]
        path_model_file = f'{path_sc_get}SECT/DRGN0.BIN/{split_model}'
        path_saf_file = f'{path_sc_get}{split_saf}'
        path_type = f'PASSIVE'
        append_this_data = this_parent, path_model_file, path_saf_file, path_type, dae_file_name
        
        return append_this_data
    
    def convert_cutscenes(self, name_sub_changed=str, paths_to_dump_files_base=list, objects_mod_saf=list, path_sc_get=str):
        objects_denested = objects_mod_saf[0]
        path_base = f'{paths_to_dump_files_base[0]}/{name_sub_changed}' # Base Place of CutScenes
        for object_cu in objects_denested:
            model_name = object_cu[0]
            model_path_base = object_cu[1]
            model_saf = object_cu[2].replace("[", "").replace("]", "").replace(", ", ",")
            path_to_dump = f'{path_base}/{model_name}'
            path_for_model = f'{path_sc_get}SECT/DRGN0.BIN/{model_path_base}'
            self.create_single_folder(folder_creation=path_to_dump)
            real_model_saf = model_saf.split(",")
            number_animation = 0
            if os.path.isdir(path_for_model):
                path_for_model = f'{path_sc_get}SECT/DRGN0.BIN/{model_path_base}/32'
            for m_saf in real_model_saf:
                this_saf = f'{path_sc_get}SECT/DRGN0.BIN/{m_saf}'
                new_dae = f'{path_to_dump}/{model_name}_{number_animation}'
                convert_batch.main(model_file=path_for_model, animation_file=this_saf, animation_type=f'Normal', new_folder=new_dae)
                number_animation += 1

    def look_for_files(self, path_to_files=str, this_parent=str) -> str | list:
        model_path_complete = f''
        saf_path_complete = f''
        animation_type = f''
        if os.path.isdir(path_to_files):
            if this_parent == 'Battle_Stages':
                files_found = self.walk_into_dir(path_to_files=path_to_files)
                model_file = f'{path_to_files}{files_found[0]}'
                saf_file = f'{path_to_files}{files_found[1]}'
                model_path_complete = model_file
                saf_path_complete = saf_file
                animation_type = f'Folder'
            
            elif this_parent == 'World_Map':
                files_found = self.walk_into_dir(path_to_files=path_to_files)
                model_file = f'{path_to_files}/{files_found[0]}'
                saf_path_complete_pre = []
                for f_found in files_found[2:]: # [1:] is ignored, because it's a TOD animation that is not used in the final game
                    saf_file = f'{path_to_files}/{f_found[0]}'
                    saf_path_complete_pre.append(saf_file)
                saf_path_complete = saf_path_complete_pre
                model_path_complete = model_file
                animation_type = f'Folder'
        
        else:
            if this_parent == 'Logo':
                model_file = f'{path_to_files}'
                model_path_complete = model_file
                animation_type = f'No Animation'
            
            elif this_parent == 'World_Map':
                model_file = f'{path_to_files}'
                model_path_complete = model_file
                animation_type = f'No Animation'
                saf_path_complete = f''

        return model_path_complete, saf_path_complete, animation_type

    def look_for_files_entities(self, path_to_files=str, this_parent=str) -> str | list:
        model_path_complete = f''
        passive_path_complete = []
        if os.path.isdir(path_to_files):
            if this_parent == f'Enemies':
                get_files = self.walk_into_dir(path_to_files=path_to_files)
                saf_1 = f'{path_to_files}/{get_files[0]}'
                saf_2 = f'{path_to_files}/{get_files[1]}'
                model = f'{path_to_files}/{get_files[2]}'
                model_path_complete = model
                passive_path_complete.append(saf_1)
                passive_path_complete.append(saf_2)
            
            elif (this_parent == f'Tutorial') or (this_parent == f'Bosses') or (this_parent == f'Characters'):
                get_files = self.walk_into_dir(path_to_files=path_to_files)
                for gf in get_files:
                    if f'32' == gf:
                        model = f'{path_to_files}/32'
                        model_path_complete = model
                    else:
                        saf = f'{path_to_files}/{gf}'
                        passive_path_complete.append(saf)

        return model_path_complete, passive_path_complete

    def look_for_attack_animations(self, path_to_files=str, this_parent=str) -> list:
        path_saf_complete = []
        if os.path.isdir(path_to_files):
            if this_parent == f'Enemies':
                if (f'/3751' in path_to_files) or (f'/3752' in path_to_files):
                    get_files = self.walk_into_dir(path_to_files=path_to_files)
                    del get_files[0]
                    for gf in get_files:
                        saf = f'{path_to_files}/{gf}'
                        path_saf_complete.append(saf)
                else:
                    get_files = self.walk_into_dir(path_to_files=path_to_files)
                    for gf in get_files:
                        saf = f'{path_to_files}/{gf}'
                        path_saf_complete.append(saf)
            
            elif (this_parent == f'Tutorial') or (this_parent == f'Bosses'):
                get_files = self.walk_into_dir(path_to_files=path_to_files)
                for gf in get_files:
                    saf = f'{path_to_files}/{gf}'
                    path_saf_complete.append(saf)
            
            elif (this_parent == f'Characters'):
                get_files = self.walk_into_dir(path_to_files=path_to_files)
                for gf in get_files:
                    if int(gf) <= 32:
                        bpe_decode = f'BPE'
                        saf = f'{path_to_files}/{gf}', bpe_decode
                        path_saf_complete.append(saf)
                    else:
                        bpe_decode = f'NO-BPE'
                        saf = f'{path_to_files}/{gf}', bpe_decode
                        path_saf_complete.append(saf)
                    
        return path_saf_complete

    def convert_passive(self, passive_path=list, path_to_dump_data=str, name_sub_changed=str, model_path=str, path_flag=str):
        number_add_passive = 0
        for passive_anims in passive_path:
            passive_path_new = path_to_dump_data.replace(f'{name_sub_changed}/{name_sub_changed}', f'{name_sub_changed}/Passive/')
            self.create_single_folder(folder_creation=passive_path_new)
            passive_path_dae_new = path_to_dump_data.replace(f'{name_sub_changed}/{name_sub_changed}', f'{name_sub_changed}/Passive/{name_sub_changed}_{number_add_passive}')
            convert_batch.main(model_file=model_path, animation_file=passive_anims, animation_type=path_flag, new_folder=passive_path_dae_new)
            number_add_passive += 1

    def convert_passive_and_attack(self, passive_path=list, path_to_dump_data=str, name_sub_changed=str, model_path=str, path_flag=str, path_attack_anims=str, this_parent=str):
        number_add = 0
        for passive_anims in passive_path:
            passive_path_new = path_to_dump_data.replace(f'{name_sub_changed}/{name_sub_changed}', f'{name_sub_changed}/Passive/')
            self.create_single_folder(folder_creation=passive_path_new)
            passive_path_dae_new = path_to_dump_data.replace(f'{name_sub_changed}/{name_sub_changed}', f'{name_sub_changed}/Passive/{name_sub_changed}_{number_add}')
            convert_batch.main(model_file=model_path, animation_file=passive_anims, animation_type=path_flag, new_folder=passive_path_dae_new)
            number_add += 1
    
        number_add_attk = 0
        path_attack_animations = self.look_for_attack_animations(path_to_files=path_attack_anims, this_parent=this_parent)
        for attack_anms in path_attack_animations:
            passive_path_new = path_to_dump_data.replace(f'{name_sub_changed}/{name_sub_changed}', f'{name_sub_changed}/Attack/')
            self.create_single_folder(folder_creation=passive_path_new)
            passive_path_dae_new = path_to_dump_data.replace(f'{name_sub_changed}/{name_sub_changed}', f'{name_sub_changed}/Attack/{name_sub_changed}_{number_add_attk}')
            convert_batch.main(model_file=model_path, animation_file=attack_anms, animation_type=path_flag, new_folder=passive_path_dae_new)
            number_add_attk += 1

    def convert_additions(self, merge_flag=int, models_specs=tuple, name_sub_changed=str):
        this_parent = models_specs[0]
        model_passive_path = models_specs[1]
        model_attack_path = models_specs[2]
        dump_folder = models_specs[4]
        
        if (f'Dart Normal' in dump_folder):
            position_string_replace = model_passive_path.find(f'SECT')
            clear_string = model_passive_path[:position_string_replace]
            new_model_string = f'{clear_string}characters/dart/models/combat'
            path_base_model_passive = self.look_for_files_entities(path_to_files=new_model_string, this_parent=this_parent)
            path_attack_animations_bpe = self.look_for_attack_animations(path_to_files=model_attack_path, this_parent=this_parent)
            self.generic_addition_conversion(path_base_model_passive=path_base_model_passive, path_attack_animations_bpe=path_attack_animations_bpe,dump_folder=dump_folder, name_sub_changed=name_sub_changed, merge_flag=merge_flag)
        
        elif (f'Lavitz Normal' in dump_folder):
            position_string_replace = model_passive_path.find(f'SECT')
            clear_string = model_passive_path[:position_string_replace]
            new_model_string = f'{clear_string}characters/lavitz/models/combat'
            path_base_model_passive = self.look_for_files_entities(path_to_files=new_model_string, this_parent=this_parent)
            path_attack_animations_bpe = self.look_for_attack_animations(path_to_files=model_attack_path, this_parent=this_parent)
            self.generic_addition_conversion(path_base_model_passive=path_base_model_passive, path_attack_animations_bpe=path_attack_animations_bpe,dump_folder=dump_folder, name_sub_changed=name_sub_changed, merge_flag=merge_flag)
        
        elif (f'Rose Normal' in dump_folder):
            position_string_replace = model_passive_path.find(f'SECT')
            clear_string = model_passive_path[:position_string_replace]
            new_model_string = f'{clear_string}characters/rose/models/combat'
            path_base_model_passive = self.look_for_files_entities(path_to_files=new_model_string, this_parent=this_parent)
            path_attack_animations_bpe = self.look_for_attack_animations(path_to_files=model_attack_path, this_parent=this_parent)
            self.generic_addition_conversion(path_base_model_passive=path_base_model_passive, path_attack_animations_bpe=path_attack_animations_bpe,dump_folder=dump_folder, name_sub_changed=name_sub_changed, merge_flag=merge_flag)
        
        elif (f'Haschel Normal' in dump_folder):
            position_string_replace = model_passive_path.find(f'SECT')
            clear_string = model_passive_path[:position_string_replace]
            new_model_string = f'{clear_string}characters/haschel/models/combat'
            path_base_model_passive = self.look_for_files_entities(path_to_files=new_model_string, this_parent=this_parent)
            path_attack_animations_bpe = self.look_for_attack_animations(path_to_files=model_attack_path, this_parent=this_parent)
            self.generic_addition_conversion(path_base_model_passive=path_base_model_passive, path_attack_animations_bpe=path_attack_animations_bpe,dump_folder=dump_folder, name_sub_changed=name_sub_changed, merge_flag=merge_flag)
        
        elif (f'Albert Normal' in dump_folder):
            position_string_replace = model_passive_path.find(f'SECT')
            clear_string = model_passive_path[:position_string_replace]
            new_model_string = f'{clear_string}characters/albert/models/combat'
            path_base_model_passive = self.look_for_files_entities(path_to_files=new_model_string, this_parent=this_parent)
            path_attack_animations_bpe = self.look_for_attack_animations(path_to_files=model_attack_path, this_parent=this_parent)
            self.generic_addition_conversion(path_base_model_passive=path_base_model_passive, path_attack_animations_bpe=path_attack_animations_bpe,dump_folder=dump_folder, name_sub_changed=name_sub_changed, merge_flag=merge_flag)
        
        elif (f'Meru Normal' in dump_folder):
            position_string_replace = model_passive_path.find(f'SECT')
            clear_string = model_passive_path[:position_string_replace]
            new_model_string = f'{clear_string}characters/meru/models/combat'
            path_base_model_passive = self.look_for_files_entities(path_to_files=new_model_string, this_parent=this_parent)
            path_attack_animations_bpe = self.look_for_attack_animations(path_to_files=model_attack_path, this_parent=this_parent)
            self.generic_addition_conversion(path_base_model_passive=path_base_model_passive, path_attack_animations_bpe=path_attack_animations_bpe,dump_folder=dump_folder, name_sub_changed=name_sub_changed, merge_flag=merge_flag)
        
        elif (f'Kongol Normal' in dump_folder):
            position_string_replace = model_passive_path.find(f'SECT')
            clear_string = model_passive_path[:position_string_replace]
            new_model_string = f'{clear_string}characters/kongol/models/combat'
            path_base_model_passive = self.look_for_files_entities(path_to_files=new_model_string, this_parent=this_parent)
            path_attack_animations_bpe = self.look_for_attack_animations(path_to_files=model_attack_path, this_parent=this_parent)
            self.generic_addition_conversion(path_base_model_passive=path_base_model_passive, path_attack_animations_bpe=path_attack_animations_bpe,dump_folder=dump_folder, name_sub_changed=name_sub_changed, merge_flag=merge_flag)
        
        elif (f'Shana Normal' in dump_folder):
            position_string_replace = model_passive_path.find(f'SECT')
            clear_string = model_passive_path[:position_string_replace]
            new_model_string = f'{clear_string}characters/shana/models/combat'
            path_base_model_passive = self.look_for_files_entities(path_to_files=new_model_string, this_parent=this_parent)
            path_attack_animations_bpe = self.look_for_attack_animations(path_to_files=model_attack_path, this_parent=this_parent)
            self.generic_addition_conversion(path_base_model_passive=path_base_model_passive, path_attack_animations_bpe=path_attack_animations_bpe,dump_folder=dump_folder, name_sub_changed=name_sub_changed, merge_flag=merge_flag)
        
        elif (f'Miranda Normal' in dump_folder):
            position_string_replace = model_passive_path.find(f'SECT')
            clear_string = model_passive_path[:position_string_replace]
            new_model_string = f'{clear_string}characters/miranda/models/combat'
            path_base_model_passive = self.look_for_files_entities(path_to_files=new_model_string, this_parent=this_parent)
            path_attack_animations_bpe = self.look_for_attack_animations(path_to_files=model_attack_path, this_parent=this_parent)
            self.generic_addition_conversion(path_base_model_passive=path_base_model_passive, path_attack_animations_bpe=path_attack_animations_bpe,dump_folder=dump_folder, name_sub_changed=name_sub_changed, merge_flag=merge_flag)
        
        elif (f'Dart Dragoon' in dump_folder):
            position_string_replace = model_passive_path.find(f'SECT')
            clear_string = model_passive_path[:position_string_replace]
            new_model_string = f'{clear_string}characters/dart/models/dragoon'
            path_base_model_passive = self.look_for_files_entities(path_to_files=new_model_string, this_parent=this_parent)
            model_path = path_base_model_passive[0]
            passive_path = path_base_model_passive[1]
            self.convert_passive(passive_path=passive_path, path_to_dump_data=dump_folder, name_sub_changed=name_sub_changed, model_path=model_path, path_flag='Normal')
        
        elif (f'Lavitz Dragoon' in dump_folder):
            position_string_replace = model_passive_path.find(f'SECT')
            clear_string = model_passive_path[:position_string_replace]
            new_model_string = f'{clear_string}characters/lavitz/models/dragoon'
            path_base_model_passive = self.look_for_files_entities(path_to_files=new_model_string, this_parent=this_parent)
            model_path = path_base_model_passive[0]
            passive_path = path_base_model_passive[1]
            self.convert_passive(passive_path=passive_path, path_to_dump_data=dump_folder, name_sub_changed=name_sub_changed, model_path=model_path, path_flag='Normal')
        
        elif (f'Shana Dragoon' in dump_folder):
            position_string_replace = model_passive_path.find(f'SECT')
            clear_string = model_passive_path[:position_string_replace]
            new_model_string = f'{clear_string}characters/shana/models/dragoon'
            path_base_model_passive = self.look_for_files_entities(path_to_files=new_model_string, this_parent=this_parent)
            model_path = path_base_model_passive[0]
            passive_path = path_base_model_passive[1]
            self.convert_passive(passive_path=passive_path, path_to_dump_data=dump_folder, name_sub_changed=name_sub_changed, model_path=model_path, path_flag='Normal')
        
        elif (f'Rose Dragoon' in dump_folder):
            position_string_replace = model_passive_path.find(f'SECT')
            clear_string = model_passive_path[:position_string_replace]
            new_model_string = f'{clear_string}characters/rose/models/dragoon'
            path_base_model_passive = self.look_for_files_entities(path_to_files=new_model_string, this_parent=this_parent)
            model_path = path_base_model_passive[0]
            passive_path = path_base_model_passive[1]
            self.convert_passive(passive_path=passive_path, path_to_dump_data=dump_folder, name_sub_changed=name_sub_changed, model_path=model_path, path_flag='Normal')
        
        elif (f'Haschel Dragoon' in dump_folder):
            position_string_replace = model_passive_path.find(f'SECT')
            clear_string = model_passive_path[:position_string_replace]
            new_model_string = f'{clear_string}characters/haschel/models/dragoon'
            path_base_model_passive = self.look_for_files_entities(path_to_files=new_model_string, this_parent=this_parent)
            model_path = path_base_model_passive[0]
            passive_path = path_base_model_passive[1]
            self.convert_passive(passive_path=passive_path, path_to_dump_data=dump_folder, name_sub_changed=name_sub_changed, model_path=model_path, path_flag='Normal')
        
        elif (f'Albert Dragoon' in dump_folder):
            position_string_replace = model_passive_path.find(f'SECT')
            clear_string = model_passive_path[:position_string_replace]
            new_model_string = f'{clear_string}characters/albert/models/dragoon'
            path_base_model_passive = self.look_for_files_entities(path_to_files=new_model_string, this_parent=this_parent)
            model_path = path_base_model_passive[0]
            passive_path = path_base_model_passive[1]
            self.convert_passive(passive_path=passive_path, path_to_dump_data=dump_folder, name_sub_changed=name_sub_changed, model_path=model_path, path_flag='Normal')
        
        elif (f'Meru Dragoon' in dump_folder):
            position_string_replace = model_passive_path.find(f'SECT')
            clear_string = model_passive_path[:position_string_replace]
            new_model_string = f'{clear_string}characters/meru/models/dragoon'
            path_base_model_passive = self.look_for_files_entities(path_to_files=new_model_string, this_parent=this_parent)
            model_path = path_base_model_passive[0]
            passive_path = path_base_model_passive[1]
            self.convert_passive(passive_path=passive_path, path_to_dump_data=dump_folder, name_sub_changed=name_sub_changed, model_path=model_path, path_flag='Normal')
        
        elif (f'Kongol Dragoon' in dump_folder):
            position_string_replace = model_passive_path.find(f'SECT')
            clear_string = model_passive_path[:position_string_replace]
            new_model_string = f'{clear_string}characters/kongol/models/dragoon'
            path_base_model_passive = self.look_for_files_entities(path_to_files=new_model_string, this_parent=this_parent)
            model_path = path_base_model_passive[0]
            passive_path = path_base_model_passive[1]
            self.convert_passive(passive_path=passive_path, path_to_dump_data=dump_folder, name_sub_changed=name_sub_changed, model_path=model_path, path_flag='Normal')
        
        elif (f'Miranda Dragoon' in dump_folder):
            position_string_replace = model_passive_path.find(f'SECT')
            clear_string = model_passive_path[:position_string_replace]
            new_model_string = f'{clear_string}characters/miranda/models/dragoon'
            path_base_model_passive = self.look_for_files_entities(path_to_files=new_model_string, this_parent=this_parent)
            model_path = path_base_model_passive[0]
            passive_path = path_base_model_passive[1]
            self.convert_passive(passive_path=passive_path, path_to_dump_data=dump_folder, name_sub_changed=name_sub_changed, model_path=model_path, path_flag='Normal')
        
        elif (f'Dart Divine Dragoon' in dump_folder):
            position_string_replace = model_passive_path.find(f'SECT')
            clear_string = model_passive_path[:position_string_replace]
            new_model_string = f'{clear_string}characters/divine/models/dragoon'
            path_base_model_passive = self.look_for_files_entities(path_to_files=new_model_string, this_parent=this_parent)
            model_path = path_base_model_passive[0]
            passive_path = path_base_model_passive[1]
            self.convert_passive(passive_path=passive_path, path_to_dump_data=dump_folder, name_sub_changed=name_sub_changed, model_path=model_path, path_flag='Normal')

    def convert_attack(self, attack_path=list, path_to_dump_data=str, name_sub_changed=str, model_path=str, path_flag=str):
        number_add_attack = 0
        for passive_anims in attack_path:
            passive_path_new = path_to_dump_data.replace(f'{name_sub_changed}/{name_sub_changed}', f'{name_sub_changed}/Attack/')
            self.create_single_folder(folder_creation=passive_path_new)
            passive_path_dae_new = path_to_dump_data.replace(f'{name_sub_changed}/{name_sub_changed}', f'{name_sub_changed}/Attack/{name_sub_changed}_{number_add_attack}')
            convert_batch.main(model_file=model_path, animation_file=passive_anims, animation_type=path_flag, new_folder=passive_path_dae_new)
            number_add_attack += 1

    def generic_addition_conversion(self, path_base_model_passive=list, path_attack_animations_bpe=list, dump_folder=str, name_sub_changed=str, merge_flag=int):
            base_model = path_base_model_passive[0]
            passive_saf = path_base_model_passive[1]
            self.convert_passive(passive_path=passive_saf, path_to_dump_data=dump_folder, name_sub_changed=name_sub_changed, model_path=base_model, path_flag='Normal')
            bpe_anims = []
            nonbpe_anims = []
            temp_dump = f''
            for path_attk in path_attack_animations_bpe:
                path_saf = path_attk[0]
                bpe_flag = path_attk[1]
                if bpe_flag == f'BPE':
                    decompressed_file = decompress_bpe.decompress_bpe(compressed_file_path=path_saf)
                    bpe_anims.append(decompressed_file)
                else:
                    nonbpe_anims.append(path_saf)
            
            path_attack_animations = []
            
            if (len(bpe_anims) > 0) and (merge_flag == 1):
                search_last_slash = dump_folder.rfind(f'/')
                temp_dump_clear = dump_folder[:search_last_slash]
                temp_dump = f'{temp_dump_clear}/TEMP/'
                self.create_single_folder(folder_creation=temp_dump)
                file_name_tmp = f'{temp_dump_clear}/TEMP/anim_merged.tmp'
                merging_saf = []
                number_of_transforms = []
                number_of_objects = []
                first_header = b''
                for number_anim in range(0, len(bpe_anims)):
                    if number_anim == 0:
                        joined_anim = b''.join(bpe_anims[number_anim])
                        get_transforms_number = joined_anim[14:16]
                        get_number_objs = joined_anim[12:14]
                        transforms_int = int.from_bytes(get_transforms_number, 'little', signed=False)
                        obj_int = int.from_bytes(get_number_objs, 'little', signed=False)
                        first_header = joined_anim[0:16]
                        merging_saf.append(joined_anim)
                        number_of_transforms.append(transforms_int)
                        number_of_objects.append(obj_int)
                    else:
                        joined_anim = b''.join(bpe_anims[number_anim])
                        get_transforms_number = joined_anim[14:16]
                        get_number_objs = joined_anim[12:14]
                        transforms_int = int.from_bytes(get_transforms_number, 'little', signed=False)
                        obj_int = int.from_bytes(get_number_objs, 'little', signed=False)
                        joined_anim_no_header = joined_anim[16:]
                        merging_saf.append(joined_anim_no_header)
                        number_of_transforms.append(transforms_int)
                        number_of_objects.append(obj_int)
                
                set_objs = [set(number_of_objects)]
                if len(set_objs) == 1:
                    pass
                else:
                    messagebox.showerror(title='FATAL CRASH', message=f'Number of Objects in merging don\'t match, exiting the program...')
                    exit()
                obj_num = []
                for obj in set_objs: # Unpacking the SET DUHHHHHH!!
                    for o in obj:
                        obj_num.append(o)
                
                int_obj = obj_num[0]
                merging_saf = b''.join(merging_saf)
                sum_transforms = sum(number_of_transforms)
                objnum_to_bytes = int.to_bytes(int_obj, 2, 'little', signed=False)
                transforms_to_bytes = int.to_bytes(sum_transforms, 2, 'little', signed=False)
                joining_stuff = objnum_to_bytes + transforms_to_bytes
                total_header_string = b'\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + joining_stuff
                new_merging_saf = merging_saf.replace(first_header, total_header_string)
                with open(file_name_tmp, 'wb') as write_merged:
                    write_merged.write(new_merging_saf)
                path_attack_animations.append(file_name_tmp)
            
            elif (len(bpe_anims) > 0) and (merge_flag == 0):
                search_last_slash = dump_folder.rfind(f'/')
                temp_dump_clear = dump_folder[:search_last_slash]
                temp_dump = f'{temp_dump_clear}/TEMP/'
                self.create_single_folder(folder_creation=temp_dump)
                for number_anim in range(0, len(bpe_anims)):
                    file_name_tmp = f'{temp_dump_clear}/TEMP/{number_anim}.tmp'
                    with open(file_name_tmp, 'wb') as write_temp_saf:
                        read_this_anim = b''.join(bpe_anims[number_anim])
                        write_temp_saf.write(read_this_anim)
                    path_attack_animations.append(file_name_tmp)
            
            attack_saf = path_attack_animations + nonbpe_anims
            self.convert_attack(attack_path=attack_saf, path_to_dump_data=dump_folder, name_sub_changed=name_sub_changed, model_path=base_model, path_flag='Normal')
            if os.path.isdir(temp_dump): # TODO THIS IS ONLY FOR DELETING TEMP FOLDER, CAN BE DISABLED?
                shutil.rmtree(temp_dump)

    def walk_into_dir(self, path_to_files=str):
        walk_dir = os.walk(path_to_files)
        files_there = []
        for root, dir, files in walk_dir:
            for f in files:
                if f != f'mrg':
                    files_there.append(f)
        return files_there
    
    def update_percent_label(self, number_add=float):
        self.percentage_label.update_idletasks()
        percent_string = "%.2f" % number_add
        print(percent_string)
        self.percentage_label.config(text=f'{percent_string}%')

    def update_bar_progression(self, model_processed=float):
        self.new_bar.update_idletasks()
        model_processed_round = round(model_processed)
        self.new_bar['value'] = model_processed_round
        print(self.new_bar['value'])