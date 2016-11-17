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

from .formatters.basic             import BasicFormatter
from .formatters.empty             import EmptyLineFormatter
from .formatters.target            import TargetHeaderFormatter
from .formatters.dependency_action import DependencyActionFormatter
from .formatters.compilec          import CompileFormatter
from .formatters.symlink           import SymlinkFormatter
from .formatters.cpheader          import CpHeaderFormatter
from .formatters.pbxcp             import PBXCpFormatter
from .formatters.codesign          import CodeSignFormatter
from .formatters.touch             import TouchFormatter
from .formatters.validate          import ValidateFormatter

from ..Helpers.Logger   import Logger

class LineEvaluator(object):

    def __init__(self) -> None:
        self._formatters = set()
        self._formatters.add(EmptyLineFormatter())
        self._formatters.add(TargetHeaderFormatter())
        self._formatters.add(CompileFormatter())
        self._formatters.add(SymlinkFormatter())
        self._formatters.add(CpHeaderFormatter())
        self._formatters.add(PBXCpFormatter())
        self._formatters.add(CodeSignFormatter())
        self._formatters.add(TouchFormatter())
        self._formatters.add(ValidateFormatter())
        self._formatters.add(DependencyActionFormatter())

    def evaluate_line(self, line_index, lines) -> object:
        line_text = lines[line_index]
        for formatter in self._formatters:
            if formatter.found_match(line_text) is True:
                Logger.write().debug('Matched line %i to formatter: %s' % (line_index, formatter.name))
                return formatter
        return None
