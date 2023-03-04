"""

TLoD TMD Converter Tool, was written for the Standard and Custom TMD from The Legend of Dragoon,
this simple tool will take the objects data, vertex data, CLUT/Palette data and Primitive data,
to export it into DAE format, and import to 3D Softwares such Blender.

Note: Custom TMD are under research so Primitives and CLUT is not fully supported

Copyright (C) 2022 DooMMetaL

"""

import standard_tmd
import standard_tmd_structure
import standard_tmd_writer
import standard_tmd_decoder
import custom_tmd
import custom_tmd_structure
import custom_tmd_decoder
import custom_tmd_writer
import ctmd_collada
import animation_file_process
import animation_file_process_batch
import tlod_tmd_saf_collada
import tlod_anim_batch_dae
import cmb_tmd_collada
import ctmd_saf_collada

print("Choose the Type of TMD to analyse: Standard TMD, Custom TMD, Animation files. \nFor standard -tmd, for custom -ctmd, animation -anm, batch animation -banm, -tmddeff")
print(f'IMPORTANT NOTE: For CTMD Files, the tool will try to find embedded CMB/LMB/SAF animations')

user_choose = input()

try:
    if (user_choose == "-tmd"):
        print("Working on a Standard TMD")
        try:
            standard_tmd.StandardTmdReader.data_reader(standard_tmd.StandardTmdReader.data_reader)
            
            standard_tmd_structure.StandardTmdStructure.object_list_reader(standard_tmd_structure.StandardTmdStructure.object_list_reader)
            standard_tmd_structure.StandardTmdStructure.object_list_converter(standard_tmd_structure.StandardTmdStructure.object_list_converter)
            standard_tmd_structure.StandardTmdStructure.vertex_block_extractor(standard_tmd_structure.StandardTmdStructure.vertex_block_extractor)
            standard_tmd_structure.StandardTmdStructure.normal_block_extractor(standard_tmd_structure.StandardTmdStructure.normal_block_extractor)
            standard_tmd_structure.StandardTmdStructure.primitive_block_extractor(standard_tmd_structure.StandardTmdStructure.primitive_block_extractor)
            standard_tmd_writer.NewFolder.convert_folder(standard_tmd_writer.NewFolder.convert_folder)
            standard_tmd_writer.PropertiesWriter.tmd_informer(standard_tmd_writer.PropertiesWriter.tmd_informer)
            standard_tmd_decoder.VertexInterpreter.vertex_decoder(standard_tmd_decoder.VertexInterpreter.vertex_decoder)
            standard_tmd_decoder.NormalInterpreter.normal_decoder(standard_tmd_decoder.NormalInterpreter.normal_decoder)
            standard_tmd_decoder.PrimitiveTmd.decode_primitive(standard_tmd_decoder.PrimitiveTmd.decode_primitive)
            # Primitives per object informer (debug)
            standard_tmd_writer.PropertiesWriter.primitives_for_object(standard_tmd_writer.PropertiesWriter.primitives_for_object)
            standard_tmd_writer.PropertiesWriter.primitives_per_obj_write(standard_tmd_writer.PropertiesWriter.primitives_per_obj_write)

            # Collada converter (experimental)
            tlod_tmd_saf_collada.ColladaAnimFileWriter.dae_from_tmdanim(tlod_tmd_saf_collada.ColladaAnimFileWriter.dae_from_tmdanim, saf_animation=False)
        except OSError:
            print("This is not a valid path, exiting")
            exit()

    elif user_choose == "-ctmd":
        print("Working on a Custom TMD - HIGHLY EXPERIMENTAL")
        try:
            # CUSTOM TMD READER
            custom_tmd.CustomTmdReader.custom_data_reader(custom_tmd.CustomTmdReader.custom_data_reader)
            # CUSTOM TMD STRUCTURE
            custom_tmd_structure.CustomTmdStructure.c_object_list_reader(custom_tmd_structure.CustomTmdStructure.c_object_list_reader)
            custom_tmd_structure.CustomTmdStructure.c_object_list_converter(custom_tmd_structure.CustomTmdStructure.c_object_list_converter)
            custom_tmd_structure.CustomTmdStructure.custom_vertex_block_extractor(custom_tmd_structure.CustomTmdStructure.custom_vertex_block_extractor)
            custom_tmd_structure.CustomTmdStructure.custom_normal_block_extractor(custom_tmd_structure.CustomTmdStructure.custom_normal_block_extractor)
            custom_tmd_structure.CustomTmdStructure.custom_primitive_block_extractor(custom_tmd_structure.CustomTmdStructure.custom_primitive_block_extractor)
            # CUSTOM TMD DECODER
            print(f'Select the Desired Attribute:\n1 = 0x14 00 00 40;\n2 = 0x14 00 00 00;\n3 = 0x50 00 00 00;\n4 = 0x64 00 00 40;\n5 = 0x54 00 00 00;\nAny other value will be set as 0x14 00 00 00')
            attribute_selection = int(input())
            custom_tmd_decoder.CustomTmdInterpreter.normal_decoder(custom_tmd_decoder.CustomTmdInterpreter.normal_decoder)
            custom_tmd_decoder.CustomTmdInterpreter.cprimitive_types_depacker(custom_tmd_decoder.CustomTmdInterpreter.cprimitive_types_depacker, attribute_selection)
            custom_tmd_decoder.CustomTmdVertexFixer.vertex_decoder(custom_tmd_decoder.CustomTmdVertexFixer.vertex_decoder)

            # CMB|||LMB
            if (custom_tmd.animation_bool == True) and (custom_tmd.cmb_animation_bool == True):
                animation_file_process.CmbFileReader.cmb_decoder(animation_file_process.CmbFileReader.cmb_decoder, cmb_bool=custom_tmd.cmb_animation_bool, cmb_anim=custom_tmd.cmb_animation_block, tmd_file_b=False, ctmd_file_b=True)
            # HERE i will place LMB too
            elif (custom_tmd.animation_bool == True) and (custom_tmd.lmb0_animation_bool == True):
                animation_file_process.LmbFileReader.lmb_type_0(animation_file_process.LmbFileReader.lmb_type_0, lmb0_bool=custom_tmd.lmb0_animation_bool, lmb_anim=custom_tmd.lmb0_animation_block)
            # HERE SAF
            elif (custom_tmd.animation_bool == True) and (custom_tmd.saf_animation_bool == True):
                animation_file_process.SafExtractor.saf_reader_embedded(animation_file_process.SafExtractor.saf_reader_embedded, saf_block=custom_tmd.saf_animation_block)
                animation_file_process.SafExtractor.convert_data(animation_file_process.SafExtractor.convert_data)
            
            elif (custom_tmd.animation_bool == None):
                print(f'if you want to choose the animation Type, write -lmb or -cmb, if you don\'t know just write -none')
                user_anim_choose = input()
                if user_anim_choose == f'-cmb':
                    pass
                elif user_anim_choose == f'-lmb':
                    pass
                else:
                    print(f'WARNING: the file will be converted with no animation!')

            # CUSTOM TMD WRITER
            custom_tmd_writer.NewFolderCustom.custom_convert_folder(custom_tmd_writer.NewFolderCustom.custom_convert_folder)

            # CUSTOM COLLADA WRITER
            if custom_tmd.saf_animation_bool == True:
                ctmd_saf_collada.ColladaAnimFileWriter.dae_from_ctmdanim(ctmd_saf_collada.ColladaAnimFileWriter.dae_from_ctmdanim, saf_animation=True)
            else:
                ctmd_collada.ColladaAnimFileWriter.dae_from_ctmdanim(ctmd_collada.ColladaAnimFileWriter.dae_from_ctmdanim, saf_animation=custom_tmd.animation_bool)
        except OSError:
            print("This is not a valid path, exiting")
            exit()

    elif user_choose == "-anm" or user_choose == "-banm":
        print("Working on a Scripted Animation Files and TMDs")
        try:
            if user_choose == "-anm":
                print("Converting Single Animation")
                animation_file_process.SafExtractor.saf_reader_input(animation_file_process.SafExtractor.saf_reader_input)
                animation_file_process.SafExtractor.saf_reader(animation_file_process.SafExtractor.saf_reader)
                standard_tmd.StandardTmdReader.data_reader(standard_tmd.StandardTmdReader.data_reader)
                animation_file_process.SafExtractor.compare_data(animation_file_process.SafExtractor.compare_data)
                animation_file_process.SafExtractor.convert_data(animation_file_process.SafExtractor.convert_data)
                
                standard_tmd_structure.StandardTmdStructure.object_list_reader(standard_tmd_structure.StandardTmdStructure.object_list_reader)
                standard_tmd_structure.StandardTmdStructure.object_list_converter(standard_tmd_structure.StandardTmdStructure.object_list_converter)
                standard_tmd_structure.StandardTmdStructure.vertex_block_extractor(standard_tmd_structure.StandardTmdStructure.vertex_block_extractor)
                standard_tmd_structure.StandardTmdStructure.normal_block_extractor(standard_tmd_structure.StandardTmdStructure.normal_block_extractor)
                standard_tmd_structure.StandardTmdStructure.primitive_block_extractor(standard_tmd_structure.StandardTmdStructure.primitive_block_extractor)
                standard_tmd_writer.NewFolder.convert_folder(standard_tmd_writer.NewFolder.convert_folder)
                standard_tmd_writer.PropertiesWriter.tmd_informer(standard_tmd_writer.PropertiesWriter.tmd_informer)
                standard_tmd_decoder.VertexInterpreter.vertex_decoder(standard_tmd_decoder.VertexInterpreter.vertex_decoder)
                standard_tmd_decoder.NormalInterpreter.normal_decoder(standard_tmd_decoder.NormalInterpreter.normal_decoder)
                standard_tmd_decoder.PrimitiveTmd.decode_primitive(standard_tmd_decoder.PrimitiveTmd.decode_primitive)
                # Primitives per object informer (debug)
                standard_tmd_writer.PropertiesWriter.primitives_for_object(standard_tmd_writer.PropertiesWriter.primitives_for_object)
                standard_tmd_writer.PropertiesWriter.primitives_per_obj_write(standard_tmd_writer.PropertiesWriter.primitives_per_obj_write)

                # Collada converter (experimental)
                tlod_tmd_saf_collada.ColladaAnimFileWriter.dae_from_tmdanim(tlod_tmd_saf_collada.ColladaAnimFileWriter.dae_from_tmdanim, saf_animation=True)
            
            elif user_choose == "-banm":
                print("Merging and Converting several Animations")
                print("WARNING: animations will be merged in the final conversion")
                animation_file_process_batch.SafExtractorBatch.batch_saf_reader_input(animation_file_process_batch.SafExtractorBatch.batch_saf_reader_input)
                animation_file_process_batch.SafExtractorBatch.batch_saf_reader(animation_file_process_batch.SafExtractorBatch.batch_saf_reader)
                standard_tmd.StandardTmdReader.data_reader(standard_tmd.StandardTmdReader.data_reader)
                animation_file_process_batch.SafExtractorBatch.batch_compare_data(animation_file_process_batch.SafExtractorBatch.batch_compare_data)
                animation_file_process_batch.SafExtractorBatch.batch_convert_data(animation_file_process_batch.SafExtractorBatch.batch_convert_data)
                
                standard_tmd_structure.StandardTmdStructure.object_list_reader(standard_tmd_structure.StandardTmdStructure.object_list_reader)
                standard_tmd_structure.StandardTmdStructure.object_list_converter(standard_tmd_structure.StandardTmdStructure.object_list_converter)
                standard_tmd_structure.StandardTmdStructure.vertex_block_extractor(standard_tmd_structure.StandardTmdStructure.vertex_block_extractor)
                standard_tmd_structure.StandardTmdStructure.normal_block_extractor(standard_tmd_structure.StandardTmdStructure.normal_block_extractor)
                standard_tmd_structure.StandardTmdStructure.primitive_block_extractor(standard_tmd_structure.StandardTmdStructure.primitive_block_extractor)
                standard_tmd_writer.NewFolder.convert_folder(standard_tmd_writer.NewFolder.convert_folder)
                standard_tmd_writer.PropertiesWriter.tmd_informer(standard_tmd_writer.PropertiesWriter.tmd_informer)
                standard_tmd_decoder.VertexInterpreter.vertex_decoder(standard_tmd_decoder.VertexInterpreter.vertex_decoder)
                standard_tmd_decoder.NormalInterpreter.normal_decoder(standard_tmd_decoder.NormalInterpreter.normal_decoder)
                standard_tmd_decoder.PrimitiveTmd.decode_primitive(standard_tmd_decoder.PrimitiveTmd.decode_primitive)
                # Primitives per object informer (debug)
                standard_tmd_writer.PropertiesWriter.primitives_for_object(standard_tmd_writer.PropertiesWriter.primitives_for_object)
                standard_tmd_writer.PropertiesWriter.primitives_per_obj_write(standard_tmd_writer.PropertiesWriter.primitives_per_obj_write)

                # Collada converter (experimental)
                tlod_anim_batch_dae.ColladaAnimFileWriter.dae_from_tmdanim(tlod_anim_batch_dae.ColladaAnimFileWriter.dae_from_tmdanim)
        except OSError:
            print("This is not a valid path, exiting")
            exit()
    
    elif user_choose == "-tmddeff":
        try:
            print(f'Working with a TMD that have CMB Animation File embedded...\nThis Type is only present on TMD files inside a DEFF Package')
            standard_tmd.DeffTmdReader.find_cmb_embedded(standard_tmd.DeffTmdReader.find_cmb_embedded)

            standard_tmd_structure.StandardTmdStructure.object_list_reader(standard_tmd_structure.StandardTmdStructure.object_list_reader)
            standard_tmd_structure.StandardTmdStructure.object_list_converter(standard_tmd_structure.StandardTmdStructure.object_list_converter)
            standard_tmd_structure.StandardTmdStructure.vertex_block_extractor(standard_tmd_structure.StandardTmdStructure.vertex_block_extractor)
            standard_tmd_structure.StandardTmdStructure.normal_block_extractor(standard_tmd_structure.StandardTmdStructure.normal_block_extractor)
            standard_tmd_structure.StandardTmdStructure.primitive_block_extractor(standard_tmd_structure.StandardTmdStructure.primitive_block_extractor)
            standard_tmd_writer.NewFolder.convert_folder(standard_tmd_writer.NewFolder.convert_folder)
            standard_tmd_writer.PropertiesWriter.tmd_informer(standard_tmd_writer.PropertiesWriter.tmd_informer)
            standard_tmd_decoder.VertexInterpreter.vertex_decoder(standard_tmd_decoder.VertexInterpreter.vertex_decoder)
            standard_tmd_decoder.NormalInterpreter.normal_decoder(standard_tmd_decoder.NormalInterpreter.normal_decoder)
            standard_tmd_decoder.PrimitiveTmd.decode_primitive(standard_tmd_decoder.PrimitiveTmd.decode_primitive)
            # Primitives per object informer (debug)
            standard_tmd_writer.PropertiesWriter.primitives_for_object(standard_tmd_writer.PropertiesWriter.primitives_for_object)
            standard_tmd_writer.PropertiesWriter.primitives_per_obj_write(standard_tmd_writer.PropertiesWriter.primitives_per_obj_write)

            # CMB Animation process
            animation_file_process.CmbFileReader.cmb_decoder(animation_file_process.CmbFileReader.cmb_decoder, cmb_bool=True, cmb_anim=standard_tmd.cmb_anim, tmd_file_b=True, ctmd_file_b=False)
            cmb_tmd_collada.ColladaAnimFileWriter.dae_from_tmd_cmb_anim(cmb_tmd_collada.ColladaAnimFileWriter.dae_from_tmd_cmb_anim, saf_animation=True)

        except OSError:
            print("This is not a valid path, exiting...")
            exit()

    else:
        print("Invalid option...")
        exit()

except KeyboardInterrupt:
    exit()