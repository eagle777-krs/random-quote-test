from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect
from django.db import transaction
from django.shortcuts import render
import random
from .models import Quote, Vote, VoteType, Author, Source
from .forms import QuoteForm, QuoteUpdateForm
from django.db.models import Q

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

@login_required
def create_quote_view(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            try:
                quote = form.save()
                return redirect('quotes:quote_detail', pk=quote.pk)
            except ValidationError as e:
                form.add_error(None, e.message)
    else:
        form = QuoteForm()
    return render(request, 'quote_create.html', {'form': form})


@login_required
def update_quote_view(request, pk):
    quote = get_object_or_404(Quote, pk=pk)

    if request.method == 'POST':
        form = QuoteUpdateForm(request.POST, instance=quote)
        if form.is_valid():
            try:
                form.save()
                return redirect('quotes:quote_detail', pk=quote.pk)
            except ValidationError as e:
                form.add_error(None, e.message)
    else:
        form = QuoteUpdateForm(instance=quote)
    return render(request, 'quote_update.html', {'form': form, 'quote': quote})

@login_required
def quote_detail(request, pk):
    quote = get_object_or_404(Quote, pk=pk)
    return render(request, 'quote_detail.html', {'quote': quote})

@login_required
def delete_quote(request, pk):
    quote = get_object_or_404(Quote, pk=pk)
    if request.method == 'POST':
        quote.delete()
        return redirect('quotes:index')
    return render(request, 'quote_confirm_delete.html', {'quote': quote})

@login_required
def browse_quotes(request):
    q = Quote.objects.all()
    search_query = request.GET.get('q', '').strip()
    top_10_by_likes = request.GET.get('top_10_by_likes')
    top_10_by_dislikes = request.GET.get('top_10_by_dislikes')

    if search_query:
        q = q.filter(
            Q(text__icontains=search_query) |
            Q(source__name__icontains=search_query) |
            Q(source__author__name__icontains=search_query)
        )

    if top_10_by_likes:
        q = q.order_by('-likes')[:10]
    elif top_10_by_dislikes:
        q = q.order_by('-dislikes')[:10]

    return render(request, 'browse_quotes.html', {'quotes': q, 'search_query': search_query})



