from xml.parsers.expat import model
from django.forms import ModelForm
from mainapp.models import post, Profile, comment

class postForm(ModelForm):
    class Meta:
        model = post
        fields = ['title', 'body', 'tags']

class profileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        
class commentForm(ModelForm):
    class Meta:
        model = comment
        fields = ['text']