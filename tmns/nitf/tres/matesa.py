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
    CETAG           = (  0,  6, FieldType.BCS_A,  'CSDIDA',  True, 'Unique Extension Type Identifier' )
    CEL             = (  1,  5, FieldType.BCS_NP,     None,  True, 'TRE Length' )
    CUR_SOURCE      = (  2, 42, FieldType.ECS_A,      None,  True, 'Current File / Segment Source' )
    CUR_MATE_TYPE   = (  3, 16, FieldType.ECS_A,      None,  True, 'Current File / Segment Type' )
    CUR_FILE_ID_LEN = (  4,  4, FieldType.BCS_NP,     None,  True, 'Length of the CUR_FILE_ID field' )
    CUR_FILE_ID     = (  5,  0, FieldType.ECS_A,      None,  True, 'ID of the Current File / Segment' )
    NUM_GROUPS      = (  6,  4, FieldType.BCS_NP,     None,  True, 'Number of Mate Relationship Groups' )
    RELATIONSHIP_N  = (  7, 24, FieldType.ECS_A,      None,  True, 'Mate Relationship' )
    NUM_MATES_N     = (  8,  4, FieldType.BCS_NP,     None,  True, 'Number of Mates in the Nth Group' )
    SOURCE_N_M      = (  9, 42, FieldType.ECS_A,      None,  True, 'Mate Source' )
    MATE_TYPE_N_M   = ( 10, 16, FieldType.ECS_A,      None,  True, 'Mate Identifier Type' )
    MATE_ID_LEN_N   = ( 11,  4, FieldType.BCS_NP,     None,  True, 'Length of the Mth Mate ID nm Field' )
    MATE_ID_N_M     = ( 12,  0, FieldType.ECS_A,      None,  True, 'Mate File Identifier' )


    @staticmethod
    def default_list( skip_cetag = False, skip_cel = False ):
        res = []
        if not skip_cetag:
            res.append( Field.CETAG )
        if not skip_cel:
            res.append( Field.CEL )

        res += [ Field.CUR_SOURCE,    Field.CUR_MATE_TYPE, Field.CUR_FILE_ID_LEN,
                 Field.CUR_FILE_ID,   Field.NUM_GROUPS ]
        return res
    
    
class MATESA( TRE_Base ):

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
        output  = f'{gap}MATESA:\n'
        for field in self.data.keys():
            output += f'{gap}   Pos {field}, Name: {self.data[field]["name"]}, Value: [{self.data[field]["data"].value()}]\n' 
        return output

    def is_valid( cetag, cel, cedata ):

        if cetag.decode('utf8') == 'MATESA':
            return True
        return False

    def build( cetag, cel, cedata ):

        field_list = deque(Field.default_list( True, True ))
        
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
        while len(field_list) > 0:

            field = field_list.popleft()
            
            #  Get the code length
            act_len = None
            if field.value[1] == 0:
                act_len = data[counter-1]['data'].value()

            value, cedata = TRE_Base.parse_field( cedata, field, override_length = act_len )
            data[counter] = value
            counter += 1

            #  If we finished the NUMGROUPS, then add blocks for each entry
            if field == Field.NUM_GROUPS:

                num_groups = value['data'].value()
                for idx in range( num_groups ):

                    field_list.append( Field.RELATIONSHIP_N )
                    field_list.append( Field.NUM_MATES_N )
            
            if field == Field.NUM_MATES_N:

                num_mates = value['data'].value()
                for idx in range( num_mates ):
                    field_list.appendleft( Field.MATE_ID_N_M )
                    field_list.appendleft( Field.MATE_ID_LEN_N )
                    field_list.appendleft( Field.MATE_TYPE_N_M )
                    field_list.appendleft( Field.SOURCE_N_M )
                    
        return MATESA( data )