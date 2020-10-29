from musica.conversor import Conversor

chords = "C21 G21 C21 G21 "
chords += "C21 G21 C21 G23 C28 C22 "
chords += "G22 C22 G22 C22 G22 a22 D22 G22 "
chords += "C21 G21 C21 G23 C28 C22"

himno = "E32 F34 G34 G34 F34 E34 D34 C34 C34 D34 E34 E33 D38 D32 "
himno += "E32 F34 G34 G34 F34 E34 D34 C34 C34 D34 E34 D33 C38 C32 "
himno += "D32 E34 C34 D34 E38 F38 E34 C34 D34 E38 F38 E34 D34 C34 D34 G22 "
himno += "E32 F34 G34 G34 F34 E34 D34 C34 C34 D34 E34 D33 C38 C32"


c = Conversor(110)
c.from_string(himno)
c.chord_from_string(chords)
c.pluckmusic.render()
c.pluckmusic.play()
