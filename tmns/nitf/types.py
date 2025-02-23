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

class FieldType(Enum):

    BCS_A          = 0
    BCS_N          = 1
    BCS_NP         = 2
    ECS_A          = 3
    UnsignedBinary = 4
    TRE            = 5

    def __repr__(self):
        return self.name

    @staticmethod
    def to_type( tp ):

        #  Basic Character Set, Alphanumeric
        if tp == FieldType.BCS_A:
            return BCS_A
        
        #  Basic Character Set, Numeric
        if tp == FieldType.BCS_N:
            return BCS_N
        
        #  Basic Character Set, Numeric
        if tp == FieldType.BCS_NP:
            return BCS_NP
        
        #  Extended Character Set, Alphanumeric
        if tp == FieldType.ECS_A:
            return ECS_A
        
        # Unsigned Binary
        if tp == FieldType.UnsignedBinary:
            return UnsignedBinary
        
        #  TRE Type
        if tp == FieldType.TRE:
            return TRE


class NITF_Character_Set:

    def value(self):
        raise NotImplementedError( f'Not implemented for base type. {self}' )
    
class BCS_A(NITF_Character_Set):

    def __init__( self, data: bytes, field_size ):
        
        #  Internal data
        self.data = data
        self.field_size = field_size
    
    def __str__(self):
        
        output = self.data.decode("utf8")
        if len(output) != self.field_size:
            output += ' ' * (self.field_size - len(output))
        return output

    def __repr__(self):
        return f'BCS_A, Data: [{str(self)}]'
    
    def value(self):
        return self.data.decode('utf8')

class BCS_N(NITF_Character_Set):

    def __init__( self, data: bytes, field_size ):
        
        #  Internal data
        self.data = data
        self.field_size = field_size
    
    def __str__(self):
        
        output = self.data.decode("utf8")
        if len(output) != self.field_size:
            output += ' ' * (self.field_size - len(output))
        return output

    def __repr__(self):
        return f'BCS_N, Data: {str(self)}'

    def value(self):
        return int(self.data.decode('utf8'))
    
class BCS_NP(NITF_Character_Set):

    def __init__( self, data: bytes, field_size ):
        
        #  Internal data
        self.data = data
        self.field_size = field_size
    
    def __str__(self):
        
        output = self.data.decode("utf8")
        if len(output) != self.field_size:
            output += ' ' * (self.field_size - len(output))
        return output

    def __repr__(self):
        return f'BCS_NP, Data: [{str(self)}]'
    
    def value(self):
        return int(self.data)
    
class ECS_A(NITF_Character_Set):

    def __init__( self, data: bytes, field_size ):
        
        #  Internal data
        self.data = data
        self.field_size = field_size
    
    def __str__(self):
        
        output = self.data.decode("utf8")
        if len(output) != self.field_size:
            output += ' ' * (self.field_size - len(output))
        return output

    def __repr__(self):
        return f'ECS_A, Data: [{str(self)}]'
    
    def value(self):
        return self.data.decode('utf8')
    
    
class UnsignedBinary(NITF_Character_Set):

    def __init__( self, data: bytes, field_size ):
        
        #  Internal data
        self.data = data
        self.field_size = field_size
    
    def __str__(self):
        
        output = self.data.decode("utf8")
        if len(output) != self.field_size:
            output += ' ' * (self.field_size - len(output))
        return output

    def __repr__(self):
        return f'ECS_A, Data: {str(self)}'
    
    def value(self):
        return self.data
    
class TRE(NITF_Character_Set):

    def __init__( self, data: bytes, field_size ):
        
        #  Internal data
        self.data = data
        self.field_size = field_size
    
    def __str__(self):
        
        output = self.data.decode("utf8")
        if len(output) != self.field_size:
            output += ' ' * (self.field_size - len(output))
        return output

    def __repr__(self):
        return f'TRE, Data: {str(self)}'
    
    def value(self):
        return self.data