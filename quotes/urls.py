from django.urls import path
from .views import index_view, vote_quote, create_quote_view, update_quote_view, delete_quote, quote_detail, browse_quotes

app_name = 'quotes'

urlpatterns = [
    path('', index_view, name='index'),
    path('vote/', vote_quote, name='vote_quote'),
    path('create/', create_quote_view, name='create_quote'),
    path('<int:pk>/edit/', update_quote_view, name='update_quote'),
    path('<int:pk>/delete/', delete_quote, name='delete_quote'),
    path('<int:pk>/', quote_detail, name='quote_detail'),
    path('browse_quotes/', browse_quotes, name='browse_quotes')
]