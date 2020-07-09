from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from modelsTest.managers import LearnerManager
import json

# Create your models here.

#################################################
# levelName - Name of the Level
#################################################
class Level(models.Model):
    levelName = models.CharField(max_length=200)

    def __str__(self):
        return self.levelName



###########################################################
# subLevelName     - Name of the Sub Level
# conceptTextOne   - First part of the concept Text
# conceptTextTwo   - Second part of the concept Text
# conceptTextThree - Third part of the concept Text
# level            - Primary Key of the level it is from
###########################################################
class SubLevelConcepts(models.Model):
    subLevelName = models.CharField(max_length=300)
    conceptTextOne = models.TextField(default="Text",null=True)
    conceptTextTwo = models.TextField(default="Text",null=True)
    conceptTextThree = models.TextField(default="Text",null=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)

    def __str__(self):
        return self.subLevelName



###########################################################
# subLevel     - Primary Key of the sub level it is from
# subLevelName - Name of the Sub Level
# question     - Self Explanatory 
# optionOne    - Self Explanatory 
# optionTwo    - Self Explanatory 
# optionThree  - Self Explanatory 
# answer       - Self Explanatory 
# hint         - Self Explanatory
# stars        - Max stars for that particular question
###########################################################
class SubLevelQuiz(models.Model):
    subLevel = models.ForeignKey(SubLevelConcepts, on_delete=models.CASCADE)
    subLevelName = models.CharField(max_length=300)
    question = models.TextField()
    optionOne = models.TextField()
    optionTwo = models.TextField()
    optionThree = models.TextField()
    answer = models.TextField()
    hint = models.TextField(blank=True)
    stars = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)],blank=True,)
    
    def __str__(self):
        return self.question



#########################################################################################
# first_name    - First Name of the User
# last_name     - Last Name of the User
# email         - Email of the User (Also username)
# date_of_birth - Date of Birth of the User

# currentLevel - Current sub level user is on
# totalStars   - Total stars he has gained till now
# avatarId     - Current avatar's Id

# google      - User property to tell whether he has signed in through Google Sign-in
# date_joined - User property of date of account making
# last_login  - User property of last login
# active      - Same as Django User model property
# staff       - Same as Django User model property
# superuser   - Same as Django User model property
#########################################################################################
class Learner(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False, null=True)

    currentLevel = models.ForeignKey(Level, related_name='currentLevel', on_delete=models.SET_NULL, null=True)
    totalStars = models.IntegerField(default=0)
    avatarId = models.IntegerField(default=0, validators=[MaxValueValidator(8),MinValueValidator(0)], null=True)

    google = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    superuser = models.BooleanField(default=False)

    objects = LearnerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def password_reset_email(self, password):
        details = {
            'email': self.email,
            'full_name': self.get_full_name(),
            'password': password,
        }
        subject = "Reset password for PaperCrunch Account"

        body = render_to_string('password_reset.txt', details)

        mail = EmailMultiAlternatives(subject, "", settings.DEFAULT_FROM_EMAIL, [self.email])
        mail.attach_alternative(body, 'text/html')
        mail.send(fail_silently=False)

    def send_email(self, subject_details, file_addr, body_details, email):
        subject = subject_details
        body = render_to_string(file_addr, body_details)
        mail = EmailMultiAlternatives(subject, "", settings.DEFAULT_FROM_EMAIL, (email, ))
        mail.attach_alternative(body, 'text/html')
        mail.send(fail_silently=False)

    
    @property
    def is_google(self):
        return self.google

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_superuser(self):
        return self.superuser

    def has_perm(self, perm, obj=None):
        return self.superuser

    def has_module_perms(self, app_label):
        return self.superuser

    @property
    def is_active(self):
        return self.active



