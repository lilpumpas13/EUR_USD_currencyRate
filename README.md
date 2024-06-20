# EUR_USD_currencyRate
Expose an endpoint displaying the currency rate of USD against EUR

Final version

docker pull lilpumpas13/currency_rate_diogo_campos:3.10.4

docker run -d -p 8000:8000 currency_rate_diogo_campos:3.10.4

http://localhost:8000/currencyRateApp/usd-to-eur -> no specified start_date or end_date

http://localhost:8000/currencyRateApp/usd-to-eur/?start_date=2024-01-01&end_date=2024-01-10 -> example for date range from 2024-01-01 to 2024-01-10
