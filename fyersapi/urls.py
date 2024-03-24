from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from fyersapi.views import Brokerconfig


urlpatterns = [
    path('broker_config', views.Brokerconfig.as_view(), name='broker_config'),
    path('brokerconnect', views.brokerconnect, name='brokerconnect'),
    path('get_accese_token', views.get_accese_token, name='get_accese_token'),



    
    

    
    # path('logout', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

   


      

]