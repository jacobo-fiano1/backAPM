from .models import Protectora, Animal
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class ProtectoraService:
    
    def getProtectora(id):
        protectora = Protectora.objects.get(pk=id)
        return protectora
    
    def createProtectora(data):
        protectora = Protectora(name = data["name"], direccion=data["direccion"], ubicacion=data["ubicacion"],
            telefono=data["telefono"], url=data["url"], correo=data["correo"], descripcion=data["descripcion"])
        protectora.save()
        logger.info("Creada nueva protectora: " +  protectora.name + " ID: " + str(protectora.id))
        
        return protectora
    
class AnimalService:
    
    def getAnimal(id):
        animal = Animal.objects.get(pk=id)
        return animal
    
    def registerAnimal(data):
        try:
            protectora = ProtectoraService.getProtectora(data["protectora"])
        except:
            return "Protectora asociada no registrada"
        
        animal = Animal(name = data["name"], fechaNacimiento=data["fechaNacimiento"], tipo=data["tipo"],
            edad=data["edad"], estado=data["estado"], vacunas=data["vacunas"], descripcion=data["descripcion"],
            protectora=protectora)
        animal.save()
        logger.info("Registrado nuevo animal con ID: " +  str(animal.id) + " en Protectora " + str(animal.protectora.name))
        
        return animal
