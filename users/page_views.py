from django.shortcuts import render

def signup(request):
    return render(request,"profile/signup.html")

def verifyopt(request):
    return render(request,"profile/verifyotp.html")