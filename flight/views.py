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
airline_name = []
flight_time = ["pagi", "siang", "malam"]

def index(request, filtered=None, airline_selected=None, schedule_selected=None):
    if filtered is None:
        with open(file, mode='r') as f:
            data = json.load(f)
    else:
        data = filtered

    for airline in data:
        if airline['name'] not in airline_name:
            airline_name.append(airline['name'])

    context = {
        'flight_schedules': data,
        'airlines': airline_name,
        'schedules': flight_time,
        'airline_selected': airline_selected,
        'schedule_selected': schedule_selected
    }

    return render(request, 'flight/index.html', context)

def add(request):
    name = request.POST['maskapai']
    time = request.POST['time']

    with open(file, mode='r') as f:
        data = json.load(f)

    data.append({"name": name, "time":time})
    with open(file, mode='w') as feeds:
        feeds.write(json.dumps(data, indent=2))
    
    return HttpResponseRedirect(reverse('flight:index'))

def delete(request, index):
    with open(file, mode='r') as f:
        data = json.load(f)

    del data[int(index)-1]
    with open(file, mode='w') as feeds:
        feeds.write(json.dumps(data, indent=2))
    
    return HttpResponseRedirect(reverse('flight:index'))

def up(request, index):
    with open(file, mode='r') as f:
        data = json.load(f)

    if int(index) > 1:
        data.insert(int(index)-2, data.pop(int(index)-1))

    with open(file, mode='w') as feeds:
        feeds.write(json.dumps(data, indent=2))
    
    return HttpResponseRedirect(reverse('flight:index'))

def down(request, index):
    with open(file, mode='r') as f:
        data = json.load(f)

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

    with open(file, mode='r') as f:
        data = json.load(f)

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
    print filtered_data2
    
    return index(request, filtered_data2, airline, schedule)

