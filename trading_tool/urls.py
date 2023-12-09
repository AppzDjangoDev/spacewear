from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from account.views import UserRegistrationView


urlpatterns = [
    # landing page
    # path('', views.homePage, name = 'home'),
    # # login 
    # path('login', views.UserloginView.as_view(), name = 'login'),
    # path('logout', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    # # path('logout', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

   


      

]