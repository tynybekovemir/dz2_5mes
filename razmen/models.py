from django.db import models

# Create your models here.


from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    geek_coins = models.PositiveIntegerField(default=0)

class Transaction(models.Model):
    sender = models.ForeignKey(UserProfile, related_name='sent_transactions', on_delete=models.CASCADE)
    recipient = models.ForeignKey(UserProfile, related_name='received_transactions', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

# serializers.py
from rest_framework import serializers

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('user', 'geek_coins')

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('sender', 'recipient', 'amount', 'timestamp')

# views.py
from rest_framework import generics, permissions
from .models import UserProfile, Transaction
from .serializers import UserProfileSerializer, TransactionSerializer

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.userprofile

class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user.userprofile
        return Transaction.objects.filter(Q(sender=user) | Q(recipient=user))

class CoinTransferView(generics.CreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        sender = self.request.user.userprofile
        recipient_username = self.request.data.get('recipient_username')
        recipient = UserProfile.objects.get(user__username=recipient_username)
        amount = int(self.request.data.get('amount'))

        if sender.geek_coins >= amount:
            sender.geek_coins -= amount
            recipient.geek_coins += amount
            sender.save()
            recipient.save()
            serializer.save(sender=sender, recipient=recipient, amount=amount)
        else:
            raise serializers.ValidationError("Not enough Geek Coins.")

# urls.py
from django.urls import path
from .views import UserProfileView, TransactionListView, CoinTransferView

urlpatterns = [
    path('api/users/profile/', UserProfileView.as_view(), name='user-profile'),
    path('api/transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('api/coins/transfer/', CoinTransferView.as_view(), name='coin-transfer'),
]
