from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer, UserProfileSerializer, BalanceTopUpSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class BalanceTopUpView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BalanceTopUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        user.balance += serializer.validated_data['amount']
        user.save()
        
        return Response(
            {"message": "Баланс успешно пополнен", "new_balance": user.balance},
            status=status.HTTP_200_OK
        )
