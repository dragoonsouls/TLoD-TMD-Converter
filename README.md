# **TLoD-TMD-Converter**

The idea of this tool is to preserve TMD Models as originally shown ingame(*). Much of the tools over internet add or remove stuff from the models (such as: Dragoon wings; convert Quad faces into Tri faces), maybe is not the BEST tool if you want something fast or bug free.

Also i added a very specific functionality for researchers and modders, when you export the 3D model two *.txt files will created, Primitive_per_Object will contain useful data of each primitive type used in models and also the quantity of each one. The other called TMD_Report will be created with a count number of Vertex/Normal/Primitive of each object in the file and a sum of all the file.

## ALPHA V 0.4

A simple converter to DAE format oriented to work with TLoD TMD format and to be imported into Blender.
Python coded (recommended version 3.10.2 64bit), so just install python, execute tlod_tmd_converter.py, follow instructions and this tool should do the trick.

Options when executing:

Choose the Type of TMD to analyse:

-tmd (Standard TMD Format).

-ctmd (Custom TMD Format, specific TLoD TMD format). - this option is not currently supported, this part of the project is halted until i finish the complete research.

-anm (SAF - Scripted File Animation). - This option combine the animation file and the model into a single DAE file.

-banm (More than one SAF). - This option will merge various SAF files with the Model to a single DAE file.

File path: (example)
C:\modding\TLoD_TMD\file.bin
Folder path (example)
C:\modding\TLoD_TMD\

Also is pretty recommend use the LoDModS tool to dump the TMD files:

# **LoDModS by theflyingzamboni**

*https://github.com/theflyingzamboni/lodmods*


TLOD TMD Converter - By DooMMetaL (DragoonSouls):

i want to thanks a lot to this people who came my main inspiration to learn programming!:

TheFlyingZamboni Monoxide Illeprih Zychronix

and all the people from the TLoD Global Discord!. Cheers!.

(*) This prove to be partially true, the main problem comes with actual 3D Software, which do not support double faces and simply delete them without any warning for the final user, while the older version (Alpha V 0.1) maintain the double faces, newer versions simply use an auto-double face duplication algorithm -sorry-. 

CHANGELOG

ALPHA 0.4 version
CODE REFACTOR (LOGIC AND ALGORITHM REFACTOR, CODE CLEAN UP)
ADDING SUPPORT FOR CONVERTING ANIMATIONS INTO THE DAE FILE
ADDING SUPPORT FOR MERGING SEVERAL ANIMATIONS AT ONCE IN A SINGLE FILE
FIXED SOME LITTLE BUGS, SPECIALLY IN THE GRADIENT COLOURS. 
IMPORTANT: THERE IS A KNOW ISSUE IN SOME MODELS THAT ADD MORE FACES WHERE IS NOT NECESSARY, THIS HAPPENS
BECAUSE THOSE MODELS HAVE DUPLICATED OR MORE MULTIPLIES OF THE VERTICES OBJECTS AND I MEAN IN THE ORIGINAL BINARY FILES, 
AT THE MOMENT I HAVE NO FIX FOR THEM:
AFFECTED MODELS I FOUND:
BATTLE STAGES
Phantom Ship
Undersea Cavern
Melbu Frahma Last Stage
Wingly City (Moon)
Archangel Battle (Moon)

Some foes (very few) have the same issue and are under researching.

ALPHA 0.3 version
CODE REFACTOR IN COLLADA CONVERSION MODULE. (NOW FACE OF CHARACTERS ARE DUPLICATED, AND COLOUR IS CONSISTENT).
ADDED SOME NEW PRIMITIVE TYPES FOUND IN SOME FILES.
GENERAL BUGFIXES.

ALPHA 0.2 version
TOTAL REFACTOR IN CODE.
PROJECT NAME CHANGED TO A PROPER ONE.
SUPPORT TO VERTEX COLOR IN FACES.
ADDED NEW FILE TYPE TO CONVERT (*.DAE) COLLADA FILE.
SOLVED THE UV ISSUE (AT LEAST IN THE NEW FORMAT TYPE DAE).

ALPHA 0.1 version
FIRST RELEASE
