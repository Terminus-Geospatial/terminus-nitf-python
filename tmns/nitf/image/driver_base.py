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


class Driver_Base:

    def __init__(self):
        pass

    def encode( self, code, image ):
        raise NotImplementedError( 'Not implemented in base class' )
    
    def decode( self, code, buffer ):
        raise NotImplementedError( 'Not implemented in base class' )