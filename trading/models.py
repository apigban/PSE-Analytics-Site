from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import date

class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    amount = models.PositiveIntegerField(default=0)
    today_price = models.PositiveIntegerField(default=0)
    company = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.symbol

class Portfolio(models.Model):
    folio_name = models.CharField(max_length=20, unique=True)
    stock_list = models.ManyToManyField(Stock, through='StockPortfolioJunction')

    def __str__(self):
        return self.folio_name

class StockPortfolioJunction(models.Model):
    stocks = models.ForeignKey(Stock, on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    created = models.DateField(editable=False)
    modified = models.DateField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(StockPortfolioJunction, self).save(*args, **kwargs)

class StockPrice(models.Model):
    price_date = models.DateField(default=date.today)
    symbol = models.ForeignKey(Stock, related_name="price_history", on_delete=models.CASCADE)
    price_open = models.IntegerField(default=0)
    price_high = models.IntegerField(default=0)
    price_low = models.IntegerField(default=0)
    price_close = models.IntegerField(default=0)
    volume = models.BigIntegerField(default=0)


    def comp_id(self):
        return ''.join((self.symbol, self.price_date))

    def __str__(self):
        return self.symbol

    class Meta:
        unique_together = ('symbol', 'price_date')

