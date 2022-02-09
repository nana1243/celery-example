from rest_framework import views
from .serializer import CreateCalculationSerializer
# Create your views here.
from rest_framework.request import Request
from rest_framework.response import Response
from .service import CalculationHandler


class CalculationAPIView(views.APIView):

    def post(self, request: Request, *args, **kwargs):
        request_serializer = CreateCalculationSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        handler = CalculationHandler()
        result = handler.handle(**request_serializer.data)
        return Response(result)


# class CalculationControlAPIView(views.APIView):
#     def post(self, request: Request, *args, **kwargs):
#         return result



