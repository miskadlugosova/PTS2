import unittest
from main import TemplateReservation

class TestReservation(TemplateReservation):
    pass


class TestTemplateReservation(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.reserve1 = TestReservation (10, 24, 'Traja patraci', 'Miska')
        cls.reserve2 = TestReservation (24, 26, 'Traja patraci', 'Adam')
        cls.reserve3 = TestReservation (1, 6, 'Traja patraci', 'Katka')
        cls.reserve4 = TestReservation (10, 15, 'Sherlock Holmes', 'Katka')

    def test_init_id(self):
        self.assertEqual(self.reserve1._id, 0)
        self.assertEqual(self.reserve2._id, 1)
        self.assertEqual(self.reserve3._id, 2)
        self.assertEqual(self.reserve4._id, 3)

    def test_overlapping(self):
        self.assertEqual(self.reserve1.overlapping(self.reserve2), True)
        self.assertEqual(self.reserve2.overlapping(self.reserve1), True)
        self.assertEqual(self.reserve1.overlapping(self.reserve3), False)
        self.assertEqual(self.reserve3.overlapping(self.reserve1), False)
        self.assertEqual(self.reserve1.overlapping(self.reserve4), True)
        self.assertEqual(self.reserve4.overlapping(self.reserve1), True)

    def test_includes(self):
        self.assertEqual(self.reserve1.includes(4), False)
        self.assertEqual(self.reserve1.includes(10), True)
        self.assertEqual(self.reserve1.includes(15), True)
        self.assertEqual(self.reserve1.includes(24), True)
        self.assertEqual(self.reserve1.includes(25), False)

    def test_change_for(self):
        self.assertEqual(self.reserve1.change_for('Jano'), None)

    def test_identify(self):
        self.assertEqual(self.reserve3.identify(5, 'Traja patraci', 'Katka'), (True, 'ok'))
        self.assertEqual(self.reserve3.identify(7, 'Traja patraci', 'Katka'), (False, 'date'))
        self.assertEqual(self.reserve3.identify(1, 'Trja patraci', 'Katka'), (False, 'book'))
        self.assertEqual(self.reserve3.identify(4, 'Poirot', 'Katka'), (False, 'book'))
        self.assertEqual(self.reserve3.identify(2, 'Traja patraci', 'Adam'), (False, 'for'))
        self.assertEqual(self.reserve1.identify(20, 'Traja patraci', 'Jano'), (True, 'ok'))

if __name__ == '__main__':
    unittest.main()
