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

class Brokerconfig(View):
    def get(self, request, *args, **kwargs):
        template = "trading_tool/html/index.html"
        context = {}
        return render(request, template, context)
def brokerconnect(request):
    # Get client_id and secret_key from settings.py
    client_id = settings.FYERS_CLIENT_ID
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
    client_id = settings.FYERS_CLIENT_ID
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
    client_id = settings.FYERS_CLIENT_ID
    access_token = request.session.get('access_token')
    if access_token:
        # Initialize the FyersModel instance with your client_id, access_token, and enable async mode
        fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="")
        order_data = fyers.orderbook()
        # Initialize an empty list to store order IDs with status 6
        orders_with_status_6 = []
        # Iterate through the orderBook
        for order in order_data.get("orderBook", []):
            # Check if the status is 6
            if order.get("status") == 6:
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
    client_id = settings.FYERS_CLIENT_ID
    access_token = request.session.get('access_token')
    if access_token:
        # Initialize the FyersModel instance with your client_id, access_token, and enable async mode
        fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")
        # Return the response received from the Fyers API
        return fyers
    else:
        print("noithing here")
        # Handle the case where access_token is not found in the session
    return fyers


from django.http import JsonResponse
def update_data_instance(request):
    context = {}
    client_id = settings.FYERS_CLIENT_ID
    access_token = request.session.get('access_token')

    if access_token:
        fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")
        response = fyers.positions()
        # Process the response and prepare the data
        data = { 'positions': response }  # Modify this according to your response structure
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Access token not found'}, status=400)

class ProfileView(View):
  def get(self, request):
    client_id = settings.FYERS_CLIENT_ID
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

class OrderHistory(View):
    def get(self, request):
        context = {}
        order_data = TradingData.objects.filter(category='ORDERS')
        paginator = Paginator(order_data, 20)  # Show 10 items per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['order_history_data'] = page_obj
        return render(request, 'trading_tool/html/order_history.html', context)

class OptionChainView(View):
    def get(self, request, slug):  # Modify to accept 'slug' parameter
        context = {}
        template = 'trading_tool/html/optionchainview.html'
        data_instance = get_data_instance(request)
        data = {
            "symbol":"NSE:"+slug+"-INDEX" ,  # Update 'symbol' to use 'slug' parameter
            "strikecount": 1,
            # "timestamp": next_thursday_timestamp
        }
        print("datadatadata", data)
        expiry_response = data_instance.optionchain(data=data)
        print("expiry_responseexpiry_responseexpiry_responseexpiry_response", expiry_response)
        first_expiry_ts = expiry_response['data']['expiryData'][0]['expiry']
        first_expiry_date = expiry_response['data']['expiryData'][0]['date']
        options_data = {
            "symbol":"NSE:"+slug+"-INDEX" ,  # Update 'symbol' to use 'slug' parameter
            "strikecount": 1,
            "timestamp": first_expiry_ts
        }
        response = data_instance.optionchain(data=options_data)
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

class ConfigureTradingView(FormView):
    template_name = 'trading_tool/html/configure_trading.html'
    form_class = TradingConfigurationsForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
