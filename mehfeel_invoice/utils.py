from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from django.http import HttpResponse

def custom_page_not_found_view(request, exception):
    return HttpResponse("Yeh to banaya hi nhi yarrr!!!!!!")