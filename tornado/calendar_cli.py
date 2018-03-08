import api_functions
from attendees import Attendees
from datetime import datetime

# <------ Need to add command line args and functions for each calendar function we need to perform

def main():
    """
    This main function will need to be removed, leaving it here for now for notes only..
    :return:
    """
    api_functions.get_next_10_events()

    # Test variables
    summary = 'Test event sum'
    location = 'Test event location'
    description = 'Test event desc'
    start_time_value = '2018/02/05 21:00:00'
    end_time_value = '2018/02/05 22:00:00'
    start_time = datetime.strptime(start_time_value, "%Y/%m/%d %H:%M:%S")
    end_time = datetime.strptime(end_time_value, "%Y/%m/%d %H:%M:%S")
    attendees=Attendees()
    attendees.add_attendee("daragh.t.lowe@gmail.com")

    # Calls the create_event function and passes variables that will be passed into it from django
    api_functions.create_event(summary, location, description, start_time, end_time, attendees)


if __name__ == '__main__':
    main()