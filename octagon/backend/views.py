from rest_framework import viewsets
from .models import AIModel, Problem, Type
from .serializers import AIModelSerializer, ProblemSerializer, TypeSerializer
from rest_framework import viewsets, generics, filters
from rest_framework.response import Response
import asyncio
import torch
from .compilemodel import prove_inference
from .evaluate_model import evaluate_model
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import VerifyModelSerializer
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .models import ModelEvaluation
import os

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
    

class EvaluateModel(generics.GenericAPIView):
    def post(self, request, id):
        model = AIModel.objects.get(id=id)
        model_path = model.file.path
        model_path = model_path.replace('/model.onnx', '')
        res = evaluate_model(model_path, "ETH_USDC_1.json")

        # add evaluation to the database as ModelEvaluation
        model_evaluation = ModelEvaluation.objects.create(
            model=model,
            feesMse=res['mse_feesUSD'],
            feesMae=res['mae_feesUSD'],
            highMse=res['mse_high'],
            highMae=res['mae_high'],
            lowMse=res['mse_low'],
            lowMae=res['mae_low']
        )
        model_evaluation.save()

        return Response({"result": res})


class DeployModel(generics.GenericAPIView):
    def post(self, request, id):
        model = AIModel.objects.get(id=id)
        model_path = model.file.path
        model_path = model_path.replace('/model.onnx', '')

        print("DELAAAAM", model_path)
        print("PATH", os.getcwd())
        # copy model to the deployment directory
        os.system(f"cp {model_path}/Verifier.sol ../deployer")
        res = os.popen(f"cd ../deployer && python main.py")
        rez = res.read()
        print(rez)
        import re
        match = re.search(r"0x[a-fA-F0-9]{40}", rez)
        print("MATCH", match)

        # print("RESS ",rez, "RESS end")

        return Response({"deployed": match.group(0)})