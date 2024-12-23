
from abc import ABC, abstractmethod
from subprocess import Popen, PIPE
from threading import Thread
from log import Logger

class Launchable(ABC):

    """An overall class for everything that can be launched and using i/o"""

    def __init__(self, compName:str, exec:str, args:list[str]):
        """
        Create a new launchable instance.

        compName: The alias for this launchable object
        exec: The path to executable file
        args: A list for strings contains the launching arguments
        """

        self.compName:str = compName
        self.exec:str = exec
        self.args:list[str] = args
        self.__serverProcess:Popen = None
        self.__stdOutHandle:Thread = None
        self.__stdErrHandle:Thread = None
        self.__logger:Logger = Logger(compName)
        pass

    def __readStream(self, stream):
        """Reading outputs from sub-process and halding related events"""
        while True:
            line = stream.readline()
            if not line:
                break
            processedCommand = line.decode().strip()
            # Call middle operations
            self.middleOperations(processedCommand)
        pass

    @abstractmethod
    def middleOperations(processedCmd:str):
        """All user added middle operations while reading streams from sub-process"""
        pass

    def start(self):
        """Start the new service"""
        # First check if the service is still running
        if self.isRunning():
            self.__logger.logError(f"Current service: {self.compName} is still running!")
            return False
        
        # Try to launch a new service
        try:
            args = ""
            for i in range(self.args.__len__()):
                args += (self.args[i] + " ")
            command = f"{self.exec} {args}"

            # Launch sub-process
            self.__serverProcess = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True)

            # Launch std-out and std-err handling thread
            self.__stdOutHandle = Thread(target=self.__readStream, args=(self.__serverProcess.stdout))
            self.__stdErrHandle = Thread(target=self.__readStream, args=(self.__serverProcess.stdout))

            # Report current status
            self.__logger.logInfo(f"Service: {self.compName} launched successfully!")
            pass
        except:
            pass
        pass

    def send(self, cmd:str):
        """Send command to service"""
        self.__serverProcess.stdin.write(cmd + "\n")
        self.__serverProcess.stdin.flush()
        pass

    @abstractmethod
    def stop(self):
        """Stop the current service safely"""
        pass

    def terminate(self):
        """Force terminate the service"""
        # Check if the service is still running
        if not self.isRunning():
            self.__logger.logError(f"Service {self.compName} already stopped! No need for execution.")
            return False
        else:
            self.__serverProcess.terminate()
            return True
        pass

    def isRunning(self):
        """Chcek if the service process is still running"""
        if self.__serverProcess != None:
            return self.__serverProcess.poll != None
        else:
            return False