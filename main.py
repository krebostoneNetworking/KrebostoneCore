from log import Logger
from gameServer import GameServer
from services import Services
from KBCore.Config.config import Config
from CLI import CLI
from KBCore.Exceptions.configExceptions import ConfigNeedsSetupException
import time
from errorHandler import ErrorHandler
import traceback
import sys
import os

mLogger:Logger = Logger("Main")
kConfig:Config = Config()
minecraftGameServer:GameServer = None
mainThread:bool = False # Control the start/stop of main thread

def cleanUp():
    mLogger.logInfo("Shutting down side services...")
    Services.stopAll()
    mLogger.logInfo("Shutting down game server...")
    if minecraftGameServer == None:
        mLogger.logWarning("Skipping shutdown process for game server: Server instance not created yet!")
    else:
        minecraftGameServer.stop()
        while minecraftGameServer.isRunning():
            time.sleep(0.1)
        return

def quitKrebostone():
    global mainThread
    mainThread = False
    mLogger.logInfo("Cleaning Krebostone...")
    cleanUp()
    mLogger.logInfo("Exiting Krebostone...")
    mLogger.logInfo("Goodbye!")
    os._exit(0)

if __name__ == "__main__":

    try:
        CLI.printLogo()
        # Start launch process

        # Config file loader
        mLogger.logInfo("Loading config file...")
        try:
            kConfig.load()
        except ConfigNeedsSetupException as e:
            mLogger.logError("Config file does not exists. A new copy has been created. Fill in all necessary information and restart!")
            sys.exit(0)
        mLogger.logInfo("Config loaded successfully")

        # Load all services
        servicesMetadata = kConfig.get("services")
        mLogger.logInfo(f"{servicesMetadata.__len__()} services found.")
        for i in servicesMetadata:
            mLogger.logInfo(f"Loading {i['instance_name']}")
            Services.addTaskFromMetadata(
                i['launch'],
                i['instance_name'],
                i['working_dir'],
                i['launch_command'],
                i['arguments'],
                i['stop']
            )

        # Start before-boot processes
        mLogger.logInfo("Launching pre-boot services")
        Services.startBefore()

        # Start game server
        minecraftGameServer = GameServer(
            kConfig.get("/minecraft_server/instance_name"), 
            kConfig.get("/minecraft_server/working_dir"), 
            kConfig.get("/minecraft_server/launch_command"),
            kConfig.get("/minecraft_server/arguments"))
        
        mLogger.logInfo("Launching Minecraft processes. If the server is asking you to enter something, enter 'mc send <THINGS TO SEND>'")
        CLI.startCLIThread(minecraftGameServer)
        time.sleep(2)
        minecraftGameServer.start()

        while (not minecraftGameServer.isMinecraftFullyLaunched):
            time.sleep(0.1)

        # Start after-boot processes
        mLogger.logInfo("Launching after-boot services")
        Services.startAfter()

        # Print done, and occupy the main thread
        mLogger.logInfo("All services are up and running! Type 'help' for list of available command")
        mainThread = True

        while mainThread:
            # Handle all possible exceptions from anywhere
            if ErrorHandler.isEmpty():
                pass
            else:
                raise ErrorHandler.getError()            
            time.sleep(0.1)

    except KeyboardInterrupt:
        mLogger.logWarning("Keyboard interrupt detected. Shutting down Krebostone safely...")
        quitKrebostone()

    except Exception as e:
        mLogger.logWarning("An unexpected error occured. Here is what happened")
        traceback.print_exc()
        quitKrebostone()
