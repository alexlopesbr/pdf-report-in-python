from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes

from .models import *
from .serializers import *
from .services import generate_report

from django.views.decorators.csrf import csrf_exempt


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key
        })


def delete(self, request, pk, format=None):
    user_delete = User.objects.filter(pk)
    user_delete.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)


def put(self, request, pk, format=None):
    editing_user = User.objects(pk)
    serializer = UserSerializer(editing_user, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductSoldViewSet(viewsets.ModelViewSet):
    queryset = ProductSold.objects.all()
    serializer_class = ProductSoldSerializer


@ csrf_exempt
@ api_view(['GET'])
@ permission_classes([IsAuthenticated])
def generate_report_view(request):
    return generate_report(request)
