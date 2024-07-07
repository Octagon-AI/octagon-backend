from rest_framework import viewsets
from .models import AIModel, Problem, Type
from .serializers import AIModelSerializer, ProblemSerializer, TypeSerializer
from rest_framework import viewsets, generics, filters
from rest_framework.response import Response
import asyncio
import torch
from .compilemodel import prove_inference
from django_filters.rest_framework import DjangoFilterBackend


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]


class AIModelViewSet(viewsets.ModelViewSet):
    queryset = AIModel.objects.all()
    serializer_class = AIModelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'problem']

class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]


from .serializers import VerifyModelSerializer
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

class VerifyModel(generics.GenericAPIView):
    serializer_class = VerifyModelSerializer

    @swagger_auto_schema(request_body=VerifyModelSerializer)
    def post(self, request, id):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            x_list = serializer.validated_data['x']

            # Convert the list of floats to a tensor
            x = torch.tensor([[x_list]])
            if x.shape != torch.Size([1,1,10]):
                return Response({"error": "Input shape must be (10)"}, status=status.HTTP_400_BAD_REQUEST)

            model = AIModel.objects.get(id=id)
            model_path = model.file.path
            model_path = model_path.replace('/model.onnx', '')
            res = asyncio.run(prove_inference(model_path, x))

            return Response({"result": res, "x": x_list})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)