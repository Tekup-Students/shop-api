from django.db.models import Count
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models.order import Order


@api_view(['GET'])
def get_orders_by_status(request):
    return Response(Order.objects.values('status').annotate(count=Count('status')))


@api_view(['GET'])
def get_orders_by_date(request):
    return Response(Order.objects.values('created_at__month').annotate(count=Count('created_at__month')))


@api_view(['GET'])
def get_income_by_month(request):
    return Response(Order.objects.values('total_cost').annotate(count=Count('created_at__month')))
