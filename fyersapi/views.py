from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf import settings
from fyers_apiv3 import fyersModel
import webbrowser
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from .models import TradingData
import datetime
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from .models import TradingData
from django.utils import timezone
from django.db.models import Q
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import TradingConfigurationsForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

class Brokerconfig(LoginRequiredMixin, View):
    login_url = '/login'
    def get(self, request, *args, **kwargs):
        template = "trading_tool/html/index.html"
        context = {}
        return render(request, template, context)
    
def brokerconnect(request):
    # Get client_id and secret_key from settings.py
    client_id = settings.FYERS_APP_ID
    secret_key = settings.FYERS_SECRET_ID
    redirect_uri = settings.FYERS_REDIRECT_URL+"/dashboard"
    # Replace these values with your actual API credentials
    # redirect_uri = "https://spacewear.co.in/dashboard"
    # redirect_uri = "https://aabe-2405-201-f007-417b-7d9c-6736-527b-61a6.ngrok-free.app/dashboard"
    response_type = "code"  
    state = "sample_state"
    # Create a session model with the provided credentials
    session = fyersModel.SessionModel(
        client_id=client_id,
        secret_key=secret_key,
        redirect_uri=redirect_uri,
        response_type=response_type
    )
    # Generate the auth code using the session model
    response = session.generate_authcode()
    # Print the auth code received in the response
    # You can redirect to another page or render a template after printing
    return redirect(response)  # Assuming 'home' is the name of a URL pattern you want to redirect to



def get_accese_token(request):
    # return redirect('some_redirect_url')
    # Get client_id and secret_key from settings.py
    client_id = settings.FYERS_APP_ID
    secret_key = settings.FYERS_SECRET_ID
    redirect_uri = settings.FYERS_REDIRECT_URL+"/dashboard"
    # redirect_uri = "https://spacewear.co.in/dashboard"
    # redirect_uri = "https://aabe-2405-201-f007-417b-7d9c-6736-527b-61a6.ngrok-free.app/dashboard"
    response_type = "code" 
    grant_type = "authorization_code"  
    # The authorization code received from Fyers after the user grants access
    # auth_code = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkubG9naW4uZnllcnMuaW4iLCJpYXQiOjE3MTEyNzg2NDgsImV4cCI6MTcxMTMwODY0OCwibmJmIjoxNzExMjc4MDQ4LCJhdWQiOiJbXCJ4OjBcIiwgXCJ4OjFcIiwgXCJ4OjJcIiwgXCJkOjFcIiwgXCJkOjJcIiwgXCJ4OjFcIiwgXCJ4OjBcIl0iLCJzdWIiOiJhdXRoX2NvZGUiLCJkaXNwbGF5X25hbWUiOiJZUzA1MTQxIiwib21zIjoiSzEiLCJoc21fa2V5IjoiNGQ0OWQzMzA2MmM4YzMyOTA4OGEyMzZkMWVkZDI0MDhhODYyY2QyZDdlMmI2M2Y4NjI3N2JkZGUiLCJub25jZSI6IiIsImFwcF9pZCI6Ikg5TzQwNlhCWFciLCJ1dWlkIjoiNTdhYzQ2MmM0YzkxNGI0MzlmMGY3OTc3MGRmMDM0YTEiLCJpcEFkZHIiOiIwLjAuMC4wIiwic2NvcGUiOiIifQ.RhnYqWn9hqR5X_yg5wHKcOGCkGFnAb4Ms2xbToDMPAw"
    auth_code = request.session.get(' ')
    # Create a session object to handle the Fyers API authentication and token generation
    session = fyersModel.SessionModel(
        client_id=client_id,
        secret_key=secret_key, 
        redirect_uri=redirect_uri, 
        response_type=response_type, 
        grant_type=grant_type
    )
    print("sessionsession", session)
    # Set the authorization code in the session object
    session.set_token(auth_code)
    # Generate the access token using the authorization code
    response = session.generate_token()
    print("responseresponse", response)
    # Print the response, which should contain the access token and other details
    access_token = response.get('access_token')
    refresh_token = response.get('refresh_token')
    if access_token:
        return access_token

    else:
        return None
        

