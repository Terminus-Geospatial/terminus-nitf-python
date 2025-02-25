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


class NITF_Container:

    def __init__(self, file_header, image_segments ):
        
        self.file_header    = file_header
        self.image_segments = image_segments

    def get_image( self, img_seg = 0 ):

        return self.image_segments[img_seg].get_image()
    
    def as_kvp( self ):

        data = {}
        kvp = self.file_header.as_kvp()
        for k in kvp.keys():
            data[f'file_header.{k}'] = kvp[k]
        
        for idx in range( len( self.image_segments ) ):
            kvp = self.image_segments[idx].as_kvp()
            for k in kvp.keys():
                data[f'image_segment.{idx}.{k}'] = kvp[k]
                
        return data

    