import not_classes as classes
import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

AUTH_KEY = os.getenv('AUTH_KEY')
parameters = {
    "X-TBA-Auth-Key": AUTH_KEY
}

def get_upcoming_week_events(week_number):
    week_events = []
    events_response = requests.get("https://www.thebluealliance.com/api/v3/events/2023", params=parameters)
    events = json.loads(events_response.content)
    for event in events:
        if event['week'] == week_number:
            if event['district'] is None:
                week_events.append(classes.Event(event['key'], event['name'], "", ""))
            else:
                week_events.append(classes.Event(event['key'], event['name'], event['district']['key'],
                                                 event['district']['key']))

    return week_events

with open('short team list.txt') as teams_file:
    teams_unformatted = teams_file.read().splitlines()

x = []

upcoming_week_events = get_upcoming_week_events(0)
print("+-------------------------------+")
print('|Week 1:                        |')
for upcoming_week_event in upcoming_week_events:
    teams = upcoming_week_event.open_alliance_teams
    event_details = []
    if teams:
        header = upcoming_week_event.name.replace('District ', '').split(' presented')[0].replace(' Event', '')
        event_details = [header, teams]

    if len(event_details) == 2:
        print('+-------------------------------+------+------+------+------+------+------+------+------+')
        print_out = '|' + event_details[0]
        for x in range(31 - len(event_details[0])):
            print_out += ' '
        print_out += '|'
        for event in event_details[1]:
            if len(event) == 4:
                print_out += ' ' + event + ' |'
            if len(event) == 3:
                print_out += ' ' + event + '  |'
            if len(event) == 2:
                print_out += '  ' + event + '  |'
        for y in range(88 - len(print_out)):
            print_out += ' '

        print(print_out + '|')
print('+-------------------------------+------+------+------+------+------+------+------+------+')

# event = classes.Event("isde1")
# print(event.get_team_ranking(test))