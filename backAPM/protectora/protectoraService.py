from .models import Protectora, Animal
from django.forms.models import model_to_dict
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class ProtectoraService:
    
    def getProtectora(id):
        try:
            protectora = Protectora.objects.get(pk=id)
            return model_to_dict(protectora)
        except:
            return "ERROR: Protectora con ID: " + id + " no registrada"
    
    def createProtectora(data):
        try:
            protectora = Protectora(name = data["name"], direccion=data["direccion"], ubicacion=data["ubicacion"],
                telefono=data["telefono"], url=data["url"], correo=data["correo"], descripcion=data["descripcion"])
            protectora.save()
            logger.info("OK: Creada nueva protectora: " +  protectora.name + " ID: " + str(protectora.id))
            return model_to_dict(protectora)
        except:
            return "ERROR: Error al crear la Protectora"
    
    def deleteProtectora(id):
        try:
            protectora = Protectora.objects.get(pk=id)
            protectora.delete()
            logger.info("Eliminada protectora con ID: " + id)
            return "OK: Protectora " + id + " eliminada." 
        except:
            return "ERROR: Protectora con ID: " + id + " no registrada"
   
        
class AnimalService:
    
    def getAnimal(id):
        try:
            animal = Animal.objects.get(pk=id)
            return model_to_dict(animal)
        except:
            return "ERROR: Animal con ID: " + id + " no encontrado."
                    
    def registerAnimal(data):
        try:
            protectora = Protectora.objects.get(pk=data["protectora"])
        except:
            return "ERROR: Protectora asociada no registrada"
        try:
            animal = Animal(name = data["name"], fechaNacimiento=data["fechaNacimiento"], tipo=data["tipo"],
                edad=data["edad"], estado=data["estado"], vacunas=data["vacunas"], descripcion=data["descripcion"],
                protectora=protectora)
            animal.save()
            logger.info("OK: Registrado nuevo animal con ID: " +  str(animal.id) + " en Protectora " + str(animal.protectora.name))
            return model_to_dict(animal)
        except:
            return "ERROR: Error al registrar el animal"
    
    def deleteAnimal(id):
        try:
            animal = Animal.objects.get(pk=id)
            animal.delete()
            logger.info("Eliminado animal con ID: " + id)
            return "OK: Animal " + id + " eliminada." 
        except:
            return "ERROR: Animal con ID: " + id + " no registrado"
