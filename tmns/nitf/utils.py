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

#  Pretty ASCII Table API
from prettytable import PrettyTable

class BitSet:

    def __init__( self, num_bits, initial_value: int = None ):

        self.value = 0
        self.bits  = [ False for x in range(num_bits) ]

        if initial_value != None:
            self.update_bitset( initial_value )

    def update_bitset( self, value: int ):

        # Iterate over value
        num_bits = value.bit_length()
        for x in range( num_bits ):
            flag = 1 << x
            result = flag & value > 0
            self.bits[x] = result

    def get( self, pos: int ):
        return self.bits[pos]
    
    def to_log_string( self, pretty = True ):

        if pretty:
            table = PrettyTable()
            table.field_names = [ f'{x}' for x in range( len(self.bits)-1, 0 ) ]
            
            for idx in range( 0, len( self.bits ) ):
                table.add_column( f'{idx}', [ self.bits[idx] ] )
            
            return f'{table.get_formatted_string()}'

        else:
            return f'{self.value}, Bits: {self.bits}'
        

