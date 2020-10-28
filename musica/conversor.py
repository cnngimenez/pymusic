# conversor ---

# Copyright 2020 cnngimenez

# Author: cnngimenez

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pluckchord import PluckMusic
from typing import Array


class Conversor(object):
    """
    Convert between strings or Array of notes into a PluckMusic
    """
    def __init__(self, tempo=90):
        self.pluckmusic = PluckMusic(tempo)

    def _parse_note(self, s: str) -> Tuple[str, int]:
        pass
        
    def from_array(self, arr: Array[str]):
        for notestr in arr:
            note = notestr
            self.pluckmusic.add_note2(note, length)
