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
import logging
import unittest

#  Terminus Libraries
import tmns.nitf.utils as utils

class TEST_utils_BitSet(unittest.TestCase):

    def test_uint32_( self ):

        #  Create bitset for the BANDSB TRE Existance Flag
        bitset = utils.BitSet( num_bits=32, initial_value = 4720411 )

        print(bitset.to_log_string())

        bitset = utils.BitSet( num_bits=32, initial_value = 453462016 )

        print(bitset.to_log_string())
         
        
