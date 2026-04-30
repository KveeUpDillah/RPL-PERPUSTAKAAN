from django.contrib import admin
from .models import Wishlist, SearchHistory, AIRecommendation

admin.site.register(Wishlist)
admin.site.register(SearchHistory)
admin.site.register(AIRecommendation)