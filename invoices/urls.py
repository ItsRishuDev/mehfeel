from django.urls import path
from invoices.views import InvoiceView, InvoiceDetailView, InvoiceGeneratorView

urlpatterns = [
    path("", InvoiceView.as_view(), name="invoice"),
    path("<uuid:invoice_id>/", InvoiceDetailView.as_view(), name="invoice_detail"),
    path("<uuid:invoice_id>/generate/", InvoiceGeneratorView.as_view(), name="invoice_generator"),
]
