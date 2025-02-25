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


#  Terminus Libraries
from tmns.nitf.enums import ImageCompression
from tmns.nitf.image.opj_driver import OPJ_Driver

class Driver_Factory:

    def __init__(self):
        
        self.decode_drivers = {}
        self.encode_drivers = {}

    
    def register_driver( self, code, decode_driver = None, encode_driver = None ):
        
        if decode_driver != None:
            self.decode_drivers[code] = decode_driver
        if encode_driver != None:
            self.encode_drivers[code] = encode_driver

    def decode( self, code, buffer ):

        return self.decode_drivers[code].decode( code, buffer )

    
    @staticmethod
    def default():

        factory = Driver_Factory()

        factory.register_driver( ImageCompression.C8, OPJ_Driver(), OPJ_Driver() )

        return factory

