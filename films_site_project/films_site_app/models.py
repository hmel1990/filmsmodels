from django.db import models
from django.utils import timezone

import uuid

    
class Genre (models.Model):
    name = models.CharField(max_length=150)
    def __str__(self):
        return f"{self.id} | {self.name}"
    class Meta ():
        permissions = [
            ("can_moderate_genre", "Может модерировать жанр"),
            ("can_delete_genre", "Может удалять жанр"),  
            ("can_add_genre", "Может добавлять жанр"),  
        ]


class Film(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    category = models.CharField(null=False, max_length=100, default='common')
    name = models.CharField(null=False, max_length=300, default='Name')
    text = models.TextField(null=False, default='Lorem')
    avatar_name = models.CharField(null=False, max_length=255, default='default')
    rating = models.FloatField(
        null=False,
        default=3.0,
    )
    genre = models.ManyToManyField(null=True, to=Genre)


    def __str__(self):
        return f"""
                    FilmID:{self.id}
                    Category:{self.category}
                    Name:{self.name}
                    Text:{self.text}
                    Avatar:{self.avatar_name}
                    Rating: {self.rating}
                """

    # class Meta:
    #     db_table = 'dj_films'
    #     constraints = [
    #         models.CheckConstraint(
    #             check=models.Q(name__regex=r'.*\S.*'),
    #             name='name_not_blank'
    #         ),
    #     ]

# class User (models.Model):

class Review(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='reviews')
    username = models.CharField(max_length=255, editable=False)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    def save(self, *args, **kwargs):
        if not self.pk:
            # Найти первый свободный постфикс
            existing_usernames = set(Review.objects.filter(film=self.film).values_list('username', flat=True))
            index = 0
            while f"testUser{index}" in existing_usernames:
                index += 1
            self.username = f"testUser{index}"
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.username} - {self.film.name}"
    class Meta ():
        permissions = [
            ("can_moderate_reviews", "Может модерировать отзывы"),
            ("can_delete_reviews", "Может удалять отзывы"),  
        ]


