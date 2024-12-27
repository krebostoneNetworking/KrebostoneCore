
from log import Logger
from threading import Thread
from gameServer import GameServer
from errorHandler import ErrorHandler

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

    def runCLI(mcServer:GameServer):
        while True:
            cmd = input()
            cmdList:list[str] = cmd.split(" ")
            if (cmdList[0] == "mc"):
                if (cmdList[1] == "send"):
                    mcServer.send(cmd[8:])
                pass
            elif (cmdList[0] == "stop"):
                ErrorHandler.enqueueError(KeyboardInterrupt)
                break
            else:
                print("Unknown Command. Type 'help for list of available command'")

    def startCLIThread(mcServer:GameServer):
        CLI.cliThread = Thread(target=CLI.runCLI, args=(mcServer,))
        CLI.cliThread.start()