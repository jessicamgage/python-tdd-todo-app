"""
The purpose of the apps.py file is to allow for a user to not have to manually configure apps via the INSTALLED_APPS bracket in settings.py.
In this case, the configuration for accounts is done in this file.
"""

from django.apps import AppConfig

class AccountsConfig(AppConfig):
    name = 'accounts'
