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

class ImageCompression(Enum):

    C1 =  0
    C3 =  1
    C4 =  2
    C5 =  3
    C6 =  4
    C7 =  5
    C8 =  6
    I1 =  7
    M1 =  8
    M3 =  9
    M4 = 10
    M5 = 11
    M6 = 12
    M7 = 13
    M8 = 14
    NC = 15
    NM = 16

    @staticmethod
    def from_str( s ):
        for x in ImageCompression:
            if x.name.lower() == s.lower():
                return x


    
