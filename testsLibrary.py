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


class Mock_over_ident(MockReserve):
    def overlapping(self, other):
        return True

    def includes(self, date):
        return True


class TestTemplateLibrary_Add_Reserve(unittest.TestCase):
    def setUp(self) -> None:
        self.library = TemplateLibrary()
        self.library._users = set(['Miska', 'Adam', 'Jano', 'Katka'])
        self.library._books['Traja patraci'] = 2
        self.library._books['Poirot'] = 2
        self.library._books['Sherlock'] = 1

    def test_a_add_user(self):
        self.assertEqual(self.library.add_user('Anicka'), True)
        self.assertEqual(self.library.add_user('Adam'), False)
        self.assertEqual(self.library.add_user('Anicka'), False)

    def test_b_add_book(self):
        self.assertEqual(self.library.add_book('Traja patraci'), None)
        self.assertEqual(self.library.add_book('Poirot'), None)

    def test_c_reserve_book_basic_failures_and_successful(self):
        MockReserve._ids = count(0)
        self.assertEqual(self.library.reserve_book('Jozo', 'Sherlock', 14, 28, MockReserve), (False, 'user'))
        self.assertEqual(self.library.reserve_book('Adam', 'Sherlock', 20, 19, MockReserve), (False, 'date'))
        self.assertEqual(self.library.reserve_book('Adam', 'Tigri tim', 2, 16, MockReserve), (False, 'book'))
        self.assertEqual(self.library.reserve_book('Jano', 'Sherlock', 5, 10, MockReserve), (True, 0))


    def test_quantity_of_books(self):
        MockReserve._ids = count(0)
        self.assertEqual(self.library.reserve_book('Miska', 'Sherlock', 10, 17, Mock_over_ident), (True, 0))
        self.assertEqual(self.library.reserve_book('Jano', 'Sherlock', 10, 17, Mock_over_ident), (False, 'quantity'))
        # self.assertEqual(self.library.reserve_book('Miska', 'Sherlock', 7, 9, M), (False, 'quantity'))
        # self.assertEqual(self.library.reserve_book('Miska', 'Sherlock', 2, 4), (True, 3))
        # self.assertEqual(self.library.reserve_book('Jano', 'Traja patraci', 1, 10), (True, 4))
        # self.assertEqual(self.library.reserve_book('Adam', 'Traja patraci', 7, 12), (True, 5))
        # self.assertEqual(self.library.reserve_book('Katka', 'Traja patraci', 9, 15), (False, 'quantity'))
        # self.assertEqual(self.library.reserve_book('Katka', 'Traja patraci', 11, 14), (True, 7))
        # self.assertEqual(self.library.reserve_book('Miska', 'Traja patraci', 12, 17), (False, 'quantity'))

    def test_d_reserve_add_reserve(self):
        MockReserve._ids = count (0)
        self.assertEqual(self.library.reserve_book('Adam', 'New book', 10, 15, MockReserve), (False, 'book'))
        self.assertEqual(self.library.add_book('New book'), None)
        self.assertEqual(self.library.reserve_book('Adam', 'New book', 10, 15, MockReserve), (True, 0))
        self.assertEqual(self.library.reserve_book('Martina', 'Poirot', 10, 15, MockReserve), (False, 'user'))
        self.assertEqual(self.library.add_user('Martina'), True)
        self.assertEqual(self.library.reserve_book('Adam', 'Poirot', 10, 15, MockReserve), (True, 1))


class TestTempLib_Change_To_Nonexisting_And_Existing_Check_Existing(unittest.TestCase):
    def setUp(self) -> None:
        self.library = TemplateLibrary()
        self.library._users = set(['Miska', 'Adam'])
        self.library._reservations += [Mock_identify(2, 4, 'Sherlock', 'Miska')]

    def test_nonexisting(self):
        self.assertEqual(self.library.change_reservation('Miska', 'Sherlock', 3, 'Jozo'), (False, 'user'))

    def test_existing(self):
        self.assertEqual(self.library.change_reservation('Micka', 'Sherlock', 3, 'Adam'), (True, 'ok'))

    def test_check(self):
        self.assertEqual(self.library.check_reservation('Miska', 'Sherlock', 3), True)


class TestTemplateLibrary_Change_With_No_Relevant_Reservation_Check_Non_Existing_Reservation(unittest.TestCase):
    def setUp(self) -> None:
        self.library = TemplateLibrary()
        self.library._users = set(['Miska', 'Adam', 'Jano', 'Katka'])
        self.library._books['Traja patraci'] = 2
        self.library._books['Poirot'] = 2
        self.library._books['Sherlock'] = 1
        self.library._reservations = [Mock_overlapping(5, 10, 'Sherlock', 'Jano')] + [
            Mock_overlapping(1, 10, 'Traja patraci', 'Jano')] + [Mock_overlapping(7, 12, 'Traja patraci', 'Adam')] + [
                                         Mock_overlapping(11, 14, 'Traja patraci', 'Katka')]

    def test_d_change_reservation(self):
        self.assertEqual(self.library.change_reservation('Miska', 'Sherlock', 10, 'Adam'),
                         (False, 'irrelevant'))  # date
        # self.assertEqual(self.library.change_reservation('Miska', 'Traja patraci', 3, 'Adam'),
        #                (False, 'irrelevant'))  # book
        # self.assertEqual(self.library.change_reservation('Adam', 'Sherlock', 7, 'Jano'),
        #                (False, 'irrelevant'))  # user

    def test_e_check_reservation(self):
        self.assertEqual(self.library.check_reservation('Miska', 'Sherlock', 3), False)
        # self.assertEqual(self.library.check_reservation('Katka', 'Sherlock', 20), False)  # non-existing
        # self.assertEqual(self.library.check_reservation('Jano', 'Sherlock', 12), False)  # date
        # self.assertEqual(self.library.check_reservation('Katka', 'Sherlock', 12), False)  # book
        # self.assertEqual(self.library.check_reservation('Katka', 'Sherlock', 9), False)  # user

    # def test_f_check_change_check(self):
    #   self.assertEqual(self.library.check_reservation('Miska', 'Sherlock', 3), True)
    #   self.assertEqual(self.library.change_reservation('Miska', 'Sherlock', 4, 'Adam'), (True, 'ok'))
    #   self.assertEqual(self.library.check_reservation('Miska', 'Sherlock', 3), False)


if __name__ == '__main__':
    unittest.main()
