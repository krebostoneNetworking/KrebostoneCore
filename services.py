
from service import Service
from Exceptions.servicesExceptions import InvalidServicePriorityException, ServiceAlreadyExistsException
import time

class Services:

    servicesList:dict[str, dict[str, Service]] = {
        "before": {},
        "after": {}
    }

    def addTaskFromMetadata(launch:str, name:str, wkdir:str, launchCmd:str, args:list[str], stopMethod="stop"):
        
        # Check valid priority
        if launch != "before" and launch != "after":
            raise InvalidServicePriorityException
        
        # Check existance
        if name in Services.servicesList[launch]:
            raise ServiceAlreadyExistsException
        
        # Append task to list
        targetList:Service = Service(name, wkdir, launchCmd, args, stopMethod)
        Services.servicesList[launch][name] = targetList

    def addTaskFromObject(launch:str, tService:Service):

        # Check valid priority
        if launch != "before" and launch != "after":
            raise InvalidServicePriorityException
        
        # Check existance
        if tService.compName in Services.servicesList[launch]:
            raise ServiceAlreadyExistsException
        
        # Append task to list
        Services.servicesList[launch][tService.compName] = tService
    
    def stopAll():

        for task in Services.servicesList['before']:
            if Services.servicesList['before'][task]['stop'] == "stop":
                Services.servicesList['before'][task].stop()
            elif Services.servicesList['before'][task]['stop'] == "kill":
                Services.servicesList['before'][task].kill()
            elif Services.servicesList['before'][task]['stop'] == "terminate":
                Services.servicesList['before'][task].terminate()
            else:
                Services.servicesList['before'][task].stop()
        
        for task in Services.servicesList['after']:
            if Services.servicesList['after'][task]['stop'] == "stop":
                Services.servicesList['after'][task].stop()
            elif Services.servicesList['after'][task]['stop'] == "kill":
                Services.servicesList['after'][task].kill()
            elif Services.servicesList['after'][task]['stop'] == "terminate":
                Services.servicesList['after'][task].terminate()
            else:
                Services.servicesList['after'][task].stop()

        # Wait until all services are stopped, before and after
        for task in Services.servicesList['before']:
            while Services.servicesList['before'][task].isRunning():
                time.sleep(0.1)
        
        for task in Services.servicesList['after']:
            while Services.servicesList['after'][task].isRunning():
                time.sleep(0.1)

    
    def startBefore():

        for task in Services.servicesList['before']:
            Services.servicesList['before'][task].start()
        
    def startAfter():

        for task in Services.servicesList['after']:
            Services.servicesList['after'][task].start()

    