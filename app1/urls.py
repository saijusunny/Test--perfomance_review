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
    path('user_management/', views.user_management, name='user_management'),
    path('logout/', views.logout, name='logout'),
    path('editpro/<int:pk>,', views.editpro, name='editpro'),
    path('trans/', views.trans, name='trans'),
    path('send_mny/<int:id>', views.send_mny, name='send_mny'),
    path('req_mny/<int:id>', views.req_mny, name='req_mny'),
    path('view_user/<int:id>', views.view_user, name='view_user'),

    
    
]