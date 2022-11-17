from django.shortcuts import render
from django.http import HttpResponse
from .models import Chat


# Create your views here.
def hello(request):
    if request.method == 'GET':
        chat_list = Chat.objects.all()
        return render(request, 'chathome.html', {"message": chat_list})
    user_name = request.POST.get('chat_name')
    message = request.POST.get('chat_message')
    print(request.POST)
    Chat.objects.create(username=user_name, message=message)
    chat_list = Chat.objects.all().order_by('send_message_time')[:]
    print(chat_list)
    return render(request, 'chathome.html', {"message": chat_list})


def index(request):
    return render(request, 'chat_index.html')


def room(request, room_name):
    return render(request, "room.html", {"room_name": room_name})
