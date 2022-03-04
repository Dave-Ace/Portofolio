from django.urls import path, include
from django.conf.urls import url
from . import views

app_name = "Profile"
urlpatterns = [ 
    path('', views.index, name="home"),
    path('contact_david/', views.contact, name="contact"),
    #path('google/auth/', views.room, name='auth'),
    path('chat/<str:room_name>/', views.room, name='chat'),
    path('blog/<slug>/', views.DetailView.as_view(), name="blog_single" ),
    path('blog/', views.ListView.as_view(), name="blog" ),
    path('logout/', views.logoutUser, name="logout"),
    path('accounts/login/', views.loginPage, name="login"),
    path('blog/author/profile/<pk>', views.Profile.as_view(), name="author_profile"),
    path('blog/comment/<slug>', views.comment, name="comment"),
]