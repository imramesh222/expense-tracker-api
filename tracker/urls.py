from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, ExpenseIncomeViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import custom_api_root

router = DefaultRouter()
router.register(r'expenses', ExpenseIncomeViewSet, basename='expense')

urlpatterns = [
    path('', custom_api_root, name='api-root'),  # This must be first!
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]