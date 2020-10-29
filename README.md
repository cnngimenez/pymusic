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
