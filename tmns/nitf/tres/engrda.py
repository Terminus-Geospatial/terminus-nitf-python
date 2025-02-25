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
from tmns.nitf.tre         import TRE_Base
from tmns.nitf.field_types import FieldType

class Field(Enum):
    CETAG     = (  0,  6, FieldType.BCS_A,  '    ENGRDA',  'Unique Extension Type Identifier' )
    CEL       = (  1,  5, FieldType.BCS_NP,         None,  'TRE Length' )
    RESRC     = (  2, 20, FieldType.BCS_A,          None,  'Unique Source System Name' )
    RECNT     = (  3,  3, FieldType.BCS_NP,         None,  'Record Entry Count' )
    ENGLN_N   = (  4,  2, FieldType.BCS_NP,         None,  'Engineering Data Label Length' )
    ENGLBL_N  = (  5,  0, FieldType.BCS_A,          None,  'Engineering Data Label' )
    ENGMTXC_N = (  6,  4, FieldType.BCS_NP,         None,  'Engineering Matrix Data Column Count' )
    ENGMTXR_N = (  7,  4, FieldType.BCS_NP,         None,  'Engineering Matrix Data Row Count' )
    ENGTYP_N  = (  8,  1, FieldType.BCS_A,          None,  'Value Type of Engineering Data Element' )
    ENGDTS_N  = (  9,  1, FieldType.BCS_N,          None,  'Engineering Data Element Size' )
    ENGDATU_N = ( 10,  2, FieldType.BCS_A,          None,  'Engineering Data Units' )
    ENGDATC_N = ( 11,  8, FieldType.BCS_NP,         None,  'Engineering Data Count' )
    ENGDATA_N = ( 12,  0, FieldType.UnsignedBinary, None,  'Engineering Data' )

    @staticmethod
    def default_list( skip_cetag = False, skip_cel = False ):
        res = []
        if not skip_cetag:
            res.append( Field.CETAG )
        if not skip_cel:
            res.append( Field.CEL )

        res += [ Field.RESRC,      Field.RECNT ]
        return res
    
    @staticmethod
    def per_element_list():

        res = [ Field.ENGLN_N,    Field.ENGLBL_N,   
                Field.ENGMTXC_N,  Field.ENGMTXR_N,
                Field.ENGTYP_N,   Field.ENGDTS_N,
                Field.ENGDATU_N,  Field.ENGDATC_N ]
        return res


class ENGRDA( TRE_Base ):

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
            data[self.data[k]['field'].name] = str(self.data[k]['data'].data)
        return data
    
    def to_log_string( self, offset = 0 ):
        
        gap = ' ' * offset
        output  = f'{gap}ENGRDA:\n'
        for field in self.data.keys():
            output += f'{gap}   Pos {field}, Name: {self.data[field]["name"]}, Value: [{self.data[field]["data"].value()}]\n' 
        return output

    def is_valid( cetag, cel, cedata ):

        if cetag.decode('utf8') == 'ENGRDA':
            return True
        
        #  TODO:  Remove Me!
        if cetag.decode('utf8') == 'ENGDRA':
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

        vals = { Field.ENGMTXC_N: 0,
                 Field.ENGMTXR_N: 0,
                 Field.ENGDTS_N:  0,
                 Field.ENGDATC_N: 0 }

        #  Parse Rest of Fields
        while len(field_list) > 0:

            field = field_list.popleft()
            #print( f'Processing Field: {field.name}' )
            
            #  Get the code length
            act_len = None
            if field.value[1] == 0:
                act_len = data[counter-1]['data'].value()

            value, cedata = TRE_Base.parse_field( cedata, field, override_length = act_len )
            data[counter] = value
            counter += 1

            #  If we finished the number of records, then add each entry's set of records
            if field == Field.RECNT:

                num_entries = value['data'].value()
                for idx in range( num_entries ):
                    field_list += Field.per_element_list()

            #  If field is in the dictionary, set value
            vals[field] = value['data'].value()
            
            if field == Field.ENGDATC_N:

                num_elements = vals[Field.ENGDTS_N]

                total = vals[Field.ENGMTXC_N] * vals[Field.ENGMTXR_N]
                for id in range( total ):
                    value, cedata = TRE_Base.parse_field( cedata, Field.ENGDATA_N, override_length = num_elements )
                    data[counter] = value
                    counter += 1


        return ENGRDA( data )
    