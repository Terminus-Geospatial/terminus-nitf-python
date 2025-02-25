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
from tmns.nitf.enums    import ImageCompression
from tmns.nitf.imsubhdr import ( Field as IM_Field )

class Image_Segment:

    def __init__( self, subheader = None, 
                        buffer    = None,
                        factory   = None  ):
        '''
        Constructor for Image Segment
        '''
        self.subheader = subheader
        self.buffer    = buffer
        self.factory   = factory

    def as_kvp(self):
        return self.subheader.as_kvp()
    
    def get_image( self ):

        #  Get the image code
        code = ImageCompression[self.subheader.get( IM_Field.IC )['data'].value()]
        
        if self.factory != None:
            return self.factory.decode( code, self.buffer )
        
        