import math
import json
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .serializers import DetailSerializer

from django.core.serializers import serialize

from .models import Detail


class DetailApiListView(APIView):
    permission_classes = [IsAuthenticated,]

    def query(self):
        return self.request.GET.get('q')

    def query_date(self):
        return self.request.GET.get('date')

    def query_status(self):
        return self.request.GET.get('status')

    def query_origin(self):
        return self.request.GET.get('origin')

    def query_destiny(self):
        return self.request.GET.get('destiny')

    def query_page(self):
        return self.request.GET.get('page', 1)

    def get(self, request):
        if request.user.is_client:
            qs = request.user.client.detail_set.exclude(tracking_code=None).order_by('-id')
        elif request.user.is_driver:
            clients = request.user.driver.get_clients()
            qs = Detail.objects.none()
            for client in clients:
                qs = qs | client.detail_set.exclude(tracking_code=None).order_by('-id')
        else:
            qs = Detail.objects.exclude(tracking_code=None).order_by('-id')
        
        qs = qs.search_detail_and_client(self.query()).search_by_address_origin(self.query_origin()).search_by_address_delivery(self.query_destiny()).search_by_status(self.query_status()).search_by_date(self.query_date())

        page = int(self.query_page())
        per_page = 10

        total = qs.count()
        start = (page - 1) * per_page
        end = page * per_page
        serializer = DetailSerializer(qs[start:end], many=True)

        return Response({
            'data': serializer.data,
            'total': total,
            'page': page,
            'per_page': per_page,
            'last_page': math.ceil(total / per_page),
            'start': start + 1,
            'end': end,
        })

class StatusDetailApiViewList(APIView):
    def get(self, request):
        status_detail = [{'label': status.label, 'status': status} for status in Detail.PackageStatus]
        return Response(status_detail)