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
from enum import Enum

#  Terminus Libraries
from tmns.nitf.tre   import TRE_Base
from tmns.nitf.field_types import FieldType

class Field(Enum):
    CETAG                   = (  0,  6, FieldType.BCS_A,  'CSDIDA',  True, 'Unique Extension Type Identifier' )
    CEL                     = (  1,  5, FieldType.BCS_NP,     None,  True, 'TRE Length' )
    DAY                     = (  2,  2, FieldType.BCS_NP,     None,  True, 'Day of Dataset Collection' )
    MONTH                   = (  3,  3, FieldType.BCS_A,      None,  True, 'Month of Dataset Collection' )
    YEAR                    = (  4,  4, FieldType.BCS_NP,     None,  True, 'Year of Dataset Collection' )
    PLATFORM_CODE           = (  5,  2, FieldType.BCS_A,      None,  True, 'Platform Identification' )
    VEHICLE_ID              = (  6,  2, FieldType.BCS_A,      None,  True, 'Vehicle Number' )
    PASS                    = (  7,  2, FieldType.BCS_NP,     None,  True, 'Pass Number' )
    OPERATION               = (  8,  3, FieldType.BCS_NP,     None,  True, 'Operation Number' )
    SENSOR_ID               = (  9,  2, FieldType.BCS_A,      None,  True, 'Sensor ID' )
    PRODUCT_ID              = ( 10,  2, FieldType.BCS_A,      None,  True, 'Product ID' )
    RESERVED_1              = ( 11,  4, FieldType.BCS_A,      None,  True, 'Fill value for future use' )
    TIME                    = ( 12, 14, FieldType.BCS_NP,     None,  True, 'Image Start Time' )
    PROCESS_TIME            = ( 13, 14, FieldType.BCS_NP,     None,  True, 'Process Completion Time' )
    RESERVED_2              = ( 14,  2, FieldType.BCS_NP,        0,  True, 'Fill value 2' )
    RESERVED_3              = ( 15,  2, FieldType.BCS_NP,        1,  True, 'Fill value 3' )
    RESERVED_4              = ( 16,  1, FieldType.BCS_A,       'N',  True, 'Fill value 4' )
    RESERVED_5              = ( 17,  1, FieldType.BCS_A,       'N',  True, 'Fill value 5' )
    SOFTWARE_VERSION_NUMBER = ( 18, 10, FieldType.BCS_A,  ' ' * 10,  True, 'Vendor Software Version Used' )

    @staticmethod
    def default_list( skip_cetag = False, skip_cel = False ):
        res = []
        if not skip_cetag:
            res.append( Field.CETAG )
        if not skip_cel:
            res.append( Field.CEL )

        res += [ Field.DAY,        Field.MONTH,      Field.YEAR,       Field.PLATFORM_CODE,
                 Field.VEHICLE_ID, Field.PASS,       Field.OPERATION,  Field.SENSOR_ID,
                 Field.PRODUCT_ID, Field.RESERVED_1, Field.TIME,       Field.PROCESS_TIME,
                 Field.RESERVED_2, Field.RESERVED_3, Field.RESERVED_4, Field.RESERVED_5,
                 Field.SOFTWARE_VERSION_NUMBER ]
        return res
    
    
class CSDIDA( TRE_Base ):

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
        output  = f'{gap}CSDIDA:\n'
        for field in self.data.keys():
            output += f'{gap}   Pos {field}, Name: {self.data[field]["name"]}, Value: {self.data[field]["data"].value()}\n' 
        return output

    def is_valid( cetag, cel, cedata ):

        if cetag.decode('utf8') == 'CSDIDA':
            return True
        return False

    def build( cetag, cel, cedata ):

        field_list = Field.default_list( True, True )
        
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

        #  Parse Rest of Fields
        for field in field_list:
            
            #  Get the code length
            value, cedata = TRE_Base.parse_field( cedata, field )
            data[counter] = value
            counter += 1

        return CSDIDA( data )