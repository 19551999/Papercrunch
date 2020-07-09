from django.urls import path, include
from modelsTest import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('levels/', views.LevelAPIView.as_view()),
    path('sub-level-concepts/', views.SubLevelConceptsAPIView.as_view()),
    path('sub-level-quiz/', views.SubLevelQuizAPIView.as_view()),
    # path('user-details/', views.LearnerAPIView.as_view()),
    path('register/', views.LearnerRegistrationAPIView.as_view()),
    path('login/', views.LearnerLoginAPIView.as_view()),
    path('reset-password/', views.ResetPasswordAPIView.as_view()),
    path('change-password/', views.ChangePasswordAPIView.as_view()),
    path('logout/', views.LearnerLogoutAPIView.as_view()),
    path('sync-from-mobile/', views.SyncUserDataFromMobileAPIView.as_view()),
    path('status/', views.SubLevelStatusAPIView.as_view()),
    path('user-progress/', views.LevelProgressAPIView.as_view()),
    path('playground/', views.PlaygroundAPIView.as_view()),
    path('google-sign-in-check/', views.GoogleSignInCheckAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)