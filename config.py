
import json
import os
import dpath
import dpath.util
from log import Logger
from Exceptions.configExceptions import ConfigNeedsSetupException as CfgSetupException

class Config:

    """A class for accessing and maintaing configs for Krebostone"""

    def __init__(self, cfgPath:str):

        # Create a template for the config
        self.__configStore:dict = {
            "debug_mode": False,
            "minecraft_server": {
                "instance_name": "",
                "working_dir": "",
                "launch_command": "",
                "arguments": []
            },
            "frp_server": [
                {
                    "instance_name": "minecraft_frp",
                    "working_dir": "",
                    "launch_command": "",
                    "arguments": []
                }
            ]
        }
        
        self.__path = cfgPath
        self.__CONFIG_PATH = os.path.join(os.getcwd(), "config.json")
        self.__logger = Logger("Config")
    
    def load(self):
        """Load config from local disk"""
        # Check if the config file exists
        if not os.path.exists(self.__CONFIG_PATH):
            with open(self.__CONFIG_PATH, "w") as cfg:
                cfg.write(json.dump(self.__configStore))
                raise CfgSetupException
        
        # Load and update config store
        with open(self.__CONFIG_PATH, "r") as j_cfg:
            source = json.load(j_cfg)
            self.__configStore.update(source)
        
    def get(self, key:str):
        """Get target config. Return None if no such key"""
        try:
            return dpath.util.get(key)
        except:
            return None