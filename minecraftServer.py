from log import Logger
import json

class MCServer:

    def __init__(self):
        try:
            # First try to load config file for necessary information
            self.logger = Logger("MinecraftServer")
            with open("config.json", "r") as jsonConfig:
                configContent = json.load(jsonConfig)
                self.folder = configContent["minecraft_server"]["location"]
                self.starterScript = configContent["minecraft_server"]["starter_script"]
            self.logger.logInfo("Minecraft Server config loaded successfully!")

            # Verify if all configuration is all valid
            if (self.folder == ""):
                self.logger.logError("An invalid value for parameter 'folder' was entered.")
                raise Exception()
            
            if (self.starterScript == ""):
                self.logger.logError("An invalid value for parameter 'starter_script' was entered.")
                raise Exception()
            
            self.logger.logInfo("Minecraft Server initialized successfully!")
            pass
        except:
            self.logger.logError("An error occured while initializing Minecraft Server. See above log for more information")
            raise Exception()