# -*- coding: utf-8 -*-
#
# debbindiff: highlight differences between two builds of Debian packages
#
# Copyright © 2014 Jérémy Bobbio <lunar@debian.org>
#
# debdindiff is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# debbindiff is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with debbindiff.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function
import difflib
import os.path
import sys
from xml.sax.saxutils import escape

HEADER = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="generator" content="pandoc">
  <title>%(title)s</title>
  <style>
    body {
      background: white;
      color: black;
    }
    .footer {
      font-size: small;
    }
    .difference {
      border: solid #ccc 1px;
      background-color:rgba(0,0,0,.1);
      margin: 0.5em;
    }
    .comment {
      font-style: italic;
    }
    .source {
      font-weight: bold;
    }
    table.diff {
      font-size: 10pt;
    }
    %(htmldiff_styles)s
  </style>
</head>
<body>
"""

FOOTER = """
%(htmldiff_legend)s
<div class="footer">Generated by debbindiff</div>
</body>
</html>
"""

MAX_PAGE_SIZE = 100 * 2 ** 10 # 100 kB

class PrintLimitReached(Exception):
    pass

def create_limited_print_func(print_func):
    def limited_print_func(s, force=False):
        if not hasattr(limited_print_func, 'char_count'):
            limited_print_func.char_count = 0
        limited_print_func.char_count += len(s)
        if not force and limited_print_func.char_count >= MAX_PAGE_SIZE:
            raise PrintLimitReached()
        print_func(s)
    return limited_print_func

def output_difference(difference, print_func):
    if not hasattr(output_difference, 'htmldiff'):
        output_difference.htmldiff = difflib.HtmlDiff(wrapcolumn=70)

    print_func("<div class='difference'>")
    try:
        if difference.source1 == difference.source2:
            print_func("<div><span class='source'>%s</div>" % escape(difference.source1))
        else:
            print_func("<div><span class='source'>%s</span> vs.</div>" % escape(difference.source1))
            print_func("<div><span class='source'>%s</span></div>" % escape(difference.source2))
        if difference.comment:
            print_func("<div class='comment'>%s</div>" % escape(difference.comment))
        if difference.lines1 and difference.lines2:
            print_func(output_difference.htmldiff.make_table(
                difference.lines1, difference.lines2,
                context=True, numlines=10))
        for detail in difference.details:
            output_difference(detail, print_func)
    except PrintLimitReached, e:
        # ok let's end it now
        pass
    print_func("</div>", force=True)

def output_html(differences, print_func=None):
    if print_func is None:
        print_func = print
    print_func = create_limited_print_func(print_func)
    try:
        print_func(HEADER % { 'title': escape(' '.join(sys.argv)),
                              'htmldiff_styles': difflib._styles })
        for difference in differences:
            output_difference(difference, print_func)
    except PrintLimitReached, e:
        # ok let's end it now
        print_func("<div class='error'>Max output size reached.</div>", force=True)
        pass
    print_func(FOOTER % { 'htmldiff_legend': difflib._legend }, force=True)
