from django.urls import path
from . import views

urlpatterns = [
path('index', views.index, name="start_page"),
path('category/<str:category>/', views.category_page, name='category_page'),
path('category/<str:category>/<str:id>/', views.news_page, name='news_page'),
path('', views.index, name="start_page"),
path('createfilm', views.create_film, name="create_film"),
path('editfilm/<uuid:film_id>/', views.edit_film, name="edit_film"),
path('addreview/<uuid:film_id>/', views.add_review, name="addreview"),
path('editreview/<int:review_id>/', views.edit_review, name="edit_review"),

]