from .models import TradingConfigurations
class ConfigureTradingView(FormView):
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
        # Retrieve values from POST data
        data_instance = get_data_instance(request)
        der_symbol = request.POST.get('der_symbol')
        ex_symbol = request.POST.get('ex_symbol')
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", der_symbol, ex_symbol)
        get_lot_count = get_deafult_lotsize(ex_symbol)
        trade_config_data = TradingConfigurations.objects.first()
        order_qty = trade_config_data.default_order_qty*get_lot_count
        data = {
            "symbol":der_symbol,
            "qty": order_qty ,
            "type":2, # Market Order
            "side":1, # Buy
            "productType":"INTRADAY",
            "limitPrice":0,
            "stopPrice":0,
            "validity":"DAY",
            "offlineOrder":False
        }
        response = data_instance.place_order(data=data)
        if response["code"] == 1101:
            # ----------------------------------------------------
            allOrderData = data_instance.orderbook()
            # Initialize an empty list to store order IDs with status 6
            orders_with_status_6 = []
            # Iterate through the orderBook
            for order in allOrderData.get("orderBook", []):
                # Check if the status is 6
                if order.get("status") == 6 and order.get("symbol") == der_symbol:
                    # Append the ID to the list
                    orders_with_status_6.append({"id": order.get("id")})
            order_cancel_response = []
            # Check if there are orders to cancel
            if orders_with_status_6:
                print("orders_with_status_6orders_with_status_6", orders_with_status_6["id"])
                exst_qty = orders_with_status_6[0]["qty"]
                orderId = orders_with_status_6[0]["id"]
                new_qty = order_qty + exst_qty
                # modify existing sl order 
                modify_data = {
                    "id":orderId, 
                    "type":4, 
                    "qty": new_qty
                }
                modify_response = data_instance.modify_order(data=modify_data)
                return JsonResponse({'response': modify_response["message"]})
            else:
                print("The code is 1101")
                # Here We need to Place Stoploss Order with default Stoploss price 
                buy_order_id = response.get("id")
                print("buy_order_id", buy_order_id)
                buy_order_data = {"id":buy_order_id}
                # get_buy_orderdata = data_instance.orderbook(data=data)
                get_buy_orderdata = {
                    "code": 200,
                    "message": "",
                    "s": "ok",
                    "orderBook": [{
                        "clientId": "XXXXX86",
                        "exchange": 10,
                        "fyToken": "101000000014366",
                        "id": "23080444447604",
                        "offlineOrder": False,
                        "source": "W",
                        "status": 2,
                        "type": 2,
                        "pan": "",
                        "limitPrice": 8.1,
                        "productType": "INTRADAY",
                        "qty": 1,
                        "disclosedQty": 0,
                        "remainingQuantity": 0,
                        "segment": 10,
                        "symbol": "NSE:IDEA-EQ",
                        "description": "VODAFONE IDEA LIMITED",
                        "ex_sym": "IDEA",
                        "orderDateTime": "02-Aug-2023 13:01:42",
                        "side": 1,
                        "orderValidity": "DAY",
                        "stopPrice": 0,
                        "tradedPrice": 117.0,
                        "filledQty": 1,
                        "exchOrdId": "1100000024706527",
                        "message": "",
                        "ch": -0.35,
                        "chp": -4.24,
                        "lp": 7.9,
                        "orderNumStatus": "23080444447604:2",
                        "slNo": 1,
                        "orderTag": "1:Ordertag"
                    }]
                }
                order_details = get_buy_orderdata["orderBook"][0]
                traded_price = order_details["tradedPrice"]
                symbol = order_details["symbol"]
                qty = order_details["qty"]
                default_stoploss = trade_config_data.default_stoploss
                # traded_price*default_stoploss/100
                stoploss_price = traded_price-(traded_price*default_stoploss/100)
                print("stoploss_price", stoploss_price)
                stoploss_limit = stoploss_price-0.25
                print("stoploss_limitstoploss_limitstoploss_limit", stoploss_limit)
                sl_data = {
                    "symbol":der_symbol,
                    "qty":qty,
                    "type":4, # SL-L Order
                    "side":1, # Buy
                    "productType":"INTRADAY",
                    "limitPrice":stoploss_limit,
                    "stopPrice":stoploss_price,
                    "validity":"DAY",
                    "offlineOrder":False,
                }
                get_sl_order_response = data_instance.place_order(data=sl_data)
                # if get_sl_order_response and  get_sl_order_response.get("code") == 1101:
                #     return get_sl_order_response.message
                # else:
                #     message="buy order Executed Without SL"e
                return JsonResponse({'response': get_sl_order_response["message"]})
        
        else:
            # need ato add alert for buy order not worked 
            print("The code is not 1101", response["message"])
            return JsonResponse({'response': response["message"]})

    else:
        # Handle GET request
        message="Some Error Occured Before Execute"
        return JsonResponse({'response': message})
