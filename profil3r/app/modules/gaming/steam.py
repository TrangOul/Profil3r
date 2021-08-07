from profil3r.app.search import search_get
import time

class Steam:

    def __init__(self, config, permutations_list):
        # 1000 ms
        self.delay = config['plateform']['steam']['rate_limit'] / 1000
        # https://steamcommunity.com/id/{username}
        self.format = config['plateform']['steam']['format']
        # Steam usernames are not case sensitive
        self.permutations_list = permutations_list
        # Gaming
        self.type = config['plateform']['steam']['type']

    # Generate all potential steam usernames
    def possible_usernames(self):
        possible_usernames = []

        for permutation in self.permutations_list:
            possible_usernames.append(self.format.format(
                permutation = permutation,
            ))
        return possible_usernames

    def search(self):
        steam_usernames = {
            "type": self.type,
            "accounts": []
        }
        possible_usernames_list = self.possible_usernames()

        for username in possible_usernames_list:
            r = search_get(username)
            if not r:
                continue
            
            # If the account exists
            if "The specified profile could not be found" not in r.text:
                steam_usernames["accounts"].append({"value": username})

            time.sleep(self.delay)
        
        return steam_usernames