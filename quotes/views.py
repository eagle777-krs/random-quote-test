from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect
from django.db import transaction
from django.shortcuts import render
import random
from .models import Quote, Vote, VoteType

def get_weighted_random_quote():
    quotes = list(Quote.objects.all())
    if not quotes:
        return None
    weights = [q.weight for q in quotes]
    return random.choices(quotes, weights=weights, k=1)[0]

@login_required
def index_view(request):
    quote = get_weighted_random_quote()
    quote.views += 1
    quote.save()
    context = {'quote':quote}
    return render(request, 'index.html', context)

@login_required
@require_POST
def vote_quote(request):
    quote_id = request.POST.get('quote_id')
    vote_type = request.POST.get('type')
    user = request.user

    quote = get_object_or_404(Quote, pk=quote_id)

    with transaction.atomic():
        try:
            vote = Vote.objects.get(user_id=user, quote_id=quote)
            if vote.type == vote_type:
                if vote_type == VoteType.LIKE:
                    quote.likes = max(quote.likes - 1, 0)
                else:
                    quote.dislikes = max(quote.dislikes - 1, 0)
                vote.delete()
            else:
                if vote.type == VoteType.LIKE:
                    quote.likes = max(quote.likes - 1, 0)
                    quote.dislikes += 1
                else:
                    quote.dislikes = max(quote.dislikes - 1, 0)
                    quote.likes += 1
                vote.type = vote_type
                vote.save()
        except Vote.DoesNotExist:
            Vote.objects.create(user_id=user, quote_id=quote, type=vote_type)
            if vote_type == VoteType.LIKE:
                quote.likes += 1
            else:
                quote.dislikes += 1

        quote.save()

    return redirect('quotes:index')