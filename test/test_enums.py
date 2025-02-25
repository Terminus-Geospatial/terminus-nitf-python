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
import unittest

#  Terminus Libraries
from tmns.nitf.enums import ImageCompression

class enums_ImageCompression(unittest.TestCase):

    def test_from_str(self):
        self.assertEqual( ImageCompression.from_str( 'C8' ), ImageCompression.C8 )
        self.assertEqual( ImageCompression.from_str( 'M8' ), ImageCompression.M8 )