def get_accese_token_store_session(request):
    # return redirect('some_redirect_url')
    # Get client_id and secret_key from settings.py
    client_id = settings.FYERS_APP_ID
    secret_key = settings.FYERS_SECRET_ID
    redirect_uri = settings.FYERS_REDIRECT_URL+"/dashboard"
    # redirect_uri = "https://spacewear.co.in/dashboard"
    # redirect_uri = "https://aabe-2405-201-f007-417b-7d9c-6736-527b-61a6.ngrok-free.app/dashboard"
    response_type = "code" 
    grant_type = "authorization_code"  
    # The authorization code received from Fyers after the user grants access
    # auth_code = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkubG9naW4uZnllcnMuaW4iLCJpYXQiOjE3MTEyNzg2NDgsImV4cCI6MTcxMTMwODY0OCwibmJmIjoxNzExMjc4MDQ4LCJhdWQiOiJbXCJ4OjBcIiwgXCJ4OjFcIiwgXCJ4OjJcIiwgXCJkOjFcIiwgXCJkOjJcIiwgXCJ4OjFcIiwgXCJ4OjBcIl0iLCJzdWIiOiJhdXRoX2NvZGUiLCJkaXNwbGF5X25hbWUiOiJZUzA1MTQxIiwib21zIjoiSzEiLCJoc21fa2V5IjoiNGQ0OWQzMzA2MmM4YzMyOTA4OGEyMzZkMWVkZDI0MDhhODYyY2QyZDdlMmI2M2Y4NjI3N2JkZGUiLCJub25jZSI6IiIsImFwcF9pZCI6Ikg5TzQwNlhCWFciLCJ1dWlkIjoiNTdhYzQ2MmM0YzkxNGI0MzlmMGY3OTc3MGRmMDM0YTEiLCJpcEFkZHIiOiIwLjAuMC4wIiwic2NvcGUiOiIifQ.RhnYqWn9hqR5X_yg5wHKcOGCkGFnAb4Ms2xbToDMPAw"
    auth_code = request.session.get('auth_code')
    # Create a session object to handle the Fyers API authentication and token generation
    session = fyersModel.SessionModel(
        client_id=client_id,
        secret_key=secret_key, 
        redirect_uri=redirect_uri, 
        response_type=response_type, 
        grant_type=grant_type
    )
    # Set the authorization code in the session object
    session.set_token(auth_code)
    # Generate the access token using the authorization code
    response = session.generate_token()
    # Print the response, which should contain the access token and other details
    access_token = response.get('access_token')
    refresh_token = response.get('refresh_token')
    if access_token and refresh_token:
        request.session['access_token'] = access_token
        request.session['refresh_token'] = refresh_token
    else:
        print("access_token or refresh_token missing")
        pass
    # You can redirect to another page or render a template after printing
    return redirect('dashboard')  # Assuming 'home' is the name of a URL pattern you want to redirect to



def close_all_positions(request):
    client_id = settings.FYERS_APP_ID
    access_token = request.session.get('access_token')
    if access_token:
        # Initialize the FyersModel instance with your client_id, access_token, and enable async mode
        fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="")
        order_data = fyers.orderbook()
        # Initialize an empty list to store order IDs with status 6
        orders_with_status_6 = []
        # Iterate through the orderBook
        for order in order_data["orderBook"]:
            # Check if the status is 6
            if order["status"] == 6:
                # Append the ID to the list
                orders_with_status_6.append({"id": order.get("id")})
        order_cancel_response = []
        # Check if there are orders to cancel
        if orders_with_status_6:
            # Cancel the orders
            order_cancel_response = fyers.cancel_basket_orders(data=orders_with_status_6)
            print("Order cancel response:", order_cancel_response)
            messages.success(request,order_cancel_response)
        else:
            print("No pending orders to cancel.")
            messages.success(request,"No pending orders to cancel.")
        # Code indicates successful cancellation or order not found
        data = {
            "segment": [11],
            "side": [1],
            "productType": ["INTRADAY"]
        }
        response = fyers.exit_positions(data=data)
        # Check if 'data' key exists in the response
        print("responseresponse", response)
        if 'message' in response:
            message = response['message']
            messages.success(request, message)
            return JsonResponse({'message': message})
        else:
            # Handle the case where 'data' key is missing
            message = "Error: Response format is unexpected"
            messages.error(request, "Error: Response format is unexpected")
            return JsonResponse({'message': message})
    return redirect('dashboard')  

