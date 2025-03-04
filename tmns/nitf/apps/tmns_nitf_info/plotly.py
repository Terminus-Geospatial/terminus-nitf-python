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
import logging

#  Plotly
import plotly.express       as px
import plotly.graph_objects as go
import plotly.subplots      as sp

#  Numpy
import numpy as np

#  Scikit Learn
from skimage import io

#  Terminus Libraries



def render_html( nitf_data, logger = None ):

    if logger == None:
        logger = logging.getLogger( 'tmns_nitf_info.plotly:render_html' )

    print('a')
    metadata = nitf_data.as_kvp()
    print('b')
    image    = nitf_data.get_image()
    print('c')
    
    #  Create primary subplot
    fig = sp.make_subplots( rows = 2, cols = 1,
                            specs=[[{'type': 'table' }],
                                   [{'type': 'scatter' }]],
                            row_heights=[0.3,0.7] )

    fig.add_trace( go.Table( header = dict( values = ['Key', 'Value'] ),
                             cells  = dict( values = [ list(metadata.keys()),
                                                       list(metadata.values()) ] ) ),
                  row = 1, col = 1 )
    
    if len(image.shape) == 2 or image.shape[2] == 1:
        fig.add_trace( go.Heatmap( z = image ), row = 2, col = 1 )
    else:
        fig.add_trace( go.Image( z = image ), row = 2, col = 1 )

    fig.update_layout( height = 1800 )

    fig.update_yaxes(
        scaleanchor="x",
        scaleratio=1,
    )
    
    fig.write_html( 'output.html' )

    