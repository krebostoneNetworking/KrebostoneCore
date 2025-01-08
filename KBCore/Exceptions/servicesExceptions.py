
class InvalidServicePriorityException(Exception):
    """Will raise if the config provides an unknown launch priority"""
    pass

class ServiceAlreadyExistsException(Exception):
    """Will raise if there is already a task with the same name in the list"""