def get_data_instance(request):
    context={}
    template="trading_tool/html/profile_view.html"
    client_id = settings.FYERS_APP_ID
    access_token = request.session.get('access_token')
    if access_token:
        # Initialize the FyersModel instance with your client_id, access_token, and enable async mode
        fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")
        # Return the response received from the Fyers API
        return fyers
    else:
        print("noithing here")
        # Handle the case where access_token is not found in the session
    return None


from django.http import JsonResponse
def update_data_instance(request):
    context = {}
    client_id = settings.FYERS_APP_ID
    access_token = request.session.get('access_token')
    total_order_status=0

    if access_token:
        data_instance = get_data_instance(request)
        # fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")
        positions_data = data_instance.positions()
        order_data = data_instance.orderbook()
        fund_data = data_instance.funds()
        if "orderBook" in order_data:
            total_order_status = sum(1 for order in order_data["orderBook"] if order["status"] == 2)
        # Process the response and prepare the data
        data = { 'positions': positions_data,
                'total_order_status': total_order_status ,
                'fund_data': fund_data,
                'order_data': order_data
                }  # Modify this according to your response structure
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Access token not found'}, status=400)

class ProfileView(LoginRequiredMixin, View):
  login_url = '/login'
  def get(self, request):
    client_id = settings.FYERS_APP_ID
    access_token = request.session.get('access_token')

    if access_token:
      fyers = fyersModel.FyersModel(
        client_id=client_id, 
        is_async=False, 
        token=access_token,
        log_path=""
      )
      response = fyers.get_profile()
      context = response
      return render(request, 'trading_tool/html/profile_view.html', context)
    
    else:
      print("no access token")
      return render(request, 'trading_tool/html/profile_view.html')
    

    

class OrderHistory(LoginRequiredMixin, View):
    login_url = '/login'  # Replace '/login/' with your actual login URL

    def get(self, request):
        context = {}
        order_data = TradingData.objects.filter(category='ORDERS')
        paginator = Paginator(order_data, 20)  # Show 20 items per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['order_history_data'] = page_obj
        return render(request, 'trading_tool/html/order_history.html', context)
    

class OptionChainView(LoginRequiredMixin,View):
    login_url = '/login'
    def get(self, request, slug):  # Modify to accept 'slug' parameter
        context = {}
        template = 'trading_tool/html/optionchainview.html'
        data_instance = get_data_instance(request)
        confData = TradingConfigurations.objects.first()
        forward_trailing_points = confData.forward_trailing_points
        reverse_trailing_points = confData.reverse_trailing_points
        data = {
            "symbol":"NSE:"+slug+"-INDEX" ,  # Update 'symbol' to use 'slug' parameter
            "strikecount": 1,
            # "timestamp": next_thursday_timestamp
        }
        try:
            expiry_response = data_instance.optionchain(data=data)
        except AttributeError as e:
            expiry_response = {'code': -1, 'message': f'Error occurred: {str(e)}', 's': 'error'}
            print("Error occurred while fetching fund data:", e)
            return render(request, template, context)


            
        first_expiry_ts = expiry_response['data']['expiryData'][0]['expiry']
        first_expiry_date = expiry_response['data']['expiryData'][0]['date']
        options_data = {
            "symbol":"NSE:"+slug+"-INDEX" ,  # Update 'symbol' to use 'slug' parameter
            "strikecount": 1,
            "timestamp": first_expiry_ts
        }
        print("options_dataoptions_dataoptions_dataoptions_dataoptions_data", options_data)
        print("data_instance", )
        response = data_instance.optionchain(data=options_data)
        context['forward_trailing_points'] = forward_trailing_points
        context['reverse_trailing_points'] = reverse_trailing_points
        context['expiry_response'] = first_expiry_date
        context['options_data'] = response
        return render(request, template, context)

