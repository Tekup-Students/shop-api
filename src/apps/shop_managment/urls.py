from django.urls import path

from .views import stats_views, order_views, product_views, category_views

urlpatterns = [
    path(r'orders', order_views.OrderCreateAPIView.as_view()),
    path(r'my-orders', order_views.MyOrdersAPIView.as_view()),
    path(r'orders/all', order_views.AllOrderListAPIView.as_view()),
    path(r'orders/<int:pk>', order_views.OrderUpdateAPIView.as_view()),
    path(r'orders/<int:pk>/deactivate', order_views.OrderDeactivateAPIView.as_view()),
    path(r'orders/<int:pk>/activate', order_views.OrderActivateAPIView.as_view()),

    path(r'products', product_views.ProductCreateAPIView.as_view()),
    path(r'products/all', product_views.AllProductListAPIView.as_view()),
    path(r'products/<int:pk>', product_views.ProductUpdateAPIView.as_view()),
    path(r'products/<int:pk>/deactivate', product_views.ProductDeactivateAPIView.as_view()),
    path(r'products/<int:pk>/activate', product_views.ProductActivateAPIView.as_view()),

    # Category
    path(r'categories', category_views.CategoryCreateAPIView.as_view()),
    path(r'categories/all', category_views.AllCategoryListAPIView.as_view()),
    path(r'categories/<int:pk>', category_views.CategoryUpdateAPIView.as_view()),
    path(r'categories/<int:pk>/deactivate', category_views.CategoryDeactivateAPIView.as_view()),
    path(r'categories/<int:pk>/activate', category_views.CategoryActivateAPIView.as_view()),    

    path(r'orders-count-by-date', stats_views.get_orders_by_date),
    path(r'orders-count-by-status', stats_views.get_orders_by_status),
    path(r'orders-income-by-date', stats_views.get_income_by_month),
 ]
