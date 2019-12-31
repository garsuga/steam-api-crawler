# SteamSpider
Games activity scraper using the Steam API

# Usage
SteamSpider gathers data on games and user playtimes. Access to the Steam API is contained in ``steam_api.py``
Accounts are traversed by receiving a starting sample of Steam user ID's and branching to friends recursively.
Storage is done using JSON in the directories ``./users`` and ``./games`` where file are named by Steam ID and App ID respectively. 

## The following files are required in the working directory to run.

``initids.txt`` Sample starting user IDs (requires at least 1 with friends to branch, repeats will be skipped during consecutive runs) Ex:
```
76561197900000000
76561197900000000
76561197900000000
76561197900000000
76561197900000000
```

``apikey.txt`` Steam API access key on a single line. Ex:
```
A3BEG254151GFANV516G...
```

To start, execute ``steam_spider.py``

# License
None, use anywhere
