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

#  Terminus Libraries
from tmns.nitf.tre   import TRE_Base
from tmns.nitf.field_types import FieldType

class Field(Enum):
    CETAG                    = (  0,  6, FieldType.BCS_A,   'CAMSDA', 'Unique Extension Type Identifier' )
    CEL                      = (  1,  5, FieldType.BCS_NP,      None, 'TRE Length' )
    NUM_CAMERA_SETS          = (  2,  3, FieldType.BCS_NP,      None, 'Number of camera sets in collection' )
    NUM_CAMERA_SETS_IN_TRE   = (  3,  3, FieldType.BCS_NP,      None, 'Number of camera sets in the CAMSDA TRE' )
    FIRST_CAMERA_SET_IN_TRE  = (  4,  3, FieldType.BCS_NP,      None, 'Index of first camera set' )
    NUM_CAMERAS_IN_SET_N     = (  5,  3, FieldType.BCS_NP,      None, 'Number of cameras in Nth camera set M.' )
    CAMERA_ID_N_M            = (  6, 36, FieldType.BCS_A,       None, 'The UUID of the Mth camera in the Nth set.' )
    CAMERA_DESC_N_M          = (  7, 80, FieldType.BCS_A,       None, 'Description of the camera' )
    LAYER_ID_N_M             = (  8, 36, FieldType.BCS_A,       None, 'Phenomenological layer for Mth camera in Nth set.' )
    IDLVL_N_M                = (  9,  3, FieldType.BCS_NP,      None, 'Image display level for Mth camera in Nth camera set.' )
    IALVL_N_M                = ( 10,  3, FieldType.BCS_NP,      None, 'Image attachment level for Mth camera set in Nth camera set.' )
    ILOC_N_M                 = ( 11, 10, FieldType.BCS_NP,      None, 'Image location' )
    NROWS_N_M                = ( 12,  8, FieldType.BCS_NP,      None, 'Number of image rows' )
    NCOLS_N_M                = ( 13,  8, FieldType.BCS_NP,      None, 'Number of image cols' )
    

    @staticmethod
    def default_list( skip_cetag, skip_cel ):
        
        res = []
        if not skip_cetag:
            res.append( Field.CETAG )
        if not skip_cel:
            res.append( Field.CEL )

        res += [ Field.NUM_CAMERA_SETS,
                 Field.NUM_CAMERA_SETS_IN_TRE,
                 Field.FIRST_CAMERA_SET_IN_TRE ]
        return res
    
class CAMSDA( TRE_Base ):

    def __init__( self, data ):
        self.data = data

    def __str__(self):
        return self.to_log_string()
    
    def get( self, field, index = 0 ):

        counter = 0
        for k in self.data.keys():
            if self.data[k]['field'] == field:
                if counter == index:
                    return self.data[k]
                else:
                    counter += 1
        return None
    
    def cetag(self):
        return self.get( Field.CETAG )['data'].value()
    
    def as_kvp(self):

        data = {}
        for k in self.data.keys():
            data[self.data[k]['field'].name] = str(self.data[k]['data'])
        return data
    
    def to_log_string( self, offset = 0 ):
        
        gap = ' ' * offset
        output  = f'{gap}CAMSDA:\n'
        for field in self.data.keys():
            val = None
            try:
                val = self.data[field]["data"].value()
            except:
                val = f'{self.data[field]["data"].data.decode('utf8')}'

            output += f'{gap}   Pos {field}, Name: {self.data[field]["name"]}, Value: [{val}]\n' 
        return output

    def is_valid( cetag, cel, cedata ):

        if cetag.decode('utf8').strip() == 'CAMSDA':
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

        field_list = Field.default_list( True, True )

        for field in field_list:

            new_value, cedata = TRE_Base.parse_field( cedata, field )
            data[counter] = new_value
            counter += 1

        # 

        return CAMSDA( data )