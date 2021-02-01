from django.views.generic import ListView, DetailView, View
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views import View
from . import models, forms
import datetime
from django.db.models import F
from posts import models as post_models
from django.shortcuts import redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms
from django.db.models import Count


class LoginView(View):
    def get(self, request):
        form = forms.LoginForm()
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        print(form)

    def delete(self, request):
        pass


def UserDetail(request, pk):
    user = models.User.objects.get(pk=pk)

    if user.mil_fin is not None and user.mil_start is not None and user.is_soldier is not None:
        date_left = user.mil_fin - datetime.date.today()
        mil_time = user.mil_fin - user.mil_start
        if date_left.days <= 0 or mil_time.days <= 0:
            print("Division by 0 방지")
            date_left = datetime.timedelta(days=1)
            mil_time = datetime.timedelta(days=1)

        user.mil_percentage = 100 * (round(1 - date_left / mil_time, 4))
        user.mil_left_date = date_left.days

    recent_posts = post_models.Post.objects.filter(user=user).order_by('-created')[:5]


    return render(request, "users/user_detail.html",
                  {"user": user, "recent_posts": recent_posts, "today": datetime.date.today()})


def UserView(request):
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

    recent_posts = post_models.Post.objects.order_by('-created')[:5]
    trending_posts = post_models.Post.objects.annotate(like_sum=F('like') - F('dislike')).order_by('-like_sum')[:5]

    # recent_posts.annotate(comments_cnt=Count(comment_models.Comment))
    # trending_posts.annotate(comments_cnt=Count(comment_models.Comment))



    return render(request, "users/user_info.html",
                  {"users": users, "today": datetime.date.today(), "recent_posts": recent_posts,
                   "trending_posts": trending_posts})


"""
def UserView(request):
    rooms = models.User.objects.all()
    return render(request, "users/", {"rooms": rooms})
"""


class LoginView(FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        # email = form.cleaned_data.get("email")
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    initial = {"first_name": "상원", "last_name": "강", "username": "kevink1113"}

    def form_valid(self, form):
        form.save()
        # email = form.cleaned_data.get("email")
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)
