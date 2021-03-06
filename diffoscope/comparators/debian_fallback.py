# -*- coding: utf-8 -*-
#
# diffoscope: in-depth comparison of files, archives, and directories
#
# Copyright © 2015 Jérémy Bobbio <lunar@debian.org>
#
# diffoscope is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# diffoscope is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with diffoscope.  If not, see <https://www.gnu.org/licenses/>.

from .text import TextFile


class DotChangesFile(TextFile):
    FILE_EXTENSION_SUFFIX = '.changes'

    def compare(self, other, *args, **kwargs):
        difference = super().compare(other, *args, **kwargs)
        if not difference:
            return None
        difference.add_comment('Unable to find Python debian module. Falling back to text comparison.')
        return difference


class DotDscFile(TextFile):
    FILE_EXTENSION_SUFFIX = '.dsc'

    def compare(self, other, *args, **kwargs):
        difference = super().compare(other, *args, **kwargs)
        if not difference:
            return None
        difference.add_comment('Unable to find Python debian module. Falling back to text comparison.')
        return difference


class DotBuildinfoFile(TextFile):
    FILE_EXTENSION_SUFFIX = '.buildinfo'

    def compare(self, other, *args, **kwargs):
        difference = super().compare(other, *args, **kwargs)
        if not difference:
            return None
        difference.add_comment('Unable to find Python debian module. Falling back to text comparison.')
        return difference
