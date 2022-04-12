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
import tlod_tmd_converter_colladaexp


print("Choose the Type of TMD to analyse: Standard TMD, Custom TMD. \nFor standard -tmd, for custom -ctmd")

user_choose = input()

try:
    if user_choose == "-tmd":
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
            # Decoders of Primitives split in methods for each one
            # (ALL) 3 Vertex LSC Textured - No Textured
            standard_tmd_decoder.PrimitiveTmd.decoded_lsc3vgt(standard_tmd_decoder.PrimitiveTmd.decoded_lsc3vgt)
            standard_tmd_decoder.PrimitiveTmd.decoded_lsc3vft(standard_tmd_decoder.PrimitiveTmd.decoded_lsc3vft)
            standard_tmd_decoder.PrimitiveTmd.decoded_new_lsc_3v_gt(standard_tmd_decoder.PrimitiveTmd.decoded_new_lsc_3v_gt)
            standard_tmd_decoder.PrimitiveTmd.decoded_new_lsc_3v_gt_2(standard_tmd_decoder.PrimitiveTmd.decoded_new_lsc_3v_gt_2)
            standard_tmd_decoder.PrimitiveTmd.decoded_lsc3vntgs(standard_tmd_decoder.PrimitiveTmd.decoded_lsc3vntgs)
            standard_tmd_decoder.PrimitiveTmd.decoded_lsc3vntfs(standard_tmd_decoder.PrimitiveTmd.decoded_lsc3vntfs)
            standard_tmd_decoder.PrimitiveTmd.decoded_lsc3vntgg(standard_tmd_decoder.PrimitiveTmd.decoded_lsc3vntgg)
            standard_tmd_decoder.PrimitiveTmd.decoded_lsc3vntfg(standard_tmd_decoder.PrimitiveTmd.decoded_lsc3vntfg)
            standard_tmd_decoder.PrimitiveTmd.decoded_new_lsc_3v_nt_fg(standard_tmd_decoder.PrimitiveTmd.decoded_new_lsc_3v_nt_fg)
            # (ALL) 4 Vertex LSC Textured - No Textured
            standard_tmd_decoder.PrimitiveTmd.decoded_lsc4vgt(standard_tmd_decoder.PrimitiveTmd.decoded_lsc4vgt)
            standard_tmd_decoder.PrimitiveTmd.decoded_lsc4vft(standard_tmd_decoder.PrimitiveTmd.decoded_lsc4vft)
            standard_tmd_decoder.PrimitiveTmd.decoded_new_lsc_4v_g_t(standard_tmd_decoder.PrimitiveTmd.decoded_new_lsc_4v_g_t)
            standard_tmd_decoder.PrimitiveTmd.decoded_new_lsc_4v_g_t_2(standard_tmd_decoder.PrimitiveTmd.decoded_new_lsc_4v_g_t_2)
            standard_tmd_decoder.PrimitiveTmd.decoded_lsc4vntgs(standard_tmd_decoder.PrimitiveTmd.decoded_lsc4vntgs)
            standard_tmd_decoder.PrimitiveTmd.decoded_lsc4vntfs(standard_tmd_decoder.PrimitiveTmd.decoded_lsc4vntfs)
            standard_tmd_decoder.PrimitiveTmd.decoded_lsc4vntgg(standard_tmd_decoder.PrimitiveTmd.decoded_lsc4vntgg)
            standard_tmd_decoder.PrimitiveTmd.decoded_lsc4vntfg(standard_tmd_decoder.PrimitiveTmd.decoded_lsc4vntfg)
            standard_tmd_decoder.PrimitiveTmd.decoded_new_lsc_4v_nt_g_s(standard_tmd_decoder.PrimitiveTmd.decoded_new_lsc_4v_nt_g_s)
            # (ALL) 3 Vertex NLSC Textured - No Textured
            standard_tmd_decoder.PrimitiveTmd.decoded_nlsc3vgt(standard_tmd_decoder.PrimitiveTmd.decoded_nlsc3vgt)
            standard_tmd_decoder.PrimitiveTmd.decoded_nlsc3vft(standard_tmd_decoder.PrimitiveTmd.decoded_nlsc3vft)
            standard_tmd_decoder.PrimitiveTmd.decoded_new_nlsc_3v_g_t(standard_tmd_decoder.PrimitiveTmd.decoded_new_nlsc_3v_g_t)
            standard_tmd_decoder.PrimitiveTmd.decoded_nlsc3vntg(standard_tmd_decoder.PrimitiveTmd.decoded_nlsc3vntg)
            standard_tmd_decoder.PrimitiveTmd.decoded_nlsc3vntf(standard_tmd_decoder.PrimitiveTmd.decoded_nlsc3vntf)
            # (ALL) 4 Vertex NLSC Textured - No Textured
            standard_tmd_decoder.PrimitiveTmd.decoded_nlsc4vgt(standard_tmd_decoder.PrimitiveTmd.decoded_nlsc4vgt)
            standard_tmd_decoder.PrimitiveTmd.decoded_nlsc4vft(standard_tmd_decoder.PrimitiveTmd.decoded_nlsc4vft)
            standard_tmd_decoder.PrimitiveTmd.decoded_new_nlsc_4v_g_t(standard_tmd_decoder.PrimitiveTmd.decoded_new_nlsc_4v_g_t)
            standard_tmd_decoder.PrimitiveTmd.decoded_nlsc4vntg(standard_tmd_decoder.PrimitiveTmd.decoded_nlsc4vntg)
            standard_tmd_decoder.PrimitiveTmd.decoded_nlsc4vntf(standard_tmd_decoder.PrimitiveTmd.decoded_nlsc4vntf)
            # NEW PRIMITIVES FOUND
            standard_tmd_decoder.PrimitiveTmd.decoded_new_lsc_4v_nt_gg(standard_tmd_decoder.PrimitiveTmd.decoded_new_lsc_4v_nt_gg)
            standard_tmd_decoder.PrimitiveTmd.decoded_new_lsc_3v_nt_gg(standard_tmd_decoder.PrimitiveTmd.decoded_new_lsc_3v_nt_gg)
            #End of Decoders of Primitives
            standard_tmd_decoder.ObjectCleaner.primitive_cleaner(standard_tmd_decoder.ObjectCleaner.primitive_cleaner)
            standard_tmd_writer.TmdConverter.object_converter(standard_tmd_writer.TmdConverter.object_converter)
            # Primitives per object informer (debug)
            standard_tmd_writer.PropertiesWriter.primitives_for_object(standard_tmd_writer.PropertiesWriter.primitives_for_object)
            standard_tmd_writer.PropertiesWriter.primitives_per_obj_write(standard_tmd_writer.PropertiesWriter.primitives_per_obj_write)

            # Collada converter (experimental)
            tlod_tmd_converter_colladaexp.ColladaFileWriter.dae_from_obj(tlod_tmd_converter_colladaexp.ColladaFileWriter.dae_from_obj)
            

        except OSError:
            print("This is not a valid path, exiting")
            exit()

    elif user_choose == "-ctmd":
        print("Working on a Custom TMD - HIGHLY EXPERIMENTAL")
        try:
            exit()
            
        
        except OSError:
            print("This is not a valid path, exiting")
            exit()

    else:
        print("That's not a valid option, exiting")
        exit()

except KeyboardInterrupt:
    exit()

