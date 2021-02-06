from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, View, FormView
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.urls import reverse, reverse_lazy
from . import models, forms
from math import floor
from django.http import HttpResponse
from django.contrib import messages
from .forms import PostForm
from .models import Post
from users import mixins as user_mixins
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.backends import Permission


class PostList(ListView, user_mixins.LoginRequiredMixin, PermissionRequiredMixin):
    raise_exception = True
    permission_required = 'post.view_post'
    """
    permissions = (
        ('can_')
    )
    """
    """ PostList Definition """
    model = models.Post
    paginate_by = 5
    paginate_orphans = 0
    ordering = "-created"
    context_object_name = "posts"


class PostDetail(DetailView, user_mixins.LoggedInOnlyView, PermissionRequiredMixin):
    raise_exception = True
    permission_required = 'post.view_post'
    """
    class Meta:
        permission_required = (
            ("view_post", "can view post"),
        )
    """
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


class SearchView(View, user_mixins.LoginRequiredMixin):
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


@login_required
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


@login_required
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
def new_post(request):
    form = PostForm()
    return render(request, 'posts/new_post.html', {"form": form})
"""

"""
class NewPost(FormView):
    form_class = forms.PostForm
    template_name = "posts/new_post.html"
    success_url = reverse_lazy("posts:list")
"""


@login_required()
def NewPost(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = Post(**form.cleaned_data)
            post.user = request.user
            post.save()
            return redirect('posts:list')
    else:
        form = PostForm()
    context = {
        'form': form
    }
    # return render(request, 'core/post_create.html', context)
    return render(request, 'posts/new_post.html', context)


@login_required()
def delete_post(request, post_pk):
    # print(f"Should delete {post_pk}")
    user = request.user
    try:
        post = models.Post.objects.get(pk=post_pk)
        if post.user.pk != user.pk:
            messages.error(request, "You can't delete that Post!!")
        else:
            models.Post.objects.filter(pk=post_pk).delete()
            messages.success(request, "Post Deleted!")
        return redirect(reverse("posts:list"))
    except models.Post.DoesNotExist:
        return redirect(reverse("core:home"))


"""
from django.urls import reverse
return redirect(reverse("core:home"))
return reverse("users:detail", kwargs={"pk": self.pk})
"""
