from django.contrib import admin
from .models import Stock, Portfolio, StockPortfolioJunction

class StockPortfolioInline(admin.TabularInline):
    model = StockPortfolioJunction
    extra = 1

class StockAdmin(admin.ModelAdmin):
    inlines = (StockPortfolioInline,)

class PortfolioAdmin(admin.ModelAdmin):
    inlines = (StockPortfolioInline,)

admin.site.register(Stock, StockAdmin)
admin.site.register(Portfolio, PortfolioAdmin)