def update_latest_data(request):
    # Call API to get data
    print("entry__1")
    data_instance = get_data_instance(request)

    # Save positions data
    positions = data_instance.positions()
    TradingData.objects.update_or_create(
        category='POSITIONS',last_updated =  timezone.now(),
        defaults={'data': positions, 'last_updated': timezone.now()},
        # other fields
    )

    # Save orders data
    orders = data_instance.orderbook()
    TradingData.objects.update_or_create(
        category='ORDERS',last_updated =  timezone.now(),
        defaults={'data': orders, 'last_updated': timezone.now()},
        # other fields
    )

    # Save funds data
    funds = data_instance.funds()
    TradingData.objects.update_or_create(
        category='FUNDS',last_updated =  timezone.now(),
        defaults={'data': funds, 'last_updated': timezone.now()},
        # other fields
    )
    return HttpResponse('Data saved')

class ConfigureTradingView(LoginRequiredMixin,FormView):
    login_url = '/login'
    template_name = 'trading_tool/html/configure_trading.html'
    form_class = TradingConfigurationsForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
   
from .models import TradingConfigurations
from django.contrib.auth.mixins import LoginRequiredMixin
class ConfigureTradingView(LoginRequiredMixin,FormView):
    login_url = '/login'
    
    template_name = 'trading_tool/html/configure_trading.html'
    form_class = TradingConfigurationsForm
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Fetch the existing TradingConfigurations object
        trading_config = TradingConfigurations.objects.first()  
        # Adjust as per your logic to fetch the existing object
        kwargs['instance'] = trading_config
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    

def get_deafult_lotsize(index):
    if index == 'MIDCPNIFTY':
        return 75
    elif index == 'FINNIFTY':
        return 40
    elif index == 'BANKNIFTY':
        return 15
    elif index == 'NIFTY':
        return 25
    else:
        return False


def instantBuyOrderWithSL(request):
    if request.method == 'POST':
        data_instance = get_data_instance(request)
        der_symbol = request.POST.get('der_symbol')
        ex_symbol = request.POST.get('ex_symbol')
        get_lot_count = get_deafult_lotsize(ex_symbol)
        
        # Retrieve default order quantity from trade configurations
        trade_config_data = TradingConfigurations.objects.first()
        order_qty = trade_config_data.default_order_qty * get_lot_count

        # Prepare order data for market buy order
        data = {
            "symbol": der_symbol,
            "qty": order_qty,
            "type": 2,  # Market Order
            "side": 1,  # Buy
            "productType": "INTRADAY",
            "validity": "DAY",
            "offlineOrder": False
        }

        # Place market buy order
        response = data_instance.place_order(data=data)
        print("BUY ORDER RESPONSE :", response["code"])

        if response["code"] == 1101:
            # Check if there's an existing pending order with status 6 for the same symbol
            allOrderData = data_instance.orderbook()
            order_with_status_6 = next((order for order in allOrderData["orderBook"] if order['status'] == 6 and order["symbol"] == der_symbol), None)

            if order_with_status_6:
                # Modify the existing order by adding the new quantity to it
                exst_qty = order_with_status_6['qty']
                orderId = order_with_status_6['id']
                new_qty = order_qty + exst_qty
                modify_data = {"id": orderId, "type": 4, "qty": new_qty}
                modify_response = data_instance.modify_order(data=modify_data)
                return JsonResponse({'response': modify_response["message"]})
            else:
                # Place stop-loss order
                buy_order_id = response["id"]
                buy_order_data = {"id": buy_order_id}
                get_buy_orderdata = data_instance.orderbook(data=buy_order_data)
                order_details = get_buy_orderdata["orderBook"][0]
                traded_price = order_details["tradedPrice"]
                
                # Calculate stop-loss and limit price
                default_stoploss = trade_config_data.default_stoploss
                stoploss_limit_slippage = trade_config_data.stoploss_limit_slippage
                stoploss_price = traded_price - (traded_price * default_stoploss / 100)
                stoploss_price = round(stoploss_price / 0.05) * 0.05
                stoploss_price = round(stoploss_price, 2)
                stoploss_limit = stoploss_price - float(stoploss_limit_slippage)
                stoploss_limit = round(stoploss_limit / 0.05) * 0.05
                stoploss_limit = round(stoploss_limit, 2)

                sl_data = {
                    "symbol": der_symbol,
                    "qty": order_qty,
                    "type": 4,  # SL-L Order
                    "side": -1,  # Sell
                    "productType": "INTRADAY",
                    "limitPrice": stoploss_limit,
                    "stopPrice": stoploss_price,
                    "validity": "DAY",
                    "offlineOrder": False,
                }

                stoploss_order_response = data_instance.place_order(data=sl_data)
                if stoploss_order_response["code"] == 1101:
                    message = "BUY/SL-L Placed Successfully"
                    return JsonResponse({'response': message})
                elif response["code"] == -99:
                    message = "SL-L not Placed, Insufficient Fund"
                    return JsonResponse({'response': message})
                else:
                    return JsonResponse({'response': stoploss_order_response["message"]})
        elif response["code"] == -99:
            message = "Insufficient Fund"
            return JsonResponse({'response': message})
        else:
            return JsonResponse({'response': response["message"]})
    else:
        message = "Some Error Occurred Before Execution"
        return JsonResponse({'response': message})

