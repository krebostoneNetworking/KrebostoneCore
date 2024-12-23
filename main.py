from log import Logger
from minecraftServer import MCServer
from frpServer import FrpServer
from CLI import runCLI
import sys

bootArgs:list[str] = []
logger:Logger = Logger("KSE")
mcServer:MCServer = None
frpServer:FrpServer = None

def logStart():
    print("Krebostone KSE-Mini v0.1 created by kimsseTheWolf")
    print(f"Booting Krebostone with arguments: {bootArgs}")
    logger.logInfo("Preparing for launch")

def loadNecessary():
    global mcServer
    global frpServer
    try:
        # Try to load minecraft server
        mcServer = MCServer()
        # Try to load frp server if necessary
        if bootArgs.count("--no-frp") == 0:
            logger.logInfo("Seeking frp service...")
            frpServer = FrpServer()
            pass
        else:
            logger.logInfo("FRP Server initialization skipped because of argument: --no-frp")
    except:
        logger.logError("Krebostone was exited because of critical error")
    
    logger.logInfo("All necessary component initialized! :)")

if __name__ == "__main__":
    bootArgs = sys.argv
    logStart()
    loadNecessary()
    try:
        runCLI(mcServer, frpServer, logger)
    except KeyboardInterrupt:
        print("\n")
        logger.logInfo("Keyboard interruption detected. Shutting down necessary services...")
    