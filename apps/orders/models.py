from django.db import models
from django.conf import settings
from products.models import Product

class CartItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='cart_items',
        verbose_name="Пользователь"
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='cart_entries',
        verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    class Meta:
        db_table = 'cart_items'
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} — {self.product.name} ({self.quantity})"


class Order(models.Model):
    STATUS_CHOICES = [
        ('CREATED', 'Создан'),
        ('PAID', 'Оплачен'),
        ('FAILED', 'Ошибка'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT, 
        related_name='orders',
        verbose_name="Пользователь"
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая стоимость")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CREATED', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        db_table = 'orders'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ №{self.id} от {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='items',
        verbose_name="Заказ"
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='order_entries',
        verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена на момент покупки")

    class Meta:
        db_table = 'order_items'
        verbose_name = 'Товар заказа'
        verbose_name_plural = 'Товары заказа'

    def __str__(self):
        return f"{self.product.name if self.product else 'Удаленный товар'} x {self.quantity}"
