#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/local/opt/python@3.8/bin/python3


# <bitbar.title></bitbar.title>
# <bitbar.author>Mithun</bitbar.author>
# <bitbar.author.github>vkmb</bitbar.author.github>
# <bitbar.desc>Display student apartments list</bitbar.desc>
# <bitbar.dependencies>python</bitbar.dependencies>
# <bitbar.version>1.10.1</bitbar.version>
# <bitbar.abouturl></bitbar.abouturl>

import os
import pickle
import requests
import datetime
from bs4 import BeautifulSoup

def insert_dict(db_dict, room, index):
    db_dict.update({
                room[index.index('Residence hall')]:{
                    "time":[datetime.datetime.utcnow()], 
                    "Position on the waiting list":[room[index.index('Position on the waiting list')]], 
                    "Number in this residence hall":[room[index.index('Number in this residence hall')]], 
                    "Rent":[room[index.index('Rent')]]
                    }
                })
    return db_dict

def pop_list_item(room):
    
    for item in room.keys():
        if len(room[item]) > 100:
            for i in range(10):
                room[item].pop(0)
    
    return room


def update_room_db(room, room_db, index):
    
    for key in room_db.keys():
        if key == "time":
            room_db["time"].append(datetime.datetime.utcnow())
            continue
        room_db[key].append(room[index.index(key)])

    
    return room_db
    
def update_db(index, data):
    
    global static_db
    db_dict =   {}   
    try:
        db_dict = pickle.load(open(static_db, 'rb'))
    except :
        pass   
    scroller, update_str = "Waitlist\r\n", ""

    with open(static_db, 'wb+') as fp:

        for i, room in enumerate(data):
            
            update_str += room[index.index("Residence hall")]+' 🏡  | color=#ff9100 \r\n'
            update_str += '-- ' + room[index.index("Rent")] + ' | color=#ef5350 \r\n'
            update_str += '-- ' + room[index.index("Number in this residence hall")] + ' 🚪 | color=#123def \r\n'

            if room[index.index('Residence hall')] not in db_dict.keys():
                insert_dict(db_dict, room, index)
                update_str += '-- ' + room[index.index("Position on the waiting list")] + ' | color=#4caf50 \r\n'
                scroller += str(i+1) +' - '+ room[index.index("Position on the waiting list")] + ' 🧘🏽‍♂️ | color=#ffffff \r\n'

            else:
                room_db = pop_list_item(db_dict[room[index.index('Residence hall')]])  
                if (room[index.index("Position on the waiting list")] != room_db["Position on the waiting list"][-1]):
                    update_str += '-- ' + room_db["Position on the waiting list"][-1] + '->' + room[index.index("Position on the waiting list")] + ' 🧘🏽‍♂️ | color=#4caf50 \r\n'
                    scroller += str(i+1) +' - '+ room_db["Position on the waiting list"][-1] + '->' + room[index.index("Position on the waiting list")] + ' 🧘🏽‍♂️ | color=#ffffff \r\n'
                    update_room_db(room, room_db, index)
                else:
                    update_str += '-- ' + room[index.index("Position on the waiting list")] + ' 🧘🏽‍♂️ | color=#4caf50 \r\n'
                    scroller += str(i+1) +' - '+ room[index.index("Position on the waiting list")] + ' 🧘🏽‍♂️ | color=#ffffff \r\n'

                time_diff = room_db['time'][-1] - datetime.datetime.utcnow()
                
                if time_diff.days > 0:
                    update_room_db(room, room_db, index)
                db_dict[room[index.index('Residence hall')]] = room_db

        pickle.dump(db_dict, fp)
    print(scroller+'---\r\n'+update_str)

pwd = os.getenv('student_key')
usr = os.getenv('student_mailid')
static_db = os.getenv('student_db')

base = "https://bewerberportal.stw.rwth-aachen.de"


headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get(base+"/en/login", headers=headers)
headers.update({"Cookie":f"PHPSESSID={r.cookies.get('PHPSESSID')}"})
soup = BeautifulSoup(r.text, 'html.parser')
csrf_token =  soup.find("input", {"name":"_csrf_token"}).get('value')
payload = {"_csrf_token":csrf_token, \
            "_username":usr,\
            "_password":pwd, "_submit":""}  
action = soup.find("form").get("action")
r = requests.post(base+action, data=payload, headers=headers)
soup = BeautifulSoup(r.text, "html.parser")
rooms = soup.find(id="rooms")
rows = rooms.findAll("tr")
index = [element.text for element in rows[0].findAll('th')]
data = [[element.text.strip('\n').strip(',').strip(' ') for element in row.findAll('td')] for row in rows[1:]]

update_db(index, data)
