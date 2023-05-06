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
from django.forms.models import model_to_dict
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
        return JsonResponse(model_to_dict(protecora))
    
    def post(self, request):
        input = json.loads(request.body)
        protectora = ProtectoraService.createProtectora(input)
        return JsonResponse(model_to_dict(protectora), safe=False)
    
class Animal(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, id):
        animal = AnimalService.getAnimal(id)
        return JsonResponse(model_to_dict(animal))
    
    def post(self, request):
        input = json.loads(request.body)
        animal = AnimalService.registerAnimal(input)
        return JsonResponse(model_to_dict(animal), safe=False)