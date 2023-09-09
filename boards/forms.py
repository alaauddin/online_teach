from django import forms
from .models import Topic, Post, Subscription, Assignment


# class NewTopicForm(forms.ModelForm):
#     message = forms.CharField(
#         widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'What is on your mind'}),
#         max_length=4000,
#         help_text='The max length of the text is 4000'
#     )

#     class Meta:
#         model = Topic
#         fields = ['subject', 'message']


# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ['message']

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = []


class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), max_length=1000)  

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['file', 'end_date']