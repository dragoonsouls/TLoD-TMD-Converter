"""

TLoD TMD Converter Tool, was written for the Standard and Custom TMD from The Legend of Dragoon,
this simple tool will take the objects data, vertex data, CLUT/Palette data and Primitive data (if possible),
to export it into OBJ Wavefont format, and import to 3D Softwares such Blender.

Note: Custom TMD are under research so Primitives and CLUT is not fully supported

Copyright (C) 2022 DooMMetaL

"""

import standard_tmd
import standard_tmd_structure
import standard_tmd_writer
import standard_tmd_decoder
import animation_file_process
import animation_file_process_batch
import tlod_tmd_saf_collada
import tlod_anim_batch_dae


print(f'===TLoD TMD Conversion Tool Ver Alpha 0.4===')
print(f'Choose the Type of TMD to analyse: Standard TMD, Custom TMD, Animation files. \nFor standard -tmd, for custom -ctmd, animation -anm, merge animation -banm')

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
            print("CUSTOM TMD CONVERSION NOT IMPLEMENTED IN THIS VERSION")

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
    else:
        print("Invalid option...")
        exit()

except KeyboardInterrupt:
    exit()