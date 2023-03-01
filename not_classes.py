import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

AUTH_KEY = os.getenv('AUTH_KEY')
parameters = {
    "X-TBA-Auth-Key": AUTH_KEY
}


class Team:
    def __init__(self, number):
        self.number = number
        self.nickname = self.get_nickname()
        self.team_key = "frc" + str(self.number)

        self.district = self.get_current_district()
        self.district_key = self.district['key']
        self.district_name = self.district['name']

    def get_nickname(self):
        team_response = requests.get("https://www.thebluealliance.com/api/v3/team/frc" + str(self.number),
                                     params=parameters)
        nickname = json.loads(team_response.content)['nickname']

        return nickname

    def get_current_district(self):
        current_district = {}
        district_response = requests.get("https://www.thebluealliance.com/api/v3/team/frc" + str(self.number) +
                                         "/districts", params=parameters)
        team_districts = json.loads(district_response.content)
        for team_district in team_districts:
            if team_district['year'] == 2023:
                current_district['key'] = team_district['key']
                current_district['name'] = team_district['display_name']
        return current_district


class Event:
    def __init__(self, key):
        self.key = key
        self.rankings = self.get_rankings()

    def get_rankings(self):
        event_rankings_response = requests.get("https://www.thebluealliance.com/api/v3/event/2023"
                                               + self.key + "/rankings", params=parameters)
        return json.loads(event_rankings_response.content)['rankings']

    def get_team_ranking(self, team):
        team_number = team.number
        for ranking in self.rankings:
            if ranking['team_key'] == 'frc' + str(team_number):
                return ranking['rank']
