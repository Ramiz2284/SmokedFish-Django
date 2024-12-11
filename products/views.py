from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, CartItem, Order
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _, ngettext
import json


def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})


def homepage(request):
    featured_products = Product.objects.filter(available=True)[:3]
    return render(request, 'products/homepage.html', {'featured_products': featured_products})


def get_cart_items(request):
    """Get cart items for authenticated user or session."""
    if request.user.is_authenticated:
        return CartItem.objects.filter(user=request.user)
    elif request.session.session_key:
        return CartItem.objects.filter(session_key=request.session.session_key)
    return CartItem.objects.none()


def cart(request):
    cart_items = get_cart_items(request)
    total_price = sum(item.get_total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


import logging

logger = logging.getLogger(__name__)

def add_to_cart(request, product_id):
    if request.method == 'POST':
        try:
            # Получаем продукт или возвращаем 404, если его нет
            product = get_object_or_404(Product, id=product_id)
            session_key = None

            # Если пользователь не авторизован, используем session_key
            if not request.user.is_authenticated:
                if not request.session.session_key:
                    request.session.create()  # Создаём сессию
                session_key = request.session.session_key

            # Добавляем товар в корзину
            cart_item = CartItem.add_to_cart(
                product=product,
                user=request.user if request.user.is_authenticated else None,
                session_key=session_key,
            )

            if cart_item:
                # Успешный ответ
                cart_count = CartItem.get_cart(user=request.user, session_key=session_key).count()
                return JsonResponse({'success': True, 'cart_count': cart_count})
            else:
                # Если по какой-то причине объект не создан
                logger.error("Failed to add item to cart. Product ID: %s", product_id)
                return JsonResponse({'success': False, 'message': 'Failed to add item to cart.'})
        except Exception as e:
            # Логируем ошибки и возвращаем ответ
            logger.exception("Error adding product to cart. Product ID: %s", product_id)
            return JsonResponse({'success': False, 'message': str(e)})

    # Неверный метод запроса
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})






def update_cart_quantity(request, item_id):
    if request.method == 'POST':
        try:
            cart_item = get_object_or_404(CartItem, id=item_id)
            # Преобразуем тело запроса в JSON
            data = json.loads(request.body)
            # Получаем количество и преобразуем в целое число
            new_quantity = int(data.get('quantity', 1))

            if new_quantity < 1:  # Проверяем, что количество корректное
                return JsonResponse({'success': False, 'message': 'Quantity must be at least 1.'})

            cart_item.quantity = new_quantity
            cart_item.save()

            total_price = sum(item.get_total_price() for item in CartItem.objects.filter(user=request.user))

            return JsonResponse({
                'success': True,
                'total_price': total_price,
                'item_total_price': cart_item.get_total_price()
            })
        except ValueError as e:
            return JsonResponse({'success': False, 'message': 'Invalid quantity value.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})



def remove_from_cart(request, cart_item_id):
    if request.method == 'POST':
        try:
            cart_item = get_object_or_404(CartItem, id=cart_item_id)
            cart_item.delete()

            # Пересчёт общей суммы корзины
            total_price = sum(item.get_total_price() for item in get_cart_items(request))

            return JsonResponse({'success': True, 'total_price': total_price})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def clear_cart(request):
    if request.method == 'POST':
        try:
            if request.user.is_authenticated:
                CartItem.objects.filter(user=request.user).delete()
            else:
                CartItem.objects.filter(session_key=request.session.session_key).delete()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def checkout(request):
    cart_items = get_cart_items(request)
    total_price = sum(item.get_total_price() for item in cart_items)
    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def order_confirm(request):
    cart_items = get_cart_items(request)
    if not cart_items:
        return JsonResponse({'success': False, 'message': _('Your cart is empty.')})

    total_price = sum(item.get_total_price() for item in cart_items)
    order = Order.objects.create(user=request.user, total_price=total_price)

    # Optionally move cart items to order
    for item in cart_items:
        order.items.create(product=item.product, quantity=item.quantity, price=item.product.price)
    cart_items.delete()

    return render(request, 'order_confirm.html', {'order': order})


def calculate_delivery(request):
    city = request.POST.get('city')
    delivery_price = 100 if city == 'Antalya' else 200
    return JsonResponse({'delivery_price': delivery_price})


# Example usage of translation functions
message = _("Hello, world!")
count = 5
message_plural = ngettext(
    '%(count)d item',
    '%(count)d items',
    count
) % {'count': count}
