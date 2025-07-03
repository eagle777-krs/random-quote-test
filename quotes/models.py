from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User

class SourceType(models.TextChoices):
    BOOK = 'book', 'Book'
    MOVIE = 'movie', 'Movie'
    TV_SERIES = 'series', 'TV Series'
    SONG = 'song', 'Song'
    PUBLIC_SPEECH = 'public_speech', 'Public Speech'

class Author(models.Model):
    name = models.CharField('Имя автора', max_length=150, unique=True, blank=True)

    def __str__(self):
        return self.name

class Source(models.Model):
    name = models.CharField('Название источника', max_length=300, unique=True, null=False, blank=False)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, default='', null=True)
    type = models.CharField('Тип источника', choices=SourceType, null=False, blank=False)

    def __str__(self):
        return self.name

class Quote(models.Model):
    text = models.TextField("Текст цитаты", max_length=1000, unique=True, null=False, blank=False)
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='quotes', null=False, blank=False)
    weight = models.PositiveIntegerField("Вес цитаты", default=1)
    views = models.PositiveIntegerField("Количество просмотров", default=0, null=False, blank=False)
    likes = models.PositiveIntegerField("Количество лайков", default=0, null=False, blank=False)
    dislikes = models.PositiveIntegerField("Количество дизлайков", default=0, null=False, blank=False)

    def clean(self):
        count = Quote.objects.filter(source=self.source).exclude(pk=self.pk).count()
        if count >= 3:
            raise ValidationError('У этого источника уже 3 цитаты')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text[:50]

class VoteType(models.TextChoices):
    LIKE = 'like', 'Like'
    DISLIKE = 'dislike', 'Dislike'

class Vote(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    quote_id = models.ForeignKey(Quote, on_delete=models.CASCADE)
    type = models.CharField(choices=VoteType)

    class Meta:
        unique_together = ('user_id', 'quote_id')

    def __str__(self):
        return self.type