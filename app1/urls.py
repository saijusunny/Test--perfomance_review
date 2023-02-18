from django import views
from django.contrib import admin
from django.urls import path
from.import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login, name='login'),
   
    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('signup/', views.signup, name='signup'),
    path('usercreate/', views.usercreate, name='usercreate'),
    path('home/', views.home, name='home'),
   
    path('logout/', views.logout, name='logout'),
    path('editpro/<int:pk>,', views.editpro, name='editpro'),
    path('trans/', views.trans, name='trans'),
    path('add_performance/<int:id>', views.add_performance, name='add_performance'),
    path('req_mny/<int:id>', views.req_mny, name='req_mny'),
    path('view_user/<int:id>', views.view_user, name='view_user'),
    path('up_pro/<int:id>', views.up_pro, name='up_pro'), 
    path('get_det_per/', views.get_det_per, name='get_det_per'), 
    path('edit_performance/<int:id>', views.edit_performance, name='edit_performance'), 
    path('home2/', views.home2, name='home2'),
    path('user_per/', views.user_per, name='user_per'), 
    path('send_feed/', views.send_feed, name='send_feed'), 
    path('sav_assign/<int:id>', views.sav_assign, name='sav_assign'), 
    path('add_feed/', views.add_feed, name='add_feed'),
   
 
 
    
    
]