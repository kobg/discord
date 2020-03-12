from controller import Controller

API_KEY = "--"
headers = {
    "Content-Type": "application/json"
}
controller = Controller(API_KEY)

def getWinrateByChampion(summonerName, championName):
    won = 0
    kills = 0
    deaths = 0
    assists = 0
    champId = controller.getChampionIdByChampionName(championName)
    gamelist = controller.getMatchListByAccountIdByChampionName(
        controller.getSummonerBySummonerName(summonerName)['accountId'], champId)
    for game in gamelist:
        gameDetails = controller.getMatchByGameId(str(game))
        try:
            for PLAYER in gameDetails['participants']:
                if (PLAYER['championId'] == int(champId) and PLAYER['stats']['win'] == True):
                    kills += PLAYER['stats']['kills']
                    assists += PLAYER['stats']['assists']
                    deaths += PLAYER['stats']['deaths']
                    won += 1
        except:
            pass
    try:
        print(won, len(gamelist), won / len(gamelist), "KdA", kills, deaths, assists, (kills + assists) / deaths)
    except:
        pass


# getWinrateByChampion("kubalo09", "Thresh")


def getWinrateBySummonerName(summonerName):
    won = 0
    accountId = controller.getSummonerBySummonerName(summonerName)['accountId']
    gamelist = controller.getMatchListByAccountId(accountId)
    for game, champ in gamelist:
        gameDetails = controller.getMatchByGameId(str(game))
        try:
            for PLAYER in gameDetails['participants']:
                if (PLAYER['championId'] == champ and PLAYER['stats']['win'] == True):
                    won += 1
        except:
            pass
    try:
        print(won,len(gamelist),won/len(gamelist))
    except:
        pass

getWinrateBySummonerName("BluuF")
