from musica.conversor import Conversor

himno = "E32 F34 G34 G34 F34 E34 D34 C34 C34 D34 E34 E33 D38 D32 "
himno += "E32 F34 G34 G34 F34 E34 D34 C34 C34 D34 E34 D33 C38 C32 "
himno += "D32 E34 C34 D34 E38 F38 E34 C34 D34 E38 F38 E34 D34 C34 D34 G22"
himno += "E32 F34 G34 G34 F34 E34 D34 C34 C34 D34 E34 D33 C38 C32"


c = Conversor(110)
c.from_string(himno)
c.pluckmusic.play()
