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

# Python Libraries
from collections import deque
from enum import Enum
import logging

#  Terminus Libraries
from tmns.nitf.types import FieldType

class Field(Enum):
    '''
    List of fields in the NITF Image Subheader.
    Values represented are (position, size (bytes), Field-Type, "default" value, "repeatable block" )

    Do not change this unless you want to own it.
    '''
    IM         = (  0,  2, FieldType.BCS_A,         'IM',   True, 'File Part Type' )
    IID1       = (  1, 10, FieldType.BCS_A,     ' ' * 10,   True, 'Image Identifier 1' )
    IDATIM     = (  2, 14, FieldType.BCS_N,            0,   True, 'Image Date and Time' )
    TGTID      = (  3, 17, FieldType.BCS_A,     ' ' * 17,   True, 'Target Identifier' )
    IID2       = (  4, 80, FieldType.ECS_A,     ' ' * 80,   True, 'Image Identifier 2' )
    ISCLAS     = (  5,  1, FieldType.ECS_A,          'U',   True, 'Image Security Classification' )
    ISCLSY     = (  6,  2, FieldType.ECS_A,         '  ',   True, 'Image Security Classification System' )
    ISCODE     = (  7, 11, FieldType.ECS_A,     ' ' * 11,   True, 'Image Codewords' )
    ISCTLH     = (  8,  2, FieldType.ECS_A,         '  ',   True, 'Image Control and Handling' )
    ISREL      = (  9, 20, FieldType.ECS_A,     ' ' * 20,   True, 'Image Releasing Instructions' )
    ISDCTP     = ( 10,  2, FieldType.ECS_A,         '  ',   True, 'Image Declassification Type' )
    ISDCDT     = ( 11,  8, FieldType.ECS_A,     ' ' *  8,   True, 'Image Declassification Date' )
    ISDCXM     = ( 12,  4, FieldType.ECS_A,     ' ' *  4,   True, 'Image Declassification Exemption' )
    ISDG       = ( 13,  1, FieldType.ECS_A,          ' ',   True, 'Image Downgrade' )
    ISDGDT     = ( 14,  8, FieldType.ECS_A,     ' ' *  8,   True, 'Image Downgrade Date' )
    ISCLTX     = ( 15, 43, FieldType.ECS_A,     ' ' * 43,   True, 'Image Classification Text' )
    ISCATP     = ( 16,  1, FieldType.ECS_A,          ' ',   True, 'Image Classification Authority Type' )
    ISCAUT     = ( 17, 40, FieldType.ECS_A,     ' ' * 40,   True, 'Image Classification Authority' )
    ISCRSN     = ( 18,  1, FieldType.ECS_A,          ' ',   True, 'Image Classification Reason' )
    ISSRDT     = ( 19,  8, FieldType.ECS_A,     ' ' *  8,   True, 'Image Security Source Date' )
    ISCTLN     = ( 20, 15, FieldType.ECS_A,     ' ' * 15,   True, 'Image Security Control Number' )
    ENCRYP     = ( 21,  1, FieldType.BCS_NP,           0,   True, 'Encryption' )
    ISORCE     = ( 22, 42, FieldType.ECS_A,     ' ' * 42,   True, 'Image Source' )
    NROWS      = ( 23,  8, FieldType.BCS_NP,           0,   True, 'Number of Significant Rows in Image' )
    NCOLS      = ( 24,  8, FieldType.BCS_NP,           0,   True, 'Number of Significant Columns in Image' )
    PVTYPE     = ( 25,  3, FieldType.BCS_A,        '   ',   True, 'Pixel Value Type' )
    IREP       = ( 26,  8, FieldType.BCS_A,     ' ' *  8,   True, 'Image Representation' )
    ICAT       = ( 27,  8, FieldType.BCS_A,     ' ' *  8,   True, 'Image Category' )
    ABPP       = ( 28,  2, FieldType.BCS_NP,        '  ',   True, 'Actual Bits-Per-Pixel Band' )
    PJUST      = ( 29,  1, FieldType.BCS_A,          ' ',   True, 'Pixel Justification' )
    ICORDS     = ( 30,  1, FieldType.BCS_A,          ' ',   True, 'Image Coordinate Representation' )
    IGEOLO     = ( 31, 60, FieldType.BCS_A,     ' ' * 60,   True, 'Image Geographic Location' )
    NICOM      = ( 32,  1, FieldType.BCS_NP,           0,   True, 'Number of Image Components' )
    ICOM_N     = ( 33, 80, FieldType.ECS_A,     ' ' * 80,   True, 'Image Comments N' )
    IC         = ( 34,  2, FieldType.BCS_A,          '  ',  True, 'Image Compression' )
    COMRAT     = ( 35,  4, FieldType.BCS_A,       ' ' * 4,  True, 'Compression Rate Code' )
    NBANDS     = ( 36,  1, FieldType.BCS_NP,            0,  True, 'Number of Bands' )
    XBANDS     = ( 37,  5, FieldType.BCS_NP,            0,  True, 'Number of Multispectral Bands' )
    IREPBAND_N = ( 38,  2, FieldType.BCS_A,          '  ',  True, 'Nth Band Representation' )
    ISUBCAT_N  = ( 39,  6, FieldType.BCS_A,       ' ' * 6,  True, 'Nth Band Subcategory' )
    IFC_N      = ( 40,  1, FieldType.BCS_A,           'N',  True, 'Nth Band Filter Condition' )
    IMFLT_N    = ( 41,  3, FieldType.BCS_A,         '   ',  True, 'Nth Band Standard Image Filter Code' )
    NLUTS_N    = ( 42,  1, FieldType.BCS_NP,            0,  True, 'Number of LUTS for the Nth Band' )
    NELUT_N    = ( 43,  5, FieldType.BCS_NP,            0,  True, 'Number of LUT Entries for the Nth Image Band.' )
    LUTD_N_M   = ( 44,  0, FieldType.UnsignedBinary, None, False, 'Nth Image Band, Mth LUT' )
    ISYNC      = ( 45,  1, FieldType.BCS_NP,            0,  True, 'Image Sync Code' )
    IMODE      = ( 46,  1, FieldType.BCS_A,           ' ',  True, 'Image Mode' )
    NBPR       = ( 47,  4, FieldType.BCS_NP,            0,  True, 'Number of Blocks Per Row' )
    NBPC       = ( 48,  4, FieldType.BCS_NP,            0,  True, 'Number of Blocks Per Column' )
    NPPBH      = ( 49,  4, FieldType.BCS_NP,            0,  True, 'Number of Pixels Per Block Horizontal' )
    NPPBV      = ( 50,  4, FieldType.BCS_NP,            0,  True, 'Number of Pixels Per Block Vertical' )
    NBPP       = ( 51,  2, FieldType.BCS_NP,            0,  True, 'Number of Bits Per Pixel Per Band' )
    IDLVL      = ( 52,  3, FieldType.BCS_NP,            1,  True, 'Image Display Level' )
    IALVL      = ( 53,  3, FieldType.BCS_NP,            0,  True, 'Attachment Level' )
    ILOC       = ( 54, 10, FieldType.BCS_NP,            0,  True, 'Image Location' )
    IMAG       = ( 55,  4, FieldType.BCS_A,           ' ',  True, 'Image Magnification' )
    UDIDL      = ( 56,  5, FieldType.BCS_NP,            0,  True, 'User Defined Image Data Length' )
    UDOFL      = ( 57,  3, FieldType.BCS_NP,            0,  True, 'User Defined Overflow' )
    UDID       = ( 58,  0, FieldType.TRE,            None, False, 'User Defined Image Data' )
    IXSHDL     = ( 59,  5, FieldType.BCS_NP,            0,  True, 'Image Extended Subheader Data Length' )
    IXSOFL     = ( 60,  3, FieldType.BCS_NP,            0,  True, 'Image Extended Subheader Overflow' )
    IXSHD      = ( 61,  0, FieldType.TRE,            None, False, 'Image Extended Subheader Data' )

    @staticmethod
    def default_list():
        return [ Field.IM,      Field.IID1,    Field.IDATIM,  Field.TGTID,   Field.IID2,
                 Field.ISCLAS,  Field.ISCLSY,  Field.ISCODE,  Field.ISCTLH,  Field.ISREL,
                 Field.ISDCTP,  Field.ISDCDT,  Field.ISDCXM,  Field.ISDG,    Field.ISDGDT,
                 Field.ISCLTX,  Field.ISCATP,  Field.ISCAUT,  Field.ISCRSN,  Field.ISSRDT,
                 Field.ISCTLN,  Field.ENCRYP,  Field.ISORCE,  Field.NROWS,   Field.NCOLS,
                 Field.PVTYPE,  Field.IREP,    Field.ICAT,    Field.ABPP,    Field.PJUST,
                 Field.ICORDS,  Field.IGEOLO,  Field.NICOM,   Field.IC,      Field.COMRAT,
                 Field.NBANDS,  Field.XBANDS,  Field.ISYNC,   Field.IMODE,   Field.NBPR,
                 Field.NBPC,    Field.NPPBH,   Field.NPPBV,   Field.NBPP,    Field.IDLVL,
                 Field.IALVL,   Field.ILOC,    Field.IMAG,    Field.UDIDL,   Field.UDOFL,
                 Field.UDID,    Field.IXSHDL,  Field.IXSOFL,  Field.IXSHD ]


