from rest_framework import viewsets
from .models import AIModel, Problem, Type
from .serializers import AIModelSerializer, ProblemSerializer, TypeSerializer
from rest_framework import viewsets, generics

class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

class AIModelViewSet(viewsets.ModelViewSet):
    queryset = AIModel.objects.all()
    serializer_class = AIModelSerializer

class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

