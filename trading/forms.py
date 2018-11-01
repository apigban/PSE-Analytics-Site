from django import forms
from .models import Stock, Portfolio
from .validators import alphanumeric


class StockSearchForm(forms.Form):
    stock_search = forms.CharField(max_length=15, required=False, label='')

    # company = forms.CharField(max_length=20, required=False)
    class Meta:
        model = Stock
        fields = ['symbol', 'company']


class StockPicker_dropdown(forms.Form):
    stock_list = Stock.objects.only('symbol')


class StockPicker_multiselect(forms.Form):
    stock_list = forms.ModelMultipleChoiceField(label='Stock', queryset=Stock.objects.only('symbol'))


class StockPicker_name(forms.ModelForm):
    folio_name = forms.CharField(max_length=20,
                                 label='',
                                 validators=[alphanumeric],
                                 widget=forms.TextInput(attrs={'placeholder': 'Enter Portfolio Name Here'}))

    class Meta:
        model = Portfolio
        fields = ['folio_name']

