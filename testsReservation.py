import unittest
from main import TemplateReservation

class Test_Template_Reservation(unittest.TestCase):
    def setUp(self) -> None:
        self.reserve1 = TemplateReservation(10, 24, 'Traja patraci', 'Miska')
        self.reserve2 = TemplateReservation(24, 26, 'Traja patraci', 'Adam')
        self.reserve3 = TemplateReservation(1, 6, 'Traja patraci', 'Katka')
        self.reserve4 = TemplateReservation(10, 15, 'Sherlock Holmes', 'Katka')

    def test_overlapping(self):
        self.assertEqual(self.reserve1.overlapping(self.reserve2), True)  # last day
        self.assertEqual(self.reserve2.overlapping(self.reserve1), True)  # first day
        self.assertEqual(self.reserve1.overlapping(self.reserve3), False)  # sooner
        self.assertEqual(self.reserve3.overlapping(self.reserve1), False)  # later
        self.assertEqual(self.reserve1.overlapping(self.reserve4), False)  # middle
        self.assertEqual(self.reserve4.overlapping(self.reserve1), False)  # around

    def test_includes(self):
        self.assertEqual(self.reserve1.includes(4), False)  # not, before
        self.assertEqual(self.reserve1.includes(10), True)  # first day
        self.assertEqual(self.reserve1.includes(15), True)  # middle
        self.assertEqual(self.reserve1.includes(24), True)  # last day
        self.assertEqual(self.reserve1.includes(25), False)  # not, after

    def test_change_for(self):
        self.assertEqual(self.reserve1.change_for('Jano'), None)

    def test_identify(self):
        self.assertEqual(self.reserve3.identify(5, 'Traja patraci', 'Katka'), (True, 'ok'))
        self.assertEqual(self.reserve3.identify(7, 'Traja patraci', 'Katka'), (False, 'date'))
        self.assertEqual(self.reserve3.identify(1, 'Trja patraci', 'Katka'), (False, 'book'))    #preklep
        self.assertEqual(self.reserve3.identify(4, 'Poirot', 'Katka'), (False, 'book'))
        self.assertEqual(self.reserve3.identify(2, 'Traja patraci', 'Adam'), (False, 'for'))

    def test_identify_change_identify(self):  # change was successful
        self.assertEqual(self.reserve1.identify(20, 'Traja patraci', 'Miska'), (True, 'ok'))
        self.assertEqual(self.reserve1.change_for('Jano'), None)
        self.assertEqual(self.reserve1.identify(20, 'Traja patraci', 'Jano'), (True, 'ok'))

if __name__ == '__main__':
    unittest.main()