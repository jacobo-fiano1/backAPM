from .models import Protectora, Animal
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
import logging
import requests
from requests_oauthlib import OAuth1Session
import os
import json


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
        
class UserService:
    
    def createUser(input):
        try:
            user = User.objects.create_user(username=input["username"], password=input["pass"])
            #user.user_permissions.add()
            user.save()
            logger.info("Registrado nueva protectora: " + user.first_name)
            return model_to_dict(user)
        except:
            return "ERROR: Ya existe un usuario con ese login"

# API Key 2bWZSRrbe3FJJ6e51fEinyKHf
# API Key Secret KoyJzMMtrbFdKBKaLSjNBu4xHwaKDHuFG4y2YLMCspA6asQ17w
# Bearer AAAAAAAAAAAAAAAAAAAAAAiNngEAAAAAAnfTFIyHF1U%2B%2F0FjlWrWhSd%2Biyc%3DKLz1FykieTgCoW0P6Ed8k2hRGcmbKpmZFeKHWL88FsizVj3mO8
# Acces Token 1659984139863355397-FL4hX9epzEx6WoCVV82UygYtLbQxpQ
# Acces Token secret dyOGB3IH5coCjwJFQjBS5zkXI8ckfKlN5NSYoR7uL2YrP
# client id dTl0aHMzbWFmYU9oeUdQRnBDbzA6MTpjaQ
# client secret 7De6Mb420sDpZjATqKUIbiCrGNEcK-N0uO4S8XTBQdVDhLIdj2


class TwitterService:
    
    
    def postTweet(protectora, data):
        
        # Representa la pass y user de mi app de desarrolador dentro de twitter, permite formar las llamadas a la APÎ de twitter.
        consumer_key = "2bWZSRrbe3FJJ6e51fEinyKHf"
        consumer_secret = "KoyJzMMtrbFdKBKaLSjNBu4xHwaKDHuFG4y2YLMCspA6asQ17w"
        
        #Representa la cuenta de twitter, en este caso la de PetMateAPM
        access_token = "1659984139863355397-FL4hX9epzEx6WoCVV82UygYtLbQxpQ"
        access_token_secret = "dyOGB3IH5coCjwJFQjBS5zkXI8ckfKlN5NSYoR7uL2YrP"
        
        payload = {"text": data["text"]}

        # Make the request
        oauth = OAuth1Session(
            consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret,
        )

        # Making the request
        response = oauth.post("https://api.twitter.com/2/tweets", json=payload)

        if response.status_code != 201:
            raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))

        print("Response code: {}".format(response.status_code))

        # Saving the response as JSON
        json_response = response.json()
        print(json.dumps(json_response, indent=4, sort_keys=True))
        return "Tweet generado correctamente"
