from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('username', 'text', 'created_at', )
    list_filter = ('created_at',)
    def has_delete_permission(self, request, obj=None):
        return request.user.has_perm("films_site_app.can_delete_reviews")
    def has_change_permission(self, request, obj=None):
        return request.user.has_perm("films_site_app.can_moderate_reviews")
    

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', )
    def has_delete_permission(self, request, obj=None):
        return request.user.has_perm("films_site_app.can_delete_genre")
    def has_change_permission(self, request, obj=None):
        return request.user.has_perm("films_site_app.can_moderate_genre")
    def has_add_permission(self, request):
        return request.user.has_perm("films_site_app.can_add_genre")
    

@admin.register(Film)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'rating', 'review_quantity')
    list_filter = ('rating', )   
    filter_horizontal = ('genre',)
    search_fields = ('name', 'category')
    ordering = ('-rating', )


    def review_quantity (self, obj:Film):
        return obj.reviews.count()
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser
