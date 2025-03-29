from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView
from invoices.models import Invoice, InvoiceItem
from invoices.serializers import InvoiceSerializer, InvoiceRequestSerializer

# Create your views here.


class InvoiceView(APIView):
    def get(self, request):
        pass

    def post(self, request):
        request_data = request.data
        serializer = InvoiceRequestSerializer(request_data)
        return Response({"message": "Invoice Created"}, status=HTTP_201_CREATED)
