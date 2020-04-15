import unittest
from main import TemplateLibrary
from itertools import count


class MockReserve(object):
    _ids = count(0)
    def __init__(self, from_, to, book, for_):
        self._id = next(self._ids)
        self._from = from_
        self._to = to
        self._book = book
        self._for = for_

    def overlapping(self, other):
        return False

    def includes(self, date):
        return False

    def identify(self, date, book, user):
        return False

    def change_for(self, new_user):
        pass


class Mock_identify(MockReserve):
    def identify(self, date, book, user):
        return True


class Mock_overlapping(MockReserve):
    def overlapping(self, other):
        return True


class Mock_overlapping_includes(Mock_overlapping):
    def includes(self, date):
        return True


class TestTemplateLibrary_Add_Reserve(unittest.TestCase):
    def setUp(self):
        self.library = TemplateLibrary()
        self.library._users = set(['Miska', 'Adam', 'Jano', 'Katka'])
        self.library._books['Traja patraci'] = 2
        self.library._books['Poirot'] = 2
        self.library._books['Sherlock'] = 1
        MockReserve._ids = count(0)  # ids starts from 0

    def test_add_user(self):
        self.assertTrue(self.library.add_user('Anicka'), True)
        self.assertTrue('Anicka' in self.library._users)
        self.assertFalse(self.library.add_user('Adam'), False)

    def test_add_book(self):
        self.assertEqual(self.library.add_book('Traja patraci'), None)
        self.assertEqual(self.library._books['Traja patraci'], 3)

    def test_reserve_book_basic_failures_and_successful(self):
        self.assertEqual(self.library.reserve_book('Jozo', 'Sherlock', 14, 28, MockReserve), (False, 'user'))
        self.assertEqual(self.library.reserve_book('Adam', 'Sherlock', 20, 19, MockReserve), (False, 'date'))
        self.assertEqual(self.library.reserve_book('Adam', 'Tigri tim', 2, 16, MockReserve), (False, 'book'))
        self.assertEqual(self.library.reserve_book('Jano', 'Sherlock', 5, 10, MockReserve), (True, 0))

    def test_quantity_of_books(self):
        self.library._reservations.append(Mock_overlapping_includes(10, 17, 'Sherlock', 'Miska'))
        self.assertEqual(self.library.reserve_book('Jano', 'Sherlock', 10, 17, Mock_overlapping_includes), (False, 'quantity'))

    #def test_reserve_add_reserve(self):                        #replaced by assert check in add functions
    #    self.assertEqual(self.library.reserve_book('Adam', 'New book', 10, 15, MockReserve), (False, 'book'))
    #    self.assertEqual(self.library.add_book('New book'), None)                                                #added problematic book
    #    self.assertEqual(self.library.reserve_book('Adam', 'New book', 10, 15, MockReserve), (True, 0))
    #    self.assertEqual(self.library.reserve_book('Martina', 'Poirot', 10, 15, MockReserve), (False, 'user'))
    #    self.assertEqual(self.library.add_user('Martina'), True)                                                 #added problematic user
    #    self.assertEqual(self.library.reserve_book('Adam', 'Poirot', 10, 15, MockReserve), (True, 1))

    def test_check_existing(self):
        self.library._reservations.append(Mock_identify(2, 4, 'Sherlock', 'Miska'))                                    #always appending due to different mock object - required different behaviout
        self.assertEqual(self.library.check_reservation('Miska', 'Sherlock', 3), True)

    def test_check_non_existing_reservation(self):
        self.library._reservations.append(MockReserve(10, 15, 'Sherlock', 'Miska'))
        self.assertEqual(self.library.check_reservation('Miska', 'Sherlock', 3), False)

    def test_change_existing(self):
        self.library._reservations.append(Mock_identify(2, 7, 'Sherlock', 'Miska'))
        self.assertEqual(self.library.change_reservation('Miska', 'Sherlock', 3, 'Adam'), (True, 'ok'))

    def test_change_nonexisting(self):
        self.library._reservations.append(Mock_identify(5, 12, 'Traja patraci', 'Miska'))
        self.assertEqual(self.library.change_reservation('Miska', 'Sherlock', 10, 'Jozo'), (False, 'user'))

    def test_change_nonexisting_reservation(self):
        self.library._reservations.append(MockReserve(5, 12, 'Traja patraci', 'Miska'))
        self.assertEqual(self.library.change_reservation('Miska', 'Sherlock', 10, 'Adam'), (False, 'irrelevant'))


if __name__ == '__main__':
    unittest.main()
