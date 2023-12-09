from django.shortcuts import render
from django.views import View  


class DashboardView(View):
    def get(self, request , **kwargs):
        template = "trading_tool/html/index.html"



        return render(request, template, context)
