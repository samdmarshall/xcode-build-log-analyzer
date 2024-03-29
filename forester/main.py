#!/usr/bin/env python3
# Copyright (c) 2016, Samantha Marshall (http://pewpewthespells.com)
# All rights reserved.
#
# https://github.com/samdmarshall/forester
# 
# Redistribution and use in source and binary forms, with or without modification, 
# are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this 
# list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice, 
# this list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
# 
# 3. Neither the name of Samantha Marshall nor the names of its contributors may 
# be used to endorse or promote products derived from this software without 
# specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. 
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, 
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF 
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR 
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED 
# OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import sys
import argparse
from .version           import __version__ as FORESTER_VERSION
from .Helpers.Logger    import Logger
from .Helpers.Switch    import Switch
from .                  import term

from .xcode.parser      import Parser as Xcode

def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='forester is a tool for parsing Xcode log files and getting more detailed information about a build')
    parser.add_argument(
        'file',
        metavar='<log file>',
        help='path to the log file from Xcode'
    )
    parser.add_argument(
        '--version',
        help='displays the version information',
        action='version',
        version=FORESTER_VERSION
    )
    parser.add_argument(
        '--quiet',
        help='Silences all logging output',
        default=False,
        action='store_true'
    )
    parser.add_argument(
        '--verbose',
        help='Adds verbosity to logging output',
        default=False,
        action='store_true'
    )
    parser.add_argument(
        '--no-ansi',
        help='Disables the ANSI color codes as part of the logger',
        default=False,
        action='store_true'
    )
    parser.add_argument(
        '--debug',
        help=argparse.SUPPRESS,
        default=False,
        action='store_true'
    )
    # -------------------------------------------------------------------------
    # Flags for various types of build logs
    # -------------------------------------------------------------------------
    parser.add_argument(
        '--type',
        help='Specify the type of log file that is given',
        choices=['xcode'],
        required=True,
    )
    
    
    args = parser.parse_args(argv)

    # perform the logging modifications before we do any other operations
    Logger.disableANSI(args.no_ansi)
    Logger.enableDebugLogger(args.debug)
    Logger.isVerbose(args.verbose)
    Logger.isSilent(args.quiet)

    # verify that this is being run in a UTF-8 supported environment
    if term.uses_suitable_locale() is False:
        Logger.write().error('Environment could not be configured to support UTF-8, exiting!')
        sys.exit(1)
    else:
        Logger.write().info('Processing %s log file: %s' % (args.type, args.file))
        for case in Switch(args.type):
            if case('xcode'):
                Xcode(args.file).parse()
                break
            if case():
                break

if __name__ == "__main__": #pragma: no cover
    main()
