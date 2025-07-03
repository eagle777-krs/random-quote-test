from django.core.exceptions import ValidationError
from django.db import models


class SourceType(models.TextChoices):
    BOOK = 'book', 'Book'
    MOVIE = 'movie', 'Movie'
    TV_SERIES = 'series', 'TV Series'
    SONG = 'song', 'Song'
    PUBLIC_SPEECH = 'public_speech', 'Public Speech'

class Author(models.Model):
    name = models.CharField(max_length=150, unique=True, blank=True)

    def __str__(self):
        return self.name

class Source(models.Model):
    name = models.CharField(max_length=300, unique=True, null=False, blank=False)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, default='', null=True)
    type = models.CharField(choices=SourceType, null=False, blank=False)

    def __str__(self):
        return self.name

class Quote(models.Model):
    text = models.TextField(max_length=1000, unique=True, null=False, blank=False)
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='quotes', null=False, blank=False)
    weight = models.PositiveIntegerField(default=1)
    views = models.PositiveIntegerField(default=0, null=False, blank=False)
    likes = models.PositiveIntegerField(default=0, null=False, blank=False)
    dislikes = models.PositiveIntegerField(default=0, null=False, blank=False)

    def clean(self):
        count = Quote.objects.filter(source=self.source).exclude(pk=self.pk).count()
        if count >= 3:
            raise ValidationError('У этого источника уже 3 цитаты')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text[:50]