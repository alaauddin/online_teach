from django.contrib import admin
from .models import Board,Topic,Post, Subscription, Comment, Assignment
# Register your models here.
admin.site.register(Board)

admin.site.register(Post)
admin.site.register(Topic)
admin.site.register(Subscription)
admin.site.register(Comment)
admin.site.register(Assignment)