###############################################################################
# learner                 - Primary key of the respective user
# subLevel1 to subLevel27 - Integer value for respective sub level status
###############################################################################
class SubLevelStatus(models.Model):
    learner = models.ForeignKey(Learner, related_name='subLevelStatus', on_delete=models.SET_NULL, null=True)
    subLevel1 = models.IntegerField(default=0, validators=[MaxValueValidator(2), MinValueValidator(0)],)
    subLevel2 = models.IntegerField(default=0, validators=[MaxValueValidator(2), MinValueValidator(0)],)
    subLevel3 = models.IntegerField(default=0, validators=[MaxValueValidator(2), MinValueValidator(0)],)
    subLevel4 = models.IntegerField(default=0, validators=[MaxValueValidator(2), MinValueValidator(0)],)
    subLevel5 = models.IntegerField(default=0, validators=[MaxValueValidator(2), MinValueValidator(0)],)
    subLevel6 = models.IntegerField(default=0, validators=[MaxValueValidator(2), MinValueValidator(0)],)
    subLevel7 = models.IntegerField(default=0, validators=[MaxValueValidator(2), MinValueValidator(0)],)
    subLevel8 = models.IntegerField(default=0, validators=[MaxValueValidator(2), MinValueValidator(0)],)
    subLevel9 = models.IntegerField(default=0, validators=[MaxValueValidator(2), MinValueValidator(0)],)
    subLevel10 = models.IntegerField(default=0, validators=[MaxValueValidator(2), MinValueValidator(0)],)
    subLevel11 = models.IntegerField(default=0, validators=[MaxValueValidator(2), MinValueValidator(0)],)
    subLevel12 = models.IntegerField(default=0, validators=[MaxValueValidator(2), MinValueValidator(0)],)
    subLevel13 = models.IntegerField(default=0, validators=[MaxValueValidator(2), MinValueValidator(0)],)
    subLevel14 = models.IntegerField(default=0, validators=[MaxValueValidator(2), MinValueValidator(0)],)
    subLevel15 = models.IntegerField(default=0, validators=[MaxValueValidator(2), MinValueValidator(0)],)
    subLevel16 = models.IntegerField(default=0, validators=[MaxValueValidator(2), MinValueValidator(0)],)
    subLevel17 = models.IntegerField(default=0, validators=[MaxValueValidator(2), MinValueValidator(0)],)
    subLevel18 = models.IntegerField(default=0, validators=[MaxValueValidator(2), MinValueValidator(0)],)
    subLevel19 = models.IntegerField(default=0, validators=[MaxValueValidator(2), MinValueValidator(0)],)
    subLevel20 = models.IntegerField(default=0, validators=[MaxValueValidator(2), MinValueValidator(0)],)
    subLevel21 = models.IntegerField(default=0, validators=[MaxValueValidator(2), MinValueValidator(0)],)
    subLevel22 = models.IntegerField(default=0, validators=[MaxValueValidator(2), MinValueValidator(0)],)
    subLevel23 = models.IntegerField(default=0, validators=[MaxValueValidator(2), MinValueValidator(0)],)
    subLevel24 = models.IntegerField(default=0, validators=[MaxValueValidator(2), MinValueValidator(0)],)
    subLevel25 = models.IntegerField(default=0, validators=[MaxValueValidator(2), MinValueValidator(0)],)
    subLevel26 = models.IntegerField(default=0, validators=[MaxValueValidator(2), MinValueValidator(0)],)
    subLevel27 = models.IntegerField(default=0, validators=[MaxValueValidator(2), MinValueValidator(0)],)

    def __str__(self):
        return self.learner.email



#########################################################################################
# learner               - Primary key of the respective user
# levelOne to levelNine - Integer value depicting the percentage of the level finished
#########################################################################################
class LevelProgress(models.Model):
    learner = models.ForeignKey(Learner, related_name='currentProgress', on_delete=models.SET_NULL, null=True)
    levelOne = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)],)
    levelTwo = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)],)
    levelThree = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)],)
    levelFour = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)],)
    levelFive = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)],)
    levelSix = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)],)
    levelSeven = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)],)
    levelEight = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)],)
    levelNine = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)],)

    def __str__(self):
        return self.learner.email
    