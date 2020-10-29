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

from musica.pluckchord import PluckMusic
from typing import Tuple
from re import match


class Conversor(object):
    """
    Convert between a string or a list of notes into a PluckMusic
    """
    def __init__(self, tempo=90):
        self.pluckmusic = PluckMusic(tempo)

    def _parse_note(self, s: str) -> Tuple[str, int]:
        result = match(r'([#\w]{1,3}\d)(\d)', s)
        return (result[1], int(result[2]))

    def _parse_from_list(self, arr: list) -> list:
        lst = []
        for note_str in arr:
            note = self._parse_note(note_str)
            lst.append(note)
        return lst

    def from_list(self, arr: list):
        lst_notes = self._parse_from_list(arr)
        print(lst_notes)
        for note in lst_notes:
            self.pluckmusic.add_note2(note[0], note[1])

    def from_string(self, score: str):
        self.from_list(score.split(" "))

    def chord_from_list(self, arr: list):
        lst_chords = self._parse_from_list(arr)
        for chord in lst_chords:
            self.pluckmusic.add_chord2(chord[0], chord[1])

    def chord_from_string(self, chords: str):
        self.chord_from_list(chords.split(" "))
