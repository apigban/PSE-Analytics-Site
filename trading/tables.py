# tutorial/tables.py
import django_tables2 as tables
from .models import Stock

class StockTable(tables.Table):
    class Meta:
        model = Stock
        template_name = 'django_tables2/bootstrap.html'