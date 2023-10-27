from xml.parsers.expat import model
from django.forms import ModelForm
from mainapp.models import post, Profile, comment
from django import forms

class postForm(ModelForm):
    class Meta:
        model = post
        fields = ['title', 'body', 'tags']

class profileForm(ModelForm):
    # genders = [
    #     ('N', 'Rather not to say'),
    #     ('M', 'Male'),
    #     ('F', 'Female'),
    # ]
    class Meta:
        model = Profile
        fields = ['full_name', 'avatar', 'bio', 'gender', 'birth_date']
    # avatar = forms.ImageField(null=True, blank=True, upload_to='avatars')
    # full_name = forms.CharField(max_length=100,null=True, blank=True)
    # bio = forms.TextField(null=True, blank=True)
    # gender = forms.CharField(max_length=1, default='N', choices=genders)
    # birth_date = forms.DateField(null=True, blank=True)
        
class commentForm(ModelForm):
    class Meta:
        model = comment
        fields = ['text']
        
    