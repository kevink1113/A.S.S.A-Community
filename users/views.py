from django.views.generic import ListView, DetailView, View
from django.shortcuts import render
from django.views import View
from . import models, forms
import datetime


class LoginView(View):
    def get(self, request):
        form = forms.LoginForm()
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        print(form)

    def delete(self, request):
        pass


class UserDetail(DetailView):
    model = models.User


class UserView(View):
    def get(self, request):
        users = models.User.objects.all()

        for user in users:
            if user.mil_fin is not None and user.mil_start is not None and user.is_soldier is not None:
                date_left = user.mil_fin - datetime.date.today()
                mil_time = user.mil_fin - user.mil_start

                if date_left.days <= 0 or mil_time.days <= 0:
                    print("Division by 0 방지")
                    date_left = datetime.timedelta(days=1)
                    mil_time = datetime.timedelta(days=1)

                user.mil_percentage = 100 * (round(1 - date_left / mil_time, 4))
                user.mil_left_date = date_left.days

        return render(request, "users/user_info.html", {"users": users, "today": datetime.date.today()})


"""
def UserView(request):
    rooms = models.User.objects.all()
    return render(request, "users/", {"rooms": rooms})
"""
