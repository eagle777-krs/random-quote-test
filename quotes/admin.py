from django.contrib import admin
from .models import Quote, Source, Author

admin.site.register(Source)
admin.site.register(Quote)
admin.site.register(Author)
