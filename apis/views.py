from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from apis.serialaizers import personSerialaizer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apis.models import Conversation, Message, Person



# Create your views 

@api_view(['POST'])
def register(request):
    user = User.objects.filter(username=request.POST['username'])
    if user.exists():
        context = {
            'status': False,
            'message': 'username already exists!',
        }
        return Response(context)
    else:
        new_user = User(
            first_name = request.POST['first_name'],
            last_name  = request.POST['last_name'],
            username   = request.POST['username'],
            email      = request.POST['email'],
            password   = request.POST['password'],
        )
        new_user.save()
        new_person = Person(
            image = request.FILES['image'],
            user  = new_user,
            phone = request.POST['phone']
        )
        new_person.save()

        context = {
            'status': True,
            'message': 'user created!',
            'user_id': User.objects.get(username=request.POST['username']).id
        }
        return Response(context)

@api_view(['POST'])
def login(request):
    username = User.objects.filter(username=request.POST['username'])
    password = User.objects.filter(username=request.POST['username'],password=request.POST['password'])
    ############ user exists #########################
    if username.exists() and password.exists():
        context = {
            'status': True,
            'message': 'successfuly loged in!',
            'user_id': User.objects.get(username = request.POST['username']).id
        }
        return Response(context)
    ############ user dose not exists #################
    if username.exists()==False and password.exists()==False:
        context = {
            'status': False,
            'message': 'username and password are wrong!',
        }
        return Response(context)
    ############ username wrong #################
    if username.exists() == False:
        context = {
            'status': False,
            'message': 'username is wrong!',
        }
        return Response(context)
    ############ password wrong #################
    if password.exists() == False:
        context = {
            'status': False,
            'message': 'password is wrong!',
        }
        return Response(context)

@api_view(['GET'])
def Persons(request):
    persons = Person.objects.all()
    serialaze = personSerialaizer(instance=persons,many=True)
    return Response(serialaze.data)


@api_view(['GET'])
def person(request,id):
    _person = Person.objects.get(user__id=id)
    serialaze = personSerialaizer(instance=_person,many=False)
    return Response(serialaze.data)

@api_view(['POST'])
def send_message(request,sender,receiver):
    new_message = Message(
            text = request.POST['text'],
            sender   = User.objects.get(id=sender),
            receiver = User.objects.get(id=receiver)
        )
    new_message.save()
    _sender   = Person.objects.get(user__id = sender) 
    _receiver = Person.objects.get(user__id = receiver)
    _conversation = Conversation.objects.filter(
            Q(
                user_1 = User.objects.get(id=sender),
                user_2 = User.objects.get(id=receiver)
            )|
            Q(
                user_2 = User.objects.get(id=sender),
                user_1 = User.objects.get(id=receiver)
            )
        )
    
    if _conversation.exists():
        _conversation[0].messages.add(new_message)
        context = {
            'status':True,
            'message':'message succesfully sent!'
            }
        return Response(context)

    else:
        new_conversation = Conversation(
        user_1 = User.objects.get(id=sender),
        user_2 = User.objects.get(id=receiver)
        )
        new_conversation.save()
        new_conversation.messages.add(new_message)
        new_conversation.save()
        _sender.conversations.add(new_conversation)
        _receiver.conversations.add(new_conversation)

        context = {
            'status':True ,
            'message':'a new conversation created and messgae sent!'
            }
        return Response(context)

@api_view(['POST'])
def edit_message(request,id):
    _message = Message.objects.filter(id=id)
    _message.update(text=request.POST['text'])
    context = {
        'satatus': True,
        'message': 'message edited!',
    }
    return Response(context)

@api_view(['GET'])
def delete_message(request,id):
    _message = Message.objects.filter(id=id)
    _message.delete()
    context = {
        'satatus': True,
        'message': 'message deleted!',
    }
    return Response(context)

@api_view(['GET'])
def online_person_status(request,id):
    _person = Person.objects.filter(user__id=id)
    _person.update(is_online = True)
@api_view(['GET'])
def offline_person_status(request,id):
    _person = Person.objects.filter(user__id=id)
    _person.update(is_online = False)

@api_view(['GET'])
def online_conversation_status(request,id):
    _conversation = Conversation.objects.filter(id=id)
    _conversation.update(is_online = True)
@api_view(['GET'])
def offline_conversation_status(request,id):
    _conversation = Conversation .objects.filter(id=id)
    _conversation.update(is_online = False)
@api_view(['GET'])
def offline_all(request,id):
    user = Person.objects.filter(user__id=id)
    user.update(is_online = False)
    Conversation.objects.filter(user_1=User.objects.get(id=id)).update(is_online = False)
    Conversation.objects.filter(user_2=User.objects.get(id=id)).update(is_online = False)





    
