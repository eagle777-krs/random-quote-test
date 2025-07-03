from django.urls import path
from .views import index_view, vote_quote, QuoteCreateView, QuoteUpdateView, delete_quote, quote_detail

app_name = 'quotes'

urlpatterns = [
    path('', index_view, name='index'),
    path('vote/', vote_quote, name='vote_quote'),
    path('create/', QuoteCreateView.as_view(), name='create_quote'),
    path('<int:pk>/edit/', QuoteUpdateView.as_view(), name='update_quote'),
    path('<int:pk>/delete/', delete_quote, name='delete_quote'),
    path('<int:pk>/', quote_detail, name='quote_detail')
]