from musica.conversor import Conversor

chords = "C21/p G C G "
chords += "C G C G23 C28 C22 "
chords += "G C G C G a D G "
chords += "C21 G C G23 C28 C22"

himno = "E32/pp F34 G | G/p F E D | C/mp C D E | E33/mf D38 D32 "
himno += "E32/f F34 G | G/ff F E D | C C D E | D33 C38 C32 "
himno += "D32/p E34 C | D/ff E38 F E34 C | D E38 F E34 D | C D G22 "
himno += "E32/mp F34 G | G F E D | C C D E | D33 C38 C32"


c = Conversor(110)
c.from_string(himno)
c.chord_from_string(chords)
pm = c.get_pluckmusic()
pm.play()
