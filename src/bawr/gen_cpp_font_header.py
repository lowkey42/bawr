# Copyright 2021 Frank David Martinez Muñoz
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in 
# the Software without restriction, including without limitation the rights to use, 
# copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
# Software, and to permit persons to whom the Software is furnished to do so, 
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION 
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from pathlib import Path
from datetime import datetime

class CppFontHeader:

    # Config
    name = None
    namespace = None
    constexpr = False
    macros = True
    macro_prefix = 'Icon_'
    source = None

    # Generated
    instance = None
    output = None

    def build(self, env):
        print("[CPP Font Header] Start ...")

        if self.source is None or self.source.instance is None:
            print(f"[CPP Font Header] Invalid source (CppFontHeader.source)")
            return

        instance = self.source.instance
        icons = instance.icons
        build_dir = env.BAWR_OUTPUT_DIR
        self.namespace = self.namespace or 'icons'
        namespace = self.namespace

        header_file = Path(build_dir, self.name or instance.name + "_codes.hpp")
        self.output = header_file
        print(f"[CPP Font Header] {str(header_file)}")
        with open(header_file, 'w') as f:
            f.write(f'#pragma once\n\n')

            if self.macros:
                for glyph in icons:
                    if glyph.code > 0:
                        code = hex(glyph.code)[2:]
                        f.write(f'#define {self.macro_prefix}{glyph.name.upper():<32} "\\u{code}"\n')

            if self.constexpr:
                constexpr = 'constexpr'
            else:
                constexpr = 'const'

            f.write(f'\nnamespace {namespace}\n{{\n')       
            f.write(f'    {constexpr} auto {"font_family":<32} = "{instance.family}";\n')
            f.write(f'    {constexpr} auto {"font_start_code":<32} = {hex(instance.start_code)};\n')
            f.write(f'    {constexpr} auto {"font_end_code":<32} = {hex(instance.end_code)};\n')
            for glyph in icons:
                if glyph.code > 0:
                    code = hex(glyph.code)[2:]
                    f.write(f'    {constexpr} auto {glyph.name:<32} = "\\u{code}";\n')

            f.write('}\n')

