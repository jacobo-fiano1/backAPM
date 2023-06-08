import json
from django.shortcuts import render
from django.views import View
from unicodedata import name
from django.shortcuts import render;
from django.http import JsonResponse;
from django.views import View
from django.views.decorators.csrf import csrf_exempt 
from django.utils.decorators import method_decorator
from .protectoraService import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from rest_framework.views import APIView

# Create your views here.

class Protecora(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        protecora = ProtectoraService.getProtectora(id)
        return JsonResponse(protecora, safe=False)
    
    def post(self, request):
        input = json.loads(request.body)
        protectora = ProtectoraService.createProtectora(input)
        return JsonResponse(protectora, safe=False)
    
    def delete(self, requset, id):
        result = ProtectoraService.deleteProtectora(id)
        return JsonResponse(result, safe=False)
    
class Users(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request):
        input = json.loads(request.body)
        user = UserService.createUser(input)
        return JsonResponse(user, safe=False)


class ProtectoraUsers(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request):
        input = json.loads(request.body)
        user = UserService.createProtectoraUser(input)
        return JsonResponse(user, safe=False)
    

class Animal(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        animal = AnimalService.getAnimal(id)
        return JsonResponse(animal, safe=False)
    
    def post(self, request):
        input = json.loads(request.body)
        animal = AnimalService.registerAnimal(input)
        return JsonResponse(animal, safe=False)
    
    def delete(self, requset, id):
        result = AnimalService.deleteAnimal(id)
        return JsonResponse(result, safe=False)
    
class AnimalSearch(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        args = {}

        for arg in ["tipo", "edad", "estado"]:
            try:
                args[arg] = request.GET[arg]
            except:
                continue

        print("search animals PARAMS: " + str(args) )
        animal = AnimalService.searchAnimal(args)
        return JsonResponse(animal, safe=False)
    
class TwitterAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        input = json.loads(request.body)
        animal = TwitterService.postTweetNewAnimal(input)
        return JsonResponse(animal, safe=False)