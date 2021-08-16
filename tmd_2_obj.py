"""

TMD TO OBJ Tool, for The Legend of Dragoon weirds tmd's,
this simple tool only will take the vertex info, obj info and texture/CLUT info (if possible),
to export it into OBJ Wavefont format, ignoring most of the primitive stuff, to get rid of it
and import to 3D Softwares such Blender

Copyright (C) 2021 DooMMetaL

"""

import os
import sys
import argparse
from tmd_lod_config import *
from tmd_reader import MyTmdReader
from tmd_reader import TmdStructure
from tmd_reader import Obj_Writer


MyTmdReader.file_reader(MyTmdReader.file_reader)
TmdStructure.object_list_reader(TmdStructure.object_list_reader)
TmdStructure.object_list_number(TmdStructure.object_list_number)
TmdStructure.data_property_reader(TmdStructure.data_property_reader)
TmdStructure.data_property_show(TmdStructure.data_property_show)
TmdStructure.address_conversion(TmdStructure.address_conversion)
Obj_Writer.read_from_address(Obj_Writer.read_from_address)
Obj_Writer.obj_converter(Obj_Writer.obj_converter)
Obj_Writer.material_converter(Obj_Writer.material_converter)
Obj_Writer.primitives_informer(Obj_Writer.primitives_informer)
