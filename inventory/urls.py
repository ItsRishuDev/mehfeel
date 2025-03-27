from django.urls import path
from inventory.views import AddOnView, CategoryView, ItemView

urlpatterns = [
    path("add-ons/", AddOnView.as_view(), name="add_on"),
    path("categories/", CategoryView.as_view(), name="category"),
    path("items/", ItemView.as_view(), name="item"),
]
