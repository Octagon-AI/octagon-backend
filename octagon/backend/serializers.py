from rest_framework import serializers
from .models import AIModel, Problem, Type

class ProblemSerializer(serializers.ModelSerializer):
    best_accuracy = serializers.SerializerMethodField()
    total_models = serializers.SerializerMethodField()
    class Meta:
        model = Problem
        fields = '__all__'

    def get_best_accuracy(self, obj):
        return AIModel.objects.filter(problem=obj).order_by('-accuracy').first().accuracy

    def get_total_models(self, obj):
        return AIModel.objects.filter(problem=obj).count()
class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'

class AIModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIModel
        fields = '__all__'
