from bs4 import BeautifulSoup
import requests
import json
from cs50 import SQL
states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "PR", "GU"]

db = SQL("sqlite:///database.db")

for state in states:
    airforce = requests.get('https://www.afrotc.com/wp-json/afrotc/colleges/state/' + str(state) + '?admission_type=&type=&dispositions=')
    det = json.loads(airforce.content)
    for dictionary in det:
        # print(dictionary['name'])
        # print(dictionary['type']['label'])
        # print(dictionary['longitude'], dictionary['latitude'])
        longitude = dictionary['longitude']
        latitude = dictionary['latitude']
        school = dictionary['name']
        if dictionary['type']['label'] == "Host":
            db.execute("INSERT or IGNORE INTO airforce (school, latitude, longitude, type) VALUES (:school, :latitude, :longitude, 'host')", school=school, latitude=latitude, longitude=longitude)
        else:
            db.execute("INSERT or IGNORE INTO airforce (school, latitude, longitude, type) VALUES (:school, :latitude, :longitude, 'crosstown')", school=school, latitude=latitude, longitude=longitude)

for state in states:
    army = requests.get('https://www.goarmy.com/rotc/find-schools.' + str(state) + '-.results.html')
    soup = BeautifulSoup(army.content, 'html.parser')
    div = soup.find_all("div", {"class": "resultsSchoolList darkLinks"})
    for x in range(len(div)):
        school = div[x].get_text()
        db.execute("INSERT or IGNORE INTO army (school, type) VALUES (:school, 'host')", school=school)
    crosstown = soup.find_all("div", {"class": "resultsSubSchools"})
    for x in range(len(crosstown)):
        school = crosstown[x].get_text()
        db.execute("INSERT or IGNORE INTO army (school, type) VALUES (:school, 'crosstown')", school=school)
    # for x in range(len(div)):
    #     print(div[x].get_text())

navy = requests.get('https://www.netc.navy.mil/Commands/Naval-Service-Training-Command/NROTC/Navy-ROTC-Schools/#')
stew = BeautifulSoup(navy.content, 'html.parser')
schools = stew.find_all('a', {'target': '_blank'})
for x in range(len(schools)):
    #print(schools[x].get_text())
    school = schools[x].get_text()
    db.execute("INSERT or IGNORE INTO navy (school) VALUES (:school)", school=school)
