from django.contrib.auth import login as django_login, \
    logout as django_logout, authenticate
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.translation import ugettext_lazy as _

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED

from .serializers import LoginSerializer
from .utils import ajax_redirect_to_login


sensitive_password = method_decorator(sensitive_post_parameters('password'))


class LoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    @sensitive_password
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(request, **serializer.validated_data)

        if user is None or not user.is_active:
            return Response(
                {
                    'status': 'error',
                    'error': 'Неверное имя пользователя или пароль!'
                },
                status=HTTP_401_UNAUTHORIZED
            )

        django_login(request, user)
        return Response({'status': 'ok'})


class LogoutView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        django_logout(request)
        return ajax_redirect_to_login()
