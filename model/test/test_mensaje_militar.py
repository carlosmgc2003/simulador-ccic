from unittest import TestCase
from model import mensaje_militar


class TestMensajeMilitar(TestCase):
    def test_mm(self):
        generator = mensaje_militar.GeneradorMensajes()
        mm = generator.generar_mensaje()
        self.assertTrue(mm.destino == "")
        self.assertTrue(mm.name == "Mensaje Militar")


class TestGeneradorMensajes(TestCase):
    def test_generar_mensaje(self):
        self.fail()

    def test_generar_clasif_seg(self):
        self.fail()

    def test_generar_precedencia(self):
        self.fail()

    def test_determinar_cifrado(self):
        self.fail()
