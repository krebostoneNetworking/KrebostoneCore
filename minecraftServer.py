from log import Logger
import json
import subprocess
import threading

class MCServer:

    def __init__(self):
        # Create server thread
        self.__logThread:threading.Thread = None
        self.__serverProcess:subprocess.Popen = None # The subprocess
        
        # Other server status
        self.isDoneBooting = False
        try:
            # First try to load config file for necessary information
            self.logger = Logger("MinecraftServer")
            with open("config.json", "r") as jsonConfig:
                configContent = json.load(jsonConfig)
                self.folder:str = configContent["minecraft_server"]["location"]
                self.starterScript:str = configContent["minecraft_server"]["starter_script"]
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
        
    def __server_logThread(self):
        
        while True:
            outputLine:str = self.__serverProcess.stdout.readline()
            # Quit this thread if process is end
            if outputLine == "":
                break

            # All middlewares go here for processing the messages
            processedMessage:str = outputLine.strip()

            # Process and output the thread
            self.logger.logInfo(processedMessage)
        
        # Fall back to none after execution
        self.__logThread = None

    
    def start(self):
        # Create new process for minecraft server
        if (self.__serverProcess != None and self.__serverProcess.poll() != None):
            self.logger.logWarning("Cannot create new instance: Server is still running!")
            return
        
        self.isDoneBooting = False

        bootCmd = f"cd {self.folder} && {self.starterScript}"
        
        commandArr = self.starterScript.split(" ")
        self.__serverProcess = subprocess.Popen(commandArr, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        # Create monitoring thread
        self.__logThread = threading.Thread(target=self.__server_logThread)

        # Start the thread
        self.__logThread.start()


    def send(self, cmd:str):
        # Filtering typing stop
        if cmd == "stop":
            self.isDoneBooting = False
            self.logger.logWarning("Directly calling stop from command is not recommended. Use command 'mc stop' instead!")

        # Otherwise send the message to the process
        self.__serverProcess.stdin.write(cmd)
        self.__serverProcess.stdin.flush()
    
    def stop(self):
        if (self.__serverProcess != None or self.__serverProcess.poll() == None):
            self.logger.logWarning("Cannot stop: Server already stopped!")
            return
        
        self.isDoneBooting = False

        self.__serverProcess.stdin.write("stop")
        self.__serverProcess.stdin.flush()


