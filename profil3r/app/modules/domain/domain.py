from profil3r.app.search import search_head
import time

class Domain:

    def __init__(self, config, permutations_list):
        # 100 ms
        self.delay = config['plateform']['domain']['rate_limit'] / 1000
        # {permutation}.{tld}
        self.format = config['plateform']['domain']['format']
        # Top level domains
        self.tld = config['plateform']['domain']['TLD']
        # Domains are not case sensitive
        self.permutations_list = [perm.lower() for perm in permutations_list]
        # Domain
        self.type = config['plateform']['domain']['type']

    # Generate all potential domains names
    def possible_domains(self):
        possible_domains = []

        # Search all TLD (.com, .net, .org...), you can add more in the config.json file
        for domain in self.tld:
            for permutation in self.permutations_list:
                possible_domains.append(self.format.format(
                    permutation = permutation,
                    domain = domain
                ))

        return possible_domains

    def search(self):
        domains_lists = {
            "type": self.type,
            "accounts": []
        }
        possible_domains_list = self.possible_domains()

        r = None
        for domain in possible_domains_list:
            r = search_head(domain)
            if not r:
                continue

            # If the domain exists
            if r.status_code < 400:
                domains_lists["accounts"].append({"value": domain})
            time.sleep(self.delay)
        
        return domains_lists 