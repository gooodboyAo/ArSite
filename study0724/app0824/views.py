from django.contrib.admin import action
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer
from .models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view


# Create your views here.

class UserInfoViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(["GET"])
def getuser(request, pk, *args, **kwargs):
    top_1 = User.objects.filter(id=pk)
    serializer = UserSerializer(instance=top_1, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
def update_info(request, pk, *args, **kwargs):
    info_row = User.objects.filter(id=pk).first()
    print(info_row)



def hello(request):
    return HttpResponse('hello')


def home(request):
    return HttpResponse('home')
