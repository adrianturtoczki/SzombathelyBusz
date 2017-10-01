import sqlite3
import ast
import re
import datetime

with open("scraping_results.txt") as f:
    imported = ast.literal_eval(f.read())
    #cur_line = imported[0][0]
    stops_and_time = imported[0][2]

for num in range(len(imported)):
    fixed_list = []
    #print(fixed_list)
    for i in imported[num][1]:
        try:
            if "(" in i:
                spec = re.search("\((.)\)",i) #TODO add specials to times
                par_loc = i[spec.start():spec.start()+3]
                before = i[:spec.start()]
                after = i[spec.start()+3:]
                if len(before) == 3:
                    new = before+after
                    hour = int(before[:-1])
                    minute = int(after)
                    time_s = datetime.timedelta(hours=hour,minutes=minute)
                    fixed_list.append(str(time_s)[:-3])
                elif len(before) == 5:
                    new = before
                    new2 = before[:2]+after
                    hour1 = int(before[:-3])
                    hour2 = int(before[:-3])
                    minute1 = int(before[3:])
                    minute2 = int(after)
                    time_s = datetime.timedelta(hours=hour1,minutes=minute1)
                    time_s2 = datetime.timedelta(hours=hour2,minutes=minute2)
                    fixed_list.append(str(time_s)[:-3])
                    fixed_list.append(str(time_s2)[:-3])
                else:
                    print("error")
            else:
                    hour = int(i[:2])
                    minute = int(i[3:])
                    time_s = datetime.timedelta(hours=hour,minutes=minute)
                    fixed_list.append(str(time_s)[:-3])
        except Exception as e:
            pass
            #fixed_list.append("")
            #print(e)
    print(imported[num][1])
    imported[num][1].clear()
    print(imported[num][1])
    #imported[num][1].append(fixed_list)
    #print(fixed_list)
    imported[num][1] = fixed_list
    print(imported[num][1])
    print()
        
db = sqlite3.connect('SzBusz.db')
c = db.cursor()

c.execute('DROP TABLE IF EXISTS main;')
c.execute("CREATE TABLE main(id INTEGER PRIMARY KEY, Lines TEXT, Stops INTEGER, Time TEXT, Coordinates TEXT);")
c.execute('DROP TABLE IF EXISTS timetable;')
c.execute("CREATE TABLE timetable(id INTEGER PRIMARY KEY, Lines TEXT, Hours TEXT, d_type TEXT, direction INTEGER);")

def main_setup():
    for i in range(len(stops_and_time)):
        cur_stop = stops_and_time[i][0]
        cur_time = stops_and_time[i][1]
        #cur_line = imported[i][0]
        cur_line = "test"
        coords = ",".join(stops_and_time[i][2])
        c.execute("INSERT INTO main(id,Lines,Stops,Time,Coordinates) VALUES(%d,'%s','%s','%s','%s');"%(i+1, cur_line, cur_stop, cur_time, coords))
def timetable_setup():
    tim_id = 0
    for i in range(len(imported)):
        d_type = imported[i][3]
        hours = imported[i][1]
        cur_line = imported[i][0]
        direction = imported[i][4]
        #print(hours)
        for j in range(len(hours)):
            tim_id+=1
            #print(hours[0][j])
            c.execute("INSERT INTO timetable(id,Lines,Hours,d_type,direction) VALUES(%d,'%s','%s','%s',%d);"%(tim_id,cur_line,hours[j],d_type,direction))
for i in range(len(imported)):
    print(i)
timetable_setup()
main_setup()
db.commit()


