# from invoice_manager.views import pos_view, create_invoice_from_pos

# urlpatterns = [
#     # ... your existing urls
#     path('pos/', pos_view, name='pos'),
#     path('pos/create/', create_invoice_from_pos, name='create_invoice_from_pos'),
# ]
# from django.urls import path
from django.urls import path
from .views import home, dashboard_view, pos_view, create_invoice_from_pos

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('pos/', pos_view, name='pos'),
    path('pos/create/', create_invoice_from_pos, name='create_invoice_from_pos'),
]
