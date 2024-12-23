
from minecraftServer import MCServer
from frpServer import FrpServer
from log import Logger

def runCLI(minecraftInstance:MCServer, frpInstance:FrpServer, logger:Logger):
    print("Entering Krebostone Server Extension CLI...")
    print("Type help for command list!")
    while True:
        command = input("> ")
        commandList = command.split(" ")
        # Minecraft server related command
        if commandList[0] == "mc":
            # Start minecraft server
            if commandList[1] == "start":
                minecraftInstance.start()

            # Send text or command to minecraft server
            elif commandList[1] == "send":
                if commandList.__len__() <= 2:
                    logger.logError("Missing argument: <COMMAND>")
                    continue
                # get all other objects into a single string, and send to subprocess
                target = ""
                for i in range(2, commandList.__len__()):
                    target += (commandList[i] + " ")
                target += "\n"
                # Send to process
                minecraftInstance.send(target)
            
            # Stop minecraft server
            elif commandList[1] == "stop":
                minecraftInstance.stop()

            else:
                logger.logError("Unknown argument")
        
        if commandList[0] == "stop":
            # Directly call stop by triggering KeyboardInterrupt
            raise KeyboardInterrupt
    pass