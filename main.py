from log import Logger
from minecraftServer import MCServer
import sys

bootArgs:list[str] = []
logger:Logger = Logger("KSE")
mcServer:MCServer = None

def logStart(args:list[str]):
    print("Krebostone KSE-Mini v0.1 created by kimsseTheWolf")
    print(f"Booting Krebostone with arguments: {args}")
    logger.logInfo("Preparing for launch")

def loadNecessary(args:list[str]):
    try:
        # Try to load minecraft server
        mcServer = MCServer()
        # Try to load frp server if necessary
        if args.count("--no-frp") != 0:
            pass
        else:
            logger.logInfo("FRP Server initialization skipped because of argument: --no-frp")
    except:
        logger.logError("Krebostone was exited because of critical error")

if __name__ == "__main__":
    bootArgs = sys.argv
    logStart()
    loadNecessary()
    