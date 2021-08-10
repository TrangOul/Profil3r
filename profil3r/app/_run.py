from profil3r.app.colors import Colors
import threading

def run(self):
    # Get arguments from the command line
    self.parse_arguments()
    
    self.load_config()
    self.print_logo()

    self.menu()
    self.get_permutations()

    modules = self.get_report_modules()

    if modules:
        # Number of permutations to test per service
        print(Colors.BOLD + "[+]" + Colors.ENDC + " {} permutations to test for each service, you can reduce this number by selecting less options if it takes too long".format(len(self.permutations_list)))

        # List of services that profil3r will search
        print("\n" + "Profil3r will search : \n " + Colors.BOLD + "[+] " + Colors.ENDC +  "{} \n".format(str('\n ' + Colors.BOLD + "[+] " + Colors.ENDC).join(modules)))

        for module in modules:
            thread = threading.Thread(target=self.modules[module]["method"])
            thread.start()
            thread.join()
    else:
        print("\nNo service selected.")
        
    if self.report_path:
        self.generate_report()