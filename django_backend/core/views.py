from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Charger, Transaction, StatusLog
from .serializers import ChargerSerializer, TransactionSerializer, StatusLogSerializer

class ChargerViewSet(viewsets.ModelViewSet):
    queryset = Charger.objects.all()
    serializer_class = ChargerSerializer
    permission_classes = [AllowAny]

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [AllowAny]

class StatusLogViewSet(viewsets.ModelViewSet):
    queryset = StatusLog.objects.all()
    serializer_class = StatusLogSerializer
    permission_classes = [AllowAny]
