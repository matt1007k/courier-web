from addresses.models import Address
from clients.models import Client
from orders.models import Order
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from details.models import UnassignOriginAddress, Detail

class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "slug",
            "full_name",
            "cell_phone",
            "driver_code",
            "store_name",
            "logo",
            "social_media",
            "user"
        ]

        def full_name(self):
            return self.model.full_name()

class OrderSerializer(ModelSerializer):
    client = ClientSerializer()
    class Meta:
        model = Order
        fields = [
            "id",
            "client",
            "status",
            "total",
            "type_ticket",
            "payed_image",
            "igv",
            "sub_total",
            "promo_code",
        ]


class AddressSerializer(ModelSerializer):
    client = ClientSerializer()
    class Meta:
        model = Address
        fields = [
            "id",
            "full_name",
            "email",
            "cell_phone",
            "address",
            "district",
            "city",
            "reference",
            "address_detail",
            "address_gps",
            "default",
            "client",
            "address_city",
            "address_complete"
        ]
        def address_city(self):
            return self.model.address_city()

        def address_complete(self):
            return self.model.address_complete()

class DetailSerializer(ModelSerializer):
    order = OrderSerializer()
    address_origin = AddressSerializer()
    address_destiny = AddressSerializer()

    class Meta:
        model = Detail
        fields = [
            'id',
            "tracking_code",
            'size',
            'contain',
            'value',
            'image',
            'description',
            'distance',
            'price_rate',
            'status',
            'order',
            'address_origin',
            'address_destiny',
            'get_created_at_format',
            'get_tracking_code_text',
        ]

        def get_tracking_code_text(self):
            return self.model.get_tracking_code_text()

        def get_created_at_format(self):
            return self.model.get_created_at_format()


class UnAssignOrignAddressSerializer(ModelSerializer):
    detail = DetailSerializer(read_only=True)
    class Meta:
        model = UnassignOriginAddress
        fields = [
            'detail'
        ]