from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.generic import View
from . import forms


class LoginView(View):
    """
    LoginView handles user authentication via a login form.

    Attributes:
        form_class: The Django form class used for user login.
        template_name: The template used to render the login page.

    Methods:
        get(request):
            Handles GET requests by rendering the login form.
            Returns the login page with an empty form and message.

        post(request):
            Handles POST requests by validating the submitted login form.
            Authenticates the user using the provided credentials.
            If authentication is successful, logs in the user and
            redirects to the homepage.
            If authentication fails, re-renders the login page with
            an error message.
    """
    form_class = forms.LoginForm
    template_name = "authentication/login.html"

    def get(self, request):
        form = self.form_class()
        message = ""

        return render(
            request, self.template_name,
            context={"form": form, "message": message}
            )

    def post(self, request):
        form = self.form_class(request.POST)
        message = ""
        button_text = "Connexion"
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
            request,
            self.template_name,
            context={
                "form": form,
                "message": message,
                "button_text": button_text
                }
            )


class LogoutView(View):
    """
    View to handle user logout.

    This view logs out the currently authenticated user and
    redirects them to the login page.

    Methods
    -------
    get(request):
        Logs out the user and redirects to the login page.
    """
    def get(self, request):
        logout(request)
        return redirect("login")


class SignUpView(View):
    """
    View handling user sign-up functionality.

    - GET: Renders the sign-up form for new users.
    - POST: Processes the submitted sign-up form. If valid,
    creates a new user, logs them in, and redirects to the
    login redirect URL. If invalid, re-renders the form with errors.

    Attributes:
        form_class: The Django form class used for user registration.

    Methods:
        get(request): Handles GET requests to display the sign-up form.
        post(request): Handles POST requests to process the sign-up
        form submission.
    """
    form_class = forms.SignUpForm

    def get(self, request):
        form = self.form_class
        return render(
            request,
            "authentication/signup.html",
            context={"form": form}
            )

    def post(self, request):
        form = self.form_class(request.POST)
        button_text = "Inscription"

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)

        return render(
            request,
            "authentication/signup.html",
            context={
                "form": form,
                "button_text": button_text
                }
            )
