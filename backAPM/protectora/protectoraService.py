import json
from .models import Protectora, Animal, UserFavs
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
import logging
import base64
from django.core.files.base import ContentFile
from requests_oauthlib import OAuth1Session

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class ProtectoraService:

    def getProtectora(id):

        protectora = Protectora.objects.get(pk=id)
        dict = model_to_dict(protectora, exclude=['imagen'])
        dict["imagen"] = base64.b64encode(open("media/" + str(protectora.imagen), "rb").read()).decode('utf-8')
        
        return dict

    def createProtectora(data):
        latitud=0.0
        longitud=0.0
        try:
            latitud=data["latitud"]
            longitud=data["longitud"]
        except:
            print("Protectora sin Long y Lat")

        protectora = Protectora(name = data["name"], direccion=data["direccion"], ubicacion=data["ubicacion"],
            telefono=data["telefono"], url=data["url"], correo=data["correo"], descripcion=data["descripcion"],
            latitud=latitud, longitud=longitud)
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
        try:
            animal = Animal.objects.get(pk=id)
            dict = model_to_dict(animal, exclude=['imagen'])
            dict["imagen"] = base64.b64encode(open("media/" + str(animal.imagen), "rb").read()).decode('utf-8')
            return dict
        except:
            return "ERROR: Animal con id " +  id + " no registrado"
                    
    def registerAnimal(data):
        try:
            protectora = Protectora.objects.get(pk=data["protectora"])
        except:
            return "ERROR: Protectora asociada no registrada"

        animal = Animal(name = data["name"], fechaNacimiento=data["fechaNacimiento"], tipo=data["tipo"],
            edad=data["edad"], estado=data["estado"], descripcion=data["descripcion"],
            protectora=protectora)
        animal.save()

        if data["twitterPub"]:
            TwitterService.postTweetNewAnimal(protectora.id, animal.id)

        format, imgstr = data["imagen"].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr))  
        file_name = animal.name + "-" + str(animal.id) +"." + ext
        animal.imagen.save(file_name, data, save=True)

        logger.info("OK: Registrado nuevo animal con ID: " +  str(animal.id) + " en Protectora " + str(animal.protectora.name))
        return model_to_dict(animal, exclude=['imagen'])

    
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
    
    def addTakeFavAnimal(idUser, idAnimal):
        AnimalService.getAnimal(idAnimal)
        usersFavs = UserFavs.objects.filter(idUsuario=idUser)
        if len(usersFavs) != 1:
            return "ERROR: Favs del Usuario no encontrados"
        
        userFavs = usersFavs[0]
        if int(idAnimal) in userFavs.idsAnimalFav:
            userFavs.idsAnimalFav.remove(int(idAnimal))
            userFavs.save()
            return {"msg": "OK: Animal con id " + idAnimal + " eliminado de  la lsita de favoritos"}
        
        userFavs.idsAnimalFav.append(idAnimal)
        userFavs.save()

        return {"msg": "OK: Animal con id " + idAnimal + " añadido a Favs"}
    
    def getFavAnimals(idUsuario):
        usersFavs = UserFavs.objects.filter(idUsuario=idUsuario)

        if len(usersFavs) != 1:
            return "ERROR: Favs del Usuario no encontrados"
        
        userFavs = usersFavs[0]

        favs = []
        for fav in userFavs.idsAnimalFav:
            animal = AnimalService.getAnimal(fav)
            favs.append(animal)

        return {"data": favs}
    
    def isAnimalFav(idUser, idAnimal):
        AnimalService.getAnimal(idAnimal)
        usersFavs = UserFavs.objects.filter(idUsuario=idUser)
        if len(usersFavs) != 1:
            return "ERROR: Favs del Usuario no encontrados"
        
        userFavs = usersFavs[0]
        if int(idAnimal) in userFavs.idsAnimalFav:
            return {"isFav" : True}
        else:
            return {"isFav" : False}

    def setAnimalEstate(idAnimal, estado):
        if estado not in ["AD", "RV", "DP"]:
            return "ERROR: Estado incorrecto"
        
        animal = Animal.objects.get(pk=idAnimal)
        animal.estado = estado
        animal.save()
        return {"msg": "OK: Animal " + idAnimal + " registrado como : AD"}


        

class UserService:
    
    def createUser(input):
        try:
            user = User.objects.create_user(username=input["username"], password=input["pass"], is_staff=False)
            user.save()

            favs = UserFavs(idUsuario=user.id, idsAnimalFav=[])
            favs.save()

            logger.info("Registrado nueva protectora: " + user.first_name)
            token, created = Token.objects.get_or_create(user=user)
            return {'token': token.key, 'Id': user.id, "isProtectora": False}
        except:
            return "ERROR: Ya existe un usuario con ese login"
        
    def createProtectoraUser(input):
        protectora = ProtectoraService.createProtectora(input)

        user = User.objects.create_user(username=input["username"], password=input['pass'], is_staff=True)
        user.first_name = str(protectora["id"])
        user.save()

        logger.info("Registrado nueva usuario protectora: " + user.first_name)
        token, created = Token.objects.get_or_create(user=user)
        return {'token': token.key, 'Id': protectora["id"], "isProtectora": True}
    
    def getUserInfo(username):
        users = User.objects.filter(username=username)

        if len(users) != 1:
            return "ERROR: No se encuentra al usuario"
        
        user = users[0]
        token, created = Token.objects.get_or_create(user=user)

        if user.is_staff == False:
            return {'token': token.key, 'Id': user.id, "isProtectora": False}
        
        return {'token': token.key, 'Id': user.first_name, "isProtectora": True}


class TwitterService:

    def postTweetNewAnimal(idProtectora, idAnimal):
        consumer_key = "2bWZSRrbe3FJJ6e51fEinyKHf"
        consumer_secret = "KoyJzMMtrbFdKBKaLSjNBu4xHwaKDHuFG4y2YLMCspA6asQ17w"
        access_token = "1659984139863355397-FL4hX9epzEx6WoCVV82UygYtLbQxpQ"
        access_token_secret = "dyOGB3IH5coCjwJFQjBS5zkXI8ckfKlN5NSYoR7uL2YrP"

        protectora = ProtectoraService.getProtectora(id=idProtectora)
        animal = Animal.objects.get(pk=idAnimal)

        msg = "! Nuevo compañero en " + protectora["name"] + " !" + "\n" + "Nuestro nuevo amigo es un " + animal.tipo + " y se llama " + animal.name + "\n"+ "\n"+ "Si estás interesado en saber más acerca de " + animal.name + " ponte en contacto con la protectora mediante su número de telefono: " + protectora["telefono"]+ " o escribiendo un correo a " + protectora["correo"] + "."

        print(msg)
        payload = {"text": msg}

        oauth = OAuth1Session(
            consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret,
        )
        response = oauth.post("https://api.twitter.com/2/tweets",json=payload)

        if response.status_code != 201:
            raise Exception(
                "Error al contactar con la API de Twitter: {} {}".format(response.status_code, response.text)
            )
 
        json_response = response.json()
        print(json.dumps(json_response, indent=4, sort_keys=True))
        return json_response
