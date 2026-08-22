from django import template
from core.currency import convert_currency

register = template.Library()

@register.filter(name='convert')
def convert(amount, user):
    """
    Usage: {{ trip.cost|convert:request.user }}
    Returns formatted string with currency symbol.
    """
    if not amount:
        amount = 0
        
    try:
        amount = float(amount)
    except (ValueError, TypeError):
        return str(amount)
        
    target_currency = 'USD'
    symbol = '$'
    
    if user and hasattr(user, 'userprofile'):
        target_currency = user.userprofile.currency
        
    # Define symbols
    symbols = {
        'USD': '$',
        'EUR': '€',
        'GBP': '£',
        'INR': '₹',
        'JPY': '¥',
        'AUD': 'A$',
        'CAD': 'C$',
    }
    symbol = symbols.get(target_currency, '$')
    
    # We assume base stored amounts are in USD for this prototype
    # If the user's currency is not USD, convert it.
    converted = convert_currency(amount, 'USD', target_currency)
    
    # Format nicely
    if converted >= 1000:
        return f"{symbol}{converted:,.0f}"
    return f"{symbol}{converted:,.2f}"
