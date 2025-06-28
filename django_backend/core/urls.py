from rest_framework.routers import DefaultRouter
from .views import ChargerViewSet, TransactionViewSet, StatusLogViewSet

router = DefaultRouter()
router.register(r'chargers', ChargerViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'status-logs', StatusLogViewSet)

urlpatterns = router.urls
