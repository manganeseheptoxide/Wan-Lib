from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name="landing-page"),
    path('login', views.login_page, name="login"),
    path('logout', views.logout_user, name="logout"),
    path('register', views.register_user, name="register"),
    path('home', views.home, name="home"),
    path('room/', views.home, name="home2"),
    path('room/<str:pk>', views.room, name="room"),
    path('create-room/', views.create_room, name="create-room"),
    path('profile/<str:pk>/', views.profile_page,name='profile'),
    path('update-room/<str:pk>', views.update_room, name="update-room"),
    path('delete-room/<str:pk>', views.delete_room, name="delete-room"),
    path('delete-message/<str:pk>', views.delete_message, name="delete-message"),
    path('update-user/', views.update_user, name="update-user"),
    path('topics/', views.topics, name="topics"),
    path('activity/', views.activity, name="activity"),
    path('knowledge/', views.knowledge, name="knowledge"),
    path('knowledge-fire/', views.knowledge_fire, name="knowledge-fire"),
    path('knowledge-air/', views.knowledge_air, name="knowledge-air"),
    path('knowledge-water/', views.knowledge_water, name="knowledge-water"),
    path('knowledge-earth/', views.knowledge_earth, name="knowledge-earth"),
    # path('knowledge-rooms/', views.knowledge_rooms, name="knowledge-rooms"),
    path('discussion/', views.discussion, name="discussion")
]
