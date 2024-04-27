from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.contrib import messages

class Brokerconfig(View):
    def get(self, request, *args, **kwargs):
        template = "trading_tool/html/index.html"
        context = {}
        return render(request, template, context)
# Import the required module from the fyers_apiv3 package
    


# ----------------------------------------------------------------------------------
# SAMPLE SUCCESS RESPONSE : 
# ----------------------------------------------------------------------------------

# https://api-t1.fyers.in/api/v3/generate-authcode?
# client_id=SPXXXXE7-100&
# redirect_uri=https%3A%2F%2Fdev.fyers.in%2Fredirection%2Findex.html
# &response_type=code&state=sample_state&nonce=sample_nonce
    


from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf import settings
from fyers_apiv3 import fyersModel
import webbrowser



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
        print("orders_with_status_6orders_with_status_6orders_with_status_6", orders_with_status_6)
        
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
            print("messagemessagemessage", message)
            messages.success(request, message)
            return JsonResponse({'message': message})
        else:
            # Handle the case where 'data' key is missing
            message = "Error: Response format is unexpected"
            messages.error(request, "Error: Response format is unexpected")
            return JsonResponse({'message': message})
      

    return redirect('dashboard')  

def get_data_instance(request):
    print("fetch enyryyy")
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


# from django.views import View
# from django.shortcuts import render

# from fyers_api import fyersModel
# import settings

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
      print("qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq")
      return render(request, 'trading_tool/html/profile_view.html', context)
    
    else:
      print("no access token")
      return render(request, 'trading_tool/html/profile_view.html')


from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from .models import TradingData

class OrderHistory(View):
    def get(self, request):
        context = {}
        order_data = TradingData.objects.filter(category='ORDERS')
        paginator = Paginator(order_data, 20)  # Show 10 items per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['order_history_data'] = page_obj
        return render(request, 'trading_tool/html/order_history.html', context)

# class OptionChainView(View):
#     def get(self, request):
#         context = {}
#         order_data = TradingData.objects.filter(category='ORDERS')
#         paginator = Paginator(order_data, 20)  # Show 10 items per page
#         page_number = request.GET.get('page')
#         page_obj = paginator.get_page(page_number)
#         context['order_history_data'] = page_obj
#         return render(request, 'trading_tool/html/optionchainview.html', context)
    

import datetime
class OptionChainView(View):
  def get(self, request):

    context={}
    template='trading_tool/html/optionchainview.html'
    # Get today's date
    today = datetime.date.today()

    # Calculate the next Thursday
    next_thursday = today + datetime.timedelta(days=(3 - today.weekday()) % 7)

    # Set the time to 10:00 AM
    next_thursday_time = datetime.time(hour=10, minute=0)

    # Combine the date and time
    next_thursday_datetime = datetime.datetime.combine(next_thursday, next_thursday_time)

    # Convert the next Thursday datetime to a timestamp
    next_thursday_timestamp = int(next_thursday_datetime.timestamp())

    print("Next Thursday at 10:00 AM (timestamp):", next_thursday_timestamp)

    data_instance = get_data_instance(request)
    data = {
        "symbol":"NSE:NIFTY50-INDEX",
        "strikecount":1,
        "timestamp": next_thursday_timestamp
    }
    response = data_instance.optionchain(data=data)
    context['optons_data'] = response

    print("responseresponseresponse", context)
    return render(request, template, context)

    # else:
    #   print("no access token")
    #   return render(request, template)


from django.http import HttpResponse
from .models import TradingData
from django.utils import timezone
from django.db.models import Q

def update_latest_data(request):
    # Call API to get data
    print("entry__1")
    data_instance = get_data_instance(request)

    # Save positions data
    positions = data_instance.positions()
    TradingData.objects.update_or_create(
        category='POSITIONS',
        defaults={'data': positions, 'last_updated': timezone.now()},
        # other fields
    )

    # Save orders data
    orders = data_instance.orderbook()
    TradingData.objects.update_or_create(
        category='ORDERS',
        defaults={'data': orders, 'last_updated': timezone.now()},
        # other fields
    )

    # Save funds data
    funds = data_instance.funds()
    TradingData.objects.update_or_create(
        category='FUNDS',
        defaults={'data': funds, 'last_updated': timezone.now()},
        # other fields
    )

    return HttpResponse('Data saved')

import time

def get_options_data(request):
    # Call API to get data
    print("entry__1")
    import datetime

    # Get today's date
    today = datetime.date.today()

    # Calculate the next Thursday
    next_thursday = today + datetime.timedelta(days=(3 - today.weekday()) % 7)

    # Set the time to 10:00 AM
    next_thursday_time = datetime.time(hour=10, minute=0)

    # Combine the date and time
    next_thursday_datetime = datetime.datetime.combine(next_thursday, next_thursday_time)

    # Convert the next Thursday datetime to a timestamp
    next_thursday_timestamp = int(next_thursday_datetime.timestamp())

    print("Next Thursday at 10:00 AM (timestamp):", next_thursday_timestamp)

    #    swal("Saved successfully.", response, "success");

    data_instance = get_data_instance(request)
    data = {
        "symbol":"NSE:NIFTY50-INDEX",
        "strikecount":5,
        "timestamp": next_thursday_timestamp
    }
    response = data_instance.optionchain(data=data);
    print("OPTIONSOPTIONSOPTIONSOPTIONS",response)

    return HttpResponse('Option Data Fetched')