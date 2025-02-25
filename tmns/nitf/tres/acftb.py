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
    CETAG             = (  0,  6, FieldType.BCS_A,         'ACFTB', 'Unique Extension Type Identifier' )
    CEL               = (  1,  5, FieldType.BCS_NP,           None, 'TRE Length' )
    AC_MSN_ID         = (  2, 20, FieldType.ECS_A, 'NOT AVAILABLE', 'Aicraft Mission Identification' )
    AC_TAIL_NO        = (  3, 10, FieldType.ECS_A,            None, 'Aircraft Tail Number' )
    AC_TO             = (  4, 12, FieldType.BCS_NP,           None, 'Aircraft Takeoff Time' )
    SENSOR_ID_TYPE    = (  5,  4, FieldType.BCS_A,            None, 'Sensor ID Type' )
    SENSOR_ID         = (  6,  6, FieldType.BCS_A,            None, 'Sensor Identification' )
    SCENE_SOURCE      = (  7,  1, FieldType.BCS_NP,           None, 'Scene Source' )
    SCNUM             = (  8,  6, FieldType.BCS_NP,           None, 'Scene Number' )
    PDATE             = (  9,  8, FieldType.BCS_NP,           None, 'Processing Date' )
    IMHOSTNO          = ( 10,  6, FieldType.BCS_NP,           None, 'Immediate Scene Host' )
    IMREQID           = ( 11,  5, FieldType.BCS_NP,           None, 'Immediate Scene Request ID' )
    MPLAN             = ( 12,  3, FieldType.BCS_NP,           None, 'Mission Plan Mode' )
    ENTLOC            = ( 13, 25, FieldType.BCS_A,            None, 'Entry Location' )
    LOC_ACCY          = ( 14,  6, FieldType.BCS_NP,           None, 'Location Accuracy' )
    ENTELV            = ( 15,  6, FieldType.BCS_N,            None, 'Entry Elevation' )
    ELV_UNIT          = ( 16,  1, FieldType.BCS_A,            None, 'Unit-of-Elevation' )
    EXITLOC           = ( 17, 25, FieldType.BCS_A,            None, 'Exit Location' )
    EXITELV           = ( 18,  6, FieldType.BCS_N,            None, 'Exit Elevation' )
    TMAP              = ( 19,  7, FieldType.BCS_N,            None, 'True Map Angle' )
    ROW_SPACING       = ( 20,  7, FieldType.BCS_NP,           None, 'Row Spacing' )
    ROW_SPACING_UNITS = ( 21,  1, FieldType.BCS_A,            None, 'Units of Row Spacing' )
    COL_SPACING       = ( 22,  7, FieldType.BCS_NP,           None, 'Column Spacing' )
    COL_SPACING_UNITS = ( 23,  1, FieldType.BCS_A,            None, 'Units of Column Spacing' )
    FOCAL_LENGTH      = ( 24,  6, FieldType.BCS_NP,           None, 'Focal Length' )
    SENSERIAL         = ( 25,  6, FieldType.BCS_A,            None, 'Sensor Vendor Serial Number' )
    ABSWVER           = ( 26,  7, FieldType.BCS_A,            None, 'Airborne Software Version' )
    CAL_DATE          = ( 27,  8, FieldType.BCS_NP,           None, 'Calibration Date' )
    PATCH_TOT         = ( 28,  4, FieldType.BCS_NP,           None, 'Patch Total' )
    MTI_TOT           = ( 29,  3, FieldType.BCS_NP,           None, 'MTI Total' )

    @staticmethod
    def default_list( skip_cetag, skip_cel ):
        
        res = []
        if not skip_cetag:
            res.append( Field.CETAG )
        if not skip_cel:
            res.append( Field.CEL )

        res += [ Field.AC_MSN_ID,
                 Field.AC_TAIL_NO,        Field.AC_TO,             Field.SENSOR_ID_TYPE,
                 Field.SENSOR_ID,         Field.SCENE_SOURCE,      Field.SCNUM,
                 Field.PDATE,             Field.IMHOSTNO,          Field.IMREQID,
                 Field.MPLAN,             Field.ENTLOC,            Field.LOC_ACCY,
                 Field.ENTELV,            Field.ELV_UNIT,          Field.EXITLOC,
                 Field.EXITELV,           Field.TMAP,              Field.ROW_SPACING,
                 Field.ROW_SPACING_UNITS, Field.COL_SPACING,       Field.COL_SPACING_UNITS,
                 Field.FOCAL_LENGTH,      Field.SENSERIAL,         Field.ABSWVER,
                 Field.CAL_DATE,          Field.PATCH_TOT,         Field.MTI_TOT ]
        return res
    
class ACFTB( TRE_Base ):

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
        output  = f'{gap}ACFTB:\n'
        for field in self.data.keys():
            val = None
            try:
                val = self.data[field]["data"].value()
            except:
                val = f'{self.data[field]["data"].data.decode('utf8')}'

            output += f'{gap}   Pos {field}, Name: {self.data[field]["name"]}, Value: [{val}]\n' 
        return output

    def is_valid( cetag, cel, cedata ):

        if cetag.decode('utf8').strip() == 'ACFTB':
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

        return ACFTB( data )