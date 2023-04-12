from django.contrib.auth import get_user_model
from django.db import models

# from users.models import User
User = get_user_model()  # Временно


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
    )


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    score = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)
