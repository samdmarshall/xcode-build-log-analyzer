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

import shlex
from .basic          import BasicFormatter
from .command_parser import commandline_parser
from .               import printer

class CompileFormatter(BasicFormatter):

    def __init__(self) -> None:
        self.name = 'Compile Formatter'
        self._match_string = r'^CompileC .*$'

    def line_span(self, line_index, lines) -> int:
        offset = line_index
        command_line_span_count = super().line_span(line_index, lines)
        if line_index + command_line_span_count < len(lines):
            line_index += command_line_span_count
            line_span_count = 0
            next_line_text = lines[line_index + line_span_count]
            found_additional_lines = next_line_text.startswith('/')
            while next_line_text.startswith('/') is True:
                line_span_count += 1
                next_line_text = lines[line_index + line_span_count]
                while next_line_text.lstrip() != '^':
                    line_span_count += 1
                    next_line_text = lines[line_index + line_span_count]
                line_span_count += 1
                next_line_text += lines[line_index + line_span_count]
            if found_additional_lines is True:
                while next_line_text.endswith('generated.') is not True:
                    line_span_count += 1
                    next_line_text = lines[line_index + line_span_count]
                line_span_count += 1
            command_line_span_count += line_span_count
        print(lines[offset:command_line_span_count])
        return command_line_span_count

    def print(self, lines) -> None:
        _, obj_file_path, source_file_path, variant, archiecture, language, compiler = shlex.split(lines[0])
        _, project_root = shlex.split(lines[1])
        export_lang = lines[2]
        export_path = lines[3]
        compile_line = commandline_parser(lines[4])
        indent_length = printer.PrintAction('Compiling', source_file_path)
        printer.PrintIndent(indent_length, '↳ '+obj_file_path)
        print('')
