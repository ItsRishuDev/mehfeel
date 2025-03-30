from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from invoices.models import Invoice, InvoiceItem
from invoices.serializers import InvoiceSerializer, AllInvoiceSerializer

# Create your views here.


class InvoiceView(APIView):
    def get(self, request):
        try:
            invoices = Invoice.objects.all()
            serializer = AllInvoiceSerializer(invoices, many=True)
            return Response(serializer.data, status=HTTP_200_OK)
        except Exception as err:
            return Response({"Error": str(err)}, status=HTTP_400_BAD_REQUEST)

    def post(self, request):
        request_data = request.data
        serializer = InvoiceSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Invoice Created"},
                status=HTTP_201_CREATED,
            )
        return Response({"message": serializer.errors}, status=HTTP_400_BAD_REQUEST)
