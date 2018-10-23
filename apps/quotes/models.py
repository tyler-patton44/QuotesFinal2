from __future__ import unicode_literals
from django.db import models
from django.db.models import Q
import re
import bcrypt
from ..usersLogin.models import *
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class QuoteManager(models.Manager):
    def mes_validator(self, postData):
        errors = {}
        if len(postData['quote']) > 250:
            errors['reg'] = "Quote cannot be more than 250 characters"
        if len(postData['quote']) < 1:
            errors['reg'] = "Quote must be more than 1 character"
        return errors

    def insertMessage(self, postData):

        self.create(content=postData['quote'], author=postData['author'] , user=User.objects.get(id=postData['hidden']))

class Quote(models.Model):
    content = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="messages")
    likes = models.ManyToManyField(User, related_name="liked_messages")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = QuoteManager()

    def __repr__(self):
        return "<Quote {}>".format(self.content)


