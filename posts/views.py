from django.views.generic import ListView, DetailView, View
from django.shortcuts import render
from django.core.paginator import Paginator
from . import models, forms
from math import floor


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
