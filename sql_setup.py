import sqlite3
import ast
import re
import datetime

with open("scraping_results.txt") as f:
    imported = ast.literal_eval(f.read())
    cur_line = imported[0][0]
    hours = imported[0][1]
    stops_and_time = imported[0][2]

fixed_list = []
for i in hours:
    if "(" in i:
        spec = re.search("\((.)\)",i)
        par_loc = i[spec.start():spec.start()+3]
        before = i[:spec.start()]
        after = i[spec.start()+3:]
        if len(before) == 3:
            new = before+after
            hour = int(before[:-1])
            minute = int(after)
            time_s = datetime.timedelta(hours=hour,minutes=minute)
            #print(time_s)
            fixed_list.append(time_s)
        elif len(before) == 5:
            #print([before,after])
            new = before
            new2 = before[:2]+after
            #print([new,new2])
            hour1 = int(before[:-3])
            hour2 = int(before[:-3])
            minute1 = int(before[3:])
            minute2 = int(after)
            time_s = datetime.timedelta(hours=hour1,minutes=minute1)
            time_s2 = datetime.timedelta(hours=hour2,minutes=minute2)
            #print(time_s)
            #print(time_s2)
            fixed_list.append(time_s)
            fixed_list.append(time_s2)
        else:
            print("error")
    else:
        hour = int(i[:2])
        minute = int(i[3:])
        time_s = datetime.timedelta(hours=hour,minutes=minute)
        #print(time_s)
        fixed_list.append(time_s)

#print(fixed_list[0]-datetime.timedelta(minutes=5))
#print(hours)
#print(imported.index([hours]))
hours.clear()
for i in fixed_list:
    hours.append(i.seconds)
#print([i.seconds for i in hours])
        
db = sqlite3.connect('SzBusz.db')
c = db.cursor()

c.execute('DROP TABLE IF EXISTS main;')
c.execute("CREATE TABLE main(id INTEGER PRIMARY KEY, Lines TEXT, Stops INTEGER, Time TEXT, Coordinates TEXT);")
c.execute('DROP TABLE IF EXISTS timetable;')
c.execute("CREATE TABLE timetable(id INTEGER PRIMARY KEY, Lines TEXT, Hours INTEGER);")

def main_setup():
    for i in range(len(stops_and_time)):
        coords = ",".join(stops_and_time[i][2])
        cur_stop = stops_and_time[i][0]
        cur_time = stops_and_time[i][1]
        c.execute("INSERT INTO main(id,Lines,Stops,Time,Coordinates) VALUES(%d,'%s','%s','%s','%s');"%(i+1, cur_line, cur_stop, cur_time, coords))
def timetable_setup():
    for i in range(len(hours)):
        c.execute("INSERT INTO timetable(id,Lines,Hours) VALUES(%d,'%s','%s');"%(i+1,cur_line,hours[i]))

timetable_setup()
main_setup()
db.commit()


