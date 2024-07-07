from rest_framework import serializers
from .models import AIModel, Problem, Type

class ProblemSerializer(serializers.ModelSerializer):
    best_accuracy = serializers.SerializerMethodField(read_only=True)
    total_models = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Problem
        fields = '__all__'

    def get_best_accuracy(self, obj):
        if AIModel.objects.filter(problem=obj).count() > 0:
            return AIModel.objects.filter(problem=obj).order_by('-accuracy')[0].accuracy
        return 0
    def get_total_models(self, obj):
        return AIModel.objects.filter(problem=obj).count()
class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'

class AIModelSerializer(serializers.ModelSerializer):
    problem_name = serializers.SerializerMethodField(read_only=True)
    type_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = AIModel
        fields = '__all__'

    def get_problem_name(self, obj):
        if obj.problem is None:
            return None
        return obj.problem.name

    def get_type_name(self, obj):
        if obj.type is None:
            return None
        return obj.type.name
