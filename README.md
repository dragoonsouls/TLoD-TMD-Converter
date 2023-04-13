***
# **TLoD-TMD-Converter**
***
---
The idea behind this tool is to preserve TMD Models as originally shown ingame(*). Much of the tools over internet add or remove stuff from the models (such as: Dragoon wings; convert Quad faces into Tri faces), maybe is not the BEST tool if you want something fast or bug free.

Also i added a very specific functionality for researchers and modders, when you export the 3D model two *.txt files will created, Primitive_per_Object will contain useful data of each primitive type used in models and also the quantity of each one. The other called TMD_Report will be created with a count number of Vertex/Normal/Primitive of each object in the file and a sum of all the file.

## BETA 0.1

**There is an available version of the tool with GUI**
You check the releases and you will find a Windows Version of it (Tested in Windows 10)
if not, you can compile it yourself.

A simple converter to DAE (Collada) format oriented to work with TLoD Model and animation formats, to later be imported into Blender. Python coded (recommended version 3.10.2 64bit), so just install python, execute tlod_tmd_converter.py, follow instructions and this tool should do the trick.
Soon i will add the GUI and in a near future a previewer for models/animations converted.

Model Type supported: **TMD - CTMD**

Animation Type Supported: ***Embedded CMB, Embedded LMB Type 0, Embedded SAF and SAF***

While executing the tool will ask the path to the Model:

>File path: (example)

>C:\your_modding_folder\TLoD_Models\file.bin

If no Animation data is found inside the file, will ask if you want to load one.

Keep in mind without animation Data/File loaded, the conversion only will use the original position of Objects from the model, that in most of the cases is set at the origin point of the scene.

---
You can use both of the ways to get the files unpacked from the Assets container:

## **LoDModS by theflyingzamboni**

*[LoDModS](https://github.com/theflyingzamboni/lodmods)*


## **Severed Chains by Monoxide**

*[Severed-Chains](https://github.com/Legend-of-Dragoon-Modding/Legend-of-Dragoon-Java)*

Both ways, we recommend use the File Mapping document, to know where the Model and Animation file are located.

**_File Mapping Document_**

*[File Mapping Doc](https://docs.google.com/spreadsheets/d/1wso1zNTpeQM2WmxW73-hVLs4bKdGa_6jswWuKdFtavE/edit?usp=share_link)*

---

**TLOD TMD Converter - By DooMMetaL (AKA - DragoonSouls):**

i want to thanks a lot to this people who came my main inspiration to learn programming!:

TheFlyingZamboni Monoxide Illeprih Zychronix

Also a special thanks to Monoxide, who did an impressive job reversing TLoD Game Engine, thanks to his job, i been able to make a converter for CTMD, SAF, CMB and LMB files!.

and all the people from the TLoD Global Discord!. Cheers!.

(*) This prove to be partially true, the main problem comes with actual 3D Software, which do not support double faces using the same vertex and simply delete them without any warning for the final user, while the older version (Alpha V 0.1 which convert models into OBJ format) maintain the double faces, newer versions simply use an auto-split vertices algorithm -sorry-. Also we found some bugs related to winding of the Vertex Index in some models, this prevent to correctly form the primitives (which later will be faces) right now this is under research

### **DISCORD**

You can find me here:

**[Discord](https://discord.gg/legendofdragoon)**

### **CHANGELOG**

```
BETA 0.1 version

ADDING GUI FOR EASY USE OF THE TOOL!
TOTAL REFACTOR ON THE CODE TO FIT THE STANDARDS
FIX SOME RETAIL BUGS RELATED TO MODELS THAT HAVE UNUSED VERTICES IN THE BLOCK

ALPHA 0.5 version (older code)
CODE CLEANING (SOME MINOR REFACTOR AND MUCH CODE CLEAN UP).
ADDING SUPPORT FOR CONVERTING CTMD'S (FINALLY!).
ADDING SUPPORT FOR NEW ANIMATION FORMATS PRESENT ONLY IN DEFF FILES (CMB AND LMB).
ADDING SUPPORT FOR TMD FILES AND CTMD FILES WHICH HAVE ANIMATION DATA EMBEDDED.
ADDING SUPPORT FOR CONVERTING DIRECTLY TMD FILES INSIDE DEFF FILES WITHOUT HEX WORKAROUND.

ALPHA 0.4 version
CODE REFACTOR (LOGIC AND ALGORITHM REFACTOR, CODE CLEAN UP).
ADDING SUPPORT FOR CONVERTING ANIMATIONS INTO THE DAE FILE.
ADDING SUPPORT FOR MERGING SEVERAL ANIMATIONS AT ONCE IN A SINGLE FILE.
FIXED SOME LITTLE BUGS, SPECIALLY IN THE GRADIENT COLOURS. 
IMPORTANT: THERE IS A KNOW ISSUE IN SOME MODELS THAT ADD MORE FACES WHERE IS NOT NECESSARY, THIS HAPPENS
BECAUSE THOSE MODELS HAVE DUPLICATED OR MORE MULTIPLIES OF THE VERTICES OBJECTS AND I MEAN IN THE ORIGINAL BINARY FILES, 
AT THE MOMENT I HAVE NO FIX FOR THEM:
BATTLE STAGES
Phantom Ship.
Undersea Cavern.
Melbu Frahma Last Stage.
Wingly City (Moon).
Archangel Battle (Moon).
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
```


![GUI](https://raw.githubusercontent.com/dragoonsouls/TLoD-TMD-Converter/main/Sample_Images/showcase_2.png)
![Complete Virage](https://raw.githubusercontent.com/dragoonsouls/TLoD-TMD-Converter/main/Sample_Images/Complete_Virage.png)
![Dart](https://raw.githubusercontent.com/dragoonsouls/TLoD-TMD-Converter/main/Sample_Images/Dart.png)
![Dart DD Transformation](https://raw.githubusercontent.com/dragoonsouls/TLoD-TMD-Converter/main/Sample_Images/Dart_DD_Transform.png)
![Fruegel](https://raw.githubusercontent.com/dragoonsouls/TLoD-TMD-Converter/main/Sample_Images/Fruegel_1.png)
![Hoax Noon](https://raw.githubusercontent.com/dragoonsouls/TLoD-TMD-Converter/main/Sample_Images/Hoax_Day_take.png)
![Meru](https://raw.githubusercontent.com/dragoonsouls/TLoD-TMD-Converter/main/Sample_Images/Meru_Cat's_Cradle.png)
![Red-Eyed Dragon](https://raw.githubusercontent.com/dragoonsouls/TLoD-TMD-Converter/main/Sample_Images/RED.png)
![Rose Dragoon](https://raw.githubusercontent.com/dragoonsouls/TLoD-TMD-Converter/main/Sample_Images/Rose_Dragoon_Tutorial.png)
![Regole](https://raw.githubusercontent.com/dragoonsouls/TLoD-TMD-Converter/main/Sample_Images/Regole.png)
![Shana GoD](https://raw.githubusercontent.com/dragoonsouls/TLoD-TMD-Converter/main/Sample_Images/Shana_GoD.png)
![Valley of Corrupted Gravity](https://raw.githubusercontent.com/dragoonsouls/TLoD-TMD-Converter/main/Sample_Images/V_o_C_Gravity_Boss_Fight.png)
![Witch](https://raw.githubusercontent.com/dragoonsouls/TLoD-TMD-Converter/main/Sample_Images/Witch.png)
