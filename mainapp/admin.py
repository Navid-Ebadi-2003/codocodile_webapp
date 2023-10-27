from django.contrib import admin
from mainapp import models

# Register your models here.
admin.site.register(models.post)
admin.site.register(models.comment)
admin.site.register(models.tag)
admin.site.register(models.Profile)
admin.site.register(models.followship)