from .models import CartItem

def cart_count(request):
    session_key = request.session.session_key
    if not session_key:
        return {'cart_count': 0}

    user = request.user if request.user.is_authenticated else None
    cart_items = CartItem.get_cart(user=user, session_key=session_key)
    return {'cart_count': cart_items.count()}
