from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from invoices.models import Invoice, InvoiceItem
from invoices.serializers import (
    InvoiceSerializer,
    AllInvoiceSerializer,
    InvoiceDetailSerializer,
)
from invoices.invoice import generate_invoice

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
            invoice_data = serializer.save()
            buffer = generate_invoice(invoice_data)
            file_name = invoice_data.get_file_name()
            response = HttpResponse(buffer, content_type='application/pdf', status=201)
            response['Content-Disposition'] = f'attachment; filename="{file_name}.pdf"'
            return response

        return Response({"message": serializer.errors}, status=HTTP_400_BAD_REQUEST)


class InvoiceDetailView(APIView):
    def get(self, request, invoice_id):
        try:
            invoice = Invoice.objects.prefetch_related(
                "items__item_addons"
            ).get(invoice_id=invoice_id)
            serializer = InvoiceDetailSerializer(invoice)
            return Response(serializer.data, status=HTTP_200_OK)
        except Exception as err:
            return Response({"Error": str(err)}, status=HTTP_400_BAD_REQUEST)


class InvoiceGeneratorView(APIView):
    def get(self, request, invoice_id):
        try:
            invoice_data = Invoice.objects.prefetch_related(
                "items__item_addons"
            ).get(invoice_id=invoice_id)
            buffer = generate_invoice(invoice_data)
            file_name = invoice_data.get_file_name()
            response = HttpResponse(buffer, content_type='application/pdf', status=201)
            response['Content-Disposition'] = f'attachment; filename="{file_name}.pdf"'
            return response
        
        except Exception as err:
            return Response({"Error": str(err)}, status=HTTP_400_BAD_REQUEST)
