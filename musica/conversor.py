# conversor.py ---

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

    NOTE_REGEX = r'([#A-Za-z]+)(\d?)(\d+)?(/(ff|f|mf|mp|pp|p))?(\!(\w+))?'

    NOTE_NAMES = {
        'DO': 'C', 'RE': 'D', 'MI': 'E', 'FA': 'F',
        'SOL': 'G', 'LA': 'A', 'SI': 'B',
        'do': 'c', 're': 'd', 'mi': 'e', 'fa': 'f',
        'sol': 'g', 'la': 'a', 'si': 'b'
    }

    def __init__(self, tempo=90):
        self.tempo = tempo
        self.lst_chords = []
        self.lst_notes = []
        self._current_scale = 3
        self._current_duration = 4  # a quarter ("negra" en castellano)
        self._current_dynamic = "mp"
        self._current_wave = "pluck"

    def _parse_note(self, s: str) -> Tuple[str, int, int, str, str]:
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
        print(s, result.groups())
        if result[2] == "":
            scale = self._current_scale
        else:
            scale = int(result[2])

        if result[3] == "" or result[3] is None:
            duration = self._current_duration
        else:
            # TODO: A try catch here...
            duration = int(result[3])

        if result[5] == "" or result[5] is None:
            dynamic = self._current_dynamic
        else:
            dynamic = result[5]

        if result[7] == "" or result[7] is None:
            wave = self._current_wave
        else:
            wave = result[7]

        # Keep the scale for the next notes
        self._current_scale = scale
        self._current_duration = duration
        self._current_dynamic = dynamic
        self._current_wave = wave

        if result[1] in self.NOTE_NAMES:
            notename = self.NOTE_NAMES[result[1]]
        else:
            notename = result[1]

        return (notename, scale, duration, dynamic, wave)

    def _parse_from_list(self, arr: List[str]) -> list:
        return [self._parse_note(note_str) for note_str in arr
                if self._parse_note(note_str) is not None]

    def from_list(self, arr: list):
        self.lst_notes = self._parse_from_list(arr)

    def from_string(self, score: str):
        if (score[0:3].isdecimal()):
            self.tempo = int(score[0:3])
            score = score[3:]

        s = score.replace("\n", " ")
        self.from_list(s.split(" "))

    def chord_from_list(self, arr: list):
        self.lst_chords = self._parse_from_list(arr)

    def chord_from_string(self, chords: str):
        s = chords.replace("\n", " ")
        self.chord_from_list(s.split(" "))

    def get_pluckmusic(self) -> PluckMusic:
        pm = PluckMusic(self.tempo)

        for note in self.lst_notes:
            pm.add_note2(note[0] + str(note[1]), note[2], note[3], note[4])
        for chord in self.lst_chords:
            pm.add_chord2(chord[0] + str(chord[1]), chord[2], chord[3],
                          chord[4])

        return pm

    def _get_lilynote(self, note: Tuple) -> str:
        s = note[0].lower()  # note
        s += "'" * (note[1] - 2)  # pitch
        # duration
        if note[2] in [1, 2, 4, 8, 16, 32, 64]:
            s += str(note[2])
        return s

    def _get_lilychord(self, chord: Tuple) -> str:
        s = chord[0].lower()  # note
        # duration
        if chord[2] in [1, 2, 4, 8, 16, 32, 64]:
            s += str(chord[2])

        if chord[0].islower():
            s += ":m"

        return s

    def get_lilypond(self) -> str:
        s = "\\version \"2.20.0\"\n{\n"
        s += f"\\tempo 4 = {self.tempo}\n"

        s += '\n<<\n'

        s += '\n{\n'
        for note in self.lst_notes:
            s += self._get_lilynote(note) + " "
        s += '\n}\n'

        s += "\n\\chords{\n"
        for chord in self.lst_chords:
            s += self._get_lilychord(chord) + " "
        s += "\n}"

        s += '\n>>\n'
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


def tocar_cancion(cancion: str,
                  tempo: int = 90,
                  chords: str = "") -> Conversor:
    '''
    Tocar la canción con el tempo designado.

    Interpretar el string en notas musicales y generar los sonidos. Luego,
    reproducir el audio.
    :param cancion: El string con las partitura.
    :param tempo: El tiempo (bps) de la canción. Por defecto es 90.
    '''
    c = Conversor(tempo)
    c.from_string(cancion)
    c.chord_from_string(chords)
    pm = c.get_pluckmusic()
    pm.play()
    return c


def guardar_cancion(path: str,
                    cancion: str,
                    tempo: int = 90,
                    chords: str = "") -> Conversor:
    c = Conversor(tempo)
    c.from_string(cancion)
    c.chord_from_string(chords)
    pm = c.get_pluckmusic()
    pm.save(path)
    return c


def generar_lilypond(path: str,
                     cancion: str,
                     tempo: int = 90,
                     chords: str = "") -> Conversor:
    c = Conversor(tempo)
    c.from_string(cancion)
    c.chord_from_string(chords)
    s = c.get_lilypond()
    f = open(path, 'w')
    f.write(s)
    f.close()
    return c
