import requests



API_URL = "https://eun1.api.riotgames.com/lol"
VERSION = requests.get("https://ddragon.leagueoflegends.com/api/versions.json",headers={"Content-Type":"application/json"}).json()
CHAMP_URL = "http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion.json".format(VERSION[0])
CHAMPIONS = requests.get(CHAMP_URL, headers={"Content-Type": "application/json"}).json()

headers = {
            "Content-Type": "application/json",
            "X-Riot-Token": "--"
        }

class Controller:

    def __init__(self, api_key):
        self.API_KEY = api_key

    def getChampionNameByChampionId(self,championId):
        for CHAMP in CHAMPIONS["data"]:
            if CHAMPIONS["data"][CHAMP]['key'] == championId:
                return CHAMPIONS["data"][CHAMP]['name']


    def getChampionIdByChampionName(self,championName):
        return CHAMPIONS["data"][championName]['key']

    def getFreeChampions(self):
        endpoint = "/platform/v3/champion-rotations"
        CHAMPIONS = requests.get(API_URL + endpoint,headers=headers).json()
        return [self.getChampionNameByChampionId(str(id)) for id in CHAMPIONS['freeChampionIds']]


    def getSummonerBySummonerName(self, summonerName):
        endpoint = "/summoner/v4/summoners/by-name/" + summonerName
        request = requests.get(API_URL + endpoint, headers=headers)
        return request.json()

    def getMatchListByAccountIdByChampionName(self,accountId,championId):
        matches = []
        endpoint = "/match/v4/matchlists/by-account/{}".format(str(accountId))
        queries = "?champion={}&queue={}".format(str(championId),420)
        MATCHLIST = requests.get(API_URL + endpoint + queries, headers=headers).json()
        for MATCH in MATCHLIST['matches']:
            matches.append(MATCH['gameId'])
        print(len(matches))
        return matches


    def getMatchListByAccountId(self,accountId):
        matches = []
        endpoint = "/match/v4/matchlists/by-account/" + accountId
        queries = "?queue={}".format(420)
        MATCHLIST = requests.get(API_URL + endpoint + queries, headers=headers).json()
        for MATCH in MATCHLIST['matches']:
            # print(MATCH)
            matches.append((MATCH['gameId'],MATCH['champion']))
        return matches

    def getMatchByGameId(self,gameId):
        endpoint = "/match/v4/matches/" + gameId
        GAME = requests.get(API_URL + endpoint,headers=headers).json()
        # if GAME['gameMode'] == 'CLASSIC' and GAME['gameType'] == 'MATCHED_GAME':
        return GAME