
from launchable import Launchable

class Service(Launchable):

    def __init__(self, compName, wdir, exec, args, stop="stop"):
        super().__init__(compName, wdir, exec, args)
        self.stopMethod = stop

    def stop(self):
        if not self.isRunning():
            self.logger.logError(f"Service {self.compName} already stopped! No need for execution.")
            return False
        else:
            self.terminate()

    def middleOperations(self, processedCmd):
        pass
