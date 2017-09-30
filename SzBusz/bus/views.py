from django.shortcuts import render,redirect
from .models import Timetable, Main
import datetime
import googlemaps
import SETTINGS_KEYS

gmaps = googlemaps.Client(key=SETTINGS_KEYS.DIR_KEY)

# Create your views here.
def index(request):
    all_lines = Timetable.objects.values("lines").distinct()
    stops = Main.objects.all()#.filter(lines=line) #TODO
    context = {"all_lines":all_lines,"stops":stops,"API_KEY":SETTINGS_KEYS.API_key}
    return render(request, 'templates/index.html',context)

def show_hours(request):
    line = request.GET["line"]
    stop_d = request.GET["stop"]
    all_lines = Timetable.objects.values("lines").distinct()
    timetable =Timetable.objects.all().filter(lines=line)
    stops = Main.objects.all()#.filter(lines=line) #TODO
    stop = [i for i in Main.objects.all().filter(lines=line,stops=stop_d)][0]
    final_time = [datetime.timedelta(hours=i.hours/3600)+datetime.timedelta(minutes=int(stop.time)) for i in timetable]
    cord_x, cord_y = stop.coordinates.split(",")
    context = {"stops":stops,"timetable":timetable,"all_lines":all_lines,"final_time":final_time,"API_KEY":SETTINGS_KEYS.API_key,"cord_x":cord_x,"cord_y":cord_y}
    return render(request, 'templates/index.html',context)

def show_directions(request):
    context = {"API_KEY":SETTINGS_KEYS.DIR_KEY}
    return render(request, 'templates/directions.html',context)