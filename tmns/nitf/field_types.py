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
import struct

class FieldType(Enum):

    BCS_A          = 0
    BCS_N          = 1
    BCS_NP         = 2
    ECS_A          = 3
    UINT32         = 4
    UnsignedBinary = 5
    IEEE_754_FLOAT = 6
    TRE            = 7

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
        
        # Unsigned Int32
        if tp == FieldType.UINT32:
            return UINT32
        
        # Unsigned Binary
        if tp == FieldType.UnsignedBinary:
            return UnsignedBinary
        
        # IEEE_754_FLOAT
        if tp == FieldType.IEEE_754_FLOAT:
            return IEEE_754_FLOAT
        
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
        
        output = ''
        try:
            output = self.data.decode("utf8")
            if len(output) != self.field_size:
                output += ' ' * (self.field_size - len(output))
        except:
            output = str(self.data)
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

class UINT32(NITF_Character_Set):

    def __init__( self, data: bytes, field_size ):
        
        #  Internal data
        self.data = data
        self.field_size = field_size
    
    def __str__(self):
        
        return str(self.data) #str(self.value())

    def __repr__(self):
        return f'UINT32, Data: {self.value()}, Len: {self.field_size}'
    
    def value(self):
        return struct.unpack( 'I', self.data )[0]
    
    
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
        return f'UnsignedBinary, Data: [{str(self.value())}], Len: {self.field_size}'
    
    def value(self):
        return self.data

class IEEE_754_FLOAT(NITF_Character_Set):

    def __init__( self, data: bytes, field_size ):

        #  Internal data
        self.data = data
        self.field_size = field_size
    
    def __str__(self):
        return str(self.value())

    def __repr__(self):
        return f'IEEE_754_FLOAT, Data: {str(self)}'
    
    def value(self):
        return struct.unpack( 'f', self.data )[0]


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