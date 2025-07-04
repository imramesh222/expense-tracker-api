from rest_framework import generics, viewsets, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import ExpenseIncome
from .serializers import UserRegisterSerializer, ExpenseIncomeSerializer
from .permissions import IsOwnerOrSuperuser
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

class ExpenseIncomeViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseIncomeSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrSuperuser]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return ExpenseIncome.objects.all().order_by('-created_at')
        return ExpenseIncome.objects.filter(user=user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@api_view(['GET'])
def custom_api_root(request, format=None):
    return Response({
        'register': reverse('register', request=request, format=format),
        'login': reverse('token_obtain_pair', request=request, format=format),
        'refresh': reverse('token_refresh', request=request, format=format),
        'expenses': reverse('expense-list', request=request, format=format),
    })