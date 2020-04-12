from itertools import count

class MyPrinter(object):
    def my_printer(self, string):
        print(string)

class TemplateReservation(object):
    _ids = count(0)

    def __init__(self, from_, to, book, for_):
        self._id = next(self._ids)
        self._from = from_
        self._to = to
        self._book = book
        self._for = for_
        self._changes = 0  #probably unnecessary variable

    def overlapping(self, other):
        return (self._book == other._book and self._to >= other._from
                and self._to >= other._from)

    def includes(self, date):
        return (self._from <= date <= self._to)

    def identify(self, date, book, for_):
        if book != self._book:
            return (False, 'book')
        if for_ != self._for:
            return (False, 'for')
        if not self.includes(date):
            return (False, 'date')
        return (True, 'ok')

    def change_for(self, for_):
        self._for = for_


class Reservation(TemplateReservation):
    def __init__(self, from_, to, book, for_, printer = MyPrinter):
        super().__init__(from_, to, book, for_)
        self.printer = printer
        print(F'Created a reservation with id {self._id} of {self._book} ' +
              F'from {self._from} to {self._to} for {self._for}.')

    def overlapping(self, other):
        ret = super().overlapping(other)
        str = 'do'
        if not ret:
            str = 'do not'
        print(F'Reservations {self._id} and {other._id} {str} overlap')
        return ret

    def includes(self, date):
        ret = super().includes(date)
        str = 'includes'
        if not ret:
            str = 'does not include'
        print(F'Reservation {self._id} {str} {date}')
        return ret;

    def identify(self, date, book, for_):
        ret = super().identify(date, book, for_)
        if not ret[0]:
            if ret[1] == 'book':
                print(F'Reservation {self._id} reserves {self._book} not {book}.')
            if ret[1] == 'for':
                print(F'Reservation {self._id} is for {self._for} not {for_}.')
            if ret[1] == 'date':
                print(F'Reservation {self._id} is from {self._from} to {self._to} which ' +
                      F'does not include {date}.')
        else:
            print(F'Reservation {self._id} is valid {for_} of {book} on {date}.')
        return ret[0]

    def change_for(self, for_):
        super().change_for(for_)
        print(F'Reservation {self._id} moved from {self._for} to {for_}')


class TemplateLibrary(object):
    def __init__(self):
        self._users = set()
        self._books = {}  # maps name to count
        self._reservations = []  # Reservations sorted by from

    def add_user(self, name):
        if name in self._users:
            return False
        self._users.add(name)
        return True

    def add_book(self, name):
        self._books[name] = self._books.get(name, 0) + 1

    def reserve_book(self, user, book, date_from, date_to, res_factory = Reservation):
        book_count = self._books.get(book, 0)
        if user not in self._users:
            return (False, 'user')
        if date_from > date_to:
            return (False, 'date')
        if book_count == 0:
            return (False, 'book')
        desired_reservation = res_factory(date_from, date_to, book, user)
        relevant_reservations = [res for res in self._reservations
                                 if desired_reservation.overlapping(res)] + [desired_reservation]
        # we check that if we add this reservation then for every reservation record that starts
        # between date_from and date_to no more than book_count books are reserved.
        for from_ in [res._from for res in relevant_reservations]:
            if desired_reservation.includes(from_):
                if sum([rec.includes(from_) for rec in relevant_reservations]) > book_count:
                    return (False, 'quantity')
        self._reservations += [desired_reservation]
        self._reservations.sort(key=lambda x: x._from)  # to lazy to make a getter
        return (True, desired_reservation._id)

    def check_reservation(self, user, book, date):
        res = any([res.identify(date, book, user) for res in self._reservations])
        return res

    def change_reservation(self, user, book, date, new_user):
        relevant_reservations = [res for res in self._reservations
                                 if res.identify(date, book, user)]
        if not relevant_reservations:
            return (False, 'irrelevant')
        if new_user not in self._users:
            return (False, 'user')
        relevant_reservations[0].change_for(new_user)
        return (True, 'ok')


class Library(TemplateLibrary):
    def __init__(self, printer = MyPrinter):
        super().__init__()
        self.printer = printer
        print(F'Library created.')

    def add_user(self, name):
        ret = super().add_user(name)
        if not ret:
            print(F'User not created, user with name {name} already exists.')
        else:
            print(F'User {name} created.')
        return ret

    def add_book(self, name):
        super().add_book(name)
        print(F'Book {name} added. We have {self._books[name]} coppies of the book.')

    def reserve_book(self, user, book, date_from, date_to, res_factory = Reservation):
        ret = super().reserve_book(user, book, date_from, date_to, res_factory)
        if not ret[0]:
            if ret[1] == 'user':
                print(F'We cannot reserve book {book} for {user} from {date_from} to {date_to}. ' +
                      F'User does not exist.')
            elif ret[1] == 'date':
                print(F'We cannot reserve book {book} for {user} from {date_from} to {date_to}. ' +
                      F'Incorrect dates.')
            elif ret[1] == 'book':
                print(F'We cannot reserve book {book} for {user} from {date_from} to {date_to}. ' +
                      F'We do not have that book.')
            elif ret[1] == 'quantity':
                print(F'We cannot reserve book {book} for {user} from {date_from} ' +
                      F'to {date_to}. We do not have enough books.')
        else:
            print(F'Reservation {ret[1]} included.')
        return ret[0]

    def check_reservation(self, user, book, date):
        ret = super().check_reservation(user, book, date)
        str = 'exists'
        if not ret:
            str = 'does not exist'
        print(F'Reservation for {user} of {book} on {date} {str}.')
        return ret

    def change_reservation(self, user, book, date, new_user):
        ret = super().change_reservation(user, book, date, new_user)
        if not ret[0]:
            if ret[1]=='irrelevant':
                print(F'Reservation for {user} of {book} on {date} does not exist.')
            if ret[1] == 'user':
                print(F'Cannot change the reservation as {new_user} does not exist.')
        else:
            print(F'Reservation for {user} of {book} on {date} changed to {new_user}.')
        return ret[0]