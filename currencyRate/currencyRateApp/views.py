from django.http import JsonResponse
import requests
from datetime import date
from .models import ExchangeRate
from django.utils.dateparse import parse_date

def fetch_and_store_latest_rate():
    response = requests.get(f'https://api.frankfurter.app/latest?from=USD&to=EUR')
    data = response.json()
    rate = data['rates']['EUR']
    exchange_rate, created = ExchangeRate.objects.get_or_create(date=date.today(), defaults={'rate': rate})
    return rate   

def fetch_and_store_historical_rate(query_date):
    response = requests.get(f'https://api.frankfurter.app/{query_date}?from=USD&to=EUR')
    data = response.json()
    rate = data['rates']['EUR']
    exchange_rate, created = ExchangeRate.objects.get_or_create(date=query_date, defaults={'rate': rate})
    return exchange_rate.rate  

def get_usd_to_eur_rate(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    single_date = request.GET.get('date')

    # if no date is specified -> expose latest currency rate
    if not start_date and not end_date and not single_date:
        try:
            fetch_and_store_latest_rate()
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    # if a single date is specified -> expose currency rate of specified date
    elif not start_date and not end_date and single_date:
        single_date = parse_date(single_date)

        if not single_date:
            return JsonResponse({'error': 'Invalid format. Use YYYY-MM-DD.'}, status=400)
        
        fetch_and_store_historical_rate(single_date)

