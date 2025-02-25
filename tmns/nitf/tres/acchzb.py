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
    CETAG     = (  0,  6, FieldType.BCS_A,  'ACCHZB',  'Unique Extension Type Identifier' )
    CEL       = (  1,  5, FieldType.BCS_NP,    None,  'TRE Length' )
    NUM_ACHZ  = (  2,  2, FieldType.BCS_NP,    None,  'Number of Horizontal Accuracy Regions' )
    UNIAAH_N  = (  3,  3, FieldType.BCS_A,     None,  'Unit of Measure for the AAH_N Field' )
    AAH_N     = (  4,  5, FieldType.BCS_NP,    None,  'Absolute Horizontal Accuracy' )
    UNIAPH_N  = (  5,  3, FieldType.BCS_A,     None,  'Unit of Measure for the APH_N Field' )
    APH_N     = (  6,  5, FieldType.BCS_NP,    None,  'Point-to-Point Horizontal Accuracy' )
    NUM_PTS_N = (  7,  3, FieldType.BCS_A,     None,  'Number of Points in the Bounding Polygon' )
    LON_N_M   = (  8, 15, FieldType.BCS_N,     None,  'Longitude or Easting Associated with the Mth Polygon Point of the Nth Polygon' )
    LAT_N_M   = (  9, 15, FieldType.BCS_N,     None,  'Latitude or Northing Associated with the Mth Polygon Point of the Nth Polygon' )

class ACCHZB( TRE_Base ):

    def __init__( self, data ):
        self.data = data

    def __str__(self):
        return self.to_log_string()
    
    def to_log_string( self, offset = 0 ):
        
        gap = ' ' * offset
        output  = f'{gap}ACCHZB:\n'
        for field in self.data.keys():
            output += f'{gap}   Pos {field}, Name: {self.data[field]["name"]}, Value: [{self.data[field]["data"].value()}]\n' 
        return output

    def is_valid( cetag, cel, cedata ):

        if cetag.decode('utf8') == 'ACCHZB':
            return True
        return False

    def build( cetag, cel, cedata ):

        data = {}
        counter = 0

        #  CETAG
        cetag_val, _ = TRE_Base.parse_field( cetag, Field.CETAG )
        data[counter] = cetag_val
        counter += 1

        #  CEL
        cel_val, _ = TRE_Base.parse_field( cel, Field.CEL )
        data[counter] = cel_val
        counter += 1

        #  NUM_ACHZ
        num_achz, cedata = TRE_Base.parse_field( cedata, Field.NUM_ACHZ )
        data[counter] = num_achz
        counter += 1
        
        #  Iterate over each point
        for n in range( num_achz['data'].value() ):

            # UNIAAHN
            uniaah, cedata = TRE_Base.parse_field( cedata, Field.UNIAAH_N )
            data[counter] = uniaah
            counter += 1

            #  AAH
            if len(str(uniaah['data'].value()).strip()) > 0:
                aah, cedata = TRE_Base.parse_field( cedata, Field.AAH_N )
                data[counter] = aah
                counter += 1
            
            #  UNIAPHN
            uniaph, cedata = TRE_Base.parse_field( cedata, Field.UNIAPH_N )
            data[counter] = uniaph
            counter += 1

            #  APHN
            if len(str(uniaph['data'].value()).strip()) > 0:
                aph, cedata = TRE_Base.parse_field( cedata, Field.APH_N )
                data[counter] = aph
                counter += 1
            
            #  Number of Points for Polygon N
            num_pts, cedata = TRE_Base.parse_field( cedata, Field.NUM_PTS_N )
            data[counter] = num_pts
            counter += 1

            #  For each point
            npval = num_pts['data'].value().strip(' ')
            if len(npval) > 0:
                for m in range( int( npval ) ):
                    #  Longitude
                    lon_nm, cedata = TRE_Base.parse_field( cedata, Field.LON_N_M )
                    data[counter] = lon_nm
                    counter += 1

                    #  Latitude
                    lat_nm, cedata = TRE_Base.parse_field( cedata, Field.LAT_N_M )
                    data[counter] = lat_nm
                    counter += 1

        return ACCHZB( data )