from rest_framework.routers import DefaultRouter

from welfarekata.webapp.views.api.account_view_set import AccountViewSet
from welfarekata.webapp.views.api.product_view_set import ProductViewSet
from welfarekata.webapp.views.api.purchase_view_set import PurchaseViewSet

app_name = 'webapp'

webapp_router_v1 = DefaultRouter()
webapp_router_v1.register(
    'accounts',
    AccountViewSet,
    basename='accounts',
)
webapp_router_v1.register(
    'products',
    ProductViewSet,
    basename='products',
)
webapp_router_v1.register(
    'purchases',
    PurchaseViewSet,
    basename='purchases',
)

urlpatterns = []
