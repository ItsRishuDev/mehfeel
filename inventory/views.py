from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from inventory.models import Item, Category, AddOn
from inventory.serializers import ItemSerializer, CategorySerializer, AddOnSerializer


class ItemView(APIView):
    def get(self, request):
        try:
            category_id = request.GET.get("category")
            if category_id:
                Category.objects.get(id=category_id)

                items = (
                    Item.objects.select_related("category")
                    .prefetch_related("add_ons")
                    .filter(category=category_id)
                )
            else:
                items = (
                    Item.objects.select_related("category")
                    .prefetch_related("add_ons")
                    .all()
                )
            serializer = ItemSerializer(items, many=True)
            return Response(serializer.data, status=HTTP_200_OK)

        except Category.DoesNotExist:
            return Response(
                {"Error": "Invalid category provided."}, status=HTTP_400_BAD_REQUEST
            )

        except Exception as err:
            return Response({"Error": str(err)}, status=HTTP_400_BAD_REQUEST)


class CategoryView(APIView):
    def get(self, request):
        try:
            items = Category.objects.all()
            serializer = CategorySerializer(items, many=True)
            return Response(serializer.data, status=HTTP_200_OK)
        except Exception as err:
            return Response({"Error": str(err)}, status=HTTP_400_BAD_REQUEST)


class AddOnView(APIView):
    def get(self, request):
        try:
            items = AddOn.objects.all()
            serializer = AddOnSerializer(items, many=True)
            return Response(serializer.data, status=HTTP_200_OK)
        except Exception as err:
            return Response({"Error": str(err)}, status=HTTP_400_BAD_REQUEST)
