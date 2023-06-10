from .models import Protectora, Animal
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
import logging
import requests
from requests_oauthlib import OAuth1Session
from django.core.files.base import ContentFile
import base64
import os
import json


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class ProtectoraService:
    
    def getProtectora(id):
        protectora = Protectora.objects.get(pk=id)
        dict = model_to_dict(protectora, exclude=['imagen'])
        dict["imagen"] = base64.b64encode(open("media/" + str(protectora.imagen), "rb").read()).decode('utf-8')
        
        return dict
    
    def createProtectora(data):
        protectora = Protectora(name = data["name"], direccion=data["direccion"], ubicacion=data["ubicacion"],
            telefono=data["telefono"], url=data["url"], correo=data["correo"], descripcion=data["descripcion"],
            latitud=data["latitud"], longitud=data["longitud"])
        protectora.save()

        format, imgstr = data["imagen"].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr))  
        file_name = protectora.name + "-" + str(protectora.id) +"." + ext
        protectora.imagen.save(file_name, data, save=True)

        logger.info("OK: Creada nueva protectora: " +  protectora.name + " ID: " + str(protectora.id))
        return model_to_dict(protectora)
    
    def deleteProtectora(id):
        try:
            protectora = Protectora.objects.get(pk=id)
            protectora.delete()
            logger.info("Eliminada protectora con ID: " + id)
            return "OK: Protectora " + id + " eliminada." 
        except:
            return "ERROR: Protectora con ID: " + id + " no registrada"
        
    def searchProtectora(args):
        protectoras = Protectora.objects.filter(**args)
        data= []
        for protectora in protectoras:
            pDict = model_to_dict(protectora, exclude=['imagen']) 
            pDict["imagen"] = base64.b64encode(open("media/" + str(protectora.imagen), "rb").read()).decode('utf-8')
            data.append(pDict)

        return{"data": data} 
   
        
class AnimalService:
    
    def getAnimal(id):
        animal = Animal.objects.get(pk=id)
        dict = model_to_dict(animal, exclude=['imagen'])
        dict["imagen"] = base64.b64encode(open("media/" + str(animal.imagen), "rb").read()).decode('utf-8')
        return dict
                    
    def registerAnimal(data):
        try:
            protectora = Protectora.objects.get(pk=data["protectora"])
        except:
            return "ERROR: Protectora asociada no registrada"
        try:
            animal = Animal(name = data["name"], fechaNacimiento=data["fechaNacimiento"], tipo=data["tipo"],
            edad=data["edad"], estado=data["estado"], descripcion=data["descripcion"],
                protectora=protectora)
            animal.save()

            format, imgstr = data["imagen"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr))  
            file_name = animal.name + "-" + str(animal.id) +"." + ext
            animal.imagen.save(file_name, data, save=True)

            logger.info("OK: Registrado nuevo animal con ID: " +  str(animal.id) + " en Protectora " + str(animal.protectora.name))
            return model_to_dict(animal, exclude=['imagen'])
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
        
    def searchAnimal(args):
        animals = Animal.objects.filter(**args)
        data= []
        for animal in animals:
            aDict = model_to_dict(animal, exclude=['imagen']) 
            aDict["imagen"] = base64.b64encode(open("media/" + str(animal.imagen), "rb").read()).decode('utf-8')
            data.append(aDict)

        return{"data": data} 
        
class UserService:
    
    def createUser(input):
        try:
            user = User.objects.create_user(username=input["username"], password=input["pass"], is_staff=False)
            user.save()
            
            logger.info("Registrado nueva protectora: " + user.first_name)
            token, created = Token.objects.get_or_create(user=user)
            return {'token': token.key, 'IdProtectora': None}
        except:
            return "ERROR: Ya existe un usuario con ese login"
        
    def createProtectoraUser(input):
        protectora = ProtectoraService.createProtectora(input)

        user = User.objects.create_user(username=input["username"], password=input['pass'], is_staff=True)
        user.first_name = str(protectora["id"])
        user.save()

        logger.info("Registrado nueva usuario protectora: " + user.first_name)
        token, created = Token.objects.get_or_create(user=user)
        return {'token': token.key, 'IdProtectora': protectora["id"]}
    
    def getUserProtectora(input):
        user = User.objects.filter(username=input["username"])[0]
        token, created = Token.objects.get_or_create(user=user)
        return {'token': token.key, 'IdProtectora': user.first_name}

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
