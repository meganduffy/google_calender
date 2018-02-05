# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.shortcuts import render


def get_calendar(request):
    return render(request, 'index.html')


