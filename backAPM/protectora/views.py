import json
from django.shortcuts import render
from django.views import View
import imp
from unicodedata import name
from django.shortcuts import render;
from django.http import JsonResponse;
from django.views import View
from django.views.decorators.csrf import csrf_exempt 
from django.utils.decorators import method_decorator
from .models import Protectora
from .protectoraService import ProtectoraService, AnimalService
import asyncio
# Create your views here.

class Protecora(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
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
    
class Animal(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
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