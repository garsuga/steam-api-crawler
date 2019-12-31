import json
import requests
import time

# API Time variables
delay = 1.5 * 1.1
lastTime = time.time()


# API Time helper function
def api_wait():
    global lastTime
    time.sleep(max(0, int(delay - (time.time() - lastTime))))
    lastTime = time.time()


class Friend:
    def __init__(self, dict):
        self.steamid = str(dict['steamid']).strip()
        self.friend_since = str(dict['friend_since']).strip()


class Game:
    def __init__(self, dict):
        self.appid = str(dict['appid']).strip()
        self.name = str(dict['name']).strip()
        self.img_icon_url = 'http://media.steampowered.com/steamcommunity/public/images/apps/%s/%s.jpg' \
                       % (str(self.appid).strip(), str(dict['img_icon_url']).strip()) if 'img_icon_url' in dict else ''
        self.img_logo_url = 'http://media.steampowered.com/steamcommunity/public/images/apps/%s/%s.jpg' \
                       % (str(self.appid).strip(), str(dict['img_logo_url']).strip()) if 'img_logo_url' in dict else ''
        self.has_community_visible_stats = bool(str(dict['has_community_visible_stats']).strip()) if 'has_community_visible_stats' in \
                                                                                      dict else False


class UserGame:
    def __init__(self, dict):
        self.appid = str(dict['appid']).strip()
        self.playtime_forever = int(str(dict['playtime_forever']).strip())
        self.playtime_2weeks = int(str(dict['playtime_2weeks']).strip()) if 'playtime_2weeks' in dict else 0


class User:
    def __init__(self, steamid, games):
        self.games = games
        self.steamid = steamid


class SteamAPI:
    def __init__(self, apiKey):
        self.apiKey = apiKey
        self.num_requests = 0

    # Requests API for steam user games, return json
    def __request_user_games(self, steamid):
        try:
            url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=%s&steamid=%s&format=json&' \
                  'include_appinfo=1&include_played_free_games=1' % (self.apiKey, str(steamid))
            api_wait()
            self.num_requests += 1
            resp = requests.get(url).json()['response']
            return resp['games'] if ('games' in resp) else {}
        except Exception as e:
            print("Caught exception in request_user_games")
            print(e)
            return {}

    # Take user ID, Request API for friends, return friends request JSON
    def __request_user_friends(self, steamid):
        try:
            url = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=%s&steamid=%s' \
                  '&relationship=friend' % (self.apiKey, str(steamid))
            api_wait()
            self.num_requests += 1
            resp = requests.get(url).json()
            if 'friendslist' in resp and 'friends' in resp['friendslist']:
                return resp['friendslist']['friends']
            return {}
        except Exception as e:
            print("Caught exception in request_user_friends")
            print(e)
            return {}

    # Return User, {Games} (combined to reduce api calls)
    def get_user_and_games(self, steamid):
        data = self.__request_user_games(steamid)
        games = {}
        user_games = {}
        for g in data:
            game = Game(g)
            user_game = UserGame(g)
            games[game.appid] = game
            user_games[user_game.appid] = user_game
        return User(steamid, user_games), games

    def get_friends(self, steamid):
        data = self.__request_user_friends(steamid)
        return [Friend(f) for f in data]