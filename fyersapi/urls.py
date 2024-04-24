from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from fyersapi.views import Brokerconfig


urlpatterns = [
    path('broker_config', views.Brokerconfig.as_view(), name='broker_config'),
    path('brokerconnect', views.brokerconnect, name='brokerconnect'),
    path('get_accese_token', views.get_accese_token, name='get_accese_token'),
    path('get_user_profile', views.get_user_profile, name='get_user_profile'),

    path('exit_pending_orders', views.exit_pending_orders, name='exit_pending_orders'),
    path('update-data-instance/', views.update_data_instance, name='update_data_instance'),


    



    
    

    
    # path('logout', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

   


      

]