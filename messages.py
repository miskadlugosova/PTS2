def res_init_message(self_id, self_book, self_from, self_to, self_for):
    print(F'Created a reservation with id {self_id} of {self_book} from {self_from} to {self_to} for {self_for}.')

def res_overlapping_message(self_id, other_id, str):
    print(F'Reservations {self_id} and {other_id} {str} overlap')

def res_includes_message(self_id, str, date):
    print(F'Reservation {self_id} {str} {date}')

def res_identity_book_message(self_id, self_book, book):
    print(F'Reservation {self_id} reserves {self_book} not {book}.')

def res_identity_for_message(self_id, self_for, for_):
    print(F'Reservation {self_id} is for {self_for} not {for_}.')

def res_identity_includes_message(self_id, self_from, self_to, date):
    print(F'Reservation {self_id} is from {self_from} to {self_to} which does not include {date}.')

def res_identity_ok_message(self_id, for_, book, date):
    print(F'Reservation {self_id} is valid {for_} of {book} on {date}.')

def res_change_for_message(self_id, self_for, for_):
    print(F'Reservation {self_id} moved from {self_for} to {for_}')

def lib_init_message():
    print(F'Library created.')

def lib_add_user_message(result, name):
    if (result):
        print(F'User {name} created.')
    else:
        print(F'User not created, user with name {name} already exists.')