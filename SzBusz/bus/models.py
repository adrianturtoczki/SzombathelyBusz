from django.db import models

# Create your models here.
class Main(models.Model):
    id = models.IntegerField(blank=True, null=True)
    lines = models.TextField(db_column='Lines', blank=True, null=True)  
    stops = models.TextField(db_column='Stops', blank=True, null=True)  
    time = models.TextField(db_column='Time', blank=True, null=True)  
    coordinates = models.TextField(db_column='Coordinates', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'main'
        app_label = "main"


class Timetable(models.Model):
    id = models.IntegerField(blank=True, null=True)
    lines = models.TextField(db_column='Lines', blank=True, null=True)  
    hours = models.TextField(db_column='Hours', blank=True, null=True)
    d_type = models.TextField(db_column='d_type', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'timetable'
        app_label = "timetable"