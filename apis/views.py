from django.db.models.query_utils import Q
from apis.serialaizers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apis.models import Conversation, Message, Person



# Create your views 

@api_view(['POST'])
def register(request):
    user = Person.objects.filter(username=request.POST['username'])
    if user.exists():
        context = {
            'status': False,
            'message': 'username already exists!',
        }
        return Response(context)
    else:
        new_user = Person(
            first_name = request.POST['first_name'],
            last_name  = request.POST['last_name'],
            username   = request.POST['username'],
            email      = request.POST['email'],
            password   = request.POST['password'],
            image = request.FILES['image'],
        )
        new_user.save()
        context = {
            'status': True,
            'message': 'user created!',
            'user_id': Person.objects.get(username=request.POST['username']).id
        }
        return Response(context)

@api_view(['POST'])
def login(request):
    username = Person.objects.filter(username=request.POST['username'])
    password = Person.objects.filter(username=request.POST['username'],password=request.POST['password'])
    ############ user exists #########################
    if username.exists() and password.exists():
        context = {
            'status': True,
            'message': 'successfuly loged in!',
            'user_id': Person.objects.get(username = request.POST['username']).id
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
    _person = Person.objects.get(id=id)
    _person_conversations = Conversation.objects.filter(
            Q(
                person_1 = _person
            )|
            Q(
                person_2 = _person
            )
        )
    _person_serialaze = personSerialaizer(instance=_person,many=False)
    _person_conversations_serialaze = conversationSerialaizer(instance=_person_conversations,many=True)

    context = {
        'person': _person_serialaze.data,
        'conversations': _person_conversations_serialaze.data,
    }
    return Response(context)

@api_view(['POST'])
def send_message(request,sender,receiver):
    _sender   = Person.objects.get(id = sender) 
    _receiver = Person.objects.get(id = receiver)
    new_message = Message(
            text = request.POST['text'],
            sender   = _sender,
            receiver = _receiver
        )
    new_message.save()
    ## search for existing conversation
    _conversation = Conversation.objects.filter(
            Q(
                person_1 = _sender,
                person_2 = _receiver
            )|
            Q(
                person_2 = _sender,
                person_1 = _receiver
            )
        )
    ## if conversation exists
    if _conversation.exists():
        _conversation[0].messages.add(new_message)
        context = {
            'status':True,
            'message':'message succesfully sent!'
            }
        return Response(context)
    ## if conversation dose not exists
    else:
        new_conversation = Conversation(
        person_1 = _sender,
        person_2 = _receiver
        )
        new_conversation.save()
        new_conversation.messages.add(new_message)
        new_conversation.save()

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
    _person = Person.objects.filter(id=id)
    _person.update(is_online = True)
@api_view(['GET'])
def offline_person_status(request,id):
    _person = Person.objects.filter(id=id)
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
    _person = Person.objects.filter(id=id)
    _person.update(is_online = False)
    Conversation.objects.filter(person_1=Person.objects.get(id=id)).update(is_online = False)
    Conversation.objects.filter(person_2=Person.objects.get(id=id)).update(is_online = False)





    
