from musica.conversor import Conversor

chords = "C21/mp G C G "
chords += "C G C G23 C28 C22 "
chords += "G C G C G a D G "
chords += "C21/mf G21/mp C21/p G23/pp C28 C22"

himno = "E32/pp F34 G | G/p F E D | C/mp C D E | E33/mf D38 D32 "
himno += "E32/f F34 G | G/ff F E D | C C D E | D33 C38 C32 "
himno += "D32/p E34 C | D/ff E38 F E34 C | D34/p E38 F E34 D | C34/ff D G22 "
himno += "E32/mf F34 G | G34/mp F E D | C34/p C D E | D33/pp C38 C32"


c = Conversor(110)
c.from_string(himno)
c.chord_from_string(chords)
pm = c.get_pluckmusic()
pm.play()