# def instantBuyOrderWithSL(request):
#     if request.method == 'POST':
#         # Retrieve values from POST data
#         data_instance = get_data_instance(request)
#         der_symbol = request.POST.get('der_symbol')
#         ex_symbol = request.POST.get('ex_symbol')
#         get_lot_count = get_deafult_lotsize(ex_symbol)
#         # get config data from table 
#         trade_config_data = TradingConfigurations.objects.first()
#         order_qty = trade_config_data.default_order_qty*get_lot_count
#         # Preparing Order Data 
#         data = {
#             "symbol":der_symbol,
#             "qty": order_qty ,
#             "type":2, # Market Order
#             "side":1, # Buy
#             "productType":"INTRADAY",
#             "validity":"DAY",
#             "offlineOrder":False
#         }
#         # order Placement
#         response = data_instance.place_order(data=data)
#         print("BUY ORDER RESPONSE :", response["code"])
#         # check response status success
#         if response["code"] == 1101:
#             allOrderData = data_instance.orderbook()
#             # Find the order with status 6, if any which is PENDING
#             order_with_status_6 = next((order for order in allOrderData["orderBook"] if order['status'] == 6 and order["symbol"] == der_symbol), None)
#             print("CHECK PENDING ORDERS:", order_with_status_6)
#             if order_with_status_6:
#                 print("orders_with_status_6orders_with_status_6", order_with_status_6["id"])
#                 exst_qty = order_with_status_6['qty']
#                 orderId = order_with_status_6['id']
#                 new_qty = order_qty + exst_qty
#                 # modify existing sl order 
#                 modify_data = {
#                     "id":orderId, 
#                     "type":4, 
#                     "qty": new_qty
#                 }
#                 print("*******************************************")
#                 print("OrderID :", orderId)
#                 print("Symbol :", der_symbol)
#                 print("Existing Qty:", exst_qty)
#                 print("New Qty :", new_qty)
#                 print("*******************************************")
#                 modify_response = data_instance.modify_order(data=modify_data)
#                 return JsonResponse({'response': modify_response["message"]})
#             else:
#                 # Here We need to Place Stoploss Order with default Stoploss price 
#                 buy_order_id = response["id"]
#                 print("BUY ORDER ID:", buy_order_id)
#                 buy_order_data = {"id":buy_order_id}
#                 get_buy_orderdata = data_instance.orderbook(data=buy_order_data)
#                 # get_buy_orderdata = {
#                 #     "code": 200,
#                 #     "message": "",
#                 #     "s": "ok",
#                 #     "orderBook": [{
#                 #         "clientId": "XXXXX86",
#                 #         "exchange": 10,
#                 #         "fyToken": "101000000014366",
#                 #         "id": "23080444447604",
#                 #         "offlineOrder": False,
#                 #         "source": "W",
#                 #         "status": 2,
#                 #         "type": 2,
#                 #         "pan": "",
#                 #         "limitPrice": 8.1,
#                 #         "productType": "INTRADAY",
#                 #         "qty": 1,
#                 #         "disclosedQty": 0,
#                 #         "remainingQuantity": 0,
#                 #         "segment": 10,
#                 #         "symbol": "NSE:IDEA-EQ",
#                 #         "description": "VODAFONE IDEA LIMITED",
#                 #         "ex_sym": "IDEA",
#                 #         "orderDateTime": "02-Aug-2023 13:01:42",
#                 #         "side": 1,
#                 #         "orderValidity": "DAY",
#                 #         "stopPrice": 0,
#                 #         "tradedPrice": 117.0,
#                 #         "filledQty": 1,
#                 #         "exchOrdId": "1100000024706527",
#                 #         "message": "",
#                 #         "ch": -0.35,
#                 #         "chp": -4.24,
#                 #         "lp": 7.9,
#                 #         "orderNumStatus": "23080444447604:2",
#                 #         "slNo": 1,
#                 #         "orderTag": "1:Ordertag"
#                 #     }]
#                 # }
#                 order_details = get_buy_orderdata["orderBook"][0]
#                 traded_price = order_details["tradedPrice"]
#                 traded_price=10
#                 #************CALCULATING SL AND SL_TRIGGER****************
#                 default_stoploss = trade_config_data.default_stoploss
#                 stoploss_limit_slippage = trade_config_data.stoploss_limit_slippage
#                 stoploss_price = traded_price-(traded_price*default_stoploss/100)
#                 stoploss_price = round(stoploss_price / 0.05) * 0.05
#                 stoploss_price = round(stoploss_price, 2)
#                 stoploss_limit = stoploss_price-float(stoploss_limit_slippage)
#                 stoploss_limit = round(stoploss_limit / 0.05) * 0.05
#                 stoploss_limit = round(stoploss_limit, 2)
#                 print("*******************************************")
#                 print("BUY_SYMBOL:", der_symbol)
#                 print("TRADED_PRICE_BUY", traded_price)
#                 print("DEFAULT SL:", default_stoploss)
#                 print("STOPLOSS:",stoploss_price)
#                 print("STOPLOSS-LIMIT:",stoploss_limit)
#                 print("ORDER-QUANTITY:",order_qty)
#                 print("*******************************************")
#                 sl_data = {
#                     "symbol":der_symbol,
#                     "qty":order_qty,
#                     "type":4, # SL-L Order
#                     "side":-1, # SELL
#                     "productType":"INTRADAY",
#                     "limitPrice":stoploss_limit,
#                     "stopPrice":stoploss_price,
#                     "validity":"DAY",
#                     "offlineOrder":False,
#                 }
#                 stoploss_order_response = data_instance.place_order(data=sl_data)
#                 print("SL ORDER RESPONSE :", stoploss_order_response)
#                 if stoploss_order_response["code"] == 1101:
#                     message="BUY/SL-L Placed Successfully"
#                     return JsonResponse({'response': message})
#                 elif response["code"] == -99:
#                     print("The code is -99", response)
#                     message="SL-L not Placed, Insufficient Fund"
#                     return JsonResponse({'response': message})
#                 else:
#                     print("The code is not 1101", response)
#                     return JsonResponse({'response': response["message"]})
                
