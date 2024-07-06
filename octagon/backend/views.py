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

class VerifyModel(generics.GenericAPIView):
    def post(self, request, id):
        x = torch.tensor([[[0.8790, 0.6273, 0.2377, 0.5785, 0.9947, 0.9937, 0.5818, 0.6087,
                            0.6087, 0.6312]]])
        model = AIModel.objects.get(id=id)
        model_path = model.file.path
        model_path = model_path.replace('/model.onnx', '')
        res = asyncio.run(prove_inference(model_path, x))
        return Response({"result": res})

