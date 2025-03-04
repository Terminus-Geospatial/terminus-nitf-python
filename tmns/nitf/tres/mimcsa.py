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
from collections import deque
from enum import Enum

#  Terminus Libraries
from tmns.nitf.tre   import TRE_Base
from tmns.nitf.field_types import FieldType

class Field(Enum):
    CETAG              = (  0,  6, FieldType.BCS_A,  'MIMCSA',  True, 'Unique Extension Type Identifier' )
    CEL                = (  1,  5, FieldType.BCS_NP,     None,  True, 'TRE Length' )
    LAYER_ID           = (  2, 36, FieldType.BCS_A,      None,  True, 'Layer Identifier' )
    NOMINAL_FRAME_RATE = (  3, 13, FieldType.BCS_A,      None,  True, 'Nominal Frame Rate in Frames/Second' )
    MIN_FRAME_RATE     = (  4, 13, FieldType.BCS_A,      None,  True, 'Minimum Frame Rate in Frames/Second' )
    MAX_FRAME_RATE     = (  5, 13, FieldType.BCS_A,      None,  True, 'Maximum Frame Rate in Frames/Second' )
    T_RSET             = (  6,  2, FieldType.BCS_NP,     None,  True, 'Temporal RSET of MI' )
    MI_REQ_DECODER     = (  7,  2, FieldType.BCS_A,      None,  True, 'MI IC Field.' )
    MI_REQ_PROFILE     = (  8, 36, FieldType.BCS_A,      None,  True, 'MI Compression Profile Name' )
    MI_REQ_LEVEL       = (  9,  6, FieldType.BCS_A,      None,  True, 'MI Compression Profile' )

