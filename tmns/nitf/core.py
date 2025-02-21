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
import os


def load_nitf( pathname,
               options: dict ):
    
    #  Make sure the file exists
    if not os.path.exists( pathname ):
        raise FileNotFoundError( f'Unable to find NITF {pathname}' )
    
    #  Open file
    with open( pathname, 'rb' ) as fin:

        print( type( fin ) )