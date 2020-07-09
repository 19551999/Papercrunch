from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from datetime import datetime

class LearnerManager(BaseUserManager):

    def register_user(self, email, password, first_name, last_name, currentLevel, avatarId, google):
        user = self.create_user(email, password)
        user.first_name = first_name
        user.last_name = last_name
        # user.date_of_birth

        user.currentLevel = currentLevel
        if google:
            user.google = True
        user.last_login = datetime.now()
        user.date_joined = datetime.now().date()
        user.avatarId = avatarId
        user.save()
        return user
    
    def create_user(self, email, password):

        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save()
        return user

    def create_staffuser(self, email, password):
        user = self.create_user(email, password)
        user.staff = True
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.staff = True
        user.superuser = True
        user.first_name = "Admin"
        user.last_name = "User"
        user.last_login = datetime.now()
        user.date_joined = datetime.now().date()
        user.save()
        return user
