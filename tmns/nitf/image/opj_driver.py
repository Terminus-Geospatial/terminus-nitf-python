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
import hashlib
import os
import random
import sys
import tempfile

#  Pillow
from skimage import io

import matplotlib
from matplotlib import pyplot as plt

#  Terminus Libraries
from tmns.nitf.image.driver_base import Driver_Base


class OPJ_Driver(Driver_Base):

    def __init__( self, config: dict = None ):
        self.config = config

    def encode( self, code, image ):
        pass

    def decode( self, code, buffer ):

        #  Write the buffer to disk
        tempdir  = tempfile.gettempdir()
        temp_j2k = f'{hashlib.sha256(random.randbytes(50)).hexdigest()}.j2k'
        codestream_path = os.path.join( tempdir, temp_j2k )

        with open( codestream_path, 'wb' ) as fout:
            fout.write( buffer )

        #  Create System Call to Convert using OpenJPG
        temp_png = f'{hashlib.sha256(random.randbytes(50)).hexdigest()}.png'
        png_path = os.path.join( tempdir, temp_png )

        #print( f'\nCodestream: {codestream_path}\nPNG: {png_path}' )
        os.system( f'opj_decompress -i {codestream_path} -o {png_path}' )
        
        #  Open the new image
        image = io.imread( png_path, plugin="pil" )
        
        #  Delete everything
        os.remove( codestream_path )
        os.remove( png_path )

        return image

    @staticmethod
    def default_config():
        config = { 'tempdir': tempfile.gettempdir() }
        return config
    
