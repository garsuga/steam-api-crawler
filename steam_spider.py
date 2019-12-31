import requests
import sys
import json
import os

import steam_api


class SteamCrawler:
    def __init__(self, file_api_key, file_init_ids, file_checked_ids, dir_games, dir_users):
        with open(file_api_key, 'r+') as f:
            self.steam = steam_api.SteamAPI(f.readline())
        self.queue = [e.strip() for e in open(file_init_ids, 'r+').readlines()]
        self.checked = [e.strip() for e in open(file_checked_ids, 'r+').readlines()]

        self.games = self.__load_games(dir_games)
        self.users = self.__load_users(dir_users)

        self.checked_out = open(file_checked_ids, 'ab', buffering=0)
        self.dir_games = dir_games
        self.dir_users = dir_users

    def __load_games(self, dir_games):
        dat = {}
        for f in os.listdir(dir_games):
            game = steam_api.Game(json.load(open(os.path.join(dir_games, f), 'r+')))
            dat[game.appid] = game
        return dat

    def __apply_game(self, game):
        self.games[game.appid] = game
        json.dump(game, open(os.path.join(self.dir_games, str(game.appid)), 'w+'), default=lambda o: o.__dict__)

    def __load_users(self, dir_users):
        usrs = {}
        for f in os.listdir(dir_users):
            dat = json.load(open(os.path.join(dir_users, f), 'r+'))
            usr_games = {}
            for (appid, g) in dat['games'].items():
                game = steam_api.UserGame(g)
                usr_games[appid] = game
            usr = steam_api.User(dat['steamid'], usr_games)
            usrs[usr.steamid] = usr
        return usrs

    def __apply_user(self, user):
        self.users[user.steamid] = user
        json.dump(user, open(os.path.join(self.dir_users, str(user.steamid)), 'w+'), default=lambda o: o.__dict__)

    def crawl(self):
        while len(self.queue) > 0:
            id = self.queue.pop(0)
            print("\t - " + str(id))
            if id in self.checked:
                print("\t\tAlready searched " + id)
            else:
                self.checked.append(id)
                self.checked_out.write((id + "\n").encode("utf8"))
                if len(self.queue) < 1000000:
                    friends = self.steam.get_friends(id)
                    if len(friends) > 0:
                        print("\t\t\t" + str(len(friends)) + " friends")
                        self.queue.extend([friend.steamid for friend in friends])
                dat = self.steam.get_user_and_games(id)
                print("\t\t\t" + str(len(dat[1])) + " games")
                for (k, g) in dat[1].items():
                    self.__apply_game(g)
                self.__apply_user(dat[0])
                print("\t\t" + str(len(self.users)) + " total users")
                print("\t\t" + str(len(self.games)) + " total games")
                print("\t\t" + str(self.steam.num_requests) + " total requests")
        self.checked_out.close()


if __name__ == "__main__":
    crawler = SteamCrawler('apikey.txt', 'initids.txt', 'checked.txt', 'games', 'users')
    crawler.crawl()