# test_app.py
import pytest
from hello import app 

def test_app_syntax():
    # Si el código tiene errores de sintaxis o nombres locos fuera de funciones,
    # este import fallará y el test no pasará.
    assert app is not None