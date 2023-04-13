"""

Animation File Process: This module process files that are animations,
The animations Types supported has been called:
SAF (Simple Animation File).
CMB (Name TBA).
LMB Type 0 (Name TBA).
LMB Type 1 (Name TBA).
LMB Type 2 (Name TBA).

The difference among them is:
SAF support ROTATION/LOCATION SINGLE TMD (Could be animating TMD, TMD_CCONTAINER, TMD_DEFF)
CMB support ROTATION/LOCATION SINGLE and VARIOUS TMDs in the scene (ONLY DEFF)
LMB all Types support ROTATION/LOCATION/SCALE but the difference is done on how are processed internally (ONLY DEFF)

Copyright (C) 2023 DooMMetaL

"""

import convert_saf as csaf
import convert_cmb as ccmb
import convert_lmb as clmb

class AnimationInterpreter:
    def __init__(self, animation_file, animation_type):
        self.self = AnimationInterpreter
        self.animation_selector(animation_file=animation_file, animation_type=animation_type)
    
    def animation_selector(self, animation_file, animation_type): # IN HERE I WILL HAVE TO ADD THE MERGE OPTION FLAG
        """Animation Type is a list which elements are:
        animation_type[0] == Number of Objects
        animation_type[1] == Number of Transformations
        animation_type[2] == Type of Animation """
        merge_flag = False
        global animation_type_check
        animation_type_check = animation_type[2]

        global animation_decoded
        global processing_anim
        animation_decoded = []
        processing_anim = f''
        if animation_type_check == f'SAF':
            processing_anim = f'\nProcessing SAF File...'
            saf_trans_info = animation_type
            saf_dec = csaf.SafConverter.saf_convert(csaf.SafConverter, animation_byte_block=animation_file, saf_transform_info=saf_trans_info, merge_flag=merge_flag)
            animation_decoded = saf_dec

        elif animation_type_check == f'CMB':
            processing_anim = f'\nProcessing CMB File...'
            cmb_trans_info_full = animation_type
            cmb_dec = ccmb.CmbConverter.cmb_convert(ccmb.CmbConverter, cmb_anim=animation_file, cmb_trans_info=cmb_trans_info_full)
            animation_decoded = cmb_dec

        elif animation_type_check == f'LMB_Type_0':
            processing_anim = f'\nProcessing LMB Type 0 File...'
            lmb0_trans_info = animation_type
            lmb_dec = clmb.LmbConverter.lmb_type0_convert(clmb.LmbConverter, lmb_anim_data=animation_file, lmb_transform_info=lmb0_trans_info)
            animation_decoded = lmb_dec[0]
            animation_type[1] = lmb_dec[1]
        elif animation_type_check == f'LMB_Type_1':
            processing_anim = f'\nLMB Type 1 IS NOT SUPPORTED FOR CONVERSION...'
        elif animation_type_check == f'LMB_Type_2':
            processing_anim = f'\nLMB TYPE 2 IS NOT SUPPORTED FOR CONVERSION...'

        return animation_decoded