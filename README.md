# TLoD-TMD-Mesh-Exporter
ALPHA 0.1

A simple exporter (to Obj format) oriented to work with TLoD TMD format and to be imported into Blender.
Python coded, so just install python, execute tmd_2_obj.py, follow instructions and this tool should do the trick.

Know Issues:

For some reason faces shown in the UV window get disordered or even dissapear from the UV coordinates, this issue is still under investigation, when resolved i will move the project to alpha 0.2.

The idea of this tool is to preserve the model as originally shown ingame. Much of the tools over internet add or remove stuff from the models (such as: Dragoon wings; convert Quad faces into Tri faces), maybe is not the BEST tool if you want something fast.

Also i added a very specific functionality for researchers and modders, when you export the 3D model a .dat file will created, this file will contain useful data of each primitive type used in models and also the quantity of each one. Also a .txt will be created with a count number of Vertex/Normal/Primitive of each object in the file and a summatory of all the file.
