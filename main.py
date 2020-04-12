from itertools import count


class TemplateReservation:

    def __init__(self, from_, to, book, for_):
        self._from = from_
        self._to = to
        self._book = book
        self._for = for_
        self._changes = 0

    def overlapping(self, other):
        return (self._book == other._book and self._to >= other._from
                and self._to >= other._from)

    def includes(self, date):
        return (self._from <= date <= self._to)

    def identify(self, date, book, for_):
        if book != self._book:
            return False
        if for_ != self._for:
            return False
        if not self.includes(date):
            return False
        return True

    def change_for(self, for_):
        self._for = for_


class Reservation(TemplateReservation):
    _ids = count(0)

    def __init__(self, from_, to, book, for_):
        super(Reservation, self).__init__(from_, to, book, for_)
        self._id = next(Reservation._ids)
        print(F'Created a reservation with id {self._id} of {self._book} ' +
              F'from {self._from} to {self._to} for {self._for}.')

    def overlapping(self, other):
        ret = super(Reservation, self).overlapping(other)
        str = 'do'
        if not ret:
            str = 'do not'
        print(F'Reservations {self._id} and {other._id} {str} overlap')
        return ret

    def includes(self, date):
        ret = super(Reservation, self).includes(date)
        str = 'includes'
        if not ret:
            str = 'does not include'
        print(F'Reservation {self._id} {str} {date}')
        return ret;

    def identify(self, date, book, for_):
        ret = super(Reservation, self).identify(date, book, for_)
        if book != self._book:
            print(F'Reservation {self._id} reserves {self._book} not {book}.')
        if for_ != self._for:
            print(F'Reservation {self._id} is for {self._for} not {for_}.')
        if not self.includes(date):
            print(F'Reservation {self._id} is from {self._from} to {self._to} which ' +
                  F'does not include {date}.')
        print(F'Reservation {self._id} is valid {for_} of {book} on {date}.')
        return ret

    def change_for(self, for_):
        print(F'Reservation {self._id} moved from {self._for} to {for_}')
        super


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

    def reserve_book(self, user, book, date_from, date_to):
        book_count = self._books.get(book, 0)
        if user not in self._users:
            return (False, 'user')
        if date_from > date_to:
            return (False, 'date')
        if book_count == 0:
            return (False, 'book')
        desired_reservation = Reservation(date_from, date_to, book, user)
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
        return (True, desired_reservation)

    def check_reservation(self, user, book, date):
        res = any([res.identify(date, book, user) for res in self._reservations])
        return res

    def change_reservation(self, user, book, date, new_user):
        relevant_reservations = [res for res in self._reservations
                                 if res.identify(date, book, user)]
        if not relevant_reservations:
            return False
        if new_user not in self._users:
            return False
        relevant_reservations[0].change_for(new_user)
        return True


class Library(TemplateLibrary):
    def __init__(self):
        super(Library, self).__init__()
        print(F'Library created.')

    def add_user(self, name):
        res = super(Library, self).add_user(name)
        if name in self._users:
            print(F'User not created, user with name {name} already exists.')
        print(F'User {name} created.')
        return res

    def add_book(self, name):
        super(Library, self).add_book(name)
        print(F'Book {name} added. We have {self._books[name]} coppies of the book.')

    def reserve_book(self, user, book, date_from, date_to):
        res = super(Library, self).reserve_book(user, book, date_from, date_to)
        if (res[0] == False):
            if (res[1] == 'user'):
                print(F'We cannot reserve book {book} for {user} from {date_from} to {date_to}. ' +
                      F'User does not exist.')
            elif (res[1] == 'date'):
                print(F'We cannot reserve book {book} for {user} from {date_from} to {date_to}. ' +
                      F'Incorrect dates.')
            elif (res[1] == 'book'):
                print(F'We cannot reserve book {book} for {user} from {date_from} to {date_to}. ' +
                      F'We do not have that book.')
            elif (res[1] == 'quantity'):
                print(F'We cannot reserve book {book} for {user} from {date_from} ' +
                      F'to {date_to}. We do not have enough books.')
            else:
                print("Unpredicted problem")
        elif (res[1] == True):
            print(F'Reservation {res[1].__id} included.')
        else:
            print("Unpredicted problem")
        return res[0]

    def check_reservation(self, user, book, date):
        res = super(Library, self).check_reservation(user, book, date)
        str = 'exists'
        if not res:
            str = 'does not exist'
        print(F'Reservation for {user} of {book} on {date} {str}.')
        return res

    def change_reservation(self, user, book, date, new_user):
        res = super(Library, self).change_reservation(user, book, date, new_user)
        relevant_reservations = [res for res in self._reservations
                                 if res.identify(date, book, user)]
        if not relevant_reservations:
            print(F'Reservation for {user} of {book} on {date} does not exist.')
        if new_user not in self._users:
            print(F'Cannot change the reservation as {new_user} does not exist.')
        print(F'Reservation for {user} of {book} on {date} changed to {new_user}.')
        relevant_reservations[0].change_for(new_user)
        return res


a = Library()
b = Reservation(10, 12, "kniha", "mna")
b.includes(9)
b.includes(11)