#         elif response["code"] == -99:
#             print("The code is -99", response)
#             message="Insufficient Fund"
#             return JsonResponse({'response': message})
        
#         else:
#             # need ato add alert for buy order not worked 
#             print("The code is not 1101", response)
#             return JsonResponse({'response': response["message"]})

#     else:
#         # Handle GET request
#         message="Some Error Occured Before Execute"
#         return JsonResponse({'response': message})
        
# def trailingtotop(request):
#     client_id = settings.FYERS_APP_ID
#     access_token = request.session.get('access_token')
#     trade_config_data = TradingConfigurations.objects.first()
#     forwrd_trail_limit = trade_config_data.forward_trailing_points
#     if access_token:
#         # Initialize the FyersModel instance with your client_id, access_token, and enable async mode
#         fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="")
#         order_data = fyers.orderbook()
#         # Initialize an empty list to store order IDs with status 6
#         orders_with_status_6 = []
#         # Iterate through the orderBook
#         for order in order_data["orderBook"]:
#             # Check if the status is 6
#             if order["status"] == 5:
#                 # Append the ID to the list
#                 orders_with_status_6.append(order["id"])
#                 existing_stop_price = order["stopPrice"]
#                 existing_limit_price = order["limitPrice"]
#         new_stop_price = existing_stop_price + forwrd_trail_limit
#         new_limit_price = existing_limit_price + forwrd_trail_limit
#         # Check if there are orders to cancel
#         if orders_with_status_6:
#             # Cancel the orders
#             orderId =orders_with_status_6[0]
#             data = {
#                 "id":orderId, 
#                 "limitPrice": new_limit_price, 
#                 "stopPrice": new_stop_price,
#             }
#             trailing_order_update = fyers.modify_order(data=data)
#             # trailing_order_update = fyers.cancel_basket_orders(data=orders_with_status_6)
#         # Code indicates successful cancellation or order not found
#         if 'message' in trailing_order_update:
#             message = trailing_order_update['message']
#             messages.success(request, message)
#             return JsonResponse({'message': message})
#         else:
#             # Handle the case where 'data' key is missing
#             message = "Error: Response format is unexpected"
#             messages.error(request, "Error: Response format is unexpected")
#             return JsonResponse({'message': message})
#     return redirect('dashboard')  

