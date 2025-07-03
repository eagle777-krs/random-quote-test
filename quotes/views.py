from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect
from django.db import transaction
from django.shortcuts import render
import random
from .models import Quote, Vote, VoteType
from .forms import QuoteForm, AuthorForm, SourceForm, ExistingAuthorForm, ExistingSourceForm
from django.contrib.auth.mixins import LoginRequiredMixin

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

class QuoteCreateView(LoginRequiredMixin, View):

    def get(self, request):
        context = {
            'quote_form': QuoteForm(),
            'author_form': AuthorForm(),
            'source_form': SourceForm(),
            'existing_author_form': ExistingAuthorForm(),
            'existing_source_form': ExistingSourceForm(),
        }
        return render(request, 'quote_create.html', context)

    def post(self, request):
        quote_form = QuoteForm(request.POST)
        author_form = AuthorForm(request.POST)
        source_form = SourceForm(request.POST)
        existing_author_form = ExistingAuthorForm(request.POST)
        existing_source_form = ExistingSourceForm(request.POST)

        selected_author = None
        selected_source = None

        with transaction.atomic():
            if existing_author_form.is_valid() and existing_author_form.cleaned_data['existing_author']:
                selected_author = existing_author_form.cleaned_data['existing_author']
            elif author_form.is_valid() and author_form.cleaned_data.get('name'):
                selected_author = author_form.save()

            if existing_source_form.is_valid() and existing_source_form.cleaned_data['existing_source']:
                selected_source = existing_source_form.cleaned_data['existing_source']
            elif source_form.is_valid() and source_form.cleaned_data.get('name') and selected_author:
                new_source = source_form.save(commit=False)
                new_source.author = selected_author
                new_source.save()
                selected_source = new_source

            if quote_form.is_valid() and selected_source:
                new_quote = quote_form.save(commit=False)
                new_quote.source = selected_source
                new_quote.save()
                return redirect('quotes:quote_detail', pk=new_quote.pk)

        context = {
            'quote_form': quote_form,
            'author_form': author_form,
            'source_form': source_form,
            'existing_author_form': existing_author_form,
            'existing_source_form': existing_source_form,
        }
        return render(request, 'quote_create.html', context)

class QuoteUpdateView(LoginRequiredMixin, View):

    def get(self, request, pk):
        quote = get_object_or_404(Quote, pk=pk)
        quote_form = QuoteForm(instance=quote)
        existing_source_form = ExistingSourceForm(initial={'existing_source': quote.source})
        context = {
            'quote_form': quote_form,
            'existing_source_form': existing_source_form,
            'quote': quote,
        }
        return render(request, 'quote_update.html', context)

    def post(self, request, pk):
        quote = get_object_or_404(Quote, pk=pk)
        quote_form = QuoteForm(request.POST, instance=quote)
        existing_source_form = ExistingSourceForm(request.POST)

        if quote_form.is_valid() and existing_source_form.is_valid():
            selected_source = existing_source_form.cleaned_data['existing_source']
            if selected_source:
                updated_quote = quote_form.save(commit=False)
                updated_quote.source = selected_source
                updated_quote.save()
                return redirect('quotes:quote_detail', pk=updated_quote.pk)
            else:
                existing_source_form.add_error('existing_source', 'Источник обязателен.')

        context = {
            'quote_form': quote_form,
            'existing_source_form': existing_source_form,
            'quote': quote,
        }
        return render(request, 'quote_update.html', context)

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