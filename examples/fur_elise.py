from musica.conversor import Conversor

# chords = ""

f = open("examples/fur_elise.txt", "r")
notes = f.read()
f.close()

c = Conversor(90)
c.from_string(notes)
# c.chord_from_string(chords)

# --------------------
# Para que escriba la partitura, usar este código.
# Luego, compilar con Lilypond.
#
# s = c.get_lilypond()
# print(s)
# f = open('t.ly', 'w')
# f.write(s)
# f.close()
# --------------------

pm = c.get_pluckmusic()
pm.play()
