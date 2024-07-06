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
    m1 = models.FloatField()
    m2 = models.FloatField()
    m3 = models.FloatField()
    m4 = models.FloatField()
    m5 = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.model.name} - {self.accuracy}'