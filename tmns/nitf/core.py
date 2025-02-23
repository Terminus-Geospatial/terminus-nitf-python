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
import io
import logging
import os

#  Terminus libraries
from tmns.nitf.base import NITF_Container
from tmns.nitf.fhdr import (
    Field as FHDR_Field,
    File_Header
)
from tmns.nitf.imsubhdr import ( 
    Field as IMGSUB_Field,
    Image_Subheader
)

from tmns.nitf.tre import TRE_Factory


def load_nitf( pathname,
               options: list = [],
               logger = None,
               tre_factory = None ):
    
    #  Setup logger, if not already set
    if logger == None:
        logger = logging.getLogger( 'tmns.nitf.core:load_nitf' )
    
    #  Setup TRE factory, if not already set
    if tre_factory == None:
        tre_factory = TRE_Factory.default()

    #  Make sure the file exists
    if not os.path.exists( pathname ):
        raise FileNotFoundError( f'Unable to find NITF {pathname}' )
    
    #  Check file size
    fsize = os.path.getsize( pathname )
    if fsize < 10:
        raise Exception( f'Image is not large enough. Size: {fsize}' )

    #  Open file
    with open( pathname, 'rb' ) as fin:

        #  Read the file header
        fhdr = File_Header.parse_binary( file_handle = fin,
                                         tre_factory = tre_factory )
        logger.debug(fhdr)

        fhdr_errors = fhdr.validate( file_size = fsize )
        if len(fhdr_errors) > 0:
            error_str = f'FHDR Errors: {len(fhdr_errors)}\n'
            for x in range( len(fhdr_errors) ):
                error_str += f'{fhdr_errors[x]}\n'
            logger.error( error_str )

        #  Read the image subheader
        image_subheaders = []
        numi = fhdr.get( FHDR_Field.NUMI )['data'].value()
        for idx in range( numi ):

            # Get size of image subheader
            imgsub_size = fhdr.get( FHDR_Field.LISH_N, index = idx )

            #  Parse image subheader
            img_subheader = Image_Subheader.parse_binary( file_handle = fin )
            logging.info( img_subheader )
            
            #  Validate and check for errors
            errors = img_subheader.validate()
            if len(errors) > 0:
                error_str = f'Image Subheader {idx} Errors: {len(errors)}\n'
                for x in range( len(errors) ):
                    error_str += f'{errors[x]}\n'
            logger.error( error_str )

            #  Add to subheader list
            image_subheaders.append( img_subheader )

            #  Parse image segment
            imgseg_size = fhdr.get( FHDR_Field.LI_N,   index = idx )


        return NITF_Container( file_header      = fhdr,
                               image_subheaders = image_subheaders )

