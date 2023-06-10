from django import forms
from .models import Job
from django.contrib.auth.forms import UserCreationForm
from .models import User

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'profile_image', 'label']

#part added for customer service email sending
class CustomerServiceForm(forms.Form):
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')
