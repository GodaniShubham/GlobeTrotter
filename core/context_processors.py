def currency_processor(request):
    currency = 'USD'
    if request.user.is_authenticated and hasattr(request.user, 'userprofile'):
        currency = request.user.userprofile.currency
    
    symbols = {
        'USD': '$',
        'EUR': '€',
        'GBP': '£',
        'INR': '₹',
        'JPY': '¥',
        'AUD': 'A$',
        'CAD': 'C$',
    }
    return {
        'user_currency': currency,
        'user_currency_symbol': symbols.get(currency, '$')
    }
