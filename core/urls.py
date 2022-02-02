from django.conf.urls import include, url
from django.urls import path
from .views import CustomAuthToken, ProductSoldViewSet, ProductViewSet, SellerViewSet, ClientViewSet, UserViewSet, generate_report_view
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'client', ClientViewSet)
router.register(r'seller', SellerViewSet)
router.register(r'product', ProductViewSet)
router.register(r'product-sold', ProductSoldViewSet)

urlpatterns = [
    path('auth/', CustomAuthToken.as_view()),
    url(r'^generate-flow-report/?$', generate_report_view),
    path('', include(router.urls)),
]
