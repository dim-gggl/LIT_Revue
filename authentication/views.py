from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from . import forms

def login_page(request):
    form = forms.LoginForm()
    message = "Connexion / Inscription"
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid:
            user = authenticate(
                username=form.data["username"],
                password=form.data["password"]
            )
            if user:
                login(request, user)
                return redirect("homepage")
            else:
                message = "Identifiants invalides !"
    return render(
        request, "authentication/login.html",
        context={"form": form, "message": message}
        )

def logout_user(request):
    logout(request)
    return redirect("login")
