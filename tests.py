import unittest
from main import TemplateReservation, TemplateLibrary
from mock import patch


#def test_simple_none(from_, to, book, for_):
 #   with patch.object(TemplateReservation, "__init__", lambda v, w, x, y, z: None):
  #      c = TemplateReservation(None, None, None, None)
   #     c._from = from_
    #    c._to = to
     #   c._book = book
      #  c._for = for_
       # assert c.includes(10) is True

class ReservationTest(TemplateReservation):
    pass


class TestTemplateReservation(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.reserve1 = ReservationTest(10, 24, 'Traja patraci', 'Miska')
        cls.reserve2 = ReservationTest(24, 26, 'Traja patraci', 'Adam')
        cls.reserve3 = ReservationTest(1, 6, 'Traja patraci', 'Katka')
        cls.reserve4 = ReservationTest(10, 15, 'Sherlock Holmes', 'Katka')

    def test_a_init_id(self):
        self.assertEqual(self.reserve1._id, 9)
        self.assertEqual(self.reserve2._id, 10)
        self.assertEqual(self.reserve3._id, 11)
        self.assertEqual(self.reserve4._id, 12)

    def test_b_overlapping(self):
        self.assertEqual(self.reserve1.overlapping(self.reserve2), True)
        self.assertEqual(self.reserve2.overlapping(self.reserve1), True)
        self.assertEqual(self.reserve1.overlapping(self.reserve3), False)
        self.assertEqual(self.reserve3.overlapping(self.reserve1), False)
        self.assertEqual(self.reserve1.overlapping(self.reserve4), False)
        self.assertEqual(self.reserve4.overlapping(self.reserve1), False)

    def test_c_includes(self):
        self.assertEqual(self.reserve1.includes(4), False)
        self.assertEqual(self.reserve1.includes(10), True)
        self.assertEqual(self.reserve1.includes(15), True)
        self.assertEqual(self.reserve1.includes(24), True)
        self.assertEqual(self.reserve1.includes(25), False)

    def test_d_change_for(self):
        self.assertEqual(self.reserve1.change_for('Jano'), None)

    def test_e_identify(self):
        self.assertEqual(self.reserve3.identify(5, 'Traja patraci', 'Katka'), (True, 'ok'))
        self.assertEqual(self.reserve3.identify(7, 'Traja patraci', 'Katka'), (False, 'date'))
        self.assertEqual(self.reserve3.identify(1, 'Trja patraci', 'Katka'), (False, 'book'))
        self.assertEqual(self.reserve3.identify(4, 'Poirot', 'Katka'), (False, 'book'))
        self.assertEqual(self.reserve3.identify(2, 'Traja patraci', 'Adam'), (False, 'for'))
        self.assertEqual(self.reserve1.identify(20, 'Traja patraci', 'Jano'), (True, 'ok'))  # change_for was successful


class LibraryTest(TemplateLibrary):
    pass


class TestTemplateLibrary(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.library = TemplateLibrary()
        cls.library.add_user('Miska')
        cls.library.add_user('Adam')
        cls.library.add_user('Jano')
        cls.library.add_book('Traja patraci')
        cls.library.add_book('Poirot')
        cls.library.add_book('Sherlock')
        cls.library.add_book('Poirot')

    def test_a_add_user(self):
        self.assertEqual(self.library.add_user('Katka'), True)
        self.assertEqual(self.library.add_user('Adam'), False)
        self.assertEqual(self.library.add_user('Katka'), False)

    def test_b_add_book(self):
        self.assertEqual(self.library.add_book('Traja patraci'), None)
        self.assertEqual(self.library.add_book('Poirot'), None)

    def test_c_reserve_book(self):
        self.assertEqual(self.library.reserve_book('Jozo', 'Sherlock', 14, 28), (False, 'user'))
        self.assertEqual(self.library.reserve_book('Adam', 'Sherlock', 20, 19), (False, 'date'))
        self.assertEqual(self.library.reserve_book('Adam', 'Tigri tim', 2, 16), (False, 'book'))
        self.assertEqual(self.library.reserve_book('Jano', 'Sherlock', 5, 10), (True, 0))
        self.assertEqual(self.library.reserve_book('Miska', 'Sherlock', 10, 17), (False, 'quantity'))
        self.assertEqual(self.library.reserve_book('Miska', 'Sherlock', 7, 9), (False, 'quantity'))
        self.assertEqual(self.library.reserve_book('Miska', 'Sherlock', 2, 4), (True, 3))
        self.assertEqual(self.library.reserve_book('Jano', 'Traja patraci', 1, 10), (True, 4))
        self.assertEqual(self.library.reserve_book('Adam', 'Traja patraci', 7, 12), (True, 5))
        self.assertEqual(self.library.reserve_book('Katka', 'Traja patraci', 9, 15), (False, 'quantity'))
        self.assertEqual(self.library.reserve_book('Katka', 'Traja patraci', 11, 14), (True, 7))
        self.assertEqual(self.library.reserve_book('Miska', 'Traja patraci', 12, 17), (False, 'quantity'))

    def test_d_change_reservation(self):
        self.assertEqual(self.library.change_reservation('Miska', 'Sherlock', 3, 'Jozo'), (False, 'user'))
        self.assertEqual(self.library.change_reservation('Miska', 'Sherlock', 10, 'Adam'),
                         (False, 'irrelevant'))  # date
        self.assertEqual(self.library.change_reservation('Miska', 'Traja patraci', 3, 'Adam'),
                         (False, 'irrelevant'))  # book
        self.assertEqual(self.library.change_reservation('Adam', 'Sherlock', 7, 'Jano'), (False, 'irrelevant'))  # user
        self.assertEqual(self.library.change_reservation('Miska', 'Sherlock', 4, 'Adam'), (True, 'ok'))

    def test_e_check_reservation(self):
        self.assertEqual(self.library.check_reservation('Jano', 'Sherlock', 9), True)
        self.assertEqual(self.library.check_reservation('Katka', 'Sherlock', 20), False)  # non-existing
        self.assertEqual(self.library.check_reservation('Jano', 'Sherlock', 12), False)  # date
        self.assertEqual(self.library.check_reservation('Katka', 'Sherlock', 12), False)  # book
        self.assertEqual(self.library.check_reservation('Katka', 'Sherlock', 9), False)  # user
        self.assertEqual(self.library.check_reservation('Miska', 'Sherlock', 3), False)  # changed user
        self.assertEqual(self.library.check_reservation('Adam', 'Sherlock', 3), True)


if __name__ == '__main__':
    unittest.main()
