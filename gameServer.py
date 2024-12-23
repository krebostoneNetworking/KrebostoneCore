
from launchable import Launchable

class GameServer(Launchable):

    def __init__(self, compName, exec, args):
        super().__init__(compName, exec, args)
        self.__isMinecraftFullyLaunched:bool = False

    