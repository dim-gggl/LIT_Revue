from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.generic import View
from . import forms

class LogginPage(View):
    form_class = forms.LoginForm
    template_name = "authentication/login.html"

    def get(self, request):
        form = self.form_class()
        message = ""

        return render(
            request, self.template_name,
            context={
                "form": form,
                "message": message
                }
            )

    def post(self, request):
        form = self.form_class(request.POST)
        message = ""

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )

            if user:
                login(request, user)
                return redirect("homepage")

        message = "Identifiants invalides !"

        return render(
            request, self.template_name,
            context={
                "form": form,
                "message": message
                }
            )


class LoggingOutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")


# def logout_user(request):
#     logout(request)
#     return redirect("login")
