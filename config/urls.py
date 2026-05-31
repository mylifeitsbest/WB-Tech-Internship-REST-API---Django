from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import RegisterView, ProfileView, BalanceTopUpView
from products.views import ProductViewSet
from orders.views import CartViewSet, OrderCreateAPIView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'cart', CartViewSet, basename='cart')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    path('api/users/register/', RegisterView.as_view(), name='auth_register'),
    path('api/users/profile/', ProfileView.as_view(), name='user_profile'),
    path('api/users/balance/topup/', BalanceTopUpView.as_view(), name='balance_topup'),
    
    path('api/orders/create/', OrderCreateAPIView.as_view(), name='order_create'),
    
    path('api/', include(router.urls)),
]
