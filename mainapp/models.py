from django.db import models
from django.contrib.auth.models import User

class post(models.Model):
    title = models.CharField(max_length=300)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.DecimalField()
    created = models.DateTimeField(auto_now=True, auto_now_add=True)
    tags = models.ManyToManyField(tag, blank=True, null=True)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.name 