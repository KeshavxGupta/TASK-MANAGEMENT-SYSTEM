from django import template
from django.db.models import Sum
from shop.models import Order

register = template.Library()

@register.filter
def filter_completed(orders):
    """Filter orders to only include completed ones."""
    return orders.filter(status='completed')

@register.filter
def get_completed_orders_count(user):
    return Order.objects.filter(user=user, status='completed').count()

@register.filter
def get_total_spent(user):
    total = Order.objects.filter(user=user, status='completed').aggregate(
        total=Sum('total')
    )['total'] or 0
    return total 