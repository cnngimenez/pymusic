from random import randint
from musica.conversor import Conversor

chords = 'C22/p | C E | G G | C E | a C | C'
a_notes = ["B28/mp", "C38/mp", "D38/mp", "E38/mp"]
b_notes = ["F38/f", "G38/f", "A38/f", "B38/f", "G38/f"]


def random_notes(notes, amount):
    # Crear musica
    lst = []
    for i in range(1, 10):
        ran = randint(0, len(notes)-1)
        lst.append(notes[ran])

    return lst


a_part = random_notes(a_notes, 6)
b_part = random_notes(b_notes, 8)

melody = ['C3']
melody += a_part
melody.append("|")
melody += b_part
melody.append("|")
melody += ['C3']
melody += a_part
# finale
melody += ['B2', 'E3', 'D3', 'C3', 'C32']

# repite
melody += melody
chords += chords

print(melody)

# Reproducir
c = Conversor(110)
c.chord_from_string(chords)
c.from_list(melody)
pm = c.get_pluckmusic()
pm.play()
