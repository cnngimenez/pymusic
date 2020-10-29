# pluckchord.py ---

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

from musical.theory import Chord, Note
from musical.audio import source, playback, save
from math import ceil


class PluckNote:

    DYMANIC_VALUES = {
        'pp': 0.1,
        'p': 0.25,
        'mp': 0.45,
        'mf': 0.65,
        'f': 0.85,
        'ff': 1
    }

    def __init__(self, notename, length, dynamic: str = 'mp'):
        self.notename = notename
        self.length = length
        self.dynamic = dynamic

        if notename == "" or notename[0] == "s":
            self.note = None
        else:
            self.note = Note(notename)

    def get_length_percentage(self) -> float:
        return 4 / self.length

    def get_duration(self, bpm: int) -> float:
        """
        Get the duration of the chord in seconds

        :param bpm: The beats-per-minute a.k.a. tempo.
        """
        return (4 / self.length) * (60 / bpm)

    def render(self, tempo):
        duration = self.get_duration(tempo)
        pluck = source.silence(duration)
        dynamic = self.DYMANIC_VALUES[self.dynamic]

        if self.note is not None:
            pluck += source.pluck(self.note, duration)
        return pluck * dynamic


class PluckChord:
    """
    :author Christian Gimenez:
    :license GPLv3:
    """
    
    # These values colud be different from PluckNote
    DYMANIC_VALUES = {
        'pp': 0.1,
        'p': 0.25,
        'mp': 0.35,
        'mf': 0.5,
        'f': 0.75,
        'ff': 1
    }

    def __init__(self, chordname, length, dynamic: str = 'mp'):
        """
        :param chordname: A string with the chord root note. For example: c3
        :param length: A number: 1, 2, 4, 8, 16, 32, ... 4 means quarter note.
        """
        self.chordname = chordname
        self.length = length
        self.dynamic = dynamic

        if chordname == "" or chordname[0] == "s":
            self.chord = None
        else:
            if chordname[0].islower():
                self.chord = Chord.minor(Note(chordname))
            else:
                self.chord = Chord.major(Note(chordname))

    def get_length_percentage(self) -> float:
        return 4 / self.length

    def get_duration(self, bpm: int) -> float:
        """
        Get the duration of the chord in seconds

        :param bpm: The beats-per-minute a.k.a. tempo.
        """
        return (4 / self.length) * (60 / bpm)

    def render(self, tempo):
        duration = self.get_duration(tempo)
        pluck = source.silence(duration)
        dynamic = self.DYMANIC_VALUES[self.dynamic]

        if self.chord is not None:
            for i in self.chord.notes:
                pluck += source.pluck(i, duration)
        return pluck * dynamic


class PluckMusic:
    """
    :author Christian Gimenez:
    :license GPLv3:
    """

    def __init__(self, tempo: int = 110):
        self._freq = 44100
        self.tempo = tempo
        self.last_render = None
        self.chords = []
        self.notes = []

    def get_beat_duration(self) -> float:
        '''
        Get the duration of each beat in seconds.
        '''
        return 60 / self.tempo

    def add_note(self, note: PluckNote):
        self.notes.append(note)

    def add_note2(self, notename: str, length: int, dynamic: str = 'mp'):
        note = PluckNote(notename, length, dynamic)
        self.notes.append(note)

    def add_chord(self, chord: PluckChord):
        self.chords.append(chord)

    def add_chord2(self, chordname: str, length: float, dynamic: str = 'mp'):
        chord = PluckChord(chordname, length, dynamic)
        self.chords.append(chord)

    def get_duration(self) -> float:
        """
        Return the seconds that the duration of the music in seconds.
        """
        total_chords = 0
        for chord in self.chords:
            total_chords += chord.get_duration(self.tempo)

        total_notes = 0
        for note in self.notes:
            total_notes += note.get_duration(self.tempo)

        return max(total_chords, total_notes)

    def render(self) -> 'numpy.ndarray':
        '''
        Generate the sound data from the chords and notes.

        :return: A numpy.ndarray of bytes. 
        '''
        # Generate a blank music to fill with notes.
        out = source.silence(self.get_duration() + 1)
        print(f"Max. bytes: {len(out)}")

        time = 0
        index = 0
        for chord in self.chords:
            # Get the wave data
            pluck = chord.render(self.tempo)
            print(f"{index}-{index + len(pluck)} {time}: {len(pluck)}")
            # Add it at the correct position
            out[index:index + len(pluck)] += pluck

            # calculate the next position.
            time += chord.get_duration(self.tempo)
            index = ceil(time * self._freq)

        time = 0
        index = 0
        for note in self.notes:
            # Get the wave data
            pluck = note.render(self.tempo)
            print(f"{index}-{index + len(pluck)} {time}: {len(pluck)}")
            # Add it at the correct position
            out[index:index + len(pluck)] += pluck

            # calculate the next position.
            time += note.get_duration(self.tempo)
            index = ceil(time * self._freq)

        self.last_render = out
        return out

    def play(self, renew=False):
        '''
        Play the music data.

        :param renew: Optional (false). Regenerate the sound data?
        '''
        if not renew and self.last_render is not None:
            playback.pyaudio_play(self.last_render)
        else:
            playback.pyaudio_play(self.render())

    def save(self, path: str, renew: bool = False):
        '''
        Save a WAV file with the generated sound data.

        :param path: The WAV file path.
        :param renew: Optional (false by default). Regenerate the sound data?
        '''
        if not renew and self.last_render is not None:
            save.save_wave(self.last_render, path)
        else:
            save.save_wave(self.render(), path)
