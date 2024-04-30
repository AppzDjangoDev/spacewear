from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from fyersapi.views import Brokerconfig
from .views import ConfigureTradingView



urlpatterns = [
    path('broker_config', views.Brokerconfig.as_view(), name='broker_config'),
    path('brokerconnect', views.brokerconnect, name='brokerconnect'),
    path('get_accese_token_store_session', views.get_accese_token_store_session, name='get_accese_token_store_session'),
    path('get_user_profile', views.ProfileView.as_view(), name='get_user_profile'),

    path('close_all_positions', views.close_all_positions, name='close_all_positions'),
    path('update-data-instance/', views.update_data_instance, name='update_data_instance'),

    # order history
    path('order-history', views.OrderHistory.as_view(), name='order_history'),
    path('update-latest-data', views.update_latest_data, name='update_latest_data'),
    # path('get-options-data', views.get_options_data, name='get_options_data'),
    # path('options-chain-view', views.OptionChainView.as_view(), name='options_chain_view'),
    path('options-chain-view/<str:slug>/', views.OptionChainView.as_view(), name='options_chain_view'),
    path('configure-trading/', ConfigureTradingView.as_view(), name='configure_trading'),
    path('instant-buy-order/', views.instantBuyOrderWithSL, name='instant_buy_order'),





    path('explore-more/', views.fyer_websocket_view, name='explore_more'),




    
    

    
    # path('logout', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

   


      

]
