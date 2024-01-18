from django.shortcuts import render

# Create your views here.
from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

class CoinBurnView(generics.CreateAPIView):
  
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        burn_unused_coins.apply_async(eta=timezone.now())
        return Response({'detail': 'Coin burning process started.'}, status=status.HTTP_200_OK)

