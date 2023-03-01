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
    def __init__(self, key, name, district_key, district_name):
        self.key = key
        self.name = name

        self.district_key = district_key
        self.district_name = district_name

        self.open_alliance_teams = self.check_for_OA_teams()
        # self.rankings = self.get_rankings()

    # def get_rankings(self):
    #     event_rankings_response = requests.get("https://www.thebluealliance.com/api/v3/event/2023"
    #                                            + self.key + "/rankings", params=parameters)
    #     return json.loads(event_rankings_response.content)['rankings']

    def get_team_ranking(self, team):
        team_number = team.number
        for ranking in self.rankings:
            if ranking['team_key'] == 'frc' + str(team_number):
                return ranking['rank']

    def check_for_OA_teams(self):
        list_file = open('OpenAlliance Teams.txt', 'r')
        team_list = list_file.read().splitlines()
        teams = []

        event_teams_response = requests.get("https://www.thebluealliance.com/api/v3/event/" + self.key +
                                            "/teams/simple", params=parameters)

        event_teams = json.loads(event_teams_response.content)
        event_teams_list = []
        for event_team in event_teams:
            event_teams_list.append(str(event_team['team_number']))

        for event_team_listed in event_teams_list:
            if event_team_listed in team_list:
                teams.append(event_team_listed)

        return teams



