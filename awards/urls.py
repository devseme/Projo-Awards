from django.urls import path
from . import views

urlpatterns=[
    # url('^$',views.welcome,name = 'welcome'),
    path('',views.index,name= 'index'),
    path('profile/', views.profile, name='profile'),
    path('upload/project/', views.upload, name = "upload"),
    path('update_profile/<int:id>',views.update_profile, name='update_profile'),
    # path('project/',views.project, name='project'),
]