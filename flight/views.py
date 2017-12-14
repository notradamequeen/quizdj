# -*- coding: utf-8 -*-
from copy import copy
from datetime import datetime
import json
import os
import re
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

file = os.path.join(settings.BASE_DIR, 'quizdj/flight/data/data.json')
data = []
airline_name = []
flight_time = ["pagi", "siang", "malam"]

def index(request, filtered=None, airline_selected=None, schedule_selected=None):
    if filtered is not None:
        flight_schedules = filtered

    else:
        flight_schedules = data

    for airline in flight_schedules:
        if airline['name'] not in airline_name:
            airline_name.append(airline['name'])

    context = {
        'flight_schedules': flight_schedules,
        'airlines': airline_name,
        'schedules': flight_time,
        'airline_selected': airline_selected,
        'schedule_selected': schedule_selected
    }

    return render(request, 'flight/index.html', context)

def add(request):
    name = request.POST['maskapai']
    time = request.POST['time']

    data.append({"name": name, "time":time})
    
    return HttpResponseRedirect(reverse('flight:index'))

def delete(request, index):
    item = data[int(index)-1]
    del data[int(index)-1]

    if item['name'] not in [airline['name'] for airline in data]:
        airline_name.remove(item['name'])
    
    return HttpResponseRedirect(reverse('flight:index'))

def up(request, index):
    if int(index) > 1:
        data.insert(int(index)-2, data.pop(int(index)-1))
    
    return HttpResponseRedirect(reverse('flight:index'))

def down(request, index):
    if int(index)-1 < len(data)-1:
        data.insert(int(index), data.pop(int(index)-1))
    with open(file, mode='w') as feeds:
        feeds.write(json.dumps(data, indent=2))
    
    return HttpResponseRedirect(reverse('flight:index'))

def filter(request):
    airline = request.POST['airline_filter']
    schedule = request.POST['schedule_filter']

    filtered_data = []
    filtered_data2 = []

    pagi = datetime.strptime("00:00", "%H:%M")
    siang = datetime.strptime("12:00", "%H:%M")
    malam = datetime.strptime("18:00", "%H:%M")

    for item in data:
        flight_time = datetime.strptime(item['time'], "%H:%M")
        if pagi < flight_time < siang:
            print 'pagi'
            item['schedule'] = "pagi"
        if flight_time >= siang and flight_time < malam:
            item['schedule'] = "siang"
        if flight_time >= malam:
            item['schedule'] = "malam"
        if airline != "all":
            if item['name'] == airline:
                filtered_data.append(item)
        else:
            filtered_data.append(item)

    if schedule != "all":
        for filtered_item in filtered_data:
            if filtered_item['schedule'] == schedule:
                filtered_data2.append(filtered_item)
    else:
        filtered_data2 = filtered_data
    
    return index(request, filtered_data2, airline, schedule)

