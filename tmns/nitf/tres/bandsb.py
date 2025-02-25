#**************************** INTELLECTUAL PROPERTY RIGHTS ****************************#
#*                                                                                    *#
#*                           Copyright (c) 2025 Terminus LLC                          *#
#*                                                                                    *#
#*                                All Rights Reserved.                                *#
#*                                                                                    *#
#*          Use of this source code is governed by LICENSE in the repo root.          *#
#*                                                                                    *#
#**************************** INTELLECTUAL PROPERTY RIGHTS ****************************#
#

#  Python Libraries
from collections import deque
from enum import Enum
import struct

#  Terminus Libraries
from tmns.nitf.tre   import TRE_Base
from tmns.nitf.field_types import FieldType
from tmns.nitf.utils import BitSet

class Field(Enum):
    CETAG                           = (  0,  6, FieldType.BCS_A,               None, 'Unique Extension Type Identifier' )
    CEL                             = (  1,  5, FieldType.BCS_NP,              None, 'TRE Length' )
    COUNT                           = (  2,  5, FieldType.BCS_NP,              None, 'Number of Bands' )
    RADIOMETRIC_QUANTITY            = (  3, 24, FieldType.BCS_A,               None, 'Data Representation' )
    RADIOMETRIC_QUANTITY_UNIT       = (  4,  1, FieldType.BCS_A,               None, 'Data Representation Unit' )
    SCALE_FACTOR                    = (  5,  4, FieldType.IEEE_754_FLOAT,      None, 'Cube Scale Factor (M)' )
    ADDITIVE_FACTOR                 = (  6,  4, FieldType.IEEE_754_FLOAT,      None, 'Cube Additive Factor (A)' )
    ROW_GSD                         = (  7,  7, FieldType.BCS_NP,              None, 'Row Ground Sample Distance' )
    ROW_GSD_UNIT                    = (  8,  1, FieldType.BCS_A,               None, 'Unit of Row Ground Sample Distance' )
    COL_GSD                         = (  9,  7, FieldType.BCS_NP,              None, 'Column Ground Sample Distance' )
    COL_GSD_UNIT                    = ( 10,  1, FieldType.BCS_A,               None, 'Unit of Column Ground Sample Distance' )
    SPT_RESP_ROW                    = ( 11,  7, FieldType.BCS_NP,              None, 'Spatial Response Function Across Rows' )
    SPT_RESP_UNIT_ROW               = ( 12,  1, FieldType.BCS_A,               None, 'Unit of Row Spatial Response' )
    SPT_RESP_COL                    = ( 13,  7, FieldType.BCS_NP,              None, 'Spatial Response Function Across Columns' )
    SPT_RESP_UNIT_COL               = ( 14,  1, FieldType.BCS_A,               None, 'Unit of Column Spatial Response' )
    DATA_FLD_1                      = ( 15, 48, FieldType.ECS_A,               None, 'Reserved for future use'  )
    EXISTENCE_MASK                  = ( 16,  4, FieldType.UINT32,              None, 'Bitwise Existing Mask Field' )
    RADIOMETRIC_ADJUSTMENT_SURFACE  = ( 17, 24, FieldType.BCS_A,               31, 'Adjustment Surface Details' )
    ATMOSPHERIC_ADJUSTMENT_ALTITUDE = ( 18,  4, FieldType.IEEE_754_FLOAT,      31, 'Adjustment Altitude Above WGS-84 Ellipsoid' )
    DIAMETER                        = ( 19,  7, FieldType.BCS_NP,              30, 'Diameter of the Lens' )
    DATA_FLD_2                      = ( 20,  4, FieldType.BCS_A,               29, 'Reserved for Future Use' )
    WAVE_LENGTH_UNIT                = ( 21,  1, FieldType.BCS_A,               None, 'Wavelength Unit' )
    BANDID_N                        = ( 22, 50, FieldType.BCS_A,               28, 'Band N Identifier' )
    BAD_BAND_N                      = ( 23,  1, FieldType.BCS_NP,              27, 'Bad Band Flag' )
    NIIRS_N                         = ( 24,  3, FieldType.BCS_NP,              26, 'NIIRS Score / Value' )
    FOCAL_LEN_N                     = ( 25,  5, FieldType.BCS_NP,              25, 'Band N Focal Length' )
    CWAVE_N                         = ( 26,  7, FieldType.BCS_NP,              24, 'Band N Center Response Wavelength' )
    FWHM_N                          = ( 27,  7, FieldType.BCS_NP,              23, 'Band N Width' )
    FWHM_UNC_N                      = ( 28,  7, FieldType.BCS_NP,              22, 'Band N Uncertainty' )
    NOM_WAVE_N                      = ( 29,  7, FieldType.BCS_NP,              21, 'Band N Nominal Wavelength' )
    NOM_WAV_UNC_N                   = ( 30,  7, FieldType.BCS_NP,              20, 'Band N Wavelength Uncertainty Measure' )
    LBOUND_N                        = ( 31,  7, FieldType.BCS_NP,              19, 'Band N Lower Wavelength Bound' )
    UBOUND_N                        = ( 32,  7, FieldType.BCS_NP,              19, 'Band N Upper Wavelength Bound' )
    SCALE_FACTOR_N                  = ( 33,  4, FieldType.IEEE_754_FLOAT,      18, 'Band N Individual Scale Factor' )
    ADDITIVE_FACTOR_N               = ( 34,  4, FieldType.IEEE_754_FLOAT,      18, 'Band N Individual Additive Factor' )
    START_TIME_N                    = ( 35, 16, FieldType.BCS_NP,              17, 'Band N Start Time' )
    INT_TIME_N                      = ( 36,  6, FieldType.BCS_NP,              16, 'Band N Integration Time' )
    CALDRK_N                        = ( 37,  6, FieldType.BCS_NP,              15, 'Band N Calibration (Dark)' )
    CALIBRATION_SENSITIVITY_N       = ( 38,  5, FieldType.BCS_NP,              15, 'Band N Calibration (Increment)' )
    ROW_GSD_N                       = ( 39,  7, FieldType.BCS_NP,              14, 'Band N Spatial Response Interval By Row' )
    ROW_GSD_UNC_N                   = ( 40,  7, FieldType.BCS_NP,              13, 'Band N Spatial Response Interval Uncertainty Row' )
    ROW_GSD_UNIT_N                  = ( 41,  1, FieldType.BCS_A,               14, 'Band N Unit of Row Spacing' )
    COL_GSD_N                       = ( 42,  7, FieldType.BCS_NP,              14, 'Band N Spatial Response Interval By Column' )
    COL_GSD_UNC_N                   = ( 43,  7, FieldType.BCS_NP,              13, 'Band N Spatial Response Interval Uncertainty Column' )
    COL_GSD_UNIT_N                  = ( 44,  1, FieldType.BCS_A,               14, 'Band N Unit of Column Spacing' )
    BKNOISE_N                       = ( 45,  5, FieldType.BCS_NP,              12, 'Band N Background Noise' )
    SCNNOISE_N                      = ( 46,  5, FieldType.BCS_NP,              12, 'Band N Scene Noise' )
    SPT_RESP_FUNCTION_ROW_N         = ( 47,  7, FieldType.BCS_NP,              11, 'Band N Spatial Response Function Across Rows' )
    SPT_RESP_UNC_ROW_N              = ( 48,  7, FieldType.BCS_NP,              10, 'Band N Spatial Response Function Uncertainty' )
    SPT_RESP_UNIT_ROW_N             = ( 49,  1, FieldType.BCS_A,               11, 'Band N Unit of Row Spatial Response' )
    SPT_RESP_FUNCTION_COL_N         = ( 50,  7, FieldType.BCS_NP,              11, 'Band N Spatial Response Function Across Columns' )
    SPT_RESP_UNC_COL_N              = ( 51,  7, FieldType.BCS_A,               10, 'Band N Spatial Response Function Uncertainty' )
    SPT_RESP_UNIT_COL_N             = ( 52,  1, FieldType.BCS_A,               11, 'Band N Unit of Column Spatial Response' )
    DATA_FLD_3_N                    = ( 53,  2, FieldType.ECS_A,                9, 'Reserved for Future Use' )
    DATA_FLD_4_N                    = ( 54,  3, FieldType.ECS_A,                8, 'Reserved for Future Use' )
    DATA_FLD_5_N                    = ( 55,  4, FieldType.ECS_A,                7, 'Reserved for Future Use' )
    DATA_FLD_6_N                    = ( 56,  6, FieldType.ECS_A,                6, 'Reserved for Future Use' )
    NUM_AUX_B                       = ( 57,  2, FieldType.BCS_NP,               0, 'Number of Auxiliary Band Level Parameters (m)' )
    NUM_AUX_C                       = ( 58,  2, FieldType.BCS_NP,               0, 'Number of Auxiliary Cube Level Parameters (k)' )
    BAPF_M                          = ( 59,  1, FieldType.BCS_A,               None, 'Band Auxilliary Parameter Value Format' )
    UBAP_M                          = ( 60,  7, FieldType.BCS_A,               None, 'Unit of Band Auxilliarly Parameter' )
    APN_M_N                         = ( 61, 10, FieldType.BCS_N,               None, 'Auxiliary Parameter Integer Value' )
    APR_M_N                         = ( 62,  4, FieldType.IEEE_754_FLOAT,      None, 'Auxiliary Parameter Real Value' )
    APA_M_N                         = ( 63, 20, FieldType.BCS_A,               None, 'Auxiliary Parameter Character String Value' )
    CAPF_K                          = ( 64,  1, FieldType.BCS_A,               None, 'Cube Auxiliarly Parameter Value Format' )
    UCAP_K                          = ( 65,  7, FieldType.BCS_A,               None, 'Unit of Cube Auxiliary Parameter' )
    APN_K                           = ( 66, 10, FieldType.BCS_N,               None, 'Auxiliary Parameter Integer Value' )
    APR_K                           = ( 67,  4, FieldType.IEEE_754_FLOAT,      None, 'Auxiliary Parameter Real Value' )
    APA_K                           = ( 68, 20, FieldType.BCS_A,               None, 'Auxiliary Parameter Character String Value' )



    @staticmethod
    def initial_list( skip_cetag, skip_cel ):
        
        res = []
        if not skip_cetag:
            res.append( Field.CETAG )
        if not skip_cel:
            res.append( Field.CEL )

        res += [ Field.COUNT,             Field.RADIOMETRIC_QUANTITY,  Field.RADIOMETRIC_QUANTITY_UNIT,
                 Field.SCALE_FACTOR,      Field.ADDITIVE_FACTOR,       Field.ROW_GSD,
                 Field.ROW_GSD_UNIT,      Field.COL_GSD,               Field.COL_GSD_UNIT,
                 Field.SPT_RESP_ROW,      Field.SPT_RESP_UNIT_ROW,     Field.SPT_RESP_COL,
                 Field.SPT_RESP_UNIT_COL, Field.DATA_FLD_1,            Field.EXISTENCE_MASK,
                 Field.RADIOMETRIC_ADJUSTMENT_SURFACE, Field.ATMOSPHERIC_ADJUSTMENT_ALTITUDE,
                 Field.DIAMETER,          Field.DATA_FLD_2,            Field.WAVE_LENGTH_UNIT ]
        return res
    
    @staticmethod
    def band_list():
        return [ Field.BANDID_N,                  Field.BAD_BAND_N,
                 Field.NIIRS_N,                   Field.FOCAL_LEN_N,
                 Field.CWAVE_N,                   Field.FWHM_N,
                 Field.FWHM_UNC_N,                Field.NOM_WAVE_N,
                 Field.NOM_WAV_UNC_N,             Field.LBOUND_N,
                 Field.UBOUND_N,                  Field.SCALE_FACTOR_N,
                 Field.ADDITIVE_FACTOR_N,         Field.START_TIME_N,
                 Field.INT_TIME_N,                Field.CALDRK_N,
                 Field.CALIBRATION_SENSITIVITY_N, Field.ROW_GSD_N,
                 Field.ROW_GSD_UNC_N,             Field.ROW_GSD_UNIT_N,
                 Field.COL_GSD_N,                 Field.COL_GSD_UNC_N,
                 Field.COL_GSD_UNIT_N,            Field.BKNOISE_N,
                 Field.SCNNOISE_N,                Field.SPT_RESP_FUNCTION_ROW_N,
                 Field.SPT_RESP_UNC_ROW_N,        Field.SPT_RESP_UNIT_ROW_N,
                 Field.SPT_RESP_FUNCTION_COL_N,   Field.SPT_RESP_UNC_COL_N,
                 Field.SPT_RESP_UNIT_COL_N,       Field.DATA_FLD_3_N,
                 Field.DATA_FLD_4_N,              Field.DATA_FLD_5_N,
                 Field.DATA_FLD_6_N ]



