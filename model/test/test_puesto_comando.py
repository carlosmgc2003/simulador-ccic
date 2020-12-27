from unittest import TestCase

from model import puesto_comando


class TestPuestoComando(TestCase):
    def test_generar_mm_saliente(self):
        test_pc = puesto_comando.PuestoComando()
        test_pc.generar_mm()
        self.assertTrue(len(test_pc.bandeja_salida) > 0, "Mensaje generado")
