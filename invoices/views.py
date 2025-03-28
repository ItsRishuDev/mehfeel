from rest_framework.views import APIView
from invoices.models import Invoice, InvoiceItem

# Create your views here.

class InvoiceView(APIView):
    def get(self, request):
        pass
    
    def post(self, request):
        pass