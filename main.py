from itertools import count
from messages import *


class Reservation(object):
    _ids = count(0)

    def __init__(self, from_, to, book, for_):
        self._id = next(Reservation._ids)
        self._from = from_
        self._to = to
        self._book = book
        self._for = for_
        self._changes = 0
        res_init_message(self._id, self._book, self._from, self._to, self._for)

    def overlapping(self, other):
        ret = (self._book == other._book and self._to >= other._from
               and self._to >= other._from)
        str = 'do'
        if not ret:
            str = 'do not'
        res_overlapping_message(self._id, other._id, str)
        return ret

    def includes(self, date):
        ret = (self._from <= date <= self._to)
        str = 'includes'
        if not ret:
            str = 'does not include'
        res_includes_message(self._id, str, date)
        return ret

    def identify(self, date, book, for_):
        if book != self._book:
            res_identity_message('book', book, for_, date, self)
            return False
        if for_ != self._for:
            res_identity_message('for', book, for_, date, self)
            return False
        if not self.includes(date):
            res_identity_message('includes', book, for_, date, self)
            return False
        res_identity_message('ok', book, for_, date, self)
        return True

    def change_for(self, for_):
        res_change_for_message(self._id, self._for, for_)
        self._for = for_


class Library(object):
    def __init__(self):
        self._users = set()
        self._books = {}  # maps name to count
        self._reservations = []  # Reservations sorted by from
        lib_init_message()

    def add_user(self, name):
        if name in self._users:
            lib_add_user_message(False, name)
            return False
        self._users.add(name)
        lib_add_user_message(True, name)
        return True

    def add_book(self, name):
        self._books[name] = self._books.get(name, 0) + 1
        lib_add_book_message(name, self._books[name])

    def reserve_book(self, user, book, date_from, date_to):
        book_count = self._books.get(book, 0)
        if user not in self._users:
            lib_reserve_book_message('user', book, user, date_from, date_to)
            return False
        if date_from > date_to:
            lib_reserve_book_message('date', book, user, date_from, date_to)
            return False
        if book_count == 0:
            lib_reserve_book_message('count', book, user, date_from, date_to)
            return False
        desired_reservation = Reservation(date_from, date_to, book, user)
        relevant_reservations = [res for res in self._reservations
                                 if desired_reservation.overlapping(res)] + [desired_reservation]
        # we check that if we add this reservation then for every reservation record that starts
        # between date_from and date_to no more than book_count books are reserved.
        for from_ in [res._from for res in relevant_reservations]:
            if desired_reservation.includes(from_):
                if sum([rec.includes(from_) for rec in relevant_reservations]) > book_count:
                    lib_reserve_book_message('not_enough', book, user, date_from, date_to)
                    return False
        self._reservations += [desired_reservation]
        self._reservations.sort(key=lambda x: x._from)  # to lazy to make a getter
        lib_reserve_book_message('ok', book, user, date_from, date_to, desired_reservation._id)
        ##!nechcem posielat vsetky zvysne argumenty!
        return True

    def check_reservation(self, user, book, date):
        res = any([res.identify(date, book, user) for res in self._reservations])
        str = 'exists'
        if not res:
            str = 'does not exist'
        lib_check_reservation_message(user, book, date, str)
        return res

    def change_reservation(self, user, book, date, new_user):
        relevant_reservations = [res for res in self._reservations
                                 if res.identify(date, book, user)]
        if not relevant_reservations:
            lib_change_reservation('reservations', user, book, date, new_user)
            return False
        if new_user not in self._users:
            lib_change_reservation('user', user, book, date, new_user)
            return False

        lib_change_reservation('ok', user, book, date, new_user)
        relevant_reservations[0].change_for(new_user)
        return True