from django.shortcuts import redirect, render
from account.forms import UserLoginForm, UserprofileUpdate
from django.contrib import auth
from django.views import View  
from django.contrib.auth import logout
from django.contrib import messages
from account.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from datetime import datetime
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import CreateView

from fyersapi.views import brokerconnect, get_accese_token, get_data_instance
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from decimal import Decimal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from urllib.parse import urlparse, parse_qs
from django.contrib.auth.decorators import login_required
import time

def homePage(request):
    return render(request,'accounts/index.html')

from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from urllib.parse import urlparse, parse_qs
from django.contrib import messages
import time

class DashboardView(TemplateView):
    template_name = "trading_tool/html/index.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            print("ppppppppppppppppppppppppppppppppppp")
            current_url = request.build_absolute_uri()
            print("current_url:", current_url)
            parsed_url = urlparse(current_url)
            query_params = parse_qs(parsed_url.query)
            auth_code = query_params.get('auth_code', [''])[0]
            print("auth_codeauth_code", auth_code)
            if auth_code:
                request.session['auth_code'] = auth_code
                messages.success(request, 'Auth code stored successfully.')
            else:
                messages.error(request, 'Failed to extract auth code from the URL.')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}. No broker connected.')

        # Delay the execution of get_access_token function by 1 second
        time.sleep(1)
        get_accese_token(request)
        data_instance = get_data_instance(request)
        self.positions_data = data_instance.positions()

        print("data_instance", self.positions_data)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['positions_data'] = self.positions_data
        return context

# Create your views here.
class UserloginView(View):
    def get(self, request):
        template = "trading_tool/html/authentication-login.html"
        context={}
        context['form']= UserLoginForm()
        print("context", context)
        logged_user = request.user

        if logged_user.is_authenticated:
            print(logged_user)
            print("dashboard__form")
            return redirect('brokerconnect')  
        else:
            print(logged_user)
            print("login__form")
            return render(request, template, context)
        
    def logoutUser(request):
        print("logout_processing")
        logout(request)
        return redirect('login')

    def post(self, request):
        context={}
        form = UserLoginForm(request.POST)
        context['form']= form
        template = "trading_tool/html/authentication-login.html"
        if request.method == "POST":
            if form.is_valid():
                login_username = request.POST["username"]
                login_password = request.POST["password"]
                print(login_username)
                print(login_password)
                user = auth.authenticate(username=login_username, password=login_password)
                if user :
                # if user is not None and  user.is_superuser==False and user.is_active==True:
                    auth.login(request, user)
                    print("login success")
                    messages.success(request, "Login Successful !")
                    # return render(request, "user/dashboard.html")
                    return redirect('brokerconnect')  
                else:
                    print("user not Exists")
                    # messages.info(request, "user not Exists")
                    messages.error(request, 'Username or Password incorrect !')
                    return render(request, template, context)
            else:
                print("user not created")
                return render(request, template, context)


class UserRegistrationView(CreateView):
    print("============================================")
    form_class = CustomUserCreationForm
    template_name = "trading_tool/html/authentication-register.html"
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)

        # Authenticate and log in the user
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        messages.success(self.request, 'Registration completed successfully')
        user = authenticate(username=username, password=password)
        messages.success(self.request, 'redirected to Dashboard')
        login(self.request, user)
        return response

class MemberListView(View):
    def get(self, request , **kwargs):
        template = "user/accountmanage.html"
        breadcrumb = {"1":"Member Management", "2":"Manage member" }
        label = { 'title' : "Manage member" }
        header = { "one": 'First Name',"two" : 'Last Name', "three" : "User Name",}
        Data =  User.objects.all()
        context = {'header':header , 'label':label, "breadcrumb":breadcrumb ,"Data": Data}
        return render(request, template, context)

class SuccessView(View):
    def get(self, request):
        template = "success_page.html"
        context={}
        print("context", context)
        return render(request, template, context)
        
      
class ProfileView(View):
    def __init__(self):
        pass

    def get(self, request):
        user_pk = request.user
        try:
            instance = User.objects.get(pk=user_pk.id)
        except User.DoesNotExist:
            instance = None
        form = UserprofileUpdate(instance=instance)
        template = "pages-account-settings-account.html"
        context={}
        context['form'] = form
        print("context", context)
        return render(request, template, context)

    def post(self, request):
        user_id = request.user.id
        instance = get_object_or_404(User, id=user_id)
        context={}
        form = UserprofileUpdate(request.POST or None, request.FILES or None,  instance=instance)
        context['form']= form
        template = "pages-account-settings-account.html"
        if form.is_valid():
            form.save()
            print("updated successfully")
            messages.success(request, 'Your Account details updated successfully!')
            return redirect('dashboard')  
        else:
            print("updating failed")
            return render(request, template, context)
        
