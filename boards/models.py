from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
from datetime import datetime, timedelta
from django.utils import timezone



# Create your models here.
class Board(models.Model):
    name = models.CharField(max_length=50,unique=True)
    description = models.CharField(max_length=150)
    picture = models.ImageField(upload_to="static/media/",null=True, blank=True)

    def __str__ (self):
        return self.name
    
    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()
    
    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_dt').first()


class Topic (models.Model):
    subject = models.CharField(max_length=255)
    video = models.FileField(upload_to='static/media/videos/trial', null=True, blank=True)
    board = models.ForeignKey(Board, related_name= 'topics', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)
    created_dt = models.DateTimeField(auto_now_add = True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__ (self):
        return self.subject


class Post (models.Model):
    message = models.TextField(max_length=4000)
    video = models.FileField(upload_to='static/media/videos', null=True, blank=True)
    topic = models.ForeignKey(Topic,related_name='posts', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='posts',on_delete=models.CASCADE)
    created_dt = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    

    
    def last_created_post_date(self):
        return Post.objects.filter(topic=self.topic).order_by('-created_dt').first().created_dt
      
    def total_likes(self):
        return self.likes.count()
    
class Comment(models.Model):
    content = models.TextField(max_length=1000)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    created_dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.created_by.username} on {self.created_dt}"


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    start_date = models.DateField(default=datetime.now)
    end_date = models.DateField()
    is_approved = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)




    def save(self, *args, **kwargs):
        # Set the end date as one month from the start date
        self.end_date = self.start_date + timedelta(days=30)
        super().save(*args, **kwargs)



class Assignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_date = models.DateField(default=datetime.now)
    file = models.FileField(upload_to='static/media/assignment', null=True, blank=True)
    end_date = models.DateField()
    solved = models.BooleanField(default=False)
    sol = models.FileField(upload_to='static/media/assignment/solutions', null=True, blank=True, default=None)

