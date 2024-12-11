from django.contrib import admin
from django.urls import path, include
from products import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

# Основные маршруты
urlpatterns = [
    path('admin/', admin.site.urls),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('order/confirm/', views.order_confirm, name='order_confirm'),
    
    path('update-cart/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('set_language/', include('django.conf.urls.i18n')),  # Поддержка смены языка
]

# Мультиязычные маршруты
urlpatterns += i18n_patterns(
    path('', views.homepage, name='homepage'),
    path('products/', views.product_list, name='product_list'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
)

# Статические и медиафайлы (в режиме разработки)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
