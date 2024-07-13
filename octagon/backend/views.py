from rest_framework import viewsets
from .models import AIModel, Problem, Type
from .serializers import AIModelSerializer, ProblemSerializer, TypeSerializer
from rest_framework import viewsets, generics
from rest_framework.response import Response
import asyncio
import torch
from .compilemodel import prove_inference

class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

class AIModelViewSet(viewsets.ModelViewSet):
    queryset = AIModel.objects.all()
    serializer_class = AIModelSerializer

class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

class VerifyModel(generics.GenericAPIView):
    def post(self, request, id):
        x = torch.tensor([[[0.8790, 0.6273, 0.2377, 0.5785, 0.9947, 0.9937, 0.5818, 0.6087,
                            0.6087, 0.6312]]])
        model = AIModel.objects.get(id=id)
        model_path = model.file.path
        model_path = model_path.replace('/model.onnx', '')
        res = asyncio.run(prove_inference(model_path, x))
        return Response({"result": res})

