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
    CETAG                  = (  0,  6, FieldType.BCS_A,   'BLOCKA', 'Unique Extension Type Identifier' )
    CEL                    = (  1,  5, FieldType.BCS_NP,      None, 'TRE Length' )
    BLOCK_INSTANCE         = (  2,  2, FieldType.BCS_NP,      None, 'Block number of image block' )
    N_GRAY                 = (  3,  5, FieldType.BCS_NP,      None, 'Number of gray fill pixels' )
    L_LINES                = (  4,  5, FieldType.BCS_NP,      None, 'Row Count' )
    LAYOVER_ANGLE          = (  5,  3, FieldType.BCS_NP,      None, 'Layover Angle' )
    SHADOW_ANGLE           = (  6,  3, FieldType.BCS_NP,      None, 'Shadow Angle' )
    RESERVED_1             = (  7, 16, FieldType.BCS_A,       None, 'Reserved' )
    FRLC_LOC               = (  8, 21, FieldType.BCS_A,       None, 'First Row, Last Column Location' )
    LRLC_LOC               = (  9, 21, FieldType.BCS_A,       None, 'Last Row, Last Column Location' )
    LRFC_LOC               = ( 10, 21, FieldType.BCS_A,       None, 'Last Row, First Column Location' )
    FRFC_LOC               = ( 11, 21, FieldType.BCS_A,       None, 'First Row, First Column Location' )
    RESERVED_2             = ( 12,  5, FieldType.ECS_A,       None, 'Reserved for Future Use' )

    

    @staticmethod
    def default_list( skip_cetag, skip_cel ):
        
        res = []
        if not skip_cetag:
            res.append( Field.CETAG )
        if not skip_cel:
            res.append( Field.CEL )

        res += [ Field.BLOCK_INSTANCE,  Field.N_GRAY,       Field.L_LINES,
                 Field.LAYOVER_ANGLE,   Field.SHADOW_ANGLE, Field.RESERVED_1,
                 Field.FRLC_LOC,        Field.LRLC_LOC,     Field.LRFC_LOC,
                 Field.FRFC_LOC,        Field.RESERVED_2 ]
        return res
    
class BLOCKA( TRE_Base ):

    def __init__( self, data ):
        self.data = data

    def __str__(self):
        return self.to_log_string()
    
    def to_log_string( self, offset = 0 ):
        
        gap = ' ' * offset
        output  = f'{gap}BLOCKA:\n'
        for field in self.data.keys():
            val = None
            try:
                val = self.data[field]["data"].value()
            except:
                val = f'{self.data[field]["data"].data.decode('utf8')}'

            output += f'{gap}   Pos {field}, Name: {self.data[field]["name"]}, Value: [{val}]\n' 
        return output

    def is_valid( cetag, cel, cedata ):

        if cetag.decode('utf8').strip() == 'BLOCKA':
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

        return BLOCKA( data )