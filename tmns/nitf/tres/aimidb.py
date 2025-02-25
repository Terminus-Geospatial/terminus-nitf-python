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
    CETAG                  = (  0,  6, FieldType.BCS_A,   'AIMIDB', 'Unique Extension Type Identifier' )
    CEL                    = (  1,  5, FieldType.BCS_NP,      None, 'TRE Length' )
    ACQUISITION_DATE       = (  2, 14, FieldType.BCS_NP,      None, 'Acquisition Date and Time' )
    MISSION_NO             = (  3,  4, FieldType.BCS_A,       None, 'Mission Number' )
    MISSION_IDENTIFICATION = (  4, 10, FieldType.BCS_A,       None, 'Name of the Mission' )
    FLIGHT_NO              = (  5,  2, FieldType.BCS_N,       None, 'Flight Number' )
    OP_NUM                 = (  6,  3, FieldType.BCS_NP,      None, 'Image Operation Number' )
    CURRENT_SEGMENT        = (  7,  2, FieldType.BCS_A,       None, 'Current Segment ID' )
    REPRO_NUM              = (  8,  2, FieldType.BCS_NP,      None, 'Reprocess Number' )
    REPLAY                 = (  9,  3, FieldType.BCS_A,       None, 'Replay' )
    RESERVED_1             = ( 10,  1, FieldType.BCS_A,       None, 'Reserved' )
    START_TILE_COLUMN      = ( 11,  3, FieldType.BCS_NP,      None, 'Starting Tile Column Number' )
    START_TILE_ROW         = ( 12,  5, FieldType.BCS_NP,      None, 'Starting Tile Row Number' )
    END_SEGMENT            = ( 13,  2, FieldType.BCS_A,       None, 'Ending Segment' )
    END_TILE_COLUMN        = ( 14,  3, FieldType.BCS_NP,      None, 'Ending Tile Column Number' )
    END_TILE_ROW           = ( 15,  5, FieldType.BCS_NP,      None, 'Ending Tile Row Number' )
    COUNTRY                = ( 16,  2, FieldType.BCS_A,       None, 'Country Code' )
    RESERVED_2             = ( 17,  4, FieldType.BCS_A,       None, 'Reserved' )
    LOCATION               = ( 18, 11, FieldType.BCS_A,       None, 'Location' )
    RESERVED_3             = ( 19, 13, FieldType.BCS_A,       None, 'Reserved' )

    @staticmethod
    def default_list( skip_cetag, skip_cel ):
        
        res = []
        if not skip_cetag:
            res.append( Field.CETAG )
        if not skip_cel:
            res.append( Field.CEL )

        res += [ Field.ACQUISITION_DATE,  Field.MISSION_NO,     Field.MISSION_IDENTIFICATION,
                 Field.FLIGHT_NO,         Field.OP_NUM,         Field.CURRENT_SEGMENT,
                 Field.REPRO_NUM,         Field.REPLAY,         Field.RESERVED_1,
                 Field.START_TILE_COLUMN, Field.START_TILE_ROW, Field.END_SEGMENT,
                 Field.END_TILE_COLUMN,   Field.END_TILE_ROW,   Field.COUNTRY,
                 Field.RESERVED_2,        Field.LOCATION,       Field.RESERVED_3 ]
        return res
    
class AIMIDB( TRE_Base ):

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
        output  = f'{gap}AIMIDB:\n'
        for field in self.data.keys():
            val = None
            try:
                val = self.data[field]["data"].value()
            except:
                val = f'{self.data[field]["data"].data.decode('utf8')}'

            output += f'{gap}   Pos {field}, Name: {self.data[field]["name"]}, Value: [{val}]\n' 
        return output

    def is_valid( cetag, cel, cedata ):

        if cetag.decode('utf8').strip() == 'AIMIDB':
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

        return AIMIDB( data )