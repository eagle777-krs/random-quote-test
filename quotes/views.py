from django.shortcuts import render
import random
from .models import Quote

def get_weighted_random_quote():
    quotes = list(Quote.objects.all())
    if not quotes:
        return None
    weights = [q.weight for q in quotes]
    return random.choices(quotes, weights=weights, k=1)[0]

def index_view(request):
    quote = get_weighted_random_quote()
    quote.views += 1
    quote.save()
    context = {'quote':quote}
    return render(request, 'index.html', context)
