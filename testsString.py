import unittest
from main import Reservation, Library

class RememberNotPrint(object):
    def my_print(self, string):
        self.string = string

#None in each test is unnecessarz
class TestReservation_Includes_Change_for_identify(unittest.TestCase):
    def setUp(self) -> None:
        self.res1 = Reservation(12, 15, 'Traja patraci', 'Miska', RememberNotPrint)

    def test_includes(self):
        self.res1.includes(14)
        self.assertEqual(self.res1.printer.string, F'Reservation {self.res1._id} includes 14')
        self.res1.includes(17)
        self.assertEqual(self.res1.printer.string, F'Reservation {self.res1._id} does not include 17')

    def test_change_for(self):
        self.res1.change_for('Jano')
        self.assertEqual(self.res1.printer.string, F'Reservation {self.res1._id} moved from {self.res1._for} to Jano')

    def test_identify(self):
        self.res1.identify(10, 'Traja patraci', 'Miska')
        self.assertEqual(self.res1.printer.string, F'Reservation {self.res1._id} is from {self.res1._from} to {self.res1._to} which does not include 10.')
        self.res1.identify(13, 'Sherlock Holmes', 'Miska')
        self.assertEqual(self.res1.printer.string, F'Reservation {self.res1._id} reserves {self.res1._book} not Sherlock Holmes.')
        self.res1.identify(12, 'Traja patraci', 'Jano')
        self.assertEqual(self.res1.printer.string, F'Reservation {self.res1._id} is for {self.res1._for} not Jano.')
        self.res1.identify(15, 'Traja patraci', 'Miska')
        self.assertEqual(self.res1.printer.string, F'Reservation {self.res1._id} is valid Miska of Traja patraci on 15.')

class TestLibrary_Add_User_Init(unittest.TestCase):
    def setUp(self) -> None:
        self.library = Library(RememberNotPrint)
        self.library._users = set(['Miska', 'Adam'])

    def test_init(self):
        self.assertEqual(self.library.printer.string, F'Library created.')

    def test_add_user(self):
        self.library.add_user('Adam')
        self.assertEqual(self.library.printer.string, F'User not created, user with name Adam already exists.')
        self.library.add_user('Jano')
        self.assertEqual(self.library.printer.string, F'User Jano created.')



if __name__ == '__main__':
    unittest.main()
