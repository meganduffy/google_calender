from __future__ import print_function

import datetime
import os

import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse

    # The default calling of argparse causes conflicts with Djangos manage.py.
    # Source: https://stackoverflow.com/questions/34758516/google-calendar-api-stops-django-from-starting
    # flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    flags = tools.argparser.parse_args([])
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


class CalendarDependencies:
    def __init__(self):
        self.credentials = self.get_credentials()
        self.http = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar', 'v3', http=self.http)
        self.now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        self.eventsResult = self.service.events().list(
            calendarId='primary', timeMin=self.now, maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        self.events = self.eventsResult.get('items', [])

    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'calendar-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            credentials = tools.run_flow(flow, store, flags)
            print('Storing credentials to ' + credential_path)
        return credentials

def get_next_10_events():
    """
    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """

    print('Getting the upcoming 10 events')
    calendar_obj = CalendarDependencies()

    if not calendar_obj.events:
        return 'No upcoming events found.'
    for event in calendar_obj.events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary']) # <---- Need to change this into a format we can return rather than printing



def create_event(summary, location, description, start_time, end_time, attendees):
    """
    Creates an event on the google calendar.

    :param summary:
    :param location:
    :param description:
    :param start_time:
    :param end_time:
    :param attendees:
    :return event_url: link to the newly created event
    """

    time_zone = 'Europe/Dublin'
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S-00:00"),
            'timeZone': time_zone,
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S-00:00"),
            'timeZone': time_zone,
        },
        'attendees': attendees.email_list,
    }

    calendar_obj = CalendarDependencies()
    event = calendar_obj.service.events().insert(calendarId='primary', body=event).execute()
    event_url = event.get('htmlLink')
    return event_url # <--- Add an exception and return success/fail?
