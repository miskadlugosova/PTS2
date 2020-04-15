import unittest
from main import TemplateReservation


class Test_Template_Reservation(unittest.TestCase):
    def setUp(self):
        self.reserve1 = TemplateReservation(10, 24, 'Traja patraci', 'Miska')
        self.reserve2 = TemplateReservation(24, 26, 'Traja patraci', 'Adam')
        self.reserve3 = TemplateReservation(1, 6, 'Traja patraci', 'Katka')
        self.reserve4 = TemplateReservation(11, 15, 'Sherlock Holmes', 'Katka')
        self.reserve5 = TemplateReservation(11, 15, 'Traja patraci', 'Katka')
        self.reserve6 = TemplateReservation(7, 14, 'Traja patraci', 'Jano')

    def test_overlapping(self):
        self.assertTrue(self.reserve1.overlapping(self.reserve2))  # last day
        self.assertTrue(self.reserve2.overlapping(self.reserve1))  # first day
        self.assertTrue(self.reserve1.overlapping(self.reserve6))   # cross
        self.assertTrue(self.reserve1.overlapping(self.reserve5))   # middle
        self.assertTrue(self.reserve5.overlapping(self.reserve1))   # around
        self.assertTrue(self.reserve1.overlapping(self.reserve1))   # same
        self.assertFalse(self.reserve1.overlapping(self.reserve3))  # sooner
        self.assertFalse(self.reserve3.overlapping(self.reserve1))  # later
        self.assertFalse(self.reserve1.overlapping(self.reserve4))  # different book

    def test_includes(self):
        self.assertFalse(self.reserve1.includes(4))  # before
        self.assertTrue(self.reserve1.includes(10))  # first day
        self.assertTrue(self.reserve1.includes(15))  # middle
        self.assertTrue(self.reserve1.includes(24))  # last day
        self.assertFalse(self.reserve1.includes(25))  # after

    def test_change_for(self):
        self.assertEqual(self.reserve1.change_for('Jano'), None)
        self.assertEqual(self.reserve1._for, 'Jano')

    def test_identify(self):
        self.assertEqual(self.reserve3.identify(5, 'Traja patraci', 'Katka'), (True, 'ok'))
        self.assertEqual(self.reserve3.identify(7, 'Traja patraci', 'Katka'), (False, 'date'))
        self.assertEqual(self.reserve3.identify(1, 'Trja patraci', 'Katka'), (False, 'book'))    #preklep
        self.assertEqual(self.reserve3.identify(4, 'Poirot', 'Katka'), (False, 'book'))
        self.assertEqual(self.reserve3.identify(2, 'Traja patraci', 'Adam'), (False, 'for'))

    #def test_identify_change_identify(self):  # change was successful                          #replaced by testing change_for by itself
    #    self.assertEqual(self.reserve1.identify(20, 'Traja patraci', 'Miska'), (True, 'ok'))
    #    self.assertEqual(self.reserve1.change_for('Jano'), None)
    #    self.assertEqual(self.reserve1.identify(20, 'Traja patraci', 'Jano'), (True, 'ok'))

if __name__ == '__main__':
    unittest.main()