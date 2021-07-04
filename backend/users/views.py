from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.views import generic

from .forms import LoginForm


class LoginView(generic.View):
    template_name = "users/login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/")
        else:
            return render(request, self.template_name, {"form": form})


class LogoutView(generic.View):
    def get(self, request):
        logout(request)
        return redirect("users:login")


class AccessDeniedView(generic.TemplateView):
    template_name = "users/access-denied.html"
