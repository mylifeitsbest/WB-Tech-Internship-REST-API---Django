from decimal import Decimal
from django.test import TestCase
from rest_framework.exceptions import ValidationError
from apps.users.models import User
from apps.products.models import Product
from apps.orders.models import CartItem, Order
from apps.orders.services import OrderService

class OrderServiceTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_buyer",
            password="secure_password_123",
            balance=Decimal("5000.00")
        )
        
        self.product_1 = Product.objects.create(
            name="Ноутбук",
            description="Игровой ноутбук",
            price=Decimal("4000.00"),
            stock=5
        )
        self.product_2 = Product.objects.create(
            name="Мышка",
            description="Беспроводная мышь",
            price=Decimal("1500.00"),
            stock=10
        )

    def test_successful_order_creation(self):
        CartItem.objects.create(user=self.user, product=self.product_1, quantity=1)

        order = OrderService.create_order_from_cart(self.user)

        self.assertIsInstance(order, Order)
        self.assertEqual(order.total_price, Decimal("4000.00"))
        
        self.user.refresh_from_db()
        self.assertEqual(self.user.balance, Decimal("1000.00"))

        self.product_1.refresh_from_db()
        self.assertEqual(self.product_1.stock, 4)

        self.assertFalse(CartItem.objects.filter(user=self.user).exists())

    def test_insufficient_funds_fails(self):
        CartItem.objects.create(user=self.user, product=self.product_1, quantity=2)

        with self.assertRaises(ValidationError) as context:
            OrderService.create_order_from_cart(self.user)
        
        self.assertIn("Недостаточно средств", str(context.exception))

        self.user.refresh_from_db()
        self.assertEqual(self.user.balance, Decimal("5000.00"))
        self.product_1.refresh_from_db()
        self.assertEqual(self.product_1.stock, 5)

    def test_insufficient_stock_fails(self):
        self.user.balance = Decimal("30000.00")
        self.user.save()
        CartItem.objects.create(user=self.user, product=self.product_1, quantity=6)

        with self.assertRaises(ValidationError) as context:
            OrderService.create_order_from_cart(self.user)

        self.assertIn("Недостаточно товара", str(context.exception))

        self.product_1.refresh_from_db()
        self.assertEqual(self.product_1.stock, 5)
