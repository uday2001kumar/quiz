from django.views import View
from django.shortcuts import render, redirect

# restframe work
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

# local 
from core.utils import success_response,error_response

# models
from authentication.models import UserRoles

class AdminDashboardView(View):
    def get(self, request):
        return render(request, "dashboard/dashboard.html")
    
class SubscriptionPageView(View):
    def get(self, request):
        return render(request, "subscription/subscriptions.html")