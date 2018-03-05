# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

import httplib2
import os
import datetime
# from dateutil import rrule
from dateutil.rrule import rrule, MINUTELY

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from .forms import CreateEventForm
from quickstart import create_event as quickstart_create_event
from attendees import Attendees

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

    def get_schedule(events):
        """Shows the hours in the day so we can ascertain which rooms are actually free
        """
        midnight = datetime.time(0, 0, 0)
        now = datetime.datetime.now()
        earliest_possible_schedule_time = datetime.datetime.combine(now, midnight)  # 12:00 am
        last_possible_schedule_time = earliest_possible_schedule_time + datetime.timedelta(hours=23.5)  # 11:30 pm

        schedule = []

        if len(events) == 0:
            # There are no events, add all 30 minute marks
            add_bookable_times(schedule, earliest_possible_schedule_time, last_possible_schedule_time)

        schedule_current_time = earliest_possible_schedule_time
        for event in events:
            event_start = event["start"]["dateTime"]
            thirty_minutes_before_event = event_start + datetime.timedelta(minutes=-30)

            # add thirty minute marks until the next event starts
            add_bookable_times(schedule, schedule_current_time, thirty_minutes_before_event)

            # add the event
            schedule.append(
                {
                    'minute': event_start,
                    'event': event
                }
            )
            schedule_current_time = event["end"]["dateTime"]

        # add the remaining minute marks until midnight
        add_bookable_times(schedule, schedule_current_time, last_possible_schedule_time)

        sorted_schedule = [i for n, i in enumerate(schedule) if i not in schedule[n + 1:]]

        return sorted_schedule

    def add_bookable_times(schedule_array, start_time, end_time):
        """
        Add thirty minute bookable times to our schedule

        :param schedule_array: an array of bookable times and events
        :param start_time: datetime
        :param end_time: datetime
        :return: no return, this function updates schedule_array in place (because pass-by-reference)
        """
        thirty_minute_marks = rrule(freq=MINUTELY, interval=30, dtstart=start_time, until=end_time)
        for timestamp in thirty_minute_marks:
            schedule_array.append(
                {
                    'minute': timestamp
                }
            )

    events = get_events()
    schedule = get_schedule(events)

    args = {"schedule": schedule}

    return render(request, 'index.html', args)


def user_create_event(request):
    """
    Logic for the form that will create an event
    """

    if request.method == "POST":
        form = CreateEventForm(request.POST)
        if form.is_valid():
            print("FORM: ", form)
            summary = request.POST.get('summary')
            start_string = request.POST.get('start')
            end_string = request.POST.get('end')
            organizer = request.POST.get('organizer')

            # format the start and end times
            start = datetime.datetime.strptime(start_string, "%Y-%m-%d %H:%M:%S")
            end = datetime.datetime.strptime(end_string, "%Y-%m-%d %H:%M:%S")

            print("ARGUMENTS: ", summary, start, end, organizer)
            print("Date Types: ", type(start), "\n", type(end))

            def create_event(summary, start, end, organizer):

                event = {u'status': u'confirmed',
                         u'kind': u'calendar#event',
                         u'end': {u'dateTime': end},
                         u'created': datetime.datetime.now(),
                         u'iCalUID': u'45f7sdfqmg5q72rd2mrq04dv7i@google.com',
                         u'reminders': {u'useDefault': True},
                         u'htmlLink': u'https://www.google.com/calendar/',
                         u'sequence': 0,
                         u'updated': datetime.datetime.now(),
                         u'summary': summary,
                         u'start': {u'dateTime': start},
                         u'etag': u'"3035662616606000"',
                         u'organizer': {u'self': True, u'email': organizer},
                         u'creator': {u'self': True, u'email': organizer},
                         u'id': u'45f7sdfqmg5q72rd2mrq04dv7i'}
                print(event)
                return event

            event = create_event(summary, start, end, organizer)
            # organizer = list(organizer)
            attendees = Attendees()
            attendees.add_attendee(organizer)


            if event:
                messages.success(request, "You have successfully created an event!")
                return redirect(reverse('index'))
            else:
                messages.error(request, "Oops, something went wrong!")
        else:
            messages.error(request, "Unable to validate form")
    else:
        form = CreateEventForm()

    args = {'form': form}

    return render(request, 'add-event.html', args)
