from itertools import count


class MyPrinter(object):
    def my_print(self, string):
        print(string)

class TemplateReservation(object):
    _ids = count(0)

    def __init__(self, from_, to, book, for_):
        self._id = next(self._ids)
        self._from = from_
        self._to = to
        self._book = book
        self._for = for_
        self._changes = 0  # probably unnecessary variable

    def overlapping(self, other):
        return (self._book == other._book and self._to >= other._from and self._from <= other._to)

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
    def __init__(self, from_, to, book, for_, printer=MyPrinter):
        super().__init__(from_, to, book, for_)
        self.printer = printer()
        string = F'Created a reservation with id {self._id} of {self._book} from {self._from} to {self._to} for {self._for}.'
        self.printer.my_print(string)

    def overlapping(self, other):
        ret = super().overlapping(other)
        str = 'do'
        if not ret:
            str = 'do not'
        string = F'Reservations {self._id} and {other._id} {str} overlap'
        self.printer.my_print(string)
        return ret

    def includes(self, date):
        ret = super().includes(date)
        str = 'includes'
        if not ret:
            str = 'does not include'
        string = F'Reservation {self._id} {str} {date}'
        self.printer.my_print(string)
        return ret

    def identify(self, date, book, for_):
        ret = super().identify(date, book, for_)
        if not ret[0]:
            if ret[1] == 'book':
                string = F'Reservation {self._id} reserves {self._book} not {book}.'
            if ret[1] == 'for':
                string = F'Reservation {self._id} is for {self._for} not {for_}.'
            if ret[1] == 'date':
                string = F'Reservation {self._id} is from {self._from} to {self._to} which does not include {date}.'
        else:
            string = F'Reservation {self._id} is valid {for_} of {book} on {date}.'
        self.printer.my_print(string)
        return ret[0]

    def change_for(self, for_):
        super().change_for(for_)
        string = F'Reservation {self._id} moved from {self._for} to {for_}'
        self.printer.my_print(string)


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

    def reserve_book(self, user, book, date_from, date_to, res_factory=Reservation):
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
    def __init__(self, printer=MyPrinter):
        super().__init__()
        self.printer = printer()
        string = F'Library created.'
        self.printer.my_print(string)

    def add_user(self, name):
        ret = super().add_user(name)
        if not ret:
            string = F'User not created, user with name {name} already exists.'
        else:
            string = F'User {name} created.'
        self.printer.my_print(string)
        return ret

    def add_book(self, name):
        super().add_book(name)
        string = F'Book {name} added. We have {self._books[name]} coppies of the book.'
        self.printer.my_print(string)

    def reserve_book(self, user, book, date_from, date_to, res_factory=Reservation):
        ret = super().reserve_book(user, book, date_from, date_to, res_factory)
        if not ret[0]:
            if ret[1] == 'user':
                string = F'We cannot reserve book {book} for {user} from {date_from} to {date_to}. User does not exist.'
            elif ret[1] == 'date':
                string = F'We cannot reserve book {book} for {user} from {date_from} to {date_to}. Incorrect dates.'
            elif ret[1] == 'book':
                string = F'We cannot reserve book {book} for {user} from {date_from} to {date_to}. We do not have that book.'
            elif ret[1] == 'quantity':
                string = F'We cannot reserve book {book} for {user} from {date_from} to {date_to}. We do not have enough books.'
        else:
            string = F'Reservation {ret[1]} included.'
        self.printer.my_print(string)
        return ret[0]

    def check_reservation(self, user, book, date):
        ret = super().check_reservation(user, book, date)
        str = 'exists'
        if not ret:
            str = 'does not exist'
        string = F'Reservation for {user} of {book} on {date} {str}.'
        self.printer.my_print(string)
        return ret

    def change_reservation(self, user, book, date, new_user):
        ret = super().change_reservation(user, book, date, new_user)
        if not ret[0]:
            if ret[1] == 'irrelevant':
                string = F'Reservation for {user} of {book} on {date} does not exist.'
            if ret[1] == 'user':
                string = F'Cannot change the reservation as {new_user} does not exist.'
        else:
            string = F'Reservation for {user} of {book} on {date} changed to {new_user}.'
        self.printer.my_print(string)
        return ret[0]