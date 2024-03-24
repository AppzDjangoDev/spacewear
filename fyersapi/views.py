from django.shortcuts import render
from django.views import View
from django.conf import settings

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

    # Replace these values with your actual API credentials
    redirect_uri = "https://spacewear.co.in/dashboard"
    response_type = "code"  
    state = "sample_state"

    # Create a session model with the provided credentials
    print("redirect_uri", redirect_uri)
    session = fyersModel.SessionModel(
        client_id=client_id,
        secret_key=secret_key,
        redirect_uri=redirect_uri,
        response_type=response_type
    )

    # Generate the auth code using the session model
    response = session.generate_authcode()

    # Print the auth code received in the response
    print("responseresponseresponse",response)
    # You can redirect to another page or render a template after printing
    return redirect(response)  # Assuming 'home' is the name of a URL pattern you want to redirect to


def get_accese_token(request):
    # return redirect('some_redirect_url')
    # Get client_id and secret_key from settings.py
    client_id = settings.FYERS_CLIENT_ID
    secret_key = settings.FYERS_SECRET_ID
    redirect_uri = "https://spacewear.co.in/dashboard"
    response_type = "code" 
    grant_type = "authorization_code"  

    # The authorization code received from Fyers after the user grants access
    auth_code = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkubG9naW4uZnllcnMuaW4iLCJpYXQiOjE3MTEyNzg2NDgsImV4cCI6MTcxMTMwODY0OCwibmJmIjoxNzExMjc4MDQ4LCJhdWQiOiJbXCJ4OjBcIiwgXCJ4OjFcIiwgXCJ4OjJcIiwgXCJkOjFcIiwgXCJkOjJcIiwgXCJ4OjFcIiwgXCJ4OjBcIl0iLCJzdWIiOiJhdXRoX2NvZGUiLCJkaXNwbGF5X25hbWUiOiJZUzA1MTQxIiwib21zIjoiSzEiLCJoc21fa2V5IjoiNGQ0OWQzMzA2MmM4YzMyOTA4OGEyMzZkMWVkZDI0MDhhODYyY2QyZDdlMmI2M2Y4NjI3N2JkZGUiLCJub25jZSI6IiIsImFwcF9pZCI6Ikg5TzQwNlhCWFciLCJ1dWlkIjoiNTdhYzQ2MmM0YzkxNGI0MzlmMGY3OTc3MGRmMDM0YTEiLCJpcEFkZHIiOiIwLjAuMC4wIiwic2NvcGUiOiIifQ.RhnYqWn9hqR5X_yg5wHKcOGCkGFnAb4Ms2xbToDMPAw"

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
    print(response)

    # You can redirect to another page or render a template after printing
    return redirect('dashboard')  # Assuming 'home' is the name of a URL pattern you want to redirect to


def get_user_profile(request):
    client_id = settings.FYERS_CLIENT_ID
    access_token = request.session.get('auth_code')
    print("client_idclient_id", client_id)
    print("access_tokenaccess_token", access_token)
    if access_token:
        # Initialize the FyersModel instance with your client_id, access_token, and enable async mode
        fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")
        # Make a request to get the user profile information
        response = fyers.get_profile()
        print("return responsereturn response",response)
        # Return the response received from the Fyers API
        return redirect('dashboard')
    else:
        print("noithing here")
        # Handle the case where access_token is not found in the session
    
    return redirect('dashboard')

# # Example usage:
# client_id = "XC4XXXXM-100"
# access_token = "eyJ0eXXXXXXXX2c5-Y3RgS8wR14g"
# profile_response = get_user_profile(client_id, access_token)
# print(profile_response)
