def res_init_message(self_id, self_book, self_from, self_to, self_for):
    print(F'Created a reservation with id {self_id} of {self_book} from {self_from} to {self_to} for {self_for}.')
    # nebolo by lepsie len poslat self?

def res_overlapping_message(self_id, other_id, str):
    print(F'Reservations {self_id} and {other_id} {str} overlap')

def res_includes_message(self_id, str, date):
    print(F'Reservation {self_id} {str} {date}')
# def res_identity_message(problem, self_id, self_book, book, for_, self_for, self_from, self_to, date):
#    if (problem == 'book'):
#       print(F'Reservation {self_id} reserves {self_book} not {book}.')
#    elif(problem == 'for'):
#        print(F'Reservation {self_id} is for {self_for} not {for_}.')
#    elif (problem == 'includes'):
#        print(F'Reservation {self_id} is from {self_from} to {self_to} which does not include {date}.')
#    elif (problem == 'ok'):
#        print(F'Reservation {self_id} is valid {for_} of {book} on {date}.')
#    else:
#        print(F'Unpredictable problem')

def res_identity_message(problem, book, for_, date, reservation):
    if (problem == 'book'):
        print(F'Reservation {reservation._id} reserves {reservation._book} not {book}.')
    elif (problem == 'for'):
        print(F'Reservation {reservation._id} is for {reservation._for} not {for_}.')
    elif (problem == 'includes'):
        print(
            F'Reservation {reservation._id} is from {reservation._from} to {reservation._to} which does not include {date}.')
    elif (problem == 'ok'):
        print(F'Reservation {reservation._id} is valid {for_} of {book} on {date}.')
    else:
        print(F'Unpredictable problem')

def res_change_for_message(self_id, self_for, for_):
    print(F'Reservation {self_id} moved from {self_for} to {for_}')

def lib_init_message():
    print(F'Library created.')

def lib_add_user_message(result, name):
    if (result):
        print(F'User {name} created.')
    else:
        print(F'User not created, user with name {name} already exists.')

def lib_add_book_message(name, num_copies):
    print(F'Book {name} added. We have {num_copies} coppies of the book.')

def lib_reserve_book_message(problem, book, user, date_from, date_to, desired_reservation_id=-1):
    if (problem == 'user'):
        print(F'We cannot reserve book {book} for {user} from {date_from} to {date_to}. User does not exist.')
    elif (problem == 'date'):
        print(F'We cannot reserve book {book} for {user} from {date_from} to {date_to}. Incorrect dates.')
    elif (problem == 'count'):
        print(F'We cannot reserve book {book} for {user} from {date_from} to {date_to}. We do not have that book.')
    elif (problem == 'not_enough'):
        print(F'We cannot reserve book {book} for {user} from {date_from} to {date_to}. We do not have enough books.')
    elif (problem == 'ok'):
        print(F'Reservation {desired_reservation_id} included.')
    else:
        print(F'Unpredictable problem')

def lib_change_reservation(problem, user, book, date, new_user):
    if (problem == 'reservations'):
        print(F'Reservation for {user} of {book} on {date} does not exist.')
    elif (problem == 'user'):
        print(F'Cannot change the reservation as {new_user} does not exist.')
    elif (problem == 'ok'):
        print(F'Reservation for {user} of {book} on {date} changed to {new_user}.')
    else:
        print(F'Unpredictable problem')

def lib_check_reservation_message(user, book, date, str):
    print(F'Reservation for {user} of {book} on {date} {str}.')