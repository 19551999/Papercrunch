from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from rest_framework.authtoken.models import Token
from modelsTest.models import Learner, Level, SubLevelConcepts, SubLevelQuiz, SubLevelStatus, LevelProgress
from modelsTest.forms import LearnerCreationForm, LearnerChangeForm

import os
# Register your models here.



class LearnerAdmin(UserAdmin): # Class to declare the databse model for registering in the Admin page

    add_form = LearnerCreationForm
    form = LearnerChangeForm

    model = Learner

    list_display = (
        'id',
        'email',
        'first_name',
        'last_name',
        'currentLevel',
        'totalStars',
        'avatarId',
        'google',
        'staff',
        'active',
        'last_login',
        )
    list_filter = (
        'email',
        'active',
        'google',
    )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Details', {'fields': ('first_name', 'last_name', 'date_of_birth', 'google')}),
        ('Learning Path', {'fields': ('currentLevel', 'totalStars')}),
        ('Permissions', {
            'classes': ('wide',),
            'fields': ('active', 'staff', 'superuser', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1')
            }
        ),
    )
    list_display_links = ('email', )
    readonly_fields = ('email',)
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('id',)
    filter_horizontal = ()
    actions = ['delete_model']


    # A function that searches all the parameters related to the user like
    # his token, respective play ground files, level progress and sub level 
    # status and deletes them
    def delete_model(self, request, queryset): 
        for obj in queryset:
            token = Token.objects.get(user=obj)
            if os.path.exists('./modelsTest/user_codes/C_Files/' + str(token) + '.c'):
                os.remove('./modelsTest/user_codes/C_Files/' + str(token) + '.c')
            if os.path.exists('./modelsTest/user_codes/Compiled_Files/' + str(token)):
                os.remove('./modelsTest/user_codes/Compiled_Files/' + str(token))
            status = SubLevelStatus.objects.get(learner=obj)
            status.delete()
            progress = LevelProgress.objects.get(learner=obj)
            progress.delete()
            obj.delete()
    delete_model.short_description = "Delete the selected objects including SubLevelStatus, Progress and Files"


class LevelAdmin(admin.ModelAdmin): # Class to declare the databse model for registering in the Admin page
    list_display = ('levelName',)


class SubLevelConceptsAdmin(admin.ModelAdmin): # Class to declare the databse model for registering in the Admin page
    list_display = ('id', 'subLevelName', 'conceptTextOne', 'conceptTextTwo', 'conceptTextThree', 'level')


class SubLevelQuizAdmin(admin.ModelAdmin): # Class to declare the databse model for registering in the Admin page
    list_display = ('id',  'subLevel', 'question', 'optionOne', 'optionTwo', 'optionThree', 'answer', 'hint', 'stars')


class SubLevelStatusAdmin(admin.ModelAdmin): # Class to declare the databse model for registering in the Admin page
    model = SubLevelStatus
    list_display = ('learner', 'subLevel1', 'subLevel2', 'subLevel3', 'subLevel4', 'subLevel5', 'subLevel6', 'subLevel7', 'subLevel8', 'subLevel9', 'subLevel10', 'subLevel11', 'subLevel12', 'subLevel13', 'subLevel14', 'subLevel15', 'subLevel16', 'subLevel17', 'subLevel18', 'subLevel19', 'subLevel20', 'subLevel21', 'subLevel22', 'subLevel23', 'subLevel24', 'subLevel25', 'subLevel26', 'subLevel27')
    list_display_links = ('learner', )


class LevelProgressAdmin(admin.ModelAdmin): # Class to declare the databse model for registering in the Admin page
    model = LevelProgress
    list_display = (
        'learner', 
        'levelOne', 
        'levelTwo', 
        'levelThree', 
        'levelFour', 
        'levelFive', 
        'levelSix', 
        'levelSeven', 
        'levelEight', 
        'levelNine'
        )
    list_display_links = ('learner', )




# Register the databse models so that they are viewed in the Admin Page
admin.site.register(Learner, LearnerAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(SubLevelConcepts, SubLevelConceptsAdmin)
admin.site.register(SubLevelQuiz, SubLevelQuizAdmin)
admin.site.register(SubLevelStatus, SubLevelStatusAdmin)
admin.site.register(LevelProgress, LevelProgressAdmin)