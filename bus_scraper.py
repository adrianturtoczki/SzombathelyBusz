import requests
import re
from bs4 import BeautifulSoup as bs

stops = []
all_lines = []
line_with_hours = []
links = []

def get_lines():
    page = requests.get("http://www.enykk.hu/aktiv_tartalom/menetrendes/web.cgi?func=stoplist&lang=hu&city=sz")
    soup = bs(page.content, 'html.parser')
    finder = soup.select('.section tr')
    for stop in finder:
        name = []
        lines = []
        links = stop.find_all('a')
        for i in range(len(links)):
            if i == 0:
                name.append(links[i].get_text().replace('\n',''))
            else:
                lines.append(links[i].get_text().replace('\n',''))
        stops.append([name,lines])

def get_all_lines():
    line_unfiltered = list(map(lambda x:x[1],stops))
    for li_ar in line_unfiltered:
        for line in li_ar:
            if not line in all_lines:
                all_lines.append(line)

def line_pages():
    page_stops = []
    time_ar = []
    i = str(6)
    
    line_page = requests.get("http://www.enykk.hu/aktiv_tartalom/menetrendes/web.cgi?func=linett&lang=hu&city=sz&line="+i+"&dir=1&spos=0")
    soup = bs(line_page.content, 'html.parser')

    page_stops = stops_and_mins(soup)
    line_times(time_ar,soup,page_stops)

def get_cord(link):
    try:
        link_page = requests.get("http://www.enykk.hu/aktiv_tartalom/menetrendes/"+link)
        soup = bs(link_page.content, 'html.parser')
        cord_y = soup.find_all("td", class_="stopgroupStopX")
        cord_x = soup.find_all("td", class_="stopgroupStopY")
        return [cord_x[1].string,cord_y[1].string]
    except Exception:
        print(Exception)
    
def stops_and_mins(soup):
    page_stops = []
    page_stop_bs = soup.find_all("td", class_="ttStopName")[1:]
    regex = soup.select("a[href*=web.cgi?func=stopinfo&lang=hu&city=sz&stop=]")
    try:
        for i in range(len(page_stop_bs)):
            cur_stop = page_stop_bs[i].get_text()
            cur_min= page_stop_bs[i].find_previous_sibling("td").string
            cur_coord = get_cord(regex[i]['href'])
            page_stops.append([cur_stop,cur_min,cur_coord])#,cur_coord])
            print(cur_stop,cur_min,cur_coord)
    except Exception as e:
        print(e)
    return page_stops
def line_times(time_ar,soup,page_stops):
    tan_times = soup.find_all("td", class_="dtI") #tanítási napok
    for i in tan_times:
        i = i.get_text().replace("\n","").replace(u"\xa0",u"")
        print(i)
        if i[-4:] == "0030":
            time_ar.append(i[:-2])
            time_ar.append(i[:3]+i[-2:])
        else:
            time_ar.append(i)
    line_with_hours.append(["6",time_ar[1:],page_stops])
line_pages()
#print(line_with_hours)

with open("scraping_results.txt","w") as f:
    f.write(str(line_with_hours))
