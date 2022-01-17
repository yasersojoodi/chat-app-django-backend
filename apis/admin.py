from django.contrib import admin
from apis.models import  Message, Person,Conversation

# Register your models here.

admin.site.register(Person)
admin.site.register(Conversation)
admin.site.register(Message)

