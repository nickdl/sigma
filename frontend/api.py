from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle
from datetime import timedelta
from ticks.models import Tick


INTERVALS = {
    '1h': 1,
    '6h': 6,
    '24h': 24,
    '72h': 72,
}
DECIMALS = 6


class TickList(ViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    throttle_classes = (AnonRateThrottle,)

    def list(self, request):
        interval = request.query_params.get('interval', None)
        symbol = request.query_params.get('symbol', None)
        if interval is not None and INTERVALS.get(interval):
            start = timezone.now() - timedelta(hours=INTERVALS.get(interval))
        else:
            start = timezone.now() - timedelta(hours=INTERVALS.get('24h'))
        symbols = [symbol] if symbol in settings.SYMBOLS else settings.SYMBOLS

        result = []
        for symbol in symbols:
            data = Tick.objects\
                .filter(symbol=symbol, date__gte=start)\
                .order_by('date').values_list('close', flat=True)
            rounded = map(lambda x: round(x, DECIMALS), data)
            result.append({'symbol': symbol, 'data': rounded})
        return Response(result)


class Logout(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    throttle_classes = (AnonRateThrottle,)

    queryset = get_user_model().objects.all()

    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class ValidToken(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    throttle_classes = (AnonRateThrottle,)

    def post(self, request, format=None):
        return Response(status=status.HTTP_200_OK)
