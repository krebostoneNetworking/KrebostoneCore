
from launchable import Launchable

class GameServer(Launchable):

    def __init__(self, compName, wdir, exec, args):
        super().__init__(compName, wdir, exec, args)
        self.isMinecraftFullyLaunched:bool = False

    def stop(self):
        if not self.isRunning():
            self.logger.logError(f"Service {self.compName} already stopped! No need for execution.")
            return False
        else:
            self.send("stop")
            self.isMinecraftFullyLaunched = False

    def middleOperations(self, processedCmd:str):
        # Monitoring if the game is started
        if (processedCmd.count("Done!") > 0):
            self.isMinecraftFullyLaunched = True
            self.logger("Minecraft server fully booted! Have fun with your friends!")
        pass


mcServer:GameServer = GameServer("test_server", "C:\\Users\\ilove\\Documents\\TestServer", "java", ["-jar", "-Xmx4G", "C:\\Users\\ilove\\Documents\\TestServer\\server.jar"])
mcServer.start()
while True:
    cmd = input()
    mcServer.send(cmd)