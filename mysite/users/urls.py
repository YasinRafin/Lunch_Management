from django.urls import path
from .views import add_to_cart, view_cart, remove_from_cart,process_checkout,order_summary,user_orders

app_name = 'users'  # Namespacing the URL names for clarity

urlpatterns = [
    path('add_to_cart/<int:item_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('remove_from_cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('process_checkout/',process_checkout,name='process_checkout'),
    path('order_summary/<int:order_id>/', order_summary, name='order_summary'),
    path('orders/', user_orders, name='user_orders'),
]