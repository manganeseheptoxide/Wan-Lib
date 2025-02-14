from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Room, Topic, Message, Type
from .forms import RoomForm, UserForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

# from django.http import HttpResponse

# rooms = [
#     {'id' : 1, 'name' : 'Lets learn python!'},
#     {'id' : 2, 'name' : 'Lets learn django!'},
#     {'id' : 3, 'name' : 'Lets learn tensorflow!'}
# ]

def login_page(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist!')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is incorrect!')


    context = {'page': page}
    return render(request, 'base/login_reg.html', context)

def logout_user(request):
    logout(request)
    return redirect('home')

def register_user(request):
    page = 'register'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    context = {'page': page, 'form':form}
    return render(request, 'base/login_reg.html',context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains = q) |
                                Q(name__icontains = q) |
                                Q(description__icontains = q))
    topics = Topic.objects.all()
    types = Type.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__name__icontains = q))
    context = {'rooms' : rooms, 'topics': topics, 
               'room_count': room_count,
               'room_messages': room_messages,
               'types': types}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    comments = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk = room.id)

    context = {'room': room, 'comments':comments, 'participants':participants}
    return render(request, 'base/room.html', context)

def profile_page(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html',context)

@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name) #it will create the object if it does not exist

        Room.objects.create(
            host = request.user,
            topic = topic,
            name= request.POST.get('name'),
            description = request.POST.get('description')

        )
        return redirect('home')

    context = {'form':form, 'topics':topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('Go Away')

    if request.method == 'POST':

        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name) #it will create the object if it does not exist
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form':form, 'topics':topics, 'room':room}

    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('Go Away')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})

@login_required(login_url='login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    room = message.room
    if request.user != message.user:
        return HttpResponse('Go Away')
    if request.method == 'POST':
        message.delete()
        return redirect('room', pk = room.id)
    
    return render(request, 'base/delete.html', {'obj': message})

@login_required(login_url='login')
def update_user(request):
    user = request.user
    form = UserForm(instance = user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)

    return render(request, 'base/update_user.html', {'form': form})

def topics(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(Q(name__icontains = q))
    return render(request, 'base/topics.html', {'topics': topics})

def activity(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})

def landing_page(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains = q) |
                                Q(name__icontains = q) |
                                Q(description__icontains = q))
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__name__icontains = q))
    context = {'rooms' : rooms, 'topics': topics, 
               'room_count': room_count,
               'room_messages': room_messages}
    return render(request, 'base/landing_page.html', context)

def knowledge(request):
    context = {}
    return render(request, 'base/knowledge.html', context)

def knowledge_water(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains = q) |
                                Q(name__icontains = q) |
                                Q(description__icontains = q))
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__name__icontains = q))
    context = {'rooms' : rooms, 'topics': topics, 
               'room_count': room_count,
               'room_messages': room_messages}
    return render(request, 'base/knowledge_water.html', context)

def knowledge_air(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains = q) |
                                Q(name__icontains = q) |
                                Q(description__icontains = q))
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__name__icontains = q))
    context = {'rooms' : rooms, 'topics': topics, 
               'room_count': room_count,
               'room_messages': room_messages}
    return render(request, 'base/knowledge_air.html', context)

def knowledge_earth(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains = q) |
                                Q(name__icontains = q) |
                                Q(description__icontains = q))
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__name__icontains = q))
    context = {'rooms' : rooms, 'topics': topics, 
               'room_count': room_count,
               'room_messages': room_messages}
    return render(request, 'base/knowledge_earth.html', context)

def knowledge_fire(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains = q) |
                                Q(name__icontains = q) |
                                Q(description__icontains = q))
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__name__icontains = q))
    context = {'rooms' : rooms, 'topics': topics, 
               'room_count': room_count,
               'room_messages': room_messages}
    return render(request, 'base/knowledge_fire.html', context)

def discussion(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains = q) |
                                Q(name__icontains = q) |
                                Q(description__icontains = q))
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__name__icontains = q))
    context = {'rooms' : rooms, 'topics': topics, 
               'room_count': room_count,
               'room_messages': room_messages}
    return render(request, 'base/discussion.html', context)

