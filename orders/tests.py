from django.test import TestCase, Client
from django.conf import settings
from pathlib import Path
from django.core.files.uploadedfile import SimpleUploadedFile, UploadedFile

from details.models import Detail
from .models import Order

static_url = settings.STATIC_URL

class OrderTestCase(TestCase):
	def setUp(self):
		self.static_url = Path(__file__).resolve().parent.parent.joinpath('static')
		self.client = Client()

	def test_verify_tracking_code(self):

		payed_image = SimpleUploadedFile('logo.png', b'file_content')
		print(payed_image)
		form_data = {
			'payed_image': payed_image,
			'type_ticket': 'BOLETA',
			'business_name': '',
			'ruc': '',
		}
		response = self.client.post('/orders/payment/', form_data)
		print(response)
		# print(Detail.objects.last())
