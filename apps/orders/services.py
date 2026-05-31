import logging
from django.db import transaction
from rest_framework.exceptions import ValidationError
from orders.models import CartItem, Order, OrderItem

logger = logging.getLogger('orders')

class OrderService:
    @staticmethod
    @transaction.atomic
    def create_order_from_cart(user):
        cart_items = CartItem.objects.filter(user=user).select_related('product')
        if not cart_items.exists():
            raise ValidationError("Корзина пуста")

        total_cost = 0
        items_to_process = []

        for item in cart_items:
            product = item.product
            product_refresh = product.__class__.objects.select_for_update().get(pk=product.pk)
            
            if product_refresh.stock < item.quantity:
                raise ValidationError(f"Недостаточно товара {product_refresh.name} на складе")
            
            total_cost += product_refresh.price * item.quantity
            items_to_process.append((item, product_refresh))

        user_db = user.__class__.objects.select_for_update().get(pk=user.pk)
        if user_db.balance < total_cost:
            raise ValidationError("Недостаточно средств на балансе")

        user_db.balance -= total_cost
        user_db.save()

        order = Order.objects.create(user=user_db, total_price=total_cost)

        for cart_item, product in items_to_process:
            product.stock -= cart_item.quantity
            product.save()

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=cart_item.quantity,
                price=product.price
            )

        cart_items.delete()

        logger.info(f"Заказ успешно создан. ID: {order.id}, Пользователь: {user_db.username}, Сумма: {total_cost}")
        
        return order
