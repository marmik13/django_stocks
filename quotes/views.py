from django.shortcuts import render, redirect
from django.contrib import messages
from . forms import StockForm
from . models import Stock
import requests
import json
# Create your views here.


def home(request):
    # pk_7d026f8ec9ab49e9ae8e0996431699fe
    if request.method == "POST":
        ticker = request.POST.get('ticker')
        api_request = requests.get(
            "https://cloud.iexapis.com/stable/stock/"+ticker+"/quote?token=pk_7d026f8ec9ab49e9ae8e0996431699fe")

        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."
        return render(request, 'home.html', {'api': api})

    else:
        return render(request, 'home.html', {'ticker': "Enter a ticker symbol in above text box to get the stock details."})


def about(request):
    return render(request, 'about.html')


def add_stock(request):
    if request.method == "POST":
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ("Stock has been added."))
            return redirect('add_stock')
    else:
        ticker = Stock.objects.all()
        result_list = []
        for ticker_item in ticker:
            api_request = requests.get(
                "https://cloud.iexapis.com/stable/stock/"+str(ticker_item)+"/quote?token=pk_7d026f8ec9ab49e9ae8e0996431699fe")

            try:
                api = json.loads(api_request.content)
                result_list.append(api)
            except Exception as e:
                api = "Error..."
        return render(request, 'add_stock.html', {'ticker': ticker, 'ticker_list': result_list})


def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock has been deleted."))
    return redirect(delete_stock)


def delete_stock(request):
    ticker = Stock.objects.all()
    result_list = []
    for ticker_item in ticker:
        api_request = requests.get(
            "https://cloud.iexapis.com/stable/stock/"+str(ticker_item)+"/quote?token=pk_7d026f8ec9ab49e9ae8e0996431699fe")

        try:
            api = json.loads(api_request.content)
            result_list.append([api['companyName'], ticker_item.id])
        except Exception as e:
            api = "Error..."
    print(result_list)
    return render(request, 'delete_stock.html', {'ticker': ticker, 'ticker_list': result_list})
