from django.db import models
from django.contrib.auth.models import User

class tag(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class post(models.Model):
    title = models.CharField(max_length=300)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=6, decimal_places=6)
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(tag, blank=True, null=True)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.name 
    
class comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(post, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.text[0:20]
    
class Profile(models.Model):
    genders = [
        ('N', 'Rather not to say'),
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    avatar = models.ImageField(null=True, blank=True, upload_to='avatars')
    full_name = models.CharField(max_length=100,null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    gender = models.CharField(max_length=1, default='N', choices=genders)
    related_user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.related_user.username