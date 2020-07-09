from rest_framework import status, generics, views, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.shortcuts import render
import string
import random
import os

from modelsTest.models import Level, SubLevelConcepts, SubLevelQuiz, Learner, SubLevelStatus, LevelProgress
from modelsTest.serializers import LevelSerializer, SubLevelConceptsSerializer, SubLevelQuizSerializer, LearnerSerializer, LearnerRegistrationSerializer, LearnerLoginSerializer, PassowrdResetSerializer, ChangePasswordSerializer, LearnerLogoutSerializer, SyncUserDataFromMobileSerializer, PlaygroundSerializer, SubLevelStatusSerializer, LevelProgressSerializer, GoogleSignInCheckSerializer



# Views for the API endpoint - /api/levels/
class LevelAPIView(generics.ListAPIView):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )



# Views for the API endpoint - /api/sub-level-conceptss/
class SubLevelConceptsAPIView(generics.ListAPIView):
    queryset = Level.objects.all()
    serializer_class = SubLevelConceptsSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )
    


# Views for the API endpoint - /api/sub-level-quiz/
class SubLevelQuizAPIView(generics.ListAPIView):
    queryset = SubLevelQuiz.objects.all()
    serializer_class = SubLevelQuizSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )
    


# Views for the API endpoint - /api/user-details/
class LearnerAPIView(generics.RetrieveAPIView):
    serializer_class = LearnerSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )

    def get(self, request):
        # print(request.auth)
        user = request.user
        serializer = self.serializer_class(user)
        # print(user)
        # print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)



# Views for the API endpoint - /api/google-sign-in-check/
class GoogleSignInCheckAPIView(views.APIView):
    serializer_class = GoogleSignInCheckSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Views for the API endpoint - /api/register/
class LearnerRegistrationAPIView(generics.CreateAPIView):
    queryset = Learner.objects.all()
    serializer_class = LearnerRegistrationSerializer



# Views for the API endpoint - /api/login/
class LearnerLoginAPIView(views.APIView):
    serializer_class = LearnerLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # print(serializer.data)
            # print(type(serializer.data['token']))
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Views for the API endpoint - /api/reset-password/
class ResetPasswordAPIView(views.APIView):
    serializer_class = PassowrdResetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)



# Views for the API endpoint - /api/change-password/
class ChangePasswordAPIView(views.APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        user = request.user
        token = request.auth

        # print(user)
        # print(token)
        # print(request.data)
        # print(request.data['password'])
        # print(request.data['new_password'])

        serializer = self.serializer_class(
            data=request.data, 
            context={'request':request}
            )
        # print(serializer.initial_data)
        # # print(serializer.is_valid())
        

        if serializer.is_valid():
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Views for the API endpoint - /api/logout/
class LearnerLogoutAPIView(views.APIView):
    serializer_class = LearnerLogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )

    def get(self, request):
        # serializer = self.serializer_class(data=request.data)
        user = request.user
        # user = Learner.objects.get(email=request.data['email'])
        old_token = Token.objects.get(user=user)
        old_c_file = './modelsTest/user_codes/C_Files/' + str(old_token) + '.c'
        old_comp_file = './modelsTest/user_codes/Compiled_Files/' + str(old_token)
        # print(old_token)
        old_token.delete()
        new_token, created = Token.objects.get_or_create(user=user)
        new_c_file = './modelsTest/user_codes/C_Files/' + str(new_token) + '.c'
        # print(new_token)
        os.rename(old_c_file, new_c_file)
        if os.path.exists(old_comp_file):
            new_comp_file = './modelsTest/user_codes/Compiled_Files/' + str(new_token)
            os.rename(old_comp_file, new_comp_file)
        return Response(status=status.HTTP_200_OK)



# Views for the API endpoint - /api/sync-from-google/
class SyncUserDataFromMobileAPIView(views.APIView):
    serializer_class = SyncUserDataFromMobileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )

    def post(self, request):

        serializer = self.serializer_class(
            data=request.data,
            context={'request':request}
        )

        if serializer.is_valid():
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)



