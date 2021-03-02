from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth import get_user_model

#from .send_mail import send_mail_on_frogot_password
from ..serializers.auth_serializers import ResetPasswordSerializer, ForgotPasswordSerializer\
    ,UserLoginSerializer, RegisterSerializer

User = get_user_model()


class TokenViewBase(generics.GenericAPIView):
    permission_classes = ()
    authentication_classes = ()

    serializer_class = None

    www_authenticate_realm = 'api'

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request, 'kwargs': kwargs})

        #try:
        serializer.is_valid(raise_exception=True)
        #except TokenError as e:
        #    raise InvalidToken(e.args[0])

        if serializer.validated_data:
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class ForgotPasswordAPIView(TokenViewBase):
    serializer_class = ForgotPasswordSerializer

class ResetPasswordAPIView(TokenViewBase):
    serializer_class = ResetPasswordSerializer

class JWTLoginView(TokenObtainPairView):
    queryset = User.objects.filter(profile__deleted_at__isnull=True)
    serializer_class = UserLoginSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
