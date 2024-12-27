
from log import Logger
from threading import Thread

class CLI:

    logger:Logger = Logger("CLI")
    cliThread:Thread = None

    def printLogo():
        print("""
  _  __         _               _                   
 | |/ /        | |             | |                  
 | ' / _ __ ___| |__   ___  ___| |_ ___  _ __   ___ 
 |  < | '__/ _ \ '_ \ / _ \/ __| __/ _ \| '_ \ / _ \\
 | . \| | |  __/ |_) | (_) \__ \ || (_) | | | |  __/
 |_|\_\_|  \___|_.__/ \___/|___/\__\___/|_| |_|\___|
                                                    
                                                    
Krebostone - Extend the possibility of Minecraft Servers by kimsseTheWolf
Version 0.1 beta
""")
        pass

    def runCLI():
        while True:
            input()

    def startCLIThread():
        CLI.cliThread = Thread(target=CLI.runCLI)