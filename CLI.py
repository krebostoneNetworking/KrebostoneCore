
from gameServer import GameServer
from log import Logger

def runCLI():
    mcServer = GameServer("test_server", "C:\\Users\\ilove\\Documents\\TestServer", "java", ["-jar", "-Xmx4G", "C:\\Users\\ilove\\Documents\\TestServer\\server.jar"])
    logger = Logger("CLI")
    logger.logInfo("Running via beta CLI")
    while True:
        cmd = input()
        args = cmd.split(" ")
        if args[0] == "start":
            mcServer.start()
        elif args[0] == "stop":
            mcServer.stop()
        else:
            logger.logError("Unknown command!")


runCLI()