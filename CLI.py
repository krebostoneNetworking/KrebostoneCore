
from KBCore.Logging.log import Logger
from threading import Thread
from KBCore.MinecraftServer.gameServer import GameServer
from KBCore.Exceptions.errorHandler import ErrorHandler
from typing import Callable

class CLI:

    logger:Logger = Logger("CLI")
    cliThread:Thread = None
    injectedHandlers:list[Callable[..., bool]] = [] # For future uses, other modules can inject their command to CLI
                                                    # The boolean represents whether the command is handled or not

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
                # Check all injected command first
                handled:bool = False
                for handler in CLI.injectedHandlers:
                    handled = handler(cmdList)
                    if handled:
                        break
                if not handled:
                    CLI.logger.logWarning(f"Command: {cmd} is not recognized!")

    def startCLIThread(mcServer:GameServer):
        CLI.cliThread = Thread(target=CLI.runCLI, args=(mcServer,))
        CLI.cliThread.start()

    def injectHandler(handler:Callable[..., bool]):
        CLI.injectedHandlers.append(handler)
        pass