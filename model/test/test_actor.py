from unittest import *

from model import Actor


class TestActor(TestCase):
    def test_empty_name(self):
        with self.assertRaises(ValueError) as cm:
            _ = Actor("")
            self.assertTrue("No se puede utilizar la cadena nula" in str(cm.exception))

