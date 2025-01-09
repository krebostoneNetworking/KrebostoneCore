
from KBCore.Config.config import Config
from KBCore.MinecraftServer.gameServer import GameServer
from KBCore.Exceptions.servicesExceptions import ServiceNotLaunchedException
import os
import json

class Whitelist:

    def __init__(self, wkdir:str, gameServer:GameServer):
        self.whitelistFilePath = os.path.join(wkdir, "whitelist.json")
        self.gameServer = gameServer
        self.minecraftWhitelist:list = None

    def loadWhitelist(self):
        """
        Load whitelist content from server workdir
        """
        try:
            with open(self.whitelistFilePath, "r") as whitelistJson:
                self.minecraftWhitelist = json.load(whitelistJson)
                return True
        except Exception as e:
            return False
        pass

    def isWhitelistLoaded(self)->bool:
        return self.minecraftWhitelist == None

    def getUserUUID(self, username:str) -> str | None:
        """
        Return the user's UUID if the user exists, otherwise return None
        """
        for i in self.minecraftWhitelist:
            if i['name'] == username:
                return i['uuid']
            
        return None
        pass

    def addUser(self,username:str):
        """
        Add target user into server whitelist.

        This operation can only be done when the server is fully launched
        """
        if not self.gameServer.isMinecraftFullyLaunched:
            raise ServiceNotLaunchedException()
        
        # Add whitelist using command
        self.gameServer.send(f"whitelist add {username}")
        pass

    def removeUser(self, username:str):
        """
        Remove target user from server whitelist.

        This operation can only be done when the server is fully launched
        """
        if not self.gameServer.isMinecraftFullyLaunched:
            raise ServiceNotLaunchedException()
        
        # Add whitelist using command
        self.gameServer.send(f"whitelist remove {username}")
        pass