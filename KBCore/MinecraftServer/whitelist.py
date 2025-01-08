
from KBCore.Config.config import Config
from KBCore.MinecraftServer.gameServer import GameServer

class Whitelist:

    def __init__(self, kConfig:Config, gameServer:GameServer):
        self.kConfig = kConfig
        self.gameServer = gameServer
        self.minecraftWhitelist:list = None

    def loadWhitelist(self):
        """
        Load whitelist content from server workdir
        """
        pass

    def isInWhitelist(username:str)->bool:
        """
        Check whether the player is exists in the server whitelist
        """
        pass

    def addUser(username:str):
        """
        Add target user into server whitelist.

        When server is on, Krebostone will automatically add user via command and refresh

        If server is offline or stopped, and with online-mode is set to off, Krebostone will directly add a new UUID
        for the user. Otherwise, it will stop this process.

        """
        pass

    def removeUser(username:str):
        """
        Remove target user from server whitelist.

        When server is on, Krebostone will automatically remove user via command and refresh

        If server is offline or stopped, and with online-mode is set to off, Krebostone will directly remove the target
        user. Otherwise, it will stop this process.

        """
        pass