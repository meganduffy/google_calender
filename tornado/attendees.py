class Attendees:
    email_list = []

    def __init__(self):
        self.email_list = []

    def add_attendee(self, email_address):
        email_dict = {'email': email_address}
        self.email_list.append(email_dict)