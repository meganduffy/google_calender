# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

import httplib2
import os
import datetime
from dateutil import rrule

from django.shortcuts import render
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


def get_calendar(request):
    return render(request, 'index.html')


def get_calendar_information(request):
    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/calendar-python-quickstart.json
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'Google Calendar API Python Quickstart'

    def get_credentials():
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
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:  # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def get_events():
        """Shows basic usage of the Google Calendar API.

        Creates a Google Calendar API service object and outputs a list of the next
        10 events on the user's calendar.
        """
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        eventsResult = service.events().list(
            calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])

        if not events:
            print('No upcoming events found.')

        else:
            for i in events:
                strttime = i["start"]["dateTime"]
                i["start"]["dateTime"] = datetime.datetime.strptime(strttime, "%Y-%m-%dT%H:%M:%SZ")
                endtime = i["end"]["dateTime"]
                i["end"]["dateTime"] = datetime.datetime.strptime(endtime, "%Y-%m-%dT%H:%M:%SZ")
            return events

    def get_hours():
        """Shows the hours in the day so we can ascertain which rooms are actually free
        """
        midnight = datetime.time(0, 0, 0)
        now = datetime.datetime.now()
        midnight_now = datetime.datetime.combine(now, midnight)
        midnight_tomorrow = midnight_now + datetime.timedelta(hours=24)
        hours = {}

        for hour in rrule.rrule(rrule.HOURLY, dtstart=midnight_now, until=midnight_tomorrow):
            hours[hour] = hour
        print(type(hours))
        print(hours)
        sorted_hours = sorted(hours.values())
        return sorted_hours

    hours = get_hours()

    args = {'hours': hours}

    return render(request, 'index.html', args)
