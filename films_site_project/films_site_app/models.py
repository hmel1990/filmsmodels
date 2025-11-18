from django.db import models

import uuid

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