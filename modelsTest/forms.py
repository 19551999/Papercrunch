from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from modelsTest.models import Learner

class LearnerCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Learner
        fields = ('email',)


class LearnerChangeForm(UserChangeForm):
    class Meta:
        model = Learner
        fields = ('email',)