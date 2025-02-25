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
    CETAG         = (  0,  6, FieldType.BCS_A,   'CCINFA',  True, 'Unique Extension Type Identifier' )
    CEL           = (  1,  5, FieldType.BCS_NP,      None,  True, 'TRE Length' )
    NUMCODE       = (  2,  3, FieldType.BCS_NP,      None,  True, 'Number of defined codes' )
    CODE_LEN_N    = (  3,  1, FieldType.BCS_NP,      None, False, 'Length of CODE_N field' )
    CODE_N        = (  4,  0, FieldType.BCS_A,       None, False, 'Code' )
    EQTYPE_N      = (  5,  1, FieldType.BCS_A,       None, False, 'Type of Equivalence' )
    ESURN_LEN_N   = (  6,  2, FieldType.BCS_NP,      None, False, 'Length of ESUR_N field' )
    ESURN_N       = (  7,  0, FieldType.BCS_A,       None, False, 'Equivalent short URN-based Item Identifier' )
    DETAIL_LEN_N  = (  8,  5, FieldType.BCS_NP,      None, False, 'Length of Detail Field' )
    DETAIL_CMPR_N = (  9,  1, FieldType.BCS_A,       None, False, 'Code Detail Compression' )
    DETAIL_N      = ( 10,  0, FieldType.ECS_A,       None, False, 'Code Detail Information' )

    @staticmethod
    def default_list( skip_cetag = False, skip_cel = False ):
        res = []
        if not skip_cetag:
            res.append( Field.CETAG )
        if not skip_cel:
            res.append( Field.CEL )
        res.append( Field.NUMCODE )
        return res
    
class CCINFA( TRE_Base ):

    def __init__( self, data ):
        self.data = data

    def __str__(self):
        return self.to_log_string()
    
    def to_log_string( self,
                       offset = 0, 
                       filter_list = [ Field.CODE_LEN_N,
                                       Field.CODE_N,
                                       Field.EQTYPE_N,
                                       Field.ESURN_LEN_N,
                                       Field.ESURN_N,
                                       Field.DETAIL_LEN_N,
                                       Field.DETAIL_CMPR_N,
                                       Field.DETAIL_N ] ):
        
        gap = ' ' * offset
        output  = f'{gap}CCINFA:\n'
        for field in self.data.keys():
            if not self.data[field]['field'] in filter_list:
                output += f'{gap}   Pos {field}, Name: {self.data[field]["name"]}, Value: {self.data[field]["data"].value()}\n'
            
        return output

    def is_valid( cetag, cel, cedata ):

        if cetag.decode('utf8') == 'CCINFA':
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

        #  Number Code
        numcode, cedata = TRE_Base.parse_field( cedata, Field.NUMCODE )
        data[counter] = numcode
        counter += 1

        for idx in range( numcode['data'].value() ):
            
            #  Get the code length
            code_len, cedata = TRE_Base.parse_field( cedata, Field.CODE_LEN_N )
            data[counter] = code_len
            counter += 1

            #  Get the code value
            code_value, cedata = TRE_Base.parse_field( cedata, Field.CODE_N,
                                                       override_length = code_len['data'].value() )
            data[counter] = code_value
            counter += 1

            #  EQTYPE_N
            eqtype, cedata = TRE_Base.parse_field( cedata, Field.EQTYPE_N )
            data[counter] = eqtype
            counter += 1

            #  ESURN_LEN_N
            esurn_len, cedata = TRE_Base.parse_field( cedata, Field.ESURN_LEN_N )
            data[counter] = esurn_len
            counter += 1

            #  ESURN Value
            esurn_val, cedata = TRE_Base.parse_field( cedata, Field.ESURN_N,override_length = esurn_len['data'].value() )
            data[counter] = esurn_val
            counter += 1

            #  Detail Len 
            detail_len, cedata = TRE_Base.parse_field( cedata, Field.DETAIL_LEN_N )
            data[counter] = detail_len
            counter += 1

            #  Detail Compression
            if detail_len['data'].value() > 0:
                detail_comp, cedata = TRE_Base.parse_field( cedata, Field.DETAIL_CMPR_N )
                data[counter] = detail_comp
                counter += 1

                #  Detail Value
                detail_val, cedata = TRE_Base.parse_field( cedata, Field.DETAIL_N, override_length = detail_len['data'].value() )
                data[counter] = detail_val
                counter += 1

        return CCINFA( data )