from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.
from .models import Board, Topic, Post, Subscription, Comment,Assignment

from django.contrib.auth.models import User
# from .forms import NewTopicForm,PostForm
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.timezone import is_aware
from .forms import SubscriptionForm,CommentForm,AssignmentForm




def home(request):
    boards = Board.objects.all()
    return render(request,'home.html',{'boards':boards})

def board_topics(request, board_id):

    board = get_object_or_404(Board,pk=board_id)

    return render(request,'topics.html',{'board':board})


# @login_required
# def new_topic(request, board_id):
#     board = get_object_or_404(Board, pk=board_id)
#     if request.method == "POST":
#         form = NewTopicForm(request.POST, request.FILES)
#         if form.is_valid():
#             topic = form.save(commit=False)
#             topic.board = board
#             topic.created_by = request.user
#             topic.save()

#             # Handle the uploaded picture
#             pic = request.FILES.get('pic')
#             if pic:
#                 topic.pic = pic
#                 topic.save()

#             post = Post.objects.create(
#                 message=form.cleaned_data.get('message'),
#                 created_by=request.user,
#                 topic=topic
#             )

#             return redirect('board_topics', board_id=board.pk)
#     else:
#         form = NewTopicForm()

    return render(request, 'new_topic.html', {'board': board, 'form': form})


@login_required
def topic_posts(request, board_id, topic_id):
    topic = get_object_or_404(Topic, board__pk=board_id, pk=topic_id)
    board = topic.board
    subs = Subscription.objects.filter(user=request.user)
    
    for sub in subs:
        if sub.end_date < timezone.now().date():
            sub.expired = True
            sub.save()
        else:
            sub.expired = False
            sub.save()

    subscription = Subscription.objects.filter(user=request.user, topic=topic, is_approved=True, expired=False).first()
    if  not subscription:
        return redirect('subscribe', topic_id=topic_id)

    if request.method == "POST" and 'like_post_id' in request.POST:
        post_id = int(request.POST.get('like_post_id'))
        post = get_object_or_404(Post, pk=post_id)

        if request.user in post.likes.all():
            # User has already liked the post, remove the like
            post.likes.remove(request.user)
        else:
            # User has not liked the post, add the like
            post.likes.add(request.user)

    return render(request, 'topic_posts.html', {'topic': topic, 'board':board})
    # return render(request,'topic_posts.html',{'topic':topic,'form':form})






@login_required
def subscribe(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    subscribes = Subscription.objects.filter(user=request.user ,topic=topic_id, is_approved=False, expired= False).first()
    if subscribes:
        # return HttpResponse("wait for approval of payment")
        text_us = "تواصل معنا لاتمام عملية الدفع"
        return render(request, 'Sub.html', {'topic': topic, 'subscribes': subscribes ,'text_us': text_us})
    
    elif request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.user = request.user
            subscription.topic = topic
            subscription.save()
            return redirect('subscribe',topic_id)
    else:
        form = SubscriptionForm()

    return render(request, 'Sub.html', {'form': form, 'topic': topic, 'subscribes': subscribes})


@login_required
def add_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            Comment.objects.create(content=content, post=post, created_by=request.user)
            return redirect('topic_posts', board_id=post.topic.board.pk, topic_id=post.topic.pk)
    else:
        form = CommentForm()
    
    return render(request, 'add_comment.html', {'form': form})














def submit_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.user = request.user
            assignment.save()
            # HttpResponse()
            return redirect('index') 
    else:
        form = AssignmentForm()
    
    return render(request, 'base.html', {'form': form})

def solved_assignments(request):
    assign = Assignment.objects.filter(user=request.user)

    return render( request ,"solved_assignment.html",{'assign': assign} )




    # one_month_after = (request.user.date_joined + timedelta(days=30)).date()
    # user_date_joined = request.user.date_joined.date()
    # today = timezone.now().date()
    # print(one_month_after,user_date_joined)
    # if one_month_after > today :
    #     topic = get_object_or_404(Topic, board__pk=board_id, pk=topic_id)

    #     if request.method == "POST" and 'like_post_id' in request.POST:
    #         post_id = int(request.POST.get('like_post_id'))
    #         post = get_object_or_404(Post, pk=post_id)

    #         if request.user in post.likes.all():
    #             # User has already liked the post, remove the like
    #             post.likes.remove(request.user)
    #         else:
    #             # User has not liked the post, add the like
    #             post.likes.add(request.user)

    #     return render(request, 'topic_posts.html', {'topic': topic})
    # else:
    #     return redirect('login')

    # # return render(request,'topic_posts.html',{'topic':topic,'form':form})
