from django.db import models
from rest_framework import serializers
from django.contrib import auth

class Message(models.Model):
    subject = models.CharField(max_length=200)
    body = models.TextField()


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ('url', 'subject', 'body', 'pk')

class User(auth.models.User):
    user_ptr = None
