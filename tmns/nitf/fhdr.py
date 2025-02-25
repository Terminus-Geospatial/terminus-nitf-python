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
import logging

#  Terminus Libraries
from tmns.nitf.tre   import ( TRE_Base,
                              TRE_Factory )
from tmns.nitf.field_types import FieldType


class Field(Enum):
    '''
    List of fields in the NITF File Header.
    Values represented are (position, size (bytes), Field-Type, "default" value, "repeatable block" )

    Do not change this unless you want to own it.
    '''
    FHDR     = (  0,  4, FieldType.BCS_A,        'NITF',  True, 'File Profile Name' )
    FVER     = (  1,  5, FieldType.BCS_A,       '02.10',  True, 'File Version' )
    CLEVEL   = (  2,  2, FieldType.BCS_NP,            1,  True, 'Complexity Level' )
    STYPE    = (  3,  4, FieldType.BCS_A,        'BF01',  True, 'Standard Type' )
    OSTAID   = (  4, 10, FieldType.BCS_A,      ' ' * 10,  True, 'Originating Station ID' )
    FDT      = (  5, 14, FieldType.BCS_N,          None,  True, 'File Date and Time' )
    FTITLE   = (  6, 80, FieldType.ECS_A,      ' ' * 80,  True, 'File Title' )
    FSCLAS   = (  7,  1, FieldType.ECS_A,           'U',  True, 'File Security Classification' )
    FSCLSY   = (  8,  2, FieldType.ECS_A,          '  ',  True, 'File Security Classification System' )
    FSCODE   = (  9, 11, FieldType.ECS_A,      ' ' * 11,  True, 'File Codewords' )
    FSCTLH   = ( 10,  2, FieldType.ECS_A,      ' ' *  2,  True, 'File Control and Handling' )
    FSREL    = ( 11, 20, FieldType.ECS_A,      ' ' * 20,  True, 'File Releasing Instructions' )
    FSDCTP   = ( 12,  2, FieldType.ECS_A,      ' ' *  2,  True, 'File Declassification Type' )
    FSDCDT   = ( 13,  8, FieldType.ECS_A,      ' ' *  8,  True, 'File Declassification Date' )
    FSDCXM   = ( 14,  4, FieldType.ECS_A,      ' ' *  4,  True, 'File Declassification Exemption' )
    FSDG     = ( 15,  1, FieldType.ECS_A,      ' ' *  1,  True, 'File Downgrade' )
    FSDGDT   = ( 16,  8, FieldType.ECS_A,      ' ' *  8,  True, 'File Downgrade Date' )
    FSCLTX   = ( 17, 43, FieldType.ECS_A,      ' ' * 43,  True, 'File Classification Text' )
    FSCATP   = ( 18,  1, FieldType.ECS_A,      ' ' *  1,  True, 'File Classification Authority Type' )
    FSCAUT   = ( 19, 40, FieldType.ECS_A,      ' ' * 40,  True, 'File Classification Authority' )
    FSCRSN   = ( 20,  1, FieldType.ECS_A,      ' ' *  1,  True, 'File Classification Reason' )
    FSSRDT   = ( 21,  8, FieldType.ECS_A,      ' ' *  8,  True, 'File Security Source Date' )
    FSCTLN   = ( 22, 15, FieldType.ECS_A,      ' ' * 15,  True, 'File Security Control Number' )
    FSCOP    = ( 23,  5, FieldType.BCS_N,      ' ' *  5,  True, 'File Copy Number' )
    FSCPYS   = ( 24,  5, FieldType.BCS_N,      ' ' *  5,  True, 'File Number of Copies' )
    ENCRYPT  = ( 25,  1, FieldType.BCS_N,             0,  True, 'Encryption' )
    FPKGC    = ( 26,  3, FieldType.UnsignedBinary, None,  True, 'File Background Color' )
    ONAME    = ( 27, 24, FieldType.ECS_A,      ' ' * 24,  True, 'Originator\'s Name' )
    OPHONE   = ( 28, 18, FieldType.ECS_A,      ' ' * 18,  True, 'Originator\'s Phone Number' )
    FL       = ( 29, 12, FieldType.BCS_NP,            0,  True, 'File Length' )
    HL       = ( 30,  6, FieldType.BCS_N,             0,  True, 'NITF File Header Length' )
    NUMI     = ( 31,  3, FieldType.BCS_N,             0,  True, 'Number of Image Segments' )
    LISH_N   = ( 32,  6, FieldType.BCS_N,             0, False, 'Length of nth Image Subheader' )
    LI_N     = ( 33, 10, FieldType.BCS_N,             0, False, 'Length of nth Image Segment' )
    NUMS     = ( 34,  3, FieldType.BCS_N,             0,  True, 'Number of Graphic Segments' )
    LSSH_N   = ( 35,  4, FieldType.BCS_N,             0, False, 'Length of nth Graphic Subheader' )
    LS_N     = ( 36,  6, FieldType.BCS_N,             0, False, 'Length of nth Graphic Segment' )
    NUMX     = ( 37,  3, FieldType.BCS_N,             0,  True, 'Reserved for Future Use' )
    NUMT     = ( 38,  3, FieldType.BCS_N,             0,  True, 'Number of Text Segments' )
    LTSH_N   = ( 39,  4, FieldType.BCS_NP,            0, False, 'Length of nth Text Subheader' )
    LT_N     = ( 40,  5, FieldType.BCS_NP,            0, False, 'Length of nth Text Segment' )
    NUMDES   = ( 41,  3, FieldType.BCS_NP,            0,  True, 'Number of Data Extension Segments' )
    LDSH_N   = ( 42,  4, FieldType.BCS_NP,            0, False, 'Length of nth Data Extension Segment Subheader' )
    LD_N     = ( 43,  9, FieldType.BCS_NP,            0, False, 'Length of nth Data Extension Segment' )
    NUM_RES  = ( 44,  3, FieldType.BCS_NP,            0,  True, 'Number of Reserved Data Extension Segments' )
    LRESH_N  = ( 45,  4, FieldType.BCS_NP,            0, False, 'Length of nth Reserved Extension Segment Subheader' )
    LRE_N    = ( 46,  7, FieldType.BCS_NP,            0, False, 'Length of nth Reserved Extension Segment' )
    UDHDL    = ( 47,  5, FieldType.BCS_NP,            0,  True, 'User-Defined Header Data Length' )
    UDHOFL   = ( 48,  3, FieldType.BCS_NP,            0, False, 'User-Defined Header Overflow' )
    UDHD     = ( 49,  0, FieldType.UnsignedBinary, None, False, 'User-Defined Header Data' )
    XHDL     = ( 50,  5, FieldType.BCS_NP,            0, False, 'Extended Header Data Length' )
    XHDLOFL  = ( 51,  3, FieldType.BCS_NP,            0, False, 'Extended Header Data Overflow' )
    XHD      = ( 52,  0, FieldType.TRE,            None, False, 'Extended Header Data' )

    @staticmethod
    def default_list():
        return [ Field.FHDR,    Field.FVER,    Field.CLEVEL, Field.STYPE,
                 Field.OSTAID,  Field.FDT,     Field.FTITLE, Field.FSCLAS,
                 Field.FSCLSY,  Field.FSCODE,  Field.FSCTLH, Field.FSREL,
                 Field.FSDCTP,  Field.FSDCDT,  Field.FSDCXM, Field.FSDG,
                 Field.FSDGDT,  Field.FSCLTX,  Field.FSCATP, Field.FSCAUT,
                 Field.FSCRSN,  Field.FSSRDT,  Field.FSCTLN, Field.FSCOP,
                 Field.FSCPYS,  Field.ENCRYPT, Field.FPKGC,  Field.ONAME,
                 Field.OPHONE,  Field.FL,      Field.HL,     Field.NUMI,
                 Field.NUMS,    Field.NUMX,    Field.NUMT,   Field.NUMDES,
                 Field.NUM_RES, Field.UDHDL,   Field.UDHD,   Field.XHDL,
                 Field.XHD ]

