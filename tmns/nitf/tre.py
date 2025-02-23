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
import logging

#  Terminus Libraries
from tmns.nitf.tres.base   import TRE_Base
from tmns.nitf.tres.ccinfa import CCINFA
from tmns.nitf.tres.csdida import CSDIDA
from tmns.nitf.tres.engrda import ENGRDA
from tmns.nitf.tres.matesa import MATESA
from tmns.nitf.types import FieldType


class TRE_Factory:

    def __init__(self):

        self.names: list      = []
        self.validators: list = []
        self.builders: list   = []

    def register(self, builder_name, builder, validator ):
        self.names.append( builder_name )
        self.builders.append( builder )
        self.validators.append( validator )

    def build( self, cetag: str, cel: int, cedata: bytes ):

        for idx in range( len( self.builders ) ):
            if self.validators[idx]( cetag, cel, cedata ):
                return self.builders[idx]( cetag, cel, cedata )
        return None

    def __str__(self):
        output  = f'TRE Factory:  (total: {len(self.builders)})\n'
        for idx in range( len( self.builders ) ):
            output += f'   - Builder {idx}, Name: {self.names[idx]}\n'
        return output

    @staticmethod
    def default():

        factory = TRE_Factory()

        #  Create a set of default TRE builders
        factory.register( CCINFA.__name__,   CCINFA.build,   CCINFA.is_valid )
        factory.register( CSDIDA.__name__,   CSDIDA.build,   CSDIDA.is_valid )
        factory.register( ENGRDA.__name__,   ENGRDA.build,   ENGRDA.is_valid )
        factory.register( MATESA.__name__,   MATESA.build,   MATESA.is_valid )
        factory.register( TRE_Base.__name__, TRE_Base.build, TRE_Base.is_valid )

        return factory
        
