from django.db import models

# Create your models here.

class Person(models.Model):
    id         = models.AutoField(unique=True,primary_key=True)
    username   = models.CharField(max_length=200, null=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name  = models.CharField(max_length=200, null=True)
    password   = models.CharField(max_length=200)
    email      = models.EmailField(null=True)
    image      = models.ImageField(upload_to='user-images',null=True,default='user-images/default.png')
    phone      = models.CharField(max_length=200, null=True)
    conversations = models.CharField(max_length=1000, null=True)
    contacts      = models.CharField(max_length=1000, null=True)
    is_online     = models.BooleanField(default=False)
    created       = models.DateTimeField(auto_created=True,auto_now_add=True)
    def __str__(self) -> str:
        return self.username

class Message(models.Model):
    id       = models.AutoField(unique=True,primary_key=True)    
    text     = models.TextField(null=True)
    image    = models.ImageField(upload_to='message-images')
    sender   = models.OneToOneField(to=Person,on_delete=models.CASCADE,related_name='sender')
    receiver = models.OneToOneField(to=Person,on_delete=models.CASCADE,related_name='receiver')
    created  = models.DateTimeField(auto_now_add=True,auto_created=True)
    def __str__(self) -> str:
        return str(self.sender.username) + ' ----> ' + str(self.receiver.username)

class Conversation(models.Model):
    id        = models.AutoField(unique=True,primary_key=True)
    person_1  = models.OneToOneField(Person, on_delete=models.CASCADE,related_name='person_1')
    person_2  = models.OneToOneField(Person, on_delete=models.CASCADE,related_name='person_2')
    messages  = models.ManyToManyField(to=Message,blank=True)
    created   = models.DateTimeField(auto_created=True,auto_now_add=True)
    is_online = models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.person_1.username