class File_Header:

    def __init__( self, data, udhd, xhd ):
        self.data = data
        self.udhd = udhd
        self.xhd  = xhd

    def get( self, field, index = 0 ):

        counter = 0
        for k in self.data.keys():
            if self.data[k]['field'] == field:
                if counter == index:
                    return self.data[k]
                else:
                    counter += 1
        return None

    def as_kvp(self):

        data = {}

        #  Primary data
        for k in self.data.keys():
            data[self.data[k]['field'].name] = str(self.data[k]['data'])
        
        # 
        if self.udhd != None:
            for tre in self.udhd:
                cetag = tre.cetag()
                tmp = tre.as_kvp()
                for k in tmp.keys():
                    data[f'udhd.{cetag}.{k}'] = str(tmp[k])

        
        if self.xhd != None:
            for tre in self.xhd:
                cetag = tre.cetag()
                tmp = tre.as_kvp()
                for k in tmp.keys():
                    data[f'xhd.{cetag}.{k}'] = str(tmp[k])

        return data

    def validate( self, file_size ):

        errors = []
        
        # File Length
        fl_entry = self.get( Field.FL )
        fl_value = fl_entry['data'].value()
        if fl_value is None:
            errors.append( ['No file length value found'] )
        if fl_value != file_size:
            errors.append( [f'File Length value ({fl_value}) does not match expected ({file_size})' ] )

        return errors

    def __str__(self):
        '''
        Convert file header to log-friendly string
        '''
        output  = 'NITF File Header:\n'
        for field in self.data.keys():
            output += f'   Pos {field}, Name: {self.data[field]["name"]}, Value: {self.data[field]["data"].value()}\n'
        
        output += f'   UDHD TREs: ({len(self.udhd)})\n'
        for tre in self.udhd:
            output += tre.to_log_string( 4 )
        
        output += f'   XHD TREs: ({len(self.xhd)})\n'
        for tre in self.xhd:
            output += tre.to_log_string( 4 )
        
        return output
    
    
    @staticmethod
    def parse_binary( file_handle, logger = None, tre_factory = None ):

        if logger is None:
            logger = logging.getLogger( 'tmns.nitf.fhdr.FileHeader.parse_binary' )
        
        if tre_factory == None:
            tre_factory = TRE_Factory.default()

        data = {}

        #  Read block by block
        fields = deque(Field.default_list())
        offset = 0
        udhd_tres = []
        xhd_tres  = []
        while len(fields) > 0:

            add_entry = True

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

            #  If UDHD, need the UDHDL flag
            if field_length <= 0 and field == Field.UDHD:
                field_length = data[offset-2]['data'].value()

            #  If XHD, need the XHDL flag
            elif field_length <= 0 and field == Field.XHD:

                field_length += data[offset-2]['data'].value()
                field_length += data[offset-1]['data'].value()

            #  Read a block of data
            field_data = file_handle.read( field_length )
            if len(field_data) != field_length:
                raise Exception( f'Reached end of file before field. Field: {field}' )
            
            #  Convert to appropriate type
            tp = FieldType.to_type( field_type )

            new_field = { 'name': Field(field).name,
                          'field': field,
                          'type': tp,
                          'data': tp(field_data, field_length) }

            #  Number of Image Segments
            if field == Field.NUMI:
                numi_value = new_field['data'].value()
                if numi_value > 0:
                    for idx in range( numi_value ):
                        fields.appendleft( Field.LI_N )
                        fields.appendleft( Field.LISH_N )
            
            # Number of Graphic Segments
            elif field == Field.NUMS:
                nums_value = new_field['data'].value()
                if nums_value > 0:
                    for idx in range( nums_value ):
                        fields.appendleft( Field.LS_N )
                        fields.appendleft( Field.LSSH_N )
            
            # Number of Text Segments
            elif field == Field.NUMT:
                numt_value = new_field['data'].value()
                if numt_value > 0:
                    for idx in range( numt_value ):
                        fields.appendleft( Field.LT_N )
                        fields.appendleft( Field.LTSH_N )
            
            # Number of Data Extension Segments
            elif field == Field.NUMDES:
                numdes_value = new_field['data'].value()
                if numdes_value > 0:

                    for idx in range( numdes_value ):
                        fields.appendleft( Field.LD_N )
                        fields.appendleft( Field.LDSH_N )
            
            elif field == Field.UDHD:
                udhd_tres = TRE_Base.parse_binary( new_field['data'].data,
                                                   factory = tre_factory )
                add_entry = False

            elif field == Field.XHD:
                xhd_data = new_field['data'].data[3:]
                xhd_tres  = TRE_Base.parse_binary( xhd_data,
                                                   factory = tre_factory )
                add_entry = False

            #  Finish and add field
            if add_entry:
                data[offset] = new_field
                offset += 1

        return File_Header( data = data,
                            udhd = udhd_tres,
                            xhd  = xhd_tres )

