
class ConfigNeedsSetupException(Exception):
    """Will raise if a new config file was generated"""
    pass

class ConfigNoSuchEntryException(Exception):
    """Will raise if a key does not exists in the config structure"""
    pass