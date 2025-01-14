from profil3r.app.search import search_get
from bs4 import BeautifulSoup
import time

class Leagueoflegends:
    def __init__(self, config, permutations_list):
        # 1000 ms
        self.delay = config['plateform']['leagueoflegends']['rate_limit'] / 1000
        # op.gg/summoner/userName={permutation}
        self.format = config['plateform']['leagueoflegends']['format']
        # League of legends usernames are not case sensitive
        self.permutations_list = permutations_list
        # Gaming
        self.type = config['plateform']['leagueoflegends']['type']
        # Servers
        self.servers = config['plateform']['leagueoflegends']['servers']

    # Generate all potential league of legends usernames
    def possible_usernames(self):
        possible_usernames = []

        for permutation in self.permutations_list:
            possible_usernames.append(self.format.format(
                permutation=permutation,
            ))
        return possible_usernames

    def search(self):
        leagueoflegends_usernames = {
            "type": self.type,
            "accounts": []
        }
        possible_usernames_list = self.possible_usernames()
        for username in possible_usernames_list:
            for server in self.servers:
                # {subdomain}{username}
                url = server["url"].format(username)
                r = search_get(url)
                if not r:
                    continue

                if r.status_code == 200:
                    # Account object
                    account = {}

                    # Get the URL
                    account["value"] = url

                    # Parse HTML response content with beautiful soup 
                    soup = BeautifulSoup(r.text, 'html.parser')

                    # Scrape the user informations
                    try:
                        user_username = str(soup.find_all(class_="Name")[0].get_text()) if soup.find_all(class_="Name") else None
                        user_elo_score = str(soup.find_all(class_="TierRank")[0].get_text()) if soup.find_all(class_="TierRank") else None
                        user_last_connection = str(soup.find_all(class_="TimeStamp")[0].find_all(class_="_timeago")[0].get_text()) if soup.find_all(class_="TimeStamp") else None
                        # If the account exists
                        if user_username:
                            account["user_username"] = {"name": "Name", "value": user_username}
                            account["user_elo"] = {"name": "Elo", "value": user_elo_score}
                            account["user_last_connection"] = {"name": "Last Connection", "value": user_last_connection}

                            # Append the account to the accounts table
                            leagueoflegends_usernames["accounts"].append(account)
                    except:
                        pass

                time.sleep(self.delay)
                
        return leagueoflegends_usernames