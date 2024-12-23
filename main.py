from log import Logger
from minecraftServer import MCServer

logger:Logger = Logger("KSE")
mcServer:MCServer = None

def logStart():
    print("Krebostone KSE-Mini v0.1 created by kimsseTheWolf")
    logger.logInfo("Preparing for launch")

def loadNecessary():
    try:
        # Try to load minecraft server
        mcServer = MCServer()
        # Try to load frp server if necessary
    except:
        logger.logError("Krebostone was exited because of critical error")

if __name__ == "__main__":
    logStart()
    loadNecessary()
    