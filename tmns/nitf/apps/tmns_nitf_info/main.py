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

#  Terminus Libraries
from tmns.core.apps import run, ArgumentParser, configure_logging
from tmns.nitf.core import load_nitf
from tmns.nitf.image.factory import Driver_Factory
from tmns.nitf.tre  import TRE_Factory
from tmns.nitf.apps.tmns_nitf_info.plotly import render_html

def parse_command_line():

    parser = ArgumentParser( description = 'Parse a NITF file and print information about it\'s contents' )

    parser.add_argument( '-v', '--verbose',
                         dest = 'log_level',
                         default = logging.INFO,
                         action = 'store_const',
                         const = logging.DEBUG )
    
    parser.add_argument( '--viz',
                         dest = 'create_viz',
                         default = False,
                         action = 'store_true',
                         help = 'Create Plotly vis of file contents' )
    
    parser.add_argument( '--viz-type',
                         dest='viz_type',
                         default = 'dash',
                         help = 'Set the rendering viz mode' )
    
    parser.add_argument( dest = 'nitf_paths',
                         action = 'append',
                         default = [],
                         help = 'List of NITF images to parse.' )

    return parser.parse_args()

def main():

    #  Parse Command-Line Options
    cmd_args = parse_command_line()

    #  Configure the logger
    logger = configure_logging( log_level = cmd_args.log_level,
                                app_name  = 'tmns_nitf_info:main' )

    #  Setup the TRE Factory Builder
    tre_factory = TRE_Factory.default()
    logger.debug( tre_factory )

    #  Setup the Image Driver Factory
    img_factory = Driver_Factory.default()
    logger.debug( img_factory )

    #  Process each NITF in sequence
    for nitf_path in cmd_args.nitf_paths:

        nitf_data = load_nitf( nitf_path, 
                               tre_factory = tre_factory,
                               img_factory = img_factory )

        render_html( nitf_data,
                     logger = logger )
        

def run_command():
    run(main)
