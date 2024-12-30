
import json
import os
import dpath
import dpath.util
from log import Logger
from KBCore.Exceptions.configExceptions import ConfigNeedsSetupException as CfgSetupException

class Config:

    """A class for accessing and maintaing configs for Krebostone"""

    def __init__(self):

        # Create a template for the config
        self.__configStore:dict = {
            "debug_mode": False,
            "minecraft_server": {
                "instance_name": "",
                "working_dir": "",
                "launch_command": "",
                "arguments": []
            },
            "services": [
                
            ]
        }
        
        self.__CONFIG_PATH = os.path.join(os.getcwd(), "config.json")
        self.__logger = Logger("Config")
    
    def load(self):
        """Load config from local disk"""
        # Check if the config file exists
        if not os.path.exists(self.__CONFIG_PATH):
            with open(self.__CONFIG_PATH, "w") as cfg:
                json.dump(self.__configStore, cfg)
                raise CfgSetupException
        
        # Load and update config store
        with open(self.__CONFIG_PATH, "r") as j_cfg:
            source = json.load(j_cfg)
            self.__configStore.update(source)
        
    def get(self, key:str):
        """Get target config. Return None if no such key"""
        try:
            return dpath.get(self.__configStore, key)
        except Exception as e:
            return None