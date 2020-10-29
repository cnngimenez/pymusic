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

from musical.theory import Note, Chord
from musica.pluckchord import PluckMusic
from typing import Tuple, List
from re import match


class Conversor(object):
    '''
    Convert between a string or a list of notes into a PluckMusic
    '''

    NOTE_REGEX = r'([#A-Za-z]+)(\d?)(\d?)(/(f|ff|mf|mp|p|pp))?'

    def __init__(self, tempo=90):
        self.tempo = tempo
        self.lst_chords = []
        self.lst_notes = []
        self._current_scale = 3
        self._current_duration = 4  # a quarter ("negra" en castellano)
        self._current_dynamic = "mp"

    def _parse_note(self, s: str) -> Tuple[str, int, int, str]:
        '''
        Parse a note string.

        :return: A tuple with the note name + the scale and the length.
            None if it couldn't be interpreted.
        '''
        # Too much code... isn't it? Should I use a new class for this? naaaah!
        result = match(self.NOTE_REGEX, s)

        if result is None:
            # It does not match!
            return None

        if result[2] == "":
            scale = self._current_scale
        else:
            scale = int(result[2])

        if result[3] == "":
            duration = self._current_duration
        else:
            # TODO: A try catch here...
            duration = int(result[3])

        if result[5] == "" or result[5] is None:
            dynamic = self._current_dynamic
        else:
            dynamic = result[5]

        # Keep the scale for the next notes
        self._current_scale = scale
        self._current_duration = duration
        self._current_dynamic = dynamic

        return (result[1], scale, duration, dynamic)

    def _parse_from_list(self, arr: List[str]) -> list:
        return [self._parse_note(note_str) for note_str in arr
                if self._parse_note(note_str) is not None]

    def from_list(self, arr: list):
        self.lst_notes = self._parse_from_list(arr)

    def from_string(self, score: str):
        self.from_list(score.split(" "))

    def chord_from_list(self, arr: list):
        self.lst_chords = self._parse_from_list(arr)

    def chord_from_string(self, chords: str):
        self.chord_from_list(chords.split(" "))

    def get_pluckmusic(self) -> PluckMusic:
        pm = PluckMusic(self.tempo)

        for note in self.lst_notes:
            pm.add_note2(note[0] + str(note[1]), note[2], note[3])
        for chord in self.lst_chords:
            pm.add_chord2(chord[0] + str(note[1]), chord[2], note[3])

        return pm

    def get_lilypond(self) -> str:
        s = "\\version \"2.20.0\"\n{\n"
        for note in self.lst_notes:
            s += note[0]
        s += "\n}"
        return s

    def get_musical_notes(self) -> List[Note]:
        '''
        Return the musical.theory.Note instances.

        Create instances of Note for the melody.
        '''
        return [Note(note_tuple[0]) for note_tuple in self.lst_notes]

    def get_musical_chords(self) -> List[Chord]:
        return [Chord(chord_tuple[0]) for chord_tuple in self.lst_chords]
