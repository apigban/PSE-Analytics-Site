from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django_tables2 import RequestConfig
from .forms import StockSearchForm, StockPicker_multiselect, StockPicker_name, PortfolioPicker_select
from .models import Stock, Portfolio, StockPortfolioJunction
from users.models import ProfilePortfolioJunction
from .tables import StockTable


@login_required
def home(request):
    if request.method == "POST":
        # Create a form instance with POST data.
        portfolio_name_form = StockPicker_name(request.POST)
        stock_picker_form = StockPicker_multiselect(request.POST)

        if portfolio_name_form.is_valid() and stock_picker_form.is_valid():

            #   Create, but don't save a new portfolio instance
            new_portfolio = portfolio_name_form.save(commit=False)

            #   Modify the portfolio in some way.
            #   new_porfolio.some_field = 'some_value'

            #   Save the new instance.
            new_portfolio.save()
            new_portfolio.refresh_from_db()

            #   Create and iterable from the 'picked' stocks
            clean_stock_picker_form = stock_picker_form.cleaned_data['stock_list']

            #   For every item in picked stocks, create a stock instance based on item
            #   obtain the stock's PK
            #   set the PK as the argument for
            #   creating a new row in the Junction Table
            for item in clean_stock_picker_form:
                #   get stock pk from Stock Model
                stock = Stock.objects.get(symbol=item)

                #   create portfolio instance
                portfolio_instance = StockPortfolioJunction(portfolio_id=new_portfolio.id, stocks_id=stock.id)
                portfolio_instance.save()

            return redirect('trading-home')

    else:
        portfolio_name_form = StockPicker_name()
        stock_picker_form = StockPicker_multiselect()

    stocks_table = StockTable(Stock.objects.all())
    RequestConfig(request).configure(stocks_table)

    context = {
        'table': stocks_table,
        'form_dropdown': stock_picker_form,
        'portfolio_name': portfolio_name_form,
    }

    return render(request, 'trading/home.html', context)


@login_required
def porfolio_management(request):
    if request.method == "POST":
        # Create a form instance with POST data.
        portfolio_name_form = StockPicker_name(request.POST)
        stock_picker_form = StockPicker_multiselect(request.POST)

        portfolio_picker_form = PortfolioPicker_select(request.POST, user_id=request.user.id)

        if portfolio_name_form.is_valid() and stock_picker_form.is_valid():

            #   Create, but don't save a new portfolio instance
            new_portfolio = portfolio_name_form.save(commit=False)

            #   Modify the portfolio in some way.
            #   new_porfolio.some_field = 'some_value'

            #   Save the new instance.
            new_portfolio.save()
            new_portfolio.refresh_from_db()

            #   Create an entry to ProfilePorfolioJunction table

            profile_portfolio_link = ProfilePortfolioJunction(owners_id=request.user.id, folio_id=new_portfolio.id)
            profile_portfolio_link.save()

            #   Create and iterable from the 'picked' stocks
            clean_stock_picker_form = stock_picker_form.cleaned_data['stock_list']

            #   For every item in picked stocks, create a stock instance based on item
            #   obtain the stock's PK
            #   set the PK as the argument for
            #   creating a new row in the Junction Table
            for item in clean_stock_picker_form:
                #   get stock pk from Stock Model
                stock = Stock.objects.get(symbol=item)

                #   create portfolio instance
                portfolio_instance = StockPortfolioJunction(portfolio_id=new_portfolio.id, stocks_id=stock.id)
                portfolio_instance.save()

            return redirect('trading-home')
    else:
        portfolio_name_form = StockPicker_name()
        stock_picker_form = StockPicker_multiselect()
        portfolio_picker_form = PortfolioPicker_select(user_id=request.user.id)
        print('WENT HERE TOO')

    context = {
        'stock_multiselect': stock_picker_form,
        'new_portfolio_name': portfolio_name_form,
        'porfolio_select': portfolio_picker_form,
    }

    return render(request, 'trading/portfolio_management.html', context)


def about(request):
    return render(request, 'trading/about.html')


def search(request):
    s_form = StockSearchForm(request.POST)

    context = {
        's_form': s_form,
    }

    return render(request, 'trading/search.html', context)
