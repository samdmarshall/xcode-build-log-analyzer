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
from ..Helpers.Logger     import Logger
from .eval                import LineEvaluator

class Parser(object):

    def __init__(self) -> None:
        self._lines = list()

    def consume_log_file(self, file_path) -> None:
        if os.path.exists(file_path) is True:
            Logger.write().debug('Found a file at path "%s"' % file_path)

            Logger.write().debug('Opening log file...')
            file_descriptor = open(file_path, 'r')

            Logger.write().debug('Reading log file...')
            self._lines = file_descriptor.read().splitlines()
            
            Logger.write().debug('Closing log file...')
            file_descriptor.close()
        else:
            Logger.write().error('No file found at path "%s"' % file_path)

    def parse(self) -> None:
        line_count = len(self._lines)
        if line_count > 0:
            Logger.write().debug('Starting LineEvaluator...')
            eval = LineEvaluator()

            line_matches = list()
            
            Logger.write().info('Parsing log file...')
            line_index = 0
            while line_index < line_count:
                Logger.write().info('Parsing line %i...' % line_index)
                line_text = self._lines[line_index]
                
                Logger.write().debug('Parsing line: "%s"' % line_text)
                formatter = eval.evaluate_line(line_index, self._lines)
                if formatter is not None:
                    line_matches.append((line_index, formatter))
                line_index += 1
            Logger.write().info('Grouping commands...')
            line_groups = list()
            group_index = 0
            first_entry = line_matches[0]
            line_groups.append((self._lines[:first_entry[0]], first_entry[1]))
            while group_index < (len(line_matches) - 1):
                entry = line_matches[group_index]
                next_entry = line_matches[group_index + 1]
                line_groups.append((self._lines[entry[0]:next_entry[0]], entry[1]))
                group_index += 1
            last_entry = line_matches[-1]
            line_groups.append((self._lines[last_entry[0]:], last_entry[1]))
            for grouping in line_groups:
                grouped_lines, formatter = grouping
                action = grouped_lines[0].split(' ')[0]
                if len(action) > 0:
                    Logger.write().critical('Action "%s" encountered' % action)
                formatter.print(grouped_lines)
                
        else:
            Logger.write().error('Log file appears to be empty!')
