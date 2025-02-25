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
import logging

#  Terminus Libraries
from tmns.nitf.field_types import FieldType

class Field(Enum):
    CETAG  = (  0,  6, FieldType.BCS_A,  None,  'Unique Extension Type Identifier' )
    CEL    = (  1,  5, FieldType.BCS_NP, None,  'Length of CEDATA Field' )
    CEDATA = (  2,  0, FieldType.UnsignedBinary, None, 'User-Defined Data' )

    @staticmethod
    def default_list():
        return [ Field.CETAG, Field.CEL, Field.CEDATA ]
    
                
class TRE_Base:

    def __init__( self, data ):
        self.data = data

    def __str__(self):
        '''
        Convert TRE to log-friendly string
        '''
        self.to_log_string()   

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
    
    def to_log_string(self, offset = 0):

        gap = ' ' * offset
        output  = f'{gap}TRE_Base:\n'
        for field in self.data.keys():
            output += f'{gap}   Pos {field}, Name: {self.data[field]["name"]}, Value: {self.data[field]["data"].value()}\n'
            
        return output

    @staticmethod
    def parse_field(  buffer, field, override_length = None ):
        
        field_length = field.value[1]
        field_type   = field.value[2]

        if override_length != None:
            field_length = override_length

        tp = FieldType.to_type( field_type )

        new_entry = { 'name':  field.name,
                      'field': field,
                      'type':  field_type,
                      'data':  tp(buffer[0:field_length], field_length) }
        
        return new_entry, buffer[field_length:]
    
    @staticmethod
    def is_valid( cetag, cel, cedata ):
        return True

    @staticmethod
    def build( cetag, cel, cedata ):
        
        data = {}

        #  Setup CETAG
        field_length = Field(Field.CETAG).value[1]
        field_type   = FieldType.to_type( Field(Field.CETAG).value[2] )
        data[0] = { 'name':  Field(Field.CETAG).name,
                    'field': Field.CETAG,
                    'type':  field_type,
                    'data':  field_type(cetag, field_length) }
        
        #  Setup CEL
        field_length = Field(Field.CEL).value[1]
        field_type   = FieldType.to_type( Field(Field.CEL).value[2] )
        data[1] = { 'name':  Field(Field.CEL).name,
                    'field': Field.CEL,
                    'type':  field_type,
                    'data':  field_type(cel, field_length) }
        
        #  Setup CETAG
        field_length = Field(Field.CEDATA).value[1]
        field_type = FieldType.to_type( Field(Field.CEDATA).value[2] )
        data[2] = { 'name':  Field(Field.CEDATA).name,
                    'field': Field.CEDATA,
                    'type':  field_type,
                    'data':  field_type(cedata, field_length) }

        return TRE_Base( data )

    @staticmethod
    def parse_binary( buffer, logger = None, factory = None ):

        if logger is None:
            logger = logging.getLogger( 'tmns.nitf.fhdr.FileHeader.parse_binary' )
        
        if factory is None:
            factory = TRE_Factory.default()

        tre_list = []

        #  Start iterating over the blocks
        idx = 0
        while idx < len(buffer):

            cetag = buffer[idx:(idx + Field.CETAG.value[1])]
            idx += Field.CETAG.value[1]

            cel   = buffer[idx:(idx + Field.CEL.value[1])]
            idx += Field.CEL.value[1]

            cel_value = int(cel.decode('utf8'))
            cedata = buffer[idx:(idx + cel_value)]
            idx += cel_value

            tre_list.append( factory.build( cetag  = cetag,
                                            cel    = cel,
                                            cedata = cedata ) )

        return tre_list