class BANDSB( TRE_Base ):

    def __init__( self, data ):
        self.data = data

    def __str__(self):
        return self.to_log_string()
    
    def to_log_string( self, offset = 0 ):
        
        gap = ' ' * offset
        output  = f'{gap}BANDSB:\n'
        for field in self.data.keys():
            val = None
            try:
                val = self.data[field]["data"].value()
            except:
                val = f'{self.data[field]["data"].data.decode('utf8')}'

            output += f'{gap}   Pos {field}, Name: {self.data[field]["name"]}, Value: [{val}]\n' 
        return output

    def is_valid( cetag, cel, cedata ):

        if cetag.decode('utf8').strip() == 'BANDSB':
            return True
        return False

    def build( cetag, cel, cedata ):

        data = {}
        counter = 0

        #  CETAG
        cetag_val, _ = TRE_Base.parse_field( cetag, Field.CETAG )
        data[counter] = cetag_val
        counter += 1

        #  CEL
        cel_val, _ = TRE_Base.parse_field( cel, Field.CEL )
        data[counter] = cel_val
        counter += 1

        #  The existance mask will play a big role later
        exist_mask = BitSet( num_bits = 32 )

        #  Start the the non-band-specific attributes
        count_val = None
        field_list = Field.initial_list( True, True )

        for field in field_list:

            #  Check if we have a spot in the existance mask
            skip_field = False
            if field.value[3] != None:

                mask_val = field.value[3]
                if not exist_mask.get(mask_val):
                    skip_field = True

            #  Parse the field if there is nothing stopping us
            if not skip_field:
                new_value, cedata = TRE_Base.parse_field( cedata, field )
                data[counter] = new_value
                counter += 1

                if field == Field.COUNT:
                    count_val = new_value['data'].value()

                elif field == Field.EXISTENCE_MASK:
                    emask = struct.unpack( "<I", struct.pack( ">I", new_value['data'].value() ))[0]
                    exist_mask.update_bitset( emask )
                    #print( f'Existance Mask:\n{exist_mask.to_log_string()}' )


        #  Process each "count"
        for N in range( count_val ):

            field_list = Field.band_list()

            for field in field_list:

                #  Check if we have a spot in the existance mask
                skip_field = False
                if field.value[3] != None:

                    mask_val = field.value[3]
                    if not exist_mask.get(mask_val):
                        skip_field = True

                if not skip_field:
                    new_value, cedata = TRE_Base.parse_field( cedata, field )
                    data[counter] = new_value
                    counter += 1

        #  NUM_AUX_B
        if exist_mask.get( Field.NUM_AUX_B.value[3] ):
            num_aux_b, cedata = TRE_Base.parse_field( cedata, Field.NUM_AUX_B )
            data[counter] = num_aux_b
            counter += 1

        #  NUM_AUX_B
        if exist_mask.get( Field.NUM_AUX_C.value[3] ):
            num_aux_c, cedata = TRE_Base.parse_field( cedata, Field.NUM_AUX_C )
            data[counter] = num_aux_b
            counter += 1

        return BANDSB( data )

