from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.utils.translation import gettext_lazy as _
from django.db.models import F, Sum
from django.core.exceptions import ValidationError


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/")


class CartItem(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, db_index=True)
    session_key = models.CharField(max_length=40, blank=True, null=True, db_index=True)  # Добавлено null=True

    class Meta:
        unique_together = ('product', 'user', 'session_key')

    def get_total_price(self):
        """Calculate the total price for this cart item."""
        return self.product.price * Decimal(self.quantity)

    @classmethod
    def get_cart(cls, user=None, session_key=None):
        """Fetch all cart items for a user or session."""
        if user:
            return cls.objects.filter(user=user)
        elif session_key:
            return cls.objects.filter(session_key=session_key)
        return cls.objects.none()

    @classmethod
    def get_total_cart_price(cls, user=None, session_key=None):
        """Calculate total price for all items in the cart."""
        cart_items = cls.get_cart(user=user, session_key=session_key).annotate(
            total_price=F('quantity') * F('product__price')
        )
        return cart_items.aggregate(total=Sum('total_price'))['total'] or Decimal('0.00')

    def increment_quantity(self, amount=1):
        """Increment the quantity of the item."""
        self.quantity += amount
        self.save()

    @classmethod
    def add_to_cart(cls, product, user=None, session_key=None, amount=1):
        """
        Add a product to the cart or increment its quantity if it already exists.
        """
        try:
            cart_item, created = cls.objects.get_or_create(
                product=product,
                user=user if user else None,
                session_key=session_key if not user else None,
            )
            if not created:
                cart_item.increment_quantity(amount)
            return cart_item
        except ValidationError:
            return None

    def clean(self):
        """Validate that either user or session_key is set."""
        if not self.user and not self.session_key:
            raise ValidationError("CartItem must have either a user or a session key.")

    def __str__(self):
        return f"CartItem: {self.product.name} (Quantity: {self.quantity}, User: {self.user or 'Guest'})"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username if self.user else 'Guest'}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"OrderItem: {self.product.name} (x{self.quantity})"
