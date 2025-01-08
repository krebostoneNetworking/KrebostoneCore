
import os
import dpath
import dpath.util

class MCServerProperties:

    def __init__(self, wkdir:str):
        self.serverPropertiesPath = os.path.join(wkdir, "server.properties")
        self.serverProperties:dict = None
        pass

    def __convertValue(self, value):
        """
        Convert a string to digits or boolean
        """
        if value.isdigit():
            return int(value)
        if value.lower() in ["true", "false"]:
            return value.lower() == "true"
        return value

    def load(self)->bool:
        """
        Load server.properties content from indicated directory

        Return true if successfully loaded, otherwise return false.
        """
        try:
            properties = {}
            with open(self.serverPropertiesPath, "r", encoding="utf-8") as file:
                for line in file:
                    # Skip empty and comments
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    # split keys and values
                    if "=" in line:
                        key, value = line.split("=", 1)
                        properties[key.strip()] = self.__convertValue(value.strip())
                self.serverProperties = properties
                return True
        except Exception as e:
            self.serverProperties = None
            return False
        
    def isLoaded(self):
        """
        Does Krebostone loaded server.properties correctly?

        Return a boolean represents its state.
        """
        return self.serverProperties == None
        
    def get(self, key:str):
        """
        Get a value from server.properties according to its key

        Return None if no such element exists
        """
        try:
            return dpath.get(self.serverProperties, key)
        except Exception as e:
            return None
