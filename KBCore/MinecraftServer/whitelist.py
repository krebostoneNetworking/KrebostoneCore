
from KBCore.Config.config import Config
from KBCore.MinecraftServer.gameServer import GameServer
import os
import json

class Whitelist:

    def __init__(self, wkdir:str):
        self.whitelistFilePath = os.path.join(wkdir, "whitelist.json")
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