
from service import Service
from Exceptions.servicesExceptions import InvalidServicePriorityException, ServiceAlreadyExistsException

class Services:

    servicesList:dict[str, dict[str, Service]] = {
        "before": {},
        "after": {}
    }

    def addTaskFromMetadata(launch:str, name:str, wkdir:str, launchCmd:str, args:list[str]):
        
        # Check valid priority
        if launch != "before" and launch != "after":
            raise InvalidServicePriorityException
        
        # Check existance
        if name in Services.servicesList[launch]:
            raise ServiceAlreadyExistsException
        
        # Append task to list
        targetList:Service = Service(name, wkdir, launchCmd, args)
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
            Services.servicesList['before'][task].stop()
        
        for task in Services.servicesList['after']:
            Services.servicesList['after'][task].stop()
    