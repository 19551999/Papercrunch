from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from modelsTest.models import Learner, Level, SubLevelConcepts, SubLevelQuiz, SubLevelStatus, LevelProgress
from modelsTest.playground import PlaygroundC
import random
import string
import os
import sys
import subprocess
from datetime import datetime



# Serializer for the API endpoint - /api/levels/
class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ('levelName',)



# Serializer for the API endpoint - /api/sub-level-concepts/
class SubLevelConceptsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubLevelConcepts
        fields = ('subLevelName', 'conceptTextOne', 'conceptTextTwo', 'conceptTextThree','level')



# Serializer for the API endpoint - /api/sub-level-quiz/
class SubLevelQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubLevelQuiz
        fields = ('question', 'optionOne', 'optionTwo', 'optionThree', 'answer', 'hint', 'stars', 'subLevel')



# Serializer for the API endpoint - /api/user-details/
class LearnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Learner
        fields = ('first_name', 'last_name')
        depth = 1       



# Serializer for the API endpoint - /api/google-sign-in-check/
class GoogleSignInCheckSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    google = serializers.BooleanField(read_only=True)
    exists = serializers.BooleanField(read_only=True)

    def validate(self, data):
        # print("Printing For Google Sign In Check")
        email = data.get('email', None)
        # print("\t{}".format(email))

        try:
            user = Learner.objects.get(email=email)
        except Learner.DoesNotExist:
            user = None

        # print(user)

        if user:
            data['exists'] = True
            if user.google:
                data['google'] = True
            else:
                data['google'] = False
        else:
            raise serializers.ValidationError("User does not exist!!")
        
        return data



# Serializer for the API endpoint - /api/register/
class LearnerRegistrationSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, style={'input_type': 'password'}, write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    google = serializers.BooleanField(required=False)
    avatarId = serializers.IntegerField(required=False, default=0)
    # date_of_birth = serializers.DateField()
    currentLevel = serializers.PrimaryKeyRelatedField(read_only=True)#, many=True)
    totalStars = serializers.IntegerField(default=0, read_only=True)

    class Meta(object):
        model = get_user_model()
        fields = ('email', 'password', 'first_name', 'last_name', 'currentLevel', 'avatarId', 'totalStars', 'avatarId', 'google')#'date_of_birth')
        depth = 1

    def validate_email(self, value):
        try:
            learner = Learner.objects.get(email=value)
        except Learner.DoesNotExist:
            learner = None
        if learner:
            if Learner.objects.get(email=value).google:
                raise serializers.ValidationError("Email already exists and Signed In through Google Auth")
            else:
                raise serializers.ValidationError("Email already exists")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password is too short")
        return value

    def create(self, validated_data):
        #### Create User ####
        user = Learner.objects.register_user(
            validated_data.get('email'), 
            validated_data.get('password'), 
            validated_data.get('first_name'), 
            validated_data.get('last_name'),
            Level.objects.all()[0],
            validated_data.get('avatarId'),
            validated_data.get('google')
            )
            
        #### Create Mail Parameters ####
        subject = "Welcome to the world of Coding {}".format(user.get_full_name())
        details = {
            'full_name' : user.get_full_name(),
            'email': user.email,
            'password': validated_data.get('password'),
        }
        file_addr = 'user_register/test.txt'
        
        #### Create Token ####
        token = Token.objects.create(user=user)
        # print(token.key)

        #### Create Files for Playground ####
        user_filename = './modelsTest/user_codes/C_Files/' + token.key + '.c'
        # print('\n\tUser Filename : {}\n'.format(user_filename))
        with open(user_filename, 'w+') as f:
            f.write("#include<stdio.h>\nint main(void){\n\tprintf(\"HelloWorld!!\");\n\treturn(0);\n}")
            f.close()

        #### Create SubLevelStatus ####
        status = SubLevelStatus.objects.create(learner=user)

        #### Create Progress ####
        progress = LevelProgress.objects.create(learner=user)

        # user.send_email(subject, file_addr, details)

        return user



# Serializer for the API endpoint - /api/login/
class LearnerLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
    token = serializers.CharField(read_only=True)
    currentLevel = serializers.PrimaryKeyRelatedField(read_only=True)#, many=True)
    totalStars = serializers.IntegerField(read_only=True)
    avatarId = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)

    class Meta(object):
        model = get_user_model()
        fields = ('email', 'password', 'token', 'currentLevel', 'totalStars', 'avatarId', 'first_name', 'last_name')

    def validate(self, data):
        # print("Printing For Login")
        email = data.get('email', None)
        password = data.get('password', None)
        # print("\t{}".format(email))
        # print("\t{}".format(password))

        if not email and not password:
            raise serializers.ValidationError("Please enter your credentials to login!!")

        user = get_user_model().objects.filter(email=email).exclude(superuser=True)
        # print("\t{}".format(user))

        if user.exists() and user.count() == 1:
            learner = user.first()
            # print("\t{}".format(learner))
        else:
            raise serializers.ValidationError("This email is not valid !!")

        if learner:
            if not learner.check_password(password):
                raise serializers.ValidationError("Invalid Credentials")
        
        if learner.active:
            token, created = Token.objects.get_or_create(user=learner)
            # print("\t{}".format(token))
            # print(type(token))
            data['token'] = token
            data['currentLevel'] = learner.currentLevel
            data['totalStars'] = learner.totalStars
            data['avatarId'] = learner.avatarId
            data['first_name'] = learner.first_name
            data['last_name'] = learner.last_name
            learner.last_login = datetime.now()
        else:
            raise serializers.ValidationError("User not active")

        return data



