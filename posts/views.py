from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from . import models, forms
from math import floor
from django.http import HttpResponse


class PostList(ListView):
    """ PostList Definition """
    model = models.Post
    paginate_by = 5
    paginate_orphans = 0
    ordering = "-created"
    context_object_name = "posts"


class PostDetail(DetailView):
    """ PostDetail Definition """
    model = models.Post
    pk = models.Post.pk

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        # models.Post.objects.count()
        pk = self.kwargs['pk']
        page_idx = models.Post.objects.count() - pk
        page_idx = floor(page_idx / 5) + 1
        if page_idx == 0:
            page_idx = 1
        # print("PK: ", page_idx)
        """
        pk = self.kwargs['pk']
        blist = models.Post.objects.order_by("-created")
        position = list(blist).index(pk)
        if position == 0:
            page = "1"
        else:
            page = math.floor(position / 5) + 1
        context['page'] = page
        """
        context['page_idx'] = page_idx
        return context


class SearchView(View):
    """ SearchView Definition """

    def get(self, request):
        title = request.GET.get("title")
        form = forms.SearchForm(request.GET)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            user = form.cleaned_data.get("user")
            filter_args = {}
            if title != "":
                filter_args["title__contains"] = title

            if user is not None:
                filter_args["user"] = user

            qs = models.Post.objects.filter(**filter_args).order_by("-created")
            paginator = Paginator(qs, 10, orphans=0)
            page = request.GET.get("page", 1)
            posts = paginator.get_page(page)

            return render(
                request, "posts/search.html", {"form": form, "posts": posts}
            )

        else:
            form = forms.SearchForm()

        return render(request, "posts/search.html", {"form": form})


def LikePost(request, pk):
    post = models.Post.objects.get(pk=pk)
    # print(post)
    # 이미 비추천이 있다면 먼저 이를 취소한다.
    if request.user in post.dislike_users.all():
        post.dislike_users.remove(request.user)
    # 이미 추천 눌렀다면, 취소.
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
    # 누른 적이 없다면 추가.
    else:
        post.like_users.add(request.user)
    # post = get_object_or_404(PostList, pk=pk)
    # if request.userin post.
    # return redirect(reverse("posts:detail", pk=pk))
    # return HttpResponse()
    return redirect('posts:detail', pk)
    # return reverse("posts:detail", kwargs={"pk": pk})


def disLikePost(request, pk):
    post = models.Post.objects.get(pk=pk)
    # 이미 추천이 있다면 먼저 이를 취소한다.
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
    # 이미 비추천 눌렀다면, 취소.
    if request.user in post.dislike_users.all():
        post.dislike_users.remove(request.user)
    # 누른 적이 없다면 추가.
    else:
        post.dislike_users.add(request.user)
    # return HttpResponse()
    # return render(request, "posts/post_detail.html", {"pk": pk})
    # return redirect(reverse("posts:detail"))
    return redirect('posts:detail', pk)

"""
from django.urls import reverse
return redirect(reverse("core:home"))
return reverse("users:detail", kwargs={"pk": self.pk})
"""