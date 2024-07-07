from django.db import models
import os
import uuid
from datetime import datetime
class Type(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
class Problem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    data_url = models.CharField(max_length=255)

    def __str__(self):
        return self.name

def ai_model_upload_to(instance, filename):
    # Generate a unique path using the model's name and a UUID
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    name = [x for x in instance.name.split() if x.isalnum()]
    name = ''.join(name)
    return os.path.join('ai_models', f'{name}-{timestamp}', 'model.onnx')

class AIModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    nevermind_tag = models.CharField(max_length=255, blank=True, null=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, null=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True)
    file = models.FileField(upload_to=ai_model_upload_to, blank=True, null=True)  # Added FileField
    accuracy = models.FloatField(null=True)
    def __str__(self):
        return self.name

class ModelEvaluation(models.Model):
    model = models.ForeignKey(AIModel, on_delete=models.CASCADE)
    feesMse = models.FloatField(default=0.0)
    feesMae = models.FloatField(default=0.0)
    highMse = models.FloatField(default=0.0)
    highMae = models.FloatField(default=0.0)
    lowMse = models.FloatField(default=0.0)
    lowMae = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.model.name} - {self.accuracy}'