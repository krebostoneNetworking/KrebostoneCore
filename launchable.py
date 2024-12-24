
from abc import ABC, abstractmethod
from subprocess import Popen, PIPE
from threading import Thread
from log import Logger
import traceback

class Launchable(ABC):

    """An overall class for everything that can be launched and using i/o"""

    def __init__(self, compName:str, wdir:str|None, exec:str, args:list[str]):
        """
        Create a new launchable instance.

        compName: The alias for this launchable object
        exec: The path to executable file
        args: A list for strings contains the launching arguments
        """

        self.compName:str = compName
        self.wdir = wdir
        self.exec:str = exec
        self.args:list[str] = args
        self.serverProcess:Popen = None
        self.stdOutHandle:Thread = None
        self.stdErrHandle:Thread = None
        self.healthMonitorThread:Thread = None
        self.logger:Logger = Logger(compName)
        pass

    def __readStream(self, stream, isErr:bool):
        """Reading outputs from sub-process and halding related events"""
        while True:
            line = stream.readline()
            if not line:
                break
            processedCommand = line.strip()

            if isErr:
                self.logger.logError(processedCommand)
            else:
                self.logger.logInfo(processedCommand)
            # Call middle operations
            self.middleOperations(processedCommand)
        pass

    def __processHealthMonitor(self):
        while True:
            if not self.isRunning():
                self.logger.logWarning(f"Detected service {self.compName} was exited!")
                break
            

    @abstractmethod
    def middleOperations(processedCmd:str):
        """All user added middle operations while reading streams from sub-process"""
        pass

    def start(self):
        """Start the new service"""
        # First check if the service is still running
        if self.isRunning():
            self.logger.logError(f"Current service: {self.compName} is still running!")
            return False
        
        # Try to launch a new service
        try:
            args = ""
            for i in range(self.args.__len__()):
                args += (self.args[i] + " ")
            command = f"{self.exec} {args}"

            # Navigate to target working directory if there is one
            if self.wdir is not None:
                command = f"cd {self.wdir} && {command}"

            self.logger.logInfo(f"Try to load service with command: {command}")

            # Launch sub-process
            self.serverProcess = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True, shell=True)

            # Launch std-out and std-err handling thread
            self.stdOutHandle = Thread(target=self.__readStream, args=(self.serverProcess.stdout, False))
            self.stdErrHandle = Thread(target=self.__readStream, args=(self.serverProcess.stderr, True))
            self.healthMonitorThread = Thread(target=self.__processHealthMonitor, args=())
            self.stdOutHandle.start()
            self.stdErrHandle.start()
            self.healthMonitorThread.start()

            # Report current status
            self.logger.logInfo(f"Service: {self.compName} launched successfully!")
            return True
            pass
        except Exception as e:
            self.logger.logError(f"An error occured while trying to launch service: {self.compName}. See the following traceback for details:")
            traceback.print_exc()
            return False
        pass

    def send(self, cmd:str):
        """Send command to service"""
        self.serverProcess.stdin.write(cmd + "\n")
        self.serverProcess.stdin.flush()
        pass

    @abstractmethod
    def stop(self):
        """Stop the current service safely"""
        pass

    def terminate(self):
        """Force terminate the service"""
        # Check if the service is still running
        if not self.isRunning():
            self.logger.logError(f"Service {self.compName} already stopped! No need for execution.")
            return False
        else:
            self.serverProcess.terminate()
            return True
        pass

    def isRunning(self):
        """Chcek if the service process is still running"""
        if self.serverProcess != None:
            return self.serverProcess.poll() != None
        else:
            return False