# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from quickstart import create_event
from attendees import Attendees
import datetime


# Create your views here.
def customer_create_event(request):
    """
    Where do these variables come from?
    :return: 
    """
    # # Test variables
    # summary = 'Test event sum'
    # location = 'Test event location'
    # description = 'Test event desc'
    # start_time_value = '2018/02/05 21:00:00'
    # end_time_value = '2018/02/05 22:00:00'
    # start_time = datetime.datetime.strptime(start_time_value, "%Y/%m/%d %H:%M:%S")
    # end_time = datetime.datetime.strptime(end_time_value, "%Y/%m/%d %H:%M:%S")
    # attendees = Attendees()
    # attendees.add_attendee("daragh.t.lowe@gmail.com")
    #
    # # Calls the create_event function and passes variables that will be passed into it from django
    # create_event(summary, location, description, start_time, end_time, attendees)

    return render(request, 'add-event.html')
