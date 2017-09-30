import sqlite3

db = sqlite3.connect('SzBusz.db')
c = db.cursor()

#print(database[0])
def bus_info(num):
    pass

def timetable(line):
    pass

def stops(line):
    stop_lst = c.execute("SELECT Stops FROM main WHERE Lines='{}';".format(line))
    #for i in stop_lst:
   #     print(i[0])
    return stop_lst.fetchall()

def stop_times(line,stop):
    stop_plus = c.execute("SELECT Stops,Time FROM main WHERE Lines='{}' AND Stops='{}';".format(line,stop))
    for s,t in stop_plus.fetchall():
        bonus = t
    stop_b = c.execute("SELECT Hours FROM timetable WHERE Lines='{}';".format(line))
    for h in stop_b.fetchall():
        print(h[0]+bonus)  #TODO
def next_bus(line,time):
    pass
    
#print(bus_info("6"))
#print(timetable(0))
#print(stops(6))
print(stop_times("6","Metro"))
