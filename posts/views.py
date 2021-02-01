from django.views.generic import ListView, DetailView, View
from django.shortcuts import render
from django.core.paginator import Paginator
from . import models, forms


class PostList(ListView):
    """ PostList Definition """
    model = models.Post
    paginate_by = 5
    paginate_orphans = 3
    ordering = "-created"
    context_object_name = "posts"


class PostDetail(DetailView):
    """ PostDetail Definition """
    model = models.Post


class SearchView(View):
    """ SearchView Definition """

    def get(self, request):
        country = request.GET.get("country")
        if country:
            form = forms.SearchForm(request.GET)
            if form.is_valid():
                city = form.cleaned_data.get("city")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                qs = models.Post.objects.filter(**filter_args).order_by("-created")

                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("page", 1)

                posts = paginator.get_page(page)

                return render(
                    request, "rooms/search.html", {"form": form, "posts": posts}
                )

        else:
            form = forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form})
