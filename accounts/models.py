"""
These models are specific to anything involving an account, such as a User model.
Models are stored in the Django database tables -- every model is a 'column' and every instance of the model is a 'row'.
A complete user model is the entire row in the database table, and in this case, contains their User profile and their unique Token.
"""

from django.db import models
from django.contrib import auth
import uuid

auth.signals.user_logged_in.disconnect(auth.models.update_last_login)

class User(models.Model):
	email = models.EmailField(primary_key=True)
	REQUIRED_FIELDS = []
	USERNAME_FIELD = 'email'
	is_anonymous = False
	is_authenticated = True

class Token(models.Model):
	email = models.EmailField()
	uid = models.CharField(default=uuid.uuid4, max_length=40)
