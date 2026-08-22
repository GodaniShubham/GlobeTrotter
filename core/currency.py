import requests
from django.core.cache import cache

def get_exchange_rates(base='USD'):
    """Fetch exchange rates from Frankfurter API and cache them for 24h"""
    cache_key = f'exchange_rates_{base}'
    rates = cache.get(cache_key)
    
    if not rates:
        try:
            # Frankfurter API
            response = requests.get(f'https://api.frankfurter.app/latest?from={base}')
            if response.status_code == 200:
                data = response.json()
                rates = data.get('rates', {})
                # Cache for 24 hours
                cache.set(cache_key, rates, 86400)
            else:
                rates = {}
        except requests.RequestException:
            rates = {}
            
    # Always include the base currency as 1.0
    rates[base] = 1.0
    return rates

def convert_currency(amount, from_currency, to_currency):
    """Convert amount from one currency to another"""
    if from_currency == to_currency:
        return amount
        
    # Get rates relative to from_currency
    rates = get_exchange_rates(base=from_currency)
    rate = rates.get(to_currency)
    
    if rate:
        return amount * rate
        
    # Fallback if direct conversion fails (route through EUR)
    if from_currency != 'EUR' and to_currency != 'EUR':
        rates_from_eur = get_exchange_rates(base='EUR')
        rate_from = rates_from_eur.get(from_currency)
        rate_to = rates_from_eur.get(to_currency)
        
        if rate_from and rate_to:
            amount_in_eur = amount / rate_from
            return amount_in_eur * rate_to
            
    return amount # fallback to original amount if conversion fails