class Image_Subheader:

    def __init__( self, data ):
        self.data = data

    def get( self, field ):

        for k in self.data.keys():
            if self.data[k]['field'] == field:
                return self.data[k]
        return None

    def validate( self ):

        errors = []

        return errors

    def __str__(self):
        '''
        Convert image subheader to log-friendly string
        '''
        output  = 'NITF Image Subheader:\n'
        for field in self.data.keys():
            output += f'   Pos {field}, Name: {self.data[field]["name"]}, Value: {self.data[field]["data"].value()}\n'
        return output
    
    
    @staticmethod
    def parse_binary( file_handle, logger = None ):

        if logger is None:
            logger = logging.getLogger( 'tmns.nitf.imgseg.Image_Subheader.parse_binary' )
        data = {}

        #  Read block by block
        fields = deque(Field.default_list())
        offset = 0
        size_queue = deque()
        while len(fields) > 0:

            #  Grab next field
            field = fields.popleft()

            #  Get field data
            fld = Field(field).value

            field_pos       = offset
            field_length    = fld[1]
            field_type      = fld[2]
            field_default   = fld[3]
            field_is_fixed  = fld[4]
            field_name      = fld[5]
            logger.debug( f'Processing ID {field_pos}, Name: {field}, Len: {field_length}, Type: {field_type} ')

            if field_length == 0:
                field_length = size_queue.popleft()

            #  Read a block of data
            field_data = file_handle.read( field_length )
            if len(field_data) != fld[1]:
                raise Exception( f'Reached end of file before field. Field: {field}' )
            
            #  Convert to appropriate type
            field_type = FieldType.to_type( field_type )
            data[offset] = { 'name': Field(field).name,
                             'field': field,
                             'type': field_type,
                             'data': field_type(field_data, field_length) }
            logging.debug( f'    -> Value: {data[offset]["data"].value()}' )

            #  Number of Image Comments
            if field == Field.NICOM:
                nicom = data[offset]['data'].value()
                if nicom > 0:
                    fields.appendleft( Field.ICOM_N )
            
            # Image Band Data
            if field == Field.XBANDS:
                nbands = data[offset-1]['data'].value()
                xbands = data[offset]['data'].value()

                val = max( nbands, xbands )
                for idx in range( val ):
                    fields.appendleft( Field.IREPBAND_N )
                    fields.appendleft( Field.ISUBCAT_N )
                    fields.appendleft( Field.IFC_N )
                    fields.appendleft( Field.NLUTS_N )
                    fields.appendleft( Field.NELUT_N )
            
            # Band LUTs
            if field == Field.NELUT_N:
                nluts = data[offset-1]['data'].value()
                nelut = data[offset]['data'].value()

                total = nluts * nelut
                size_queue.appendleft( total )
            
            offset += 1

        return Image_Subheader( data = data )