# Views for the API endpoint - /api/status/
class SubLevelStatusAPIView(views.APIView):
    serializer_class = SubLevelStatusSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )

    def get(self, request):
        user = request.user
        try:
            sublevelstatus = SubLevelStatus.objects.get(learner=user)
        except SubLevelStatus.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(sublevelstatus)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # print("\nPrinting for Status update")
        user = request.user
        try:
            sublevelstatus = SubLevelStatus.objects.get(learner=user)
        except SubLevelStatus.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        # print("\t{}".format(sublevelstatus))
        # print("\t{}".format(request.data))

        serializer = self.serializer_class(data=request.data)

        # print("\n")
        # print("\t{}".format(serializer.is_valid()))
        # print("\n")
        # print("\t{}".format(serializer.data))

        sublevelstatus.subLevel1 = serializer.data['subLevel1']
        sublevelstatus.subLevel2 = serializer.data['subLevel2']
        sublevelstatus.subLevel3 = serializer.data['subLevel3']
        sublevelstatus.subLevel4 = serializer.data['subLevel4']
        sublevelstatus.subLevel5 = serializer.data['subLevel5']
        sublevelstatus.subLevel6 = serializer.data['subLevel6']
        sublevelstatus.subLevel7 = serializer.data['subLevel7']
        sublevelstatus.subLevel8 = serializer.data['subLevel8']
        sublevelstatus.subLevel9 = serializer.data['subLevel9']
        sublevelstatus.subLevel10 = serializer.data['subLevel10']
        sublevelstatus.subLevel11 = serializer.data['subLevel11']
        sublevelstatus.subLevel12 = serializer.data['subLevel12']
        sublevelstatus.subLevel13 = serializer.data['subLevel13']
        sublevelstatus.subLevel14 = serializer.data['subLevel14']
        sublevelstatus.subLevel15 = serializer.data['subLevel15']
        sublevelstatus.subLevel16 = serializer.data['subLevel16']
        sublevelstatus.subLevel17 = serializer.data['subLevel17']
        sublevelstatus.subLevel18 = serializer.data['subLevel18']
        sublevelstatus.subLevel19 = serializer.data['subLevel19']
        sublevelstatus.subLevel20 = serializer.data['subLevel20']
        sublevelstatus.subLevel21 = serializer.data['subLevel21']
        sublevelstatus.subLevel22 = serializer.data['subLevel22']
        sublevelstatus.subLevel23 = serializer.data['subLevel23']
        sublevelstatus.subLevel24 = serializer.data['subLevel24']
        sublevelstatus.subLevel25 = serializer.data['subLevel25']
        sublevelstatus.subLevel26 = serializer.data['subLevel26']
        sublevelstatus.subLevel27 = serializer.data['subLevel27']

        sublevelstatus.save()
        # print("Status Done")
        # # print(sublevelstatus)
        # # print(serializer.data)
        return Response(status=status.HTTP_201_CREATED)



# Views for the API endpoint - /api/user-progress/
class LevelProgressAPIView(views.APIView):
    serializer_class = LevelProgressSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )

    def get(self, request):
        user = request.user
        try:
            progress = LevelProgress.objects.get(learner=user)
        except LevelProgress.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(progress)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        # print("\nPrinting for Progress POST")
        user = request.user
        try:
            progress = LevelProgress.objects.get(learner=user)
        except LevelProgress.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # print("\t{}".format(progress))
        # print("\t{}".format(request.data))

        serializer = self.serializer_class(data=request.data)

        # print("\n")
        # print("\t{}".format(serializer.is_valid()))
        # print("\n")
        # print("\t{}".format(serializer.data))

        progress.levelOne = serializer.data['levelOne']
        progress.levelTwo = serializer.data['levelTwo']
        progress.levelThree = serializer.data['levelThree']
        progress.levelFour = serializer.data['levelFour']
        progress.levelFive = serializer.data['levelFive']
        progress.levelSix = serializer.data['levelSix']
        progress.levelSeven = serializer.data['levelSeven']
        progress.levelEight = serializer.data['levelEight']
        progress.levelNine = serializer.data['levelNine']

        progress.save()
        # print("Progress Done")
        # # print(status)
        # # print(serializer.data)
        return Response(status=status.HTTP_200_OK)
        # else:
        #     serializer = self.serializer_class(progress)
        #     print(progress)
        #     print(serializer.data)
        #     return Response(serializer.data, status=status.HTTP_200_OK)



# Views for the API endpoint - /api/playground/
class PlaygroundAPIView(views.APIView):
    serializer_class = PlaygroundSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



