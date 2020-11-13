# Crear música desde Python.

# Requerimientos 

Para instalar las dependencias en el sistema:

```
pip install -r requirements.txt
```

Si se desea instalar en el usuario:

```
pip install --user  -r requirements.txt
```

# Uso

```python
from musica.conversor import Conversor

c = Conversor()
c.from_string("C34 D34 E34 F34 G34 A34 B34 C34")
c.pluckmusic.play()
```

Las notas tienen el siguiente formato:

`C#316/ff!pluck`

- `C#` es do sostenido. Puede escribirse `DO#`. `s` o `S` significa silencio. En el caso de los acordes, es sensible a las mayúsculas: `do#` es do# menor, `DO#` es do# mayor.
- `3` es la escala.
- `16` es la duración: 1 redonda, 2 blanca, 4 negra, 8 corchea, 16 semicorchea
- `/ff` es el volumen o dinámica. Acepta: ff, f, mf, mp, p, pp.
- `!pluck` es la forma de la onda a generar. Acepta: pluck, square, sine, sawtooth.
