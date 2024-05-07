from rest_framework.views import APIView
from  rest_framework import  status , response

from Products.serializers import ProductSerializer

class CreateProduct(APIView):

    def post(self,request):

        date = request.date
        serializer=ProductSerializer(date)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return  response.Response({'msg':'send'},status.HTTP_200_OK)



