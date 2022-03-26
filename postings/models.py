from django.db import models

from users.models import User

class Post(models.Model):
    user       = models.ForeignKey('users.User', on_delete = models.CASCADE)
    content    = models.TextField(null = True)
    created_at = models.DateTimeField(auto_now = True)
    updated_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'posts'

class Image(models.Model):
    post       = models.ForeignKey('Post', on_delete = models.CASCADE)
    image_url  = models.CharField(max_length=1000)

    class Meta: 
        db_table = 'images'

class Comment(models.Model):
    user       = models.ForeignKey('users.User', on_delete = models.CASCADE)
    post       = models.ForeignKey('Post', on_delete = models.CASCADE)
    comment    = models.TextField()
    created_at = models.DateField(auto_now = True)
    
    class Meta:
        db_table = 'comments'