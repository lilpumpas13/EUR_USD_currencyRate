from django.http import JsonResponse
import requests

def get_usd_to_eur_rate(request):
    try:
        response = requests.get('https://api.frankfurter.app//latest?from=USD&to=EUR')
        data = response.json()
        rate = data['rates']['EUR']
        return JsonResponse({'USD_EUR': rate})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)