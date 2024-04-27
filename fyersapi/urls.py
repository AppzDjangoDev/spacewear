from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from fyersapi.views import Brokerconfig


urlpatterns = [
    path('broker_config', views.Brokerconfig.as_view(), name='broker_config'),
    path('brokerconnect', views.brokerconnect, name='brokerconnect'),
    path('get_accese_token', views.get_accese_token, name='get_accese_token'),
    path('get_user_profile', views.ProfileView.as_view(), name='get_user_profile'),

    path('close_all_positions', views.close_all_positions, name='close_all_positions'),
    path('update-data-instance/', views.update_data_instance, name='update_data_instance'),

    # order history
    path('order-history', views.OrderHistory.as_view(), name='order_history'),
    path('update-latest-data', views.update_latest_data, name='update_latest_data'),
    path('get-options-data', views.get_options_data, name='get_options_data'),



    


    



    
    

    
    # path('logout', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

   


      

]