# Serializer for the API endpoint - /api/reset-password/
class PassowrdResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, data):
        # print("Printing for Password Reset")

        email = data.get('email', None)
        user = Learner.objects.get(email=email)
        subject = "Reset password for PaperCrunch Account - {}".format(user.email)
        
        # print("\t{}".format(user.password))
        
        password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
        details = {
            'email': user.email,
            'full_name': user.get_full_name(),
            'password': password,
        }
        
        # print("\t{}".format(password))
        
        user.set_password(password)
        user.save()
        
        # print("\t{}".format(user.password))
        
        file_addr = 'password_reset/password_reset_body.txt'

        if user:
            # user.send_email(subject, file_addr, details, email)
            pass
        return data



# Serializer for the API endpoint - /api/change-password/
class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
    new_password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        # print("Printing for Password Change")
        password = data['password']
        new_password = data['new_password']
        request = self.context['request']
        token = request.auth
        user = Token.objects.get(key=token).user
        # print("\n")
        # print("\t{}".format(data))
        # print("\t{}".format(data['password']))
        # print("\t{}".format(data['new_password']))
        # print("\t{}".format(token))
        # print("\t{}".format(user.email))
        # print("\t{}".format(user.check_password(password)))


        if user.check_password(password):
            # print("\t{}".format("Old Password"))
            # print("\t{}".format(user.password))
            user.set_password(new_password)
            user.save()
            # print("\t{}".format("New Password"))
            # print("\t{}".format(user.password))
        else:
            # print("\t{}".format("WTF"))
            raise serializers.ValidationError("Please enter a valid password !!")
        return data



# Serializer for the API endpoint - /api/logout/
class LearnerLogoutSerializer(serializers.Serializer):
    # email = serializers.EmailField(required=True, write_only=True)
    success = serializers.CharField(read_only=True, default="False")



# Serializer for the API endpoint - /api/sync-from-mobile/
class SyncUserDataFromMobileSerializer(serializers.ModelSerializer):
    
    currentLevel = serializers.PrimaryKeyRelatedField(queryset=Level.objects.all(), write_only=True)#, many=True)
    totalStars = serializers.IntegerField(write_only=True)
    avatarId = serializers.IntegerField(write_only=True)

    class Meta(object):
        model = get_user_model()
        fields = ('currentLevel', 'totalStars', 'avatarId')

    def validate(self, data):
        # print("\nPrinting For Sync from Mobile")
        request = self.context['request']
        token = request.auth
        user = request.user
        # print("\tToken : {}".format(token))
        # print("\tUser : {}".format(user))
        if not token:
            raise serializers.ValidationError("Please submit the User Token !!")
        
        if user.active:
            # # print("\n")
            # print("\t{}".format(repr(data)))
            # print("\t{}".format(data['currentLevel']))
            # # print("\n")
            user.currentLevel = data['currentLevel']
            user.totalStars = data['totalStars']
            user.avatarId = data['avatarId']
            user.save()
            # print("Sync from Mobile Done")
        else:
            raise serializers.ValidationError("User not active")

        return user



# Serializer for the API endpoint - /api/status/
class SubLevelStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubLevelStatus
        fields = ('subLevel1', 'subLevel2', 'subLevel3', 'subLevel4', 'subLevel5', 'subLevel6', 'subLevel7', 'subLevel8', 'subLevel9', 'subLevel10', 'subLevel11', 'subLevel12', 'subLevel13', 'subLevel14', 'subLevel15', 'subLevel16', 'subLevel17', 'subLevel18', 'subLevel19', 'subLevel20', 'subLevel21', 'subLevel22', 'subLevel23', 'subLevel24', 'subLevel25', 'subLevel26', 'subLevel27')



# Serializer for the API endpoint - /api/user-progress/
class LevelProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelProgress
        fields = ('levelOne', 'levelTwo', 'levelThree', 'levelFour', 'levelFive', 'levelSix', 'levelSeven', 'levelEight', 'levelNine')



# Serializer for the API endpoint - /api/playground/
class PlaygroundSerializer(serializers.Serializer):

    code = serializers.CharField(write_only=True)
    compiled_result = serializers.CharField(read_only=True)
    run_result = serializers.CharField(read_only=True, default="No Result")

    def validate(self, data):
        # print("Printing For Sync from Mobile")
        # print(data['code'])
        request = self.context['request']
        token = request.auth
        # print("\tToken : {}".format(token))

        token = str(request.auth)

        code = PlaygroundC(token, data['code'])

        data['compiled_result'], data['run_result'] = code.run_c_program()

        # print(data['compiled_result'])
        # print("\n")
        # print(data['run_result'])
        
        return data