def trailingtotop(request):
    client_id = settings.FYERS_APP_ID
    access_token = request.session.get('access_token')
    
    if access_token:
        # Initialize the FyersModel instance with your client_id, access_token, and enable async mode
        fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="")
        order_data = fyers.orderbook()
        print("pppppppppppppppp", order_data)
        
        # Initialize variables to store stop and limit prices
        existing_stop_price = None
        existing_limit_price = None
        
        # Iterate through the orderBook
        for order in order_data.get("orderBook", []):
            print("pppppppppppppppp", order)
            # Check if the status is 6
            if order.get("status") == 6:
                # Get the stop and limit prices
                existing_stop_price = order.get("stopPrice", existing_stop_price)
                existing_limit_price = order.get("limitPrice", existing_limit_price)
                symbol = order["symbol"]
        if existing_stop_price is not None and existing_limit_price is not None:
            trade_config_data = TradingConfigurations.objects.first()
            forwrd_trail_limit = trade_config_data.forward_trailing_points

            # Calculate new stop and limit prices
            new_stop_price = existing_stop_price + forwrd_trail_limit
            new_limit_price = existing_limit_price + forwrd_trail_limit
            
            # Check if there are orders to cancel
            if existing_stop_price is not None:
                # Modify the order with new stop and limit prices
                data = {"id": order["id"], "limitPrice": new_limit_price, "stopPrice": new_stop_price}
                trailing_order_update = fyers.modify_order(data=data)
                
                # Check the response
                if 'message' in trailing_order_update:
                    message = trailing_order_update['message']
                    messages.success(request, message)
                    return JsonResponse({'message': message})
        
        # Handle the case where 'data' key is missing
        message = "No SL/Pending Orders"
        messages.error(request, message)
        return JsonResponse({'message': message})
    
    return redirect('dashboard')


def trailingtodown(request):
    client_id = settings.FYERS_APP_ID
    access_token = request.session.get('access_token')
    
    if access_token:
        # Initialize the FyersModel instance with your client_id, access_token, and enable async mode
        fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="")
        order_data = fyers.orderbook()
        
        
        # Initialize variables to store stop and limit prices
        existing_stop_price = None
        existing_limit_price = None
        
        # Iterate through the orderBook
        for order in order_data.get("orderBook", []):
            # Check if the status is 6
            if order.get("status") == 6:
                # Get the stop and limit prices
                existing_stop_price = order.get("stopPrice", existing_stop_price)
                existing_limit_price = order.get("limitPrice", existing_limit_price)
                symbol = order["symbol"]
        if existing_stop_price is not None and existing_limit_price is not None:
            trade_config_data = TradingConfigurations.objects.first()
            reverse_trail_limit = trade_config_data.reverse_trailing_points

            # Calculate new stop and limit prices
            new_stop_price = existing_stop_price - reverse_trail_limit
            new_limit_price = existing_limit_price - reverse_trail_limit
            
            # Check if there are orders to cancel
            if existing_stop_price is not None:
                # Modify the order with new stop and limit prices
                data = {"id": order["id"], "limitPrice": new_limit_price, "stopPrice": new_stop_price}
                trailing_order_update = fyers.modify_order(data=data)
                
                # Check the response
                if 'message' in trailing_order_update:
                    message = trailing_order_update['message']
                    messages.success(request, message)
                    return JsonResponse({'message': message})
        
        # Handle the case where 'data' key is missing
        message = "No SL/Pending Orders"
        messages.error(request, message)
        return JsonResponse({'message': message})
    
    return redirect('dashboard')




def fyer_websocket_view(request):
    template_name = 'trading_tool/html/fyerwebsocket.html'
    access_token = request.session.get('access_token')
    return render(request, template_name)