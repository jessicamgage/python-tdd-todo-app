"""
The purpose of an authentication.py file is to make sure that a user who sends a certain request has the credentials to receive the response they requested.
"""
from accounts.models import User, Token

class PasswordlessAuthenticationBackend(object):
	def authenticate(self, uid):
		try:
			token = Token.objects.get(uid=uid)
			return User.objects.get(email=token.email)
		except User.DoesNotExist:
			return User.objects.create(email=token.email)
		except Token.DoesNotExist:
			return None

	def get_user(self, email):
		try:
			return User.objects.get(email=email)
		except User.DoesNotExist:
			return None
