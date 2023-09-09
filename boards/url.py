from django.urls import path
from . import views
from boards import views




urlpatterns = [

    path("",views.home,name ='index'),
    path('boards/<int:board_id>/',views.board_topics,name = 'board_topics'),
    path('boards/<int:board_id>/topics/<int:topic_id>', views.topic_posts , name ='topic_posts' ),
    path('topics/<int:topic_id>/subscribe', views.subscribe, name='subscribe'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('submit_assignment/', views.submit_assignment, name='submit_assignment'),
    path('my_sloved_assignments/',views.solved_assignments, name="solved_assignment"),
    
]
