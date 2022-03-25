from django.db import models

from users.models import User

class Post(models.Model):
    user       = models.ForeignKey(User, on_delete = models.CASCADE)
    caption    = models.TextField(null = True)
    created_at = models.DateTimeField(auto_now = True)
    updated_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'posts'

class Image(models.Model):
    post   = models.ForeignKey('Post', on_delete = models.CASCADE)
    image  = models.CharField(max_length=1000)

    class Meta: 
        db_table = 'images'


    