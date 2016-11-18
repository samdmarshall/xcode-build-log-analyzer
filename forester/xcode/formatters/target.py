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

import re
import shutil
from .basic         import BasicFormatter
from .              import printer

class TargetHeaderFormatter(BasicFormatter):

    def __init__(self) -> None:
        self.name = 'Target Header Formatter'
        self._match_string = r'^=== [A-Z]+ TARGET [a-zA-Z0-9_-]+ OF PROJECT [a-zA-Z0-9_-]+ .* ===$'

    def print(self, lines) -> None:
        output = lines[0].strip('=== ')

        action = None
        target = None
        project = None
        configuration = None

        result = re.search('^(.+?) TARGET ', output)
        if result is not None:
            action = result.group(1)
        result = re.search(' TARGET (.+?) OF ', output)
        if result is not None:
            target = result.group(1)
        result = re.search(' PROJECT (.+?) WITH ', output)
        if result is not None:
            project = result.group(1)
        result = re.search(' CONFIGURATION (.+?)$', output)
        if result is not None:
            configuration = result.group(1)

        print('-'*shutil.get_terminal_size().columns)
        printer.PrintAction('Xcode Action', action)
        printer.PrintIndent(2, 'Project: '+project)
        printer.PrintIndent(2, 'Target: '+target)
        printer.PrintIndent(2, 'Configuration: '+configuration)
        print('')