from django.db.models import Count
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models.order import Order, OrderItem


@api_view(['GET'])
def get_orders_by_status(request):
    result = Order.objects.raw("""
        SELECT 1 id, COUNT(*) as count, status as status 
        FROM shop_managment_order 
        GROUP BY status""")
    return Response([ dict(count=order.count, status=order.status) for order in result ])


@api_view(['GET'])
def get_orders_by_date(request):
    result = Order.objects.raw("""
        SELECT 1 id, COUNT(*) as count, extract(month from created_at) as month 
        FROM shop_managment_order 
        GROUP BY extract(month from created_at)""")
    return Response([ dict(count=order.count, month=order.month) for order in result ])


@api_view(['GET'])
def get_income_by_month(request):
    result = OrderItem.objects.raw("""
        SELECT 1 id, SUM(price * quantity) as price, extract(month from created_at) as month 
        FROM shop_managment_orderItem
        GROUP BY extract(month from created_at)""")
    return Response([ dict(price=order.price, month=order.month) for order in result ])
