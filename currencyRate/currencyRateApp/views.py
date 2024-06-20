from django.http import JsonResponse
import requests
from datetime import date, timedelta
from .models import ExchangeRate
from django.utils.dateparse import parse_date

def fetch_and_store_latest_rate():
    response = requests.get(f'https://api.frankfurter.app/latest?from=USD&to=EUR')
    data = response.json()
    rate = data['rates']['EUR']
    exchange_rate, created = ExchangeRate.objects.get_or_create(date=date.today(), defaults={'rate': rate})
    return exchange_rate.rate  

def fetch_and_store_historical_rate(query_date):
    response = requests.get(f'https://api.frankfurter.app/{query_date}?from=USD&to=EUR')
    data = response.json()
    rate = data['rates']['EUR']
    exchange_rate, created = ExchangeRate.objects.get_or_create(date=query_date, defaults={'rate': rate})
    return exchange_rate.rate  

def get_usd_to_eur_rate(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # if no date is specified -> expose latest currency rate
    if not request.GET:
        try:
            rate = fetch_and_store_latest_rate()
            return JsonResponse({'USD_EUR': rate})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    if start_date and end_date:
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)

            if not start_date or not end_date:
                return JsonResponse({'error': 'Invalid format. Use YYYY-MM-DD.'}, status=400)
                
            date_range = [start_date + timedelta(days=1) for i in range((end_date - start_date).days + 1)]
            rates = []

            for single_date in date_range:
                exchange_rate, created = ExchangeRate.objects.get_or_create(date=single_date)
                if not created:
                    try:
                        rate = fetch_and_store_historical_rate(single_date)
                    except Exception as e:
                        return JsonResponse({'error': str(e)}, status=500)
                rates.append(exchange_rate.rate)
                        
            if not rates:
                return JsonResponse({'error': 'No exchange rate data found for the given date range.'}, status=404)
            
            average_rate = sum(rates) / len(rates)
            return JsonResponse({'average_USD_EUR': average_rate})