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


class Mock_over_ident(Mock_overlapping):
    def includes(self, date):
        return True


class TestTemplateLibrary_Add_Reserve(unittest.TestCase):
    def setUp(self) -> None:
        self.library = TemplateLibrary()
        self.library._users = set(['Miska', 'Adam', 'Jano', 'Katka'])
        self.library._books['Traja patraci'] = 2
        self.library._books['Poirot'] = 2
        self.library._books['Sherlock'] = 1

#use assertTrue, assertFalse
    def test_add_user(self):
        self.assertEqual(self.library.add_user('Anicka'), True)
        self.assertEqual(self.library.add_user('Adam'), False)
        self.assertEqual(self.library.add_user('Anicka'), False)   #if user was added

    def test_add_book(self):
        self.assertEqual(self.library.add_book('Traja patraci'), None)

#setting count in setup, not everywhere
    def test_reserve_book_basic_failures_and_successful(self):
        MockReserve._ids = count(0)      #ids starts from 0
        self.assertEqual(self.library.reserve_book('Jozo', 'Sherlock', 14, 28, MockReserve), (False, 'user'))
        self.assertEqual(self.library.reserve_book('Adam', 'Sherlock', 20, 19, MockReserve), (False, 'date'))
        self.assertEqual(self.library.reserve_book('Adam', 'Tigri tim', 2, 16, MockReserve), (False, 'book'))
        self.assertEqual(self.library.reserve_book('Jano', 'Sherlock', 5, 10, MockReserve), (True, 0))

#you test correct adding in different test, ou don't have to do it here
    def test_quantity_of_books(self):
        MockReserve._ids = count(0)     #ids start from 0
        self.assertEqual(self.library.reserve_book('Miska', 'Sherlock', 10, 17, Mock_over_ident), (True, 0))
        self.assertEqual(self.library.reserve_book('Jano', 'Sherlock', 10, 17, Mock_over_ident), (False, 'quantity'))

#you can check adds with self.assertEqual(self.library._books[name] = num_of_copies - also the same for users using something like 'name' in set
    def test_reserve_add_reserve(self):
        MockReserve._ids = count (0)    #ids start from 0
        self.assertEqual(self.library.reserve_book('Adam', 'New book', 10, 15, MockReserve), (False, 'book'))
        self.assertEqual(self.library.add_book('New book'), None)                                                #added problematic book
        self.assertEqual(self.library.reserve_book('Adam', 'New book', 10, 15, MockReserve), (True, 0))
        self.assertEqual(self.library.reserve_book('Martina', 'Poirot', 10, 15, MockReserve), (False, 'user'))
        self.assertEqual(self.library.add_user('Martina'), True)                                                 #added problematic user
        self.assertEqual(self.library.reserve_book('Adam', 'Poirot', 10, 15, MockReserve), (True, 1))

#maybe try adding necessary "reservations" in the beginning of every test function, so you don't need so many classes and can test one function in the same class, not in two
class TestTemporaryLibrary_Change_To_Nonexisting_And_Existing_Check_Existing(unittest.TestCase):                    #division with next function necessary due to required mocks
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
        #self.library._users = set(['Miska', 'Adam', 'Jano', 'Katka'])
#you don't need so many reservations
        self.library._reservations = [Mock_overlapping(5, 10, 'Sherlock', 'Jano')] + [
            Mock_overlapping(1, 10, 'Traja patraci', 'Jano')] + [Mock_overlapping(7, 12, 'Traja patraci', 'Adam')] + [
                                         Mock_overlapping(11, 14, 'Traja patraci', 'Katka')]

#you only need indentify to return false here in both
    def test_change_no_relevant(self):
        self.assertEqual(self.library.change_reservation('Miska', 'Sherlock', 10, 'Adam'),
                         (False, 'irrelevant'))

    def test_check_non_existing_reservation(self):
        self.assertEqual(self.library.check_reservation('Miska', 'Sherlock', 3), False)

if __name__ == '__main__':
    unittest.main()
