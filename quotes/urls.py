from django.urls import path
from .views import index_view, vote_quote

app_name = 'quotes'

urlpatterns = [
    path('', index_view, name='index'),
    path('vote/', vote_quote, name='vote_quote')
]