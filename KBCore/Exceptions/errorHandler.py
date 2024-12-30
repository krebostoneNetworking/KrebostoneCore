
from queue import Queue

class ErrorHandler:

    errQueue:Queue = Queue()

    @staticmethod
    def enqueueError(e:Exception):
        ErrorHandler.errQueue.put(e)

    @staticmethod
    def getError()->Exception | None:
        if ErrorHandler.errQueue.empty():
            return None
        else:
            return ErrorHandler.errQueue.get_nowait()
        
    @staticmethod
    def isEmpty():
        return ErrorHandler.errQueue.empty()