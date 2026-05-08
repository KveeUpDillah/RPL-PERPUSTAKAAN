from django.contrib import admin
from .models import Wishlist, LoginHistory, SearchHistory, AIRecommendation

admin.site.register(Wishlist)
admin.site.register(LoginHistory)
admin.site.register(SearchHistory)
admin.site.register(AIRecommendation)