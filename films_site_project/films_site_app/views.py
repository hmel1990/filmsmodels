from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponseNotAllowed
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.template.response import TemplateResponse
from films_site_app.models import Film, Review
from django.shortcuts import get_object_or_404


import random


from .forms import FilmForm, ReviewForm

import uuid
import os
from datetime import datetime
def current_timestamp():
    return str(int(datetime.timestamp(datetime.now())))


class FilmForSite:
    def __init__(self, category='common', name='Name', text='Lorem', avatar_name='default'):
        self.id = str(uuid.uuid4())  # уникальный id
        self.category = category
        self.name = name
        self.text = text
        self.avatar_name = avatar_name

    def __str__(self):
        return f"Category: {self.category}"


def seed_films():
    films_list = [
        ('action', 'Operation Storm', 'An elite squad embarks on a mission to rescue hostages deep in the jungle.', '1.jpg'),
        ('action', 'City Without Rules', 'A lone vigilante fights to clean up the crime-ridden streets of a sprawling metropolis.', '2.jpg'),
        ('action', 'The Last Raid', 'A special forces team faces betrayal from within during a high-stakes operation.', '3.jpg'),

        ('adventure', 'Lost Island', 'A group of explorers stumbles upon a mysterious island filled with ancient secrets.', '4.jpg'),
        ('adventure', 'Desert Path', 'A traveler crosses the desert in search of a legendary artifact.', '5.jpg'),
        ('adventure', 'Treasure Map', 'Teenagers discover an old map and set off on a dangerous quest for treasure.', '6.jpg'),

        ('romance', 'Autumn Waltz', 'A heartfelt love story unfolds in a quiet coastal town.', '7.jpg'),
        ('romance', 'Letters from the Past', 'A woman uncovers family secrets through a series of old letters.', '8.jpg'),
        ('romance', 'Forever in My Heart', 'Two lovers fight to stay together against all odds.', '9.jpg'),

        ('adventure', 'Polar Expedition', 'Scientists venture into the Arctic and make unexpected discoveries.', '10.jpg')
    ]

    for category, name, text, avatar_name in films_list:
        Film.objects.create(
            category=category,
            name=name,
            text=text,
            avatar_name=avatar_name,
            rating=random.uniform(1.0, 5.0) 
        ).save()


# seed_films()

def index (request):
    fims_list = Film.objects.all()
    news_list_categories = list(set(news.category for news in fims_list))
    return TemplateResponse(request, 'main.html', {"news_list_categories":news_list_categories})

def category_page (request, category):

    sort_by = request.GET.get('sort', 'name')
    if sort_by not in ['name', '-name', 'rating', '-rating']:
        sort_by = 'name'

    # category_list = list(filter(lambda news: news.category == category, fims_list))
    category_list = Film.objects.filter(category=category).order_by(sort_by)
    # return TemplateResponse(request, 'category_page.html', {"category_list":category_list, "MEDIA_URL": settings.MEDIA_URL})
    return TemplateResponse(request, 'category_page.html', {
    "category_list": category_list,
    "MEDIA_URL": settings.MEDIA_URL,
    "category": category,
    "sort_by": sort_by
    })



def news_page(request, category, id):
    film = get_object_or_404(Film, id=id, category=category)
    film.rating_int = int(film.rating)
    reviews = Review.objects.filter(film = film)
    return TemplateResponse(request, 'news_page.html', {
        "films": film,
        "MEDIA_URL": settings.MEDIA_URL,
        "rating":film.rating_int,
        'reviews':reviews
    })



filmForm = FilmForm()

def create_film(request: HttpRequest):
    if request.method == "POST":
        filmform = FilmForm(request.POST, request.FILES)
        if filmform.is_valid():
            avatar = filmform.cleaned_data["avatar"]
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            file_type = avatar.name.split('.')[-1]
            file_name = fs.save(f"{current_timestamp()}.{file_type}", avatar)

            Film.objects.create(
                category=filmform.cleaned_data["category"],
                name=filmform.cleaned_data["name"],
                text=filmform.cleaned_data["text"],
                avatar_name=file_name,
                rating=filmform.cleaned_data.get("rating", 3.0)
            )
            return redirect('start_page')
        return render(request, 'create_film.html', {"form": filmform})
    return render(request, 'create_film.html', {"form": FilmForm()})


    
def edit_film(request: HttpRequest, film_id):
    film = get_object_or_404(Film, id=film_id)

    if request.method == "POST":
        form = FilmForm(request.POST, request.FILES, is_editing=True)
        if form.is_valid():
            cd = form.cleaned_data

            if cd.get("category"):
                film.category = cd["category"]
            if cd.get("name"):
                film.name = cd["name"]
            if cd.get("text"):
                film.text = cd["text"]
            if cd.get("rating") is not None:
                film.rating = cd["rating"]
            if "avatar" in request.FILES:
                avatar = cd["avatar"]
                fs = FileSystemStorage(location=settings.MEDIA_ROOT)
                file_type = avatar.name.split('.')[-1]
                file_name = fs.save(f"{current_timestamp()}.{file_type}", avatar)
                film.avatar_name = file_name
            film.save()
            return redirect("start_page")

        return render(request, "edit_film.html", {"form": form, "film": film})

    return render(request, "edit_film.html", {"form": FilmForm(is_editing=True), "film": film})

def add_review(request: HttpRequest, film_id):
    film = get_object_or_404(Film, id=film_id)
    
    if request.method == "POST":
        reviewform = ReviewForm(request.POST)

        if reviewform.is_valid():
            Review.objects.create(
                film=film,
                text=reviewform.cleaned_data["text"]
            )
            return redirect("news_page", category=str(film.category), id=str(film.id))
        return render(request, 'create_review.html', {"form": reviewform})
    return render(request, 'create_review.html', {"form": ReviewForm()})


def edit_review (request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if request.method == "POST":
        reviewform = ReviewForm(request.POST)
        if reviewform.is_valid():
            review.text = reviewform.cleaned_data["text"]
            review.save()
            return redirect("news_page", category=str(review.film.category), id=str(review.film.id))
        return render(request, 'edit_review.html', {"form": reviewform})
    return render(request, 'edit_review.html', {"form": ReviewForm(), "review": review})


    