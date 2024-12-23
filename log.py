
from colorama import Fore, Back, Style
from datetime import datetime

__debug_mode:bool = False

def setDebugMode(isDebug:bool):
    __debug_mode = isDebug

def isDebugMode():
    return __debug_mode

DATE_TEMPLATE = "2022-01-01 12:00:00"

class Logger:

    def __init__(self, packageName:str):
        self.packageName = packageName

    def generateTimestamp(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def logInfo(self, msg:str):
        print(f"[{Fore.GREEN}INFO{Fore.WHITE}][{self.generateTimestamp()}][{self.packageName}] {msg}")
    
    def logWarning(self, msg:str):
        print(f"[{Fore.LIGHTRED_EX}WARNING{Fore.WHITE}][{self.generateTimestamp()}][{self.packageName}] {msg}")

    def logError(self, msg:str):
        print(f"[{Fore.RED}ERROR{Fore.WHITE}][{self.generateTimestamp()}][{self.packageName}] {msg